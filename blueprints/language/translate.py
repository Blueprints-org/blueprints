"""Translate LaTeX text using CSV-based manual translations and Google Translate."""

import asyncio
import csv
import logging
import os
import re

try:
    from googletrans import Translator
except ImportError:  # pragma: no cover
    raise ImportError(
        "\n\nThe translate features require the translate module of blueprints. Install it through:\n"
        "- pip install blueprints[translate]\n"
        "- uv add blueprints[translate]\n"
    )  # pragma: no cover


class TranslateLatex:
    """
    Utility class for extracting and translating LaTeX text.
    WARNING: uses Google Translate service when translations haven't been manually entered.
    When the services are not available, (sections of) text will be left in English.
    """

    def __init__(
        self,
        latex: str,
        dest_language: str,
        service_urls: list[str] | None = None,
        custom_csv_path: str | None = None,
    ) -> None:
        r"""
        Initialize the Translate class with text and destination language.
        WARNING: uses Google Translate service when translations haven't been manually entered.
        When the services are not available, (sections of) text will be left in English.

        Parameters
        ----------
        latex : str
            The LaTeX string to be translated.
        dest_language : str
            The target language code (e.g., 'nl' for Dutch, full list on https://docs.cloud.google.com/translate/docs/languages).
        service_urls : list[str], optional
            Optional list of service URLs for the translator.
        """
        if service_urls is None:
            service_urls = ["translate.googleapis.com"]
        self.translator = Translator(service_urls=service_urls)
        self.original = latex
        self.dest_language = dest_language
        self.csv_path = os.path.join(os.path.dirname(__file__), "translations.csv")
        if custom_csv_path:
            self.csv_path = custom_csv_path
        self.translation_dict = self._load_translation_dict(
            dest_language.replace("-", "_")
        )  # Normalize for CSV filename and Google: use underscores, not hyphens
        self.translation_failed = False
        self.translated = self._translate_latex()

    def _load_translation_dict(self, dest_language: str) -> dict[str, str]:
        r"""
        Load translation dictionary from a CSV file if it exists.
        The CSV should be named '<dest_language>.csv' and be in the same directory as this script.
        The CSV format has language codes as headers (e.g., en,nl,de,fr) with the first column as source.
        Returns a dict mapping source text to translated text.
        If a translation is "-", the source text is used instead.
        """
        translation_dict: dict[str, str] = {}
        if os.path.isfile(self.csv_path):
            with open(self.csv_path, encoding="utf-8", newline="") as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader, None)

                if header:
                    # Find the column index for the destination language
                    try:
                        dest_col_index = header.index(dest_language)
                    except ValueError:
                        return translation_dict

                    # Load translations from the appropriate column
                    for row in reader:
                        if len(row) > dest_col_index:
                            source_text = row[0]
                            translation = row[dest_col_index]
                            # If translation is "-", use the source text
                            if translation == "-":
                                translation_dict[source_text] = source_text
                            else:
                                translation_dict[source_text] = translation
        return translation_dict

    def _wildcard_match(self, text: str) -> str | None:
        r"""
        If a manual translation contains '**', treat each as a wildcard and match/replace the corresponding substrings in the input text.
        Supports multiple wildcards. Returns the translated string if a wildcard match is found, else None.
        """
        for src, tgt in getattr(self, "translation_dict", {}).items():
            if "**" in src:
                if src.count("**") != tgt.count("**"):
                    logging.warning(f"Mismatched wildcard counts in translation: '{src}' -> '{tgt}'")
                    continue
                # Split source pattern into fixed parts
                parts = src.split("**")
                # Build regex pattern for matching, escaping fixed parts
                regex = "^" + "".join(re.escape(part) + "(.*?)" for part in parts[:-1]) + re.escape(parts[-1]) + "$"
                match = re.match(regex, text)
                if match:
                    # Replace each '**' in tgt with corresponding group
                    result = tgt
                    for i, group in enumerate(match.groups()):
                        result = result.replace("**", group, 1)
                    return result
        return None

    def _translate_bulk(self, texts: list) -> list[str | None]:
        r"""
        Translate a list of strings to the destination language.
        First checks the translation dictionary loaded from CSV. If not found, uses Google Translate.
        Preserves leading and trailing spaces in the translated text.

        Parameters
        ----------
        texts : list[str]
            The list of strings to be translated.

        Returns
        -------
        list[str]
            The list of translated strings.
        """
        # Try to use CSV dictionary for all, fallback to Google Translate for missing
        results: list[str | None] = []
        missing: list[str] = []
        missing_indices: list[int] = []
        missing_spaces: list[tuple[str, str]] = []  # Store (leading_space, trailing_space) for each missing text

        for i, t in enumerate(texts):
            if hasattr(self, "translation_dict") and t in self.translation_dict:
                results.append(self.translation_dict[t])
            else:
                wildcard_result = self._wildcard_match(t)
                if wildcard_result is not None:
                    results.append(wildcard_result)
                else:
                    results.append(None)
                    # Extract leading and trailing spaces
                    leading_space = t[: len(t) - len(t.lstrip())]
                    trailing_space = t[len(t.rstrip()) :]
                    stripped_text = t.strip()
                    missing.append(stripped_text)
                    missing_indices.append(i)
                    missing_spaces.append((leading_space, trailing_space))

        # for missing texts, use Google Translate
        if missing:
            # In case of network issues or other exceptions, handle gracefully
            try:
                # Use Google Translate for all missing texts in bulk
                translations = self.translator.translate(missing, dest=self.dest_language)

                # Check if the result is a coroutine (async), and handle accordingly
                if asyncio.iscoroutine(translations):
                    try:
                        # Try to get the current running event loop
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        # If no event loop is running, run the coroutine synchronously
                        translations = asyncio.run(translations)
                    else:
                        # If an event loop is running, run the coroutine until complete
                        translations = loop.run_until_complete(translations)  # pragma: no cover, requires async context
                translated_texts = [tr.text for tr in translations]  # pragma: no cover, could fail if google is offline
            except Exception:
                self.translation_failed = True
                # Failsafe: if translation fails, keep original English text (with spaces)
                translated_texts = missing
                logging.exception("Google translation failed, using original English text.")

            # Restore leading and trailing spaces
            for idx, val, (leading, trailing) in zip(missing_indices, translated_texts, missing_spaces):
                results[idx] = leading + val + trailing
        return results

    def _replace_text_commands(self, replacements: list) -> str:
        r"""
        Replace all \text{...}, \txt{...}, \textbf{...}, and \textit{...} in the string with the corresponding replacements.
        Only captures the innermost text content when commands are nested.

        Parameters
        ----------
        replacements : list[str]
            The list of replacement strings.

        Returns
        -------
        str
            The string with \text{...}, \txt{...}, \textbf{...}, and \textit{...} replaced by the corresponding replacements.
        """
        replacement_index = 0

        def _repl(match: re.Match) -> str:
            nonlocal replacement_index
            command = match.group(1)  # Captures 'text', 'txt', 'textbf', or 'textit'
            replacement = replacements[replacement_index]
            replacement_index += 1
            return f"\\{command}{{{replacement}}}"

        # Apply all replacements in one pass (since we only extract innermost text)
        return re.sub(r"\\(text|txt|textbf|textit)\{([^{}]*)\}", _repl, self.original)

    def _replace_section_commands(self, text: str, replacements: list) -> str:
        r"""
        Replace all \section{...}, \subsection{...}, \subsubsection{...}, and \title{...} in the string with the corresponding replacements.
        Only captures the innermost text content when commands are nested.

        Parameters
        ----------
        text : str
            The LaTeX string to process.
        replacements : list[str]
            The list of replacement strings.

        Returns
        -------
        str
            The string with \section{...}, \subsection{...}, \subsubsection{...}, and \title{...} replaced by the corresponding replacements.
        """
        replacement_index = 0

        def _repl(match: re.Match) -> str:
            nonlocal replacement_index
            command = match.group(1)  # Captures 'section', 'subsection', 'subsubsection', or 'title'
            replacement = replacements[replacement_index]
            replacement_index += 1
            return f"\\{command}{{{replacement}}}"

        # Apply all replacements in one pass (since we only extract innermost text)
        return re.sub(r"\\(section|subsection|subsubsection|title)\{([^{}]*)\}", _repl, text)

    def _replace_caption_commands(self, text: str, replacements: list) -> str:
        r"""
        Replace all \caption{...} in the string with the corresponding replacements.
        Only captures the innermost text content when commands are nested.

        Parameters
        ----------
        text : str
            The LaTeX string to process.
        replacements : list[str]
            The list of replacement strings.

        Returns
        -------
        str
            The string with \caption{...} replaced by the corresponding replacements.
        """
        replacement_index = 0

        def _repl(_match: re.Match) -> str:
            nonlocal replacement_index
            replacement = replacements[replacement_index]
            replacement_index += 1
            return f"\\caption{{{replacement}}}"

        # Apply all replacements in one pass (since we only extract innermost text)
        return re.sub(r"\\caption\{([^{}]*)\}", _repl, text)

    def _replace_item_commands(self, text: str, replacements: list) -> str:
        r"""
        Replace all \item content in the string with the corresponding replacements.
        Only processes \item commands without nested braces.

        Parameters
        ----------
        text : str
            The LaTeX string to process.
        replacements : list[str]
            The list of replacement strings.

        Returns
        -------
        str
            The string with \item content replaced by the corresponding replacements.
        """
        replacement_index = 0

        def _repl(match: re.Match) -> str:
            nonlocal replacement_index
            # Get the whitespace after \item
            whitespace = match.group(1)
            replacement = replacements[replacement_index]
            replacement_index += 1
            return f"\\item{whitespace}{replacement}"

        # Match \item followed by whitespace and text up to newline or next command
        # This captures plain text items without nested structure
        return re.sub(r"\\item(\s+)([^\\]+?)(?=\\|$)", _repl, text, flags=re.DOTALL)

    def _replace_table_cells(self, text: str, replacements: list) -> str:
        r"""
        Replace text content in table cells with the corresponding replacements.
        Only processes cells that don't contain LaTeX commands (except \text{...}).

        Parameters
        ----------
        text : str
            The LaTeX string to process.
        replacements : list[str]
            The list of replacement strings.

        Returns
        -------
        str
            The string with table cell content replaced by the corresponding replacements.
        """
        replacement_index = 0

        def _repl_row(match: re.Match) -> str:
            nonlocal replacement_index
            row_content = match.group(0)
            # Split by & to get cells
            cells = row_content.split("&")
            new_cells = []

            for cell in cells:
                # Check if this cell contains translatable plain text (not just LaTeX commands)
                cell_stripped = cell.strip()
                # Skip if cell is empty, only has \text{} commands, or has other LaTeX commands
                if cell_stripped and not re.match(r"^\s*$", cell_stripped) and not re.search(r"\\(?!text\{|txt\{|textbf\{|textit\{)", cell_stripped):
                    # Check if there's actual text content outside of \text{} commands
                    temp_text = re.sub(r"\\(?:text|txt|textbf|textit)\{[^}]*\}", "", cell_stripped)
                    if temp_text.strip() and replacement_index < len(replacements):
                        # This cell has translatable text
                        new_cells.append(cell.replace(cell_stripped, replacements[replacement_index]))
                        replacement_index += 1
                        continue
                new_cells.append(cell)

            return "&".join(new_cells)

        # Match table rows (content between \\ or at end of tabular)
        # Process content within tabular environments
        def _process_tabular(match: re.Match) -> str:
            nonlocal replacement_index
            tabular_start = match.group(1)  # \begin{tabular}{...}
            tabular_content = match.group(2)
            tabular_end = match.group(3)  # \end{tabular}

            # Skip header lines (before \midrule)
            parts = re.split(r"(\\midrule)", tabular_content, maxsplit=1)
            header_part = parts[0]
            midrule = parts[1]
            content_part = parts[2]

            # Process rows in content part
            processed_content = re.sub(r"([^\\].*?)(?=\\\\|\\bottomrule|\\end)", _repl_row, content_part, flags=re.DOTALL)

            return tabular_start + header_part + midrule + processed_content + tabular_end

        # Match tabular environments
        return re.sub(r"(\\begin\{tabular\}\{[^}]+\})(.*?)(\\end\{tabular\})", _process_tabular, text, flags=re.DOTALL)

    def _check_decimal_separator(self, s: str) -> str:
        r"""
        Replace all periods with commas outside of \text{...}, \txt{...}, etc. blocks and \begin{figure}...\end{figure} blocks.

        Parameters
        ----------
        s : str
            The LaTeX string to process.

        Returns
        -------
        str
            The processed LaTeX string with periods replaced by commas outside of text blocks and figure blocks if in a relevant language.
        """
        # Languages that use comma as decimal separator
        comma_decimal_languages_1 = ["bg", "ca", "cs", "da", "de", "el", "es", "et", "eu", "fi", "fr", "gl", "hr", "hu", "is", "it", "lt", "lv"]
        comma_decimal_languages_2 = ["nl", "no", "pl", "pt", "ro", "ru", "sk", "sl", "sr", "sv", "tr", "uk"]
        if self.dest_language not in comma_decimal_languages_1 + comma_decimal_languages_2:
            return s

        # Use regex to split into text blocks, figure blocks, and non-protected blocks
        # Match text commands and figure environments
        pattern = re.compile(r"(\\(?:text|txt|textbf|textit)\{.*?\}|\\begin\{figure\}.*?\\end\{figure\})", re.DOTALL)
        parts = pattern.split(s)

        def is_protected_block(seg: str) -> bool:
            return (seg.startswith((r"\text{", r"\txt{", r"\textbf{", r"\textit{")) and seg.endswith("}")) or (
                seg.startswith(r"\begin{figure}") and seg.endswith(r"\end{figure}")
            )

        new_segments = [seg if is_protected_block(seg) else seg.replace(".", ",") for seg in parts]
        return "".join(new_segments)

    def _extract_balanced_content(self, text: str, start_pos: int) -> tuple[str, int]:
        r"""
        Extract content from balanced braces starting at start_pos.
        Returns (content, end_position).
        """
        depth = 0
        i = start_pos
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        return text[start_pos + 1 : i], i

    def _extract_text_commands(self) -> list[str]:
        r"""Extract innermost text content from \text{}, \txt{}, \textbf{}, and \textit{} commands."""
        texts = []
        pattern = r"\\(?:text|txt|textbf|textit)\{"
        for match in re.finditer(pattern, self.original):
            start = match.end() - 1  # Position of '{'
            content, _ = self._extract_balanced_content(self.original, start)
            # Only include if content doesn't contain nested text commands
            if not re.search(r"\\(?:text|txt|textbf|textit)\{", content):
                texts.append(content)
        return texts

    def _extract_section_commands(self) -> list[str]:
        r"""Extract content from \section{}, \subsection{}, \subsubsection{}, and \title{} commands."""
        section_texts = []
        section_pattern = r"\\(?:section|subsection|subsubsection|title)\{"
        for match in re.finditer(section_pattern, self.original):
            start = match.end() - 1  # Position of '{'
            content, _ = self._extract_balanced_content(self.original, start)
            section_texts.append(content)
        return section_texts

    def _extract_caption_commands(self) -> list[str]:
        r"""Extract content from \caption{} commands."""
        caption_texts = []
        caption_pattern = r"\\caption\{"
        for match in re.finditer(caption_pattern, self.original):
            start = match.end() - 1  # Position of '{'
            content, _ = self._extract_balanced_content(self.original, start)
            caption_texts.append(content)
        return caption_texts

    def _extract_item_commands(self) -> list[str]:
        r"""Extract content from \item commands."""
        item_texts = []
        item_pattern = r"\\item\s+([^\\]+?)(?=\\|$)"
        for match in re.finditer(item_pattern, self.original, re.DOTALL):
            content = match.group(1).strip()
            # Only extract if it's plain text (not nested lists or commands except \text{})
            if content and not re.search(r"\\(?!text\{|txt\{|textbf\{|textit\{)", content):
                # Remove any \text{} commands temporarily to check for actual text
                temp_content = re.sub(r"\\(?:text|txt|textbf|textit)\{[^}]*\}", "", content)
                if temp_content.strip():
                    item_texts.append(content)
        return item_texts

    def _extract_table_cells(self) -> list[str]:
        """Extract content from table cells."""
        table_texts = []
        # Find all tabular environments
        tabular_pattern = r"\\begin\{tabular\}\{[^}]+\}(.*?)\\end\{tabular\}"
        for tabular_match in re.finditer(tabular_pattern, self.original, re.DOTALL):
            tabular_content = tabular_match.group(1)
            # Skip header part (before \midrule)
            parts = re.split(r"\\midrule", tabular_content, maxsplit=1)
            content_part = parts[1] if len(parts) >= 2 else tabular_content

            # Extract cells from rows
            row_pattern = r"([^\\]+?)(?=\\\\|\\bottomrule|\\end)"
            for row_match in re.finditer(row_pattern, content_part, re.DOTALL):
                row_content = row_match.group(1)
                # Split by & to get cells
                cells = row_content.split("&")
                for cell in cells:
                    cell_stripped = cell.strip()
                    # Only extract if it's simple text (not complex LaTeX)
                    if cell_stripped and not re.search(r"\\(?!text\{|txt\{|textbf\{|textit\{)", cell_stripped):
                        # Check if there's actual text content outside of \text{} commands
                        temp_text = re.sub(r"\\(?:text|txt|textbf|textit)\{[^}]*\}", "", cell_stripped)
                        if temp_text.strip():
                            table_texts.append(cell_stripped)
        return table_texts

    def _translate_latex(self) -> str:
        r"""
        Extract, translate, and reconstruct LaTeX string with translated text commands.
        Also translates content in \section{}, \subsection{}, \subsubsection{}, and \title{}.
        Also translates content in \caption{} (figure/table captions).
        Also translates content in \item commands (itemize/enumerate lists) and table cells.
        For certain languages, also replace periods with commas outside of text blocks.

        Returns
        -------
        str
            The LaTeX string with translated text commands.
        """
        # Extract text from various LaTeX commands
        texts = self._extract_text_commands()
        section_texts = self._extract_section_commands()
        caption_texts = self._extract_caption_commands()
        item_texts = self._extract_item_commands()
        table_texts = self._extract_table_cells()

        if not texts and not section_texts and not caption_texts and not item_texts and not table_texts:
            # If no text blocks, still apply period-to-comma if needed
            return self._check_decimal_separator(self.original)

        # Translate all texts in one bulk operation
        all_texts = texts + section_texts + caption_texts + item_texts + table_texts
        all_translations = self._translate_bulk(all_texts)

        # Split translations back into different parts
        idx = 0
        text_translations = all_translations[idx : idx + len(texts)]
        idx += len(texts)
        section_translations = all_translations[idx : idx + len(section_texts)]
        idx += len(section_texts)
        caption_translations = all_translations[idx : idx + len(caption_texts)]
        idx += len(caption_texts)
        item_translations = all_translations[idx : idx + len(item_texts)]
        idx += len(item_texts)
        table_translations = all_translations[idx : idx + len(table_texts)]

        # Apply replacements
        replaced = self._replace_text_commands(text_translations) if texts else self.original

        if section_texts:
            replaced = self._replace_section_commands(replaced, section_translations)

        if caption_texts:
            replaced = self._replace_caption_commands(replaced, caption_translations)

        if item_texts:
            replaced = self._replace_item_commands(replaced, item_translations)

        if table_texts:
            replaced = self._replace_table_cells(replaced, table_translations)

        # Only replace periods with commas outside text blocks for certain languages
        return self._check_decimal_separator(replaced)

    def __str__(self) -> str:
        """
        Return the translated LaTeX string.

        Returns
        -------
        str
            The translated LaTeX string.
        """
        return self.translated
