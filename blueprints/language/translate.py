"""Translate LaTeX text using CSV-based manual translations and Google Translate."""

import asyncio
import csv
import logging
import os
import re

from googletrans import Translator


class TranslateLatex:
    """
    Utility class for extracting and translating LaTeX text.
    WARNING: uses Google Translate service when translations haven't been manually entered.
    When the services are not available, (sections of) text will be left in English.
    """

    def __init__(self, latex: str, dest_language: str, service_urls: list[str] | None = None) -> None:
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
        self.translation_dict = self._load_translation_dict(dest_language.replace("-", "_"))  # Google uses underscores instead of hyphens
        self.translated = self._translate_latex()

    def _load_translation_dict(self, dest_language: str) -> dict:
        r"""
        Load translation dictionary from a CSV file if it exists.
        The CSV should be named '<dest_language>.csv' and be in the same directory as this script.
        Returns a dict mapping source text to translated text.
        Handles quoted fields and commas within quotes.
        """
        csv_path = os.path.join(os.path.dirname(__file__), f"{dest_language}.csv")
        translation_dict = {}
        if os.path.isfile(csv_path):
            with open(csv_path, encoding="utf-8", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Skip header row
                for row in reader:
                    if len(row) == 2:
                        translation_dict[row[0]] = row[1]
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

    def _translate_bulk(self, texts: list) -> list:
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
        results = []
        missing = []
        missing_indices = []

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
                translated_texts = [tr.text for tr in translations]
            except Exception:
                # Failsafe: if translation fails, keep original English text
                translated_texts = missing
                logging.exception("Google translation failed, using original English text.")

            for idx, val in zip(missing_indices, translated_texts):
                results[idx] = val
        return results

    def _replace_text_commands(self, replacements: list) -> str:
        r"""
        Replace all \text{...} in the string with the corresponding replacements.

        Parameters
        ----------
        replacements : list[str]
            The list of replacement strings.

        Returns
        -------
        str
            The string with \text{...} replaced by the corresponding replacements.
        """
        replacements_iter = iter(replacements)

        def repl(_: re.Match) -> str:
            return r"\text{" + next(replacements_iter) + "}"

        return re.sub(r"\\text\{(.*?)\}", repl, self.original)

    def _check_decimal_separator(self, s: str) -> str:
        r"""
        Replace all periods with commas outside of \text{...} blocks.

        Parameters
        ----------
        s : str
            The LaTeX string to process.

        Returns
        -------
        str
            The processed LaTeX string with periods replaced by commas outside of \text{...} blocks if in a relevant language.
        """
        # Languages that use comma as decimal separator
        comma_decimal_languages_1 = ["bg", "ca", "cs", "da", "de", "el", "es", "et", "eu", "fi", "fr", "gl", "hr", "hu", "is", "it", "lt", "lv"]
        comma_decimal_languages_2 = ["nl", "no", "pl", "pt", "ro", "ru", "sk", "sl", "sr", "sv", "tr", "uk"]
        if self.dest_language not in comma_decimal_languages_1 + comma_decimal_languages_2:
            return s

        # Use regex to split into text blocks and non-text blocks
        pattern = re.compile(r"(\\text\{.*?\})")
        parts = pattern.split(s)

        def is_text_block(seg: str) -> bool:
            return seg.startswith(r"\text{") and seg.endswith("}")

        new_segments = [seg if is_text_block(seg) else seg.replace(".", ",") for seg in parts]
        return "".join(new_segments)

    def _translate_latex(self) -> str:
        r"""
        Extract, translate, and reconstruct LaTeX string with translated text commands.
        For certain languages, also replace periods with commas outside of text blocks.

        Returns
        -------
        str
            The LaTeX string with translated \text{...} commands.
        """
        texts = re.findall(r"\\text\{(.*?)\}", self.original)
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
