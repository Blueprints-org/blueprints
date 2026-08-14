"""Translate LaTeX text using CSV-based manual translations and Google Translate."""

import asyncio
import csv
import logging
import os
import re
from pathlib import Path
from typing import Any, cast

from googletrans import Translator


class LatexTranslator:
    r"""
    Utility class for extracting and translating LaTeX text. Note: this feature is slow in a .ipynb notebook environment.

    Supports translation between any language pair when using a CSV translation file.
    Falls back to Google Translate for text not found in the CSV.

    If Google Translate fails (network error, API limit, etc.), the original text
    is preserved and the error is logged. Translation continues gracefully.

    WARNING: uses Google Translate service when translations haven't been manually entered.
    When the service is unavailable, text will remain in the original language.

    Examples
    --------
    Basic usage with default CSV:

    >>> latex = r"\\text{Hello world} with formula $x = 5.2$"
    >>> translator = LatexTranslator(latex, destination_language="nl")
    >>> print(translator.text)
    \\text{Hallo wereld} with formula $x = 5,2$

    Using a custom CSV file:

    >>> from pathlib import Path
    >>> custom_csv = Path("my_translations.csv")
    >>> # CSV contains: en,nl
    >>> #                "Concrete strength","Betonsterkte"
    >>> latex = r"\\section{Concrete strength}"
    >>> translator = LatexTranslator(latex, "nl", custom_csv=custom_csv)
    >>> str(translator)
    '\\\\section{Betonsterkte}'

    Translating from non-English source:

    >>> latex_de = r"\\text{Hallo Welt}"
    >>> translator = LatexTranslator(latex_de, destination_language="en", source_language="de")
    >>> print(translator.text)
    \\text{Hello World}

    The translator handles various LaTeX commands:
    - Text commands: \\text{}, \\txt{}, \\textbf{}, \\textit{}
    - Sections: \\section{}, \\subsection{}, \\subsubsection{}, \\title{}
    - Captions: \\caption{}
    - Lists: \\item content
    - Tables: content within tabular environments
    - Equations: decimal separator conversion for certain languages (e.g.: '.' → ',' for Dutch)
    """

    def __init__(
        self,
        original_text: str,
        destination_language: str,
        source_language: str = "en",
        custom_csv: Path | str | None = None,
    ) -> None:
        r"""
        Initialize the LatexTranslator class with text and destination language.

        WARNING: uses Google Translate service when translations haven't been manually entered.
        When the services are not available, (sections of) text will be left in the original language.

        Parameters
        ----------
        original_text : str
            The LaTeX string to be translated.
        destination_language : str
            The target language code (e.g., 'nl' for Dutch, full list on https://docs.cloud.google.com/translate/docs/languages).
        source_language : str, optional
            The source language code of the LaTeX document (default: 'en' for English).
        custom_csv : Path | str, optional
            Optional custom path to the CSV file containing manual translations. Will use default 'translations.csv' declared in Blueprints.

            Warning:
            When no custom CSV is provided, the default 'translations.csv' file in Blueprints is used.
            This file may probably not contain translations for your specific use case and language pair.
            We will use Google Translate for missing translations, but results may vary.

            Therefore, it is recommended to provide a custom CSV file with manual translations for your specific use case and language pair:
            - column headers are language codes (e.g., 'en,nl,de,fr').
            - each row contains translations for the same concept across different languages.
            - use '-' as a translation value to keep the source text unchanged for that language.
            - supports (multiple) wildcard patterns using '**' to match and preserve variable content.

            When a custom CSV is provided, it should follow the example format described below:
            ```
            en, nl, de, fr
            "Hello", "Hallo", "Hallo", "Bonjour"
            "With formula **:", "Met formule **:", "Mit Formel **:", "-"
            ```
            With this CSV, you can translate en→nl, nl→fr, de→en, etc. Using the same file.

        """
        self.original_text = original_text
        self.source_language = source_language
        self.destination_language = destination_language
        self.csv_path = str(custom_csv) if custom_csv else os.path.join(os.path.dirname(__file__), "translations.csv")
        self._translation = ""

    def _load_translation_dict(self, source_language: str, dest_language: str) -> dict[str, str]:
        r"""
        Load translation dictionary from a CSV file if it exists.
        The CSV format has language codes as headers (e.g., en,nl,de,fr).
        Returns a dict mapping source text (from source_language column) to translated text (from dest_language column).
        If a translation is "-", the source text is used instead.

        Parameters
        ----------
        source_language : str
            The source language code (determines which column to use as lookup key).
        dest_language : str
            The destination language code (determines which column to use as translation value).

        Returns
        -------
        dict[str, str]
            Dictionary mapping source language text to destination language text.
        """
        translation_dict: dict[str, str] = {}
        if os.path.isfile(self.csv_path):
            with open(self.csv_path, encoding="utf-8", newline="") as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader, None)

                if header:
                    # Find the column indices for both source and destination languages
                    try:
                        source_col_index = header.index(source_language)
                        dest_col_index = header.index(dest_language)
                    except ValueError:
                        # If either language is not found in the CSV, return empty dict
                        return translation_dict

                    # Load translations from the appropriate columns
                    for row in reader:
                        if len(row) > max(source_col_index, dest_col_index):
                            source_text = row[source_col_index]
                            translation = row[dest_col_index]
                            # If translation is "-", use the source text
                            if translation == "-":
                                translation_dict[source_text] = source_text
                            else:
                                translation_dict[source_text] = translation
        return translation_dict

    def _wildcard_match(self, text: str, translation_dict: dict[str, str]) -> str | None:
        r"""
        If a manual translation contains '**', treat each as a wildcard and match/replace the corresponding substrings in the input text.
        Supports multiple wildcards. Returns the translated string if a wildcard match is found, else None.
        """
        for src, tgt in translation_dict.items():
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

    def _remove_zero_width_spaces(self, s: str) -> str:
        """Remove all zero-width space (U+200B) characters from a string."""
        return s.replace("\u200b", "")

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

        # Normalize for CSV filename and Google: use underscores, not hyphens
        translation_dict = self._load_translation_dict(
            source_language=self.source_language.replace("-", "_"),
            dest_language=self.destination_language.replace("-", "_"),
        )

        for i, t in enumerate(texts):
            if t in translation_dict:
                clean_translation = self._remove_zero_width_spaces(translation_dict[t])
                results.append(clean_translation)
            else:
                wildcard_result = self._wildcard_match(t, translation_dict)
                if wildcard_result is not None:
                    clean_wildcard = self._remove_zero_width_spaces(wildcard_result)
                    results.append(clean_wildcard)
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
                translator = Translator()
                translations = translator.translate(missing, dest=self.destination_language)

                # Check if the result is a coroutine (async), and handle accordingly
                if asyncio.iscoroutine(translations):
                    # Type narrow: translations is a coroutine at this point
                    coro = cast(Any, translations)
                    try:
                        # Try to get the current running event loop
                        loop = asyncio.get_running_loop()
                        # If a loop is running, schedule the coroutine on it
                        translations = asyncio.run_coroutine_threadsafe(coro, loop).result()  # pragma: no cover, requires async context
                    except RuntimeError:
                        # If no event loop is running, run the coroutine synchronously
                        translations = asyncio.run(coro)
                translated_texts = [tr.text for tr in translations]  # pragma: no cover, could fail if google is offline
            except Exception as e:
                # Graceful fallback: if translation fails, keep original text (with spaces)
                translated_texts = missing
                logging.exception(f"Translation failed ({type(e).__name__}), using original text.")

            # Restore leading and trailing spaces
            for idx, val, (leading, trailing) in zip(missing_indices, translated_texts, missing_spaces):
                clean_val = self._remove_zero_width_spaces(val)
                results[idx] = leading + clean_val + trailing
        return results

    @staticmethod
    def _replace_text_commands(text: str, replacements: list) -> str:
        r"""
        Replace all \text{...}, \txt{...}, \textbf{...}, and \textit{...} in the string with the corresponding replacements.
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
        return re.sub(r"\\(text|txt|textbf|textit)\{([^{}]*)\}", _repl, text)

    @staticmethod
    def _replace_section_commands(text: str, replacements: list) -> str:
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

    @staticmethod
    def _replace_caption_commands(text: str, replacements: list) -> str:
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

        def _repl(_: re.Match) -> str:
            nonlocal replacement_index
            replacement = replacements[replacement_index]
            replacement_index += 1
            return f"\\caption{{{replacement}}}"

        # Apply all replacements in one pass (since we only extract innermost text)
        return re.sub(r"\\caption\{([^{}]*)\}", _repl, text)

    @staticmethod
    def _replace_item_commands(text: str, replacements: list) -> str:
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

    @staticmethod
    def _replace_table_cells(text: str, replacements: list) -> str:  # noqa: C901
        r"""
        Replace plain text content in table cells with translations, preserving \text{} commands.
        Only replaces the plain text portions that were extracted (excluding \text{} content).

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

        # Match table rows (content between \\ or at end of tabular)
        # Process content within tabular environments
        def _process_tabular(match: re.Match) -> str:
            nonlocal replacement_index
            tabular_start = match.group(1)  # \begin{tabular}{...}
            tabular_content = match.group(2)
            tabular_end = match.group(3)  # \end{tabular}

            # Split by table rules to get header and body sections, preserving the rules with their spacing
            parts = re.split(r"(\s*\\(?:toprule|midrule|bottomrule)\s*)", tabular_content)

            result = tabular_start
            for part in parts:
                if re.match(r"\s*\\(?:toprule|midrule|bottomrule)\s*", part):
                    result += part
                elif part:  # Process any non-empty part
                    # Check if this part is just an empty row (e.g., " \\ ")
                    if part.strip() in ("", "\\\\"):
                        result += part
                        continue

                    # Split by \\ to get rows
                    rows = part.split("\\\\")
                    for row in rows:
                        row_stripped = row.strip()
                        if not row_stripped:
                            continue

                        # Process cells but preserve original row spacing
                        modified_row = row
                        cells = row.split("&")

                        for i, cell in enumerate(cells):
                            cell_stripped = cell.strip()
                            # Only replace if cell is plain text (no LaTeX except allowed text commands)
                            if cell_stripped and not re.search(r"\\(?!text\{|txt\{|textbf\{|textit\{)", cell_stripped):
                                plain_text = re.sub(r"\\(?:text|txt|textbf|textit)\{[^}]*\}", "", cell_stripped)
                                if plain_text.strip() and replacement_index < len(replacements):
                                    # Replace the entire cell content (preserving original leading/trailing spaces)
                                    leading = cell[: len(cell) - len(cell.lstrip())]
                                    trailing = cell[len(cell.rstrip()) :]
                                    cells[i] = f"{leading}{replacements[replacement_index]}{trailing}"
                                    replacement_index += 1
                        # Reconstruct the row with original ampersands and spacing
                        modified_row = " & ".join(cells)

                        result += modified_row.rstrip() + " \\\\"

            result += tabular_end
            return result

        # Match tabular environments
        return re.sub(r"(\\begin\{tabular\}\{[^}]+\})(.*?)(\\end\{tabular\})", _process_tabular, text, flags=re.DOTALL)

    def _check_decimal_separator(self, s: str) -> str:
        r"""
        Replace all periods with commas in equation environments and inline math ($ ... $).
        Does NOT replace periods inside \tag{} commands.

        Parameters
        ----------
        s : str
            The LaTeX string to process.

        Returns
        -------
        str
            The processed LaTeX string with periods replaced by commas in equations if in a relevant language.
        """
        # Languages that use comma as decimal separator
        comma_decimal_languages_1 = ["bg", "ca", "cs", "da", "de", "el", "es", "et", "eu", "fi", "fr", "gl", "hr", "hu", "is", "it", "lt", "lv"]
        comma_decimal_languages_2 = ["nl", "no", "pl", "pt", "ro", "ru", "sk", "sl", "sr", "sv", "tr", "uk"]
        if self.destination_language not in comma_decimal_languages_1 + comma_decimal_languages_2:
            return s

        def _replace_excluding_tag(content: str) -> str:
            r"""Replace periods with commas, excluding \tag{} content."""
            tag_match = re.search(r"\\tag\{[^}]*\}", content)
            if tag_match:
                return content[: tag_match.start()].replace(".", ",") + tag_match.group(0) + content[tag_match.end() :].replace(".", ",")
            return content.replace(".", ",")

        # Replace in inline math and equation environments
        s = re.sub(r"(?<!\\)\$([^$]+?)\$", lambda m: "$" + _replace_excluding_tag(m.group(1)) + "$", s)
        return re.sub(r"\\begin\{equation\}.*?\\end\{equation\}", lambda m: _replace_excluding_tag(m.group(0)), s, flags=re.DOTALL)

    @staticmethod
    def _extract_balanced_content(text: str, start_pos: int) -> tuple[str, int]:
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
        for match in re.finditer(pattern, self.original_text):
            start = match.end() - 1  # Position of '{'
            content, _ = self._extract_balanced_content(self.original_text, start)
            # Only include if content doesn't contain nested text commands
            if not re.search(r"\\(?:text|txt|textbf|textit)\{", content):
                texts.append(content)
        return texts

    def _extract_section_commands(self) -> list[str]:
        r"""Extract content from \section{}, \subsection{}, \subsubsection{}, and \title{} commands."""
        section_texts = []
        section_pattern = r"\\(?:section|subsection|subsubsection|title)\{"
        for match in re.finditer(section_pattern, self.original_text):
            start = match.end() - 1  # Position of '{'
            content, _ = self._extract_balanced_content(self.original_text, start)
            section_texts.append(content)
        return section_texts

    def _extract_caption_commands(self) -> list[str]:
        r"""Extract content from \caption{} commands."""
        caption_texts = []
        caption_pattern = r"\\caption\{"
        for match in re.finditer(caption_pattern, self.original_text):
            start = match.end() - 1  # Position of '{'
            content, _ = self._extract_balanced_content(self.original_text, start)
            caption_texts.append(content)
        return caption_texts

    def _extract_item_commands(self) -> list[str]:
        r"""Extract content from \item commands."""
        item_texts = []
        item_pattern = r"\\item\s+([^\\]+?)(?=\\|$)"
        for match in re.finditer(item_pattern, self.original_text, re.DOTALL):
            content = match.group(1)
            # Only strip leading whitespace, preserve trailing spaces
            content = content.lstrip()
            # Only extract if it's plain text (not nested lists or commands except \text{})
            if content and not re.search(r"\\(?!text\{|txt\{|textbf\{|textit\{)", content):
                # Remove any \text{} commands temporarily to check for actual text
                temp_content = re.sub(r"\\(?:text|txt|textbf|textit)\{[^}]*\}", "", content)
                if temp_content.strip():
                    item_texts.append(content)
        return item_texts

    def _extract_table_cells(self) -> list[str]:
        r"""Extract plain text content from table cells, excluding \\text{} commands."""
        table_texts = []
        # Find all tabular environments
        tabular_pattern = r"\\begin\{tabular\}\{[^}]+\}(.*?)\\end\{tabular\}"
        for tabular_match in re.finditer(tabular_pattern, self.original_text, re.DOTALL):
            tabular_content = tabular_match.group(1)
            # Split by table rules to get header and body sections
            parts = re.split(r"\\(?:toprule|midrule|bottomrule)", tabular_content)
            # parts[0] is before toprule (usually empty), parts[1] is header, parts[2] is body
            for section in parts[1:3]:  # Process header and body sections
                rows = section.split("\\\\")
                for row in rows:
                    row_stripped = row.strip()
                    if not row_stripped:
                        continue
                    # Split by & to get cells
                    cells = row_stripped.split("&")
                    for cell in cells:
                        cell_stripped = cell.strip()
                        # Only extract if it's simple text (not complex LaTeX)
                        if cell_stripped and not re.search(r"\\(?!text\{|txt\{|textbf\{|textit\{)", cell_stripped):
                            # Extract only plain text portions, excluding \text{} commands to avoid double-extraction
                            plain_text_only = re.sub(r"\\(?:text|txt|textbf|textit)\{[^}]*\}", "", cell_stripped)
                            if plain_text_only.strip():
                                table_texts.append(plain_text_only.strip())
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
            return self._check_decimal_separator(self.original_text)

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

        # Apply replacements - table cells must be replaced before text commands
        # to prevent mismatch when cells contain \text{} commands
        replaced = self.original_text

        if table_texts:
            replaced = self._replace_table_cells(replaced, table_translations)

        if texts:
            replaced = self._replace_text_commands(replaced, text_translations)

        if section_texts:
            replaced = self._replace_section_commands(replaced, section_translations)

        if caption_texts:
            replaced = self._replace_caption_commands(replaced, caption_translations)

        if item_texts:
            replaced = self._replace_item_commands(replaced, item_translations)

        # Only replace periods with commas outside text blocks for certain languages
        return self._check_decimal_separator(replaced)

    @property
    def text(self) -> str:
        """
        Return the translated LaTeX string.

        Returns
        -------
        str
            The translated LaTeX string.
        """
        if not self._translation:
            self._translation = self._translate_latex()
        return self._translation

    def __str__(self) -> str:
        """
        Return the translated LaTeX string.

        Returns
        -------
        str
            The translated LaTeX string.
        """
        return self.text
