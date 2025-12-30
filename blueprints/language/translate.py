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
                        logging.warning(f"Language '{dest_language}' not found in CSV header: {header}")
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

        for i, t in enumerate(texts):
            if hasattr(self, "translation_dict") and t in self.translation_dict:
                results.append(self.translation_dict[t])
            else:
                wildcard_result = self._wildcard_match(t)
                if wildcard_result is not None:
                    results.append(wildcard_result)
                else:
                    results.append(None)
                    missing.append(t)
                    missing_indices.append(i)

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
                # Failsafe: if translation fails, keep original English text
                translated_texts = missing
                logging.exception("Google translation failed, using original English text.")

            for idx, val in zip(missing_indices, translated_texts):
                results[idx] = val
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

        def repl(match: re.Match) -> str:
            nonlocal replacement_index
            command = match.group(1)  # Captures 'text', 'txt', 'textbf', or 'textit'
            content = match.group(2)

            # Check if content contains nested text commands
            if re.search(r"\\(text|txt|textbf|textit)\{", content):
                # Return as-is, let outer loop handle inner content
                return match.group(0)
            # This is innermost text, replace it
            if replacement_index < len(replacements):
                replacement = replacements[replacement_index]
                replacement_index += 1
                return f"\\{command}{{{replacement}}}"
            return match.group(0)  # No more replacements available

        # Keep applying replacements until no more nested commands remain
        prev = None
        result = self.original
        while prev != result:
            prev = result
            result = re.sub(r"\\(text|txt|textbf|textit)\{([^{}]*)\}", repl, result)

        return result

    def _check_decimal_separator(self, s: str) -> str:
        r"""
        Replace all periods with commas outside of \text{...}, \txt{...}, etc. blocks.

        Parameters
        ----------
        s : str
            The LaTeX string to process.

        Returns
        -------
        str
            The processed LaTeX string with periods replaced by commas outside of text blocks if in a relevant language.
        """
        # Languages that use comma as decimal separator
        comma_decimal_languages_1 = ["bg", "ca", "cs", "da", "de", "el", "es", "et", "eu", "fi", "fr", "gl", "hr", "hu", "is", "it", "lt", "lv"]
        comma_decimal_languages_2 = ["nl", "no", "pl", "pt", "ro", "ru", "sk", "sl", "sr", "sv", "tr", "uk"]
        if self.dest_language not in comma_decimal_languages_1 + comma_decimal_languages_2:
            return s

        # Use regex to split into text blocks and non-text blocks
        pattern = re.compile(r"(\\(?:text|txt|textbf|textit)\{.*?\})")
        parts = pattern.split(s)

        def is_text_block(seg: str) -> bool:
            return seg.startswith((r"\text{", r"\txt{", r"\textbf{", r"\textit{")) and seg.endswith("}")

        new_segments = [seg if is_text_block(seg) else seg.replace(".", ",") for seg in parts]
        return "".join(new_segments)

    def _translate_latex(self) -> str:
        r"""
        Extract, translate, and reconstruct LaTeX string with translated text commands.
        For certain languages, also replace periods with commas outside of text blocks.

        Returns
        -------
        str
            The LaTeX string with translated text commands.
        """
        texts = re.findall(r"\\(?:text|txt|textbf|textit)\{(.*?)\}", self.original)
        if not texts:
            # If no text blocks, still apply period-to-comma if needed
            return self._check_decimal_separator(self.original)
        translations = self._translate_bulk(texts)
        replaced = self._replace_text_commands(translations)
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
