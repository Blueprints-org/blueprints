"""Translate LaTeX text using CSV-based manual translations and Google Translate."""

import asyncio
import csv
import os
import re

from googletrans import Translator

COMMA_LANGUAGES = ["nl", "de", "fr", "es"]  # Languages that use comma as decimal separator


class Translate:
    """
    Utility class for extracting and translating LaTeX text.
    WARNING: Uses Google Translate service when translations haven't been manually entered.
    """

    def __init__(self, latex: str, dest_language: str, service_urls: list[str] | None = None) -> None:
        r"""
        Initialize the Translate class with text and destination language.
        Warning: uses Google Translate service when translations haven't been manually entered.

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
        self.translation_dict = self._load_translation_dict(dest_language)
        self.translated = self.translate_latex(self.original, self.dest_language)

    def _load_translation_dict(self, dest_language: str) -> dict:
        r"""
        Load translation dictionary from a CSV file if it exists.
        The CSV should be named '<dest_language>.csv' and be in the same directory as this script.
        Returns a dict mapping source text to translated text.
        """
        csv_path = os.path.join(os.path.dirname(__file__), f"{dest_language}.csv")
        translation_dict = {}
        if os.path.isfile(csv_path):
            try:
                with open(csv_path, encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) >= 2:
                            translation_dict[row[1].strip()] = row[2].strip()
            except Exception:
                pass
        return translation_dict

    def _wildcard_match(self, text: str) -> str | None:
        r"""
        If a manual translation contains '**', treat it as a wildcard and match/replace the corresponding substring in the input text.
        Returns the translated string if a wildcard match is found, else None.
        """
        for src, tgt in getattr(self, "translation_dict", {}).items():
            if "**" in src:
                parts = src.split("**")
                if len(parts) == 2:
                    prefix, suffix = parts
                    if text.startswith(prefix) and text.endswith(suffix) and len(text) > len(prefix) + len(suffix):
                        middle = text[len(prefix) : -len(suffix)] if len(suffix) > 0 else text[len(prefix) :]
                        return tgt.replace("**", middle)
        return None

    def translate_bulk(self, texts: list, dest_language: str) -> list:
        r"""
        Translate a list of strings to the destination language.
        First checks the translation dictionary loaded from CSV. If not found, uses Google Translate.

        Parameters
        ----------
        texts : list[str]
            The list of strings to be translated.
        dest_language : str
            The target language code.

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
            elif "**" in t:
                results.append(self._wildcard_match(t))
            else:
                results.append(None)
                missing.append(t)
                missing_indices.append(i)

        # for missing texts, use Google Translate
        if missing:
            # Use Google Translate for all missing texts in bulk
            translations = self.translator.translate(missing, dest=dest_language)
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
                    translations = loop.run_until_complete(translations)
            translated_texts = [tr.text for tr in translations]
            for idx, val in zip(missing_indices, translated_texts):
                results[idx] = val
        return results

    @staticmethod
    def extract_text_commands(s: str) -> list:
        r"""
        Extract all substrings between \text{...} in the given string.

        Parameters
        ----------
        s : str
            The string to search for LaTeX \text{...} commands.

        Returns
        -------
        list[str]
            List of substrings found between \text{...}.
        """
        return re.findall(r"\\text\{(.*?)\}", s)

    @staticmethod
    def replace_text_commands(s: str, replacements: list) -> str:
        r"""
        Replace all \text{...} in the string with the corresponding replacements.

        Parameters
        ----------
        s : str
            The string containing LaTeX \text{...} commands.
        replacements : list[str]
            The list of replacement strings.

        Returns
        -------
        str
            The string with \text{...} replaced by the corresponding replacements.
        """
        replacements_iter = iter(replacements)

        def repl(_: re.Match) -> str:
            r"""Replacement function for re.sub to replace \text{...} blocks.

            Parameters
            ----------
            _: re.Match
                The regex match object (not used).

            Returns
            -------
            str
                The string with \text{...} replaced by the corresponding replacements.
            """
            return r"\text{" + next(replacements_iter) + "}"

        return re.sub(r"\\text\{(.*?)\}", repl, s)

    @staticmethod
    def replace_periods_outside_text_blocks(s: str, to_comma: bool = True) -> str:
        r"""
        Replace all periods with commas outside of \text{...} blocks.
        If to_comma is False, does nothing.

        Parameters
        ----------
        s : str
            The LaTeX string to process.
        to_comma : bool, optional
            If True, replace periods with commas outside of \text{...} blocks. Default is True.

        Returns
        -------
        str
            The processed LaTeX string with periods replaced by commas outside of \text{...} blocks if to_comma is True.
        """
        if not to_comma:
            return s
        # Use regex to split into text blocks and non-text blocks
        pattern = re.compile(r"(\\text\{.*?\})")
        parts = pattern.split(s)

        def is_text_block(seg: str) -> bool:
            return seg.startswith(r"\text{") and seg.endswith("}")

        new_segments = [seg if is_text_block(seg) else seg.replace(".", ",") for seg in parts]
        return "".join(new_segments)

    def translate_latex(self, s: str, dest_language: str) -> str:
        r"""
        Extract, translate, and reconstruct LaTeX string with translated text commands.
        For certain languages, also replace periods with commas outside of text blocks.

        Parameters
        ----------
        s : str
            The LaTeX string to process.
        dest_language : str
            The target language code.

        Returns
        -------
        str
            The LaTeX string with translated \text{...} commands.
        """
        texts = self.extract_text_commands(s)
        if not texts:
            # If no text blocks, still apply period-to-comma if needed
            return self.replace_periods_outside_text_blocks(s, to_comma=(dest_language in COMMA_LANGUAGES))
        translations = self.translate_bulk(texts, dest_language)
        replaced = self.replace_text_commands(s, translations)
        # Only replace periods with commas outside text blocks for certain languages
        return self.replace_periods_outside_text_blocks(replaced, to_comma=(dest_language in COMMA_LANGUAGES))

    def __str__(self) -> str:
        """
        Return the translated LaTeX string.

        Returns
        -------
        str
            The translated LaTeX string.
        """
        return self.translated


if __name__ == "__main__":
    example_latex = (
        r"\text{Checking normal force: compression checks applied using chapter 6.2.4.}\\ "
        r"\text{With formula 6.10:}\\N_{c,Rd} = \frac{A \cdot f_y}{\gamma_{M0}} = "
        r"\frac{14912.0 \cdot 355.0}{1.0} = 5293746.7 \ N\\\text{With formula 6.9:}\\CHECK "
        r"\to \left( \frac{N_{Ed}}{N_{c,Rd}} \leq 1 \right) \to \left( \frac{100000.0}{5293746.7} "
        r"\leq 1 \right) \to OK"
    )

    result_nl = Translate(example_latex, "nl")
