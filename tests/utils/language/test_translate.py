"""Tests for language translations."""

import os
import tempfile
from unittest.mock import MagicMock, patch

from blueprints.utils.language.translate import LatexTranslator


class TestLatexTranslator:
    """Tests for language translations in Blueprints."""

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        # Path to the test CSV file
        self.test_csv_path = os.path.join(os.path.dirname(__file__), "example_language.csv")

    def test_translate_with_formula_manual(self) -> None:
        """Test LatexTranslator with translation from CSV."""
        latex = r"\txt{This is a test}"
        result = LatexTranslator(latex, "example_language", custom_csv=self.test_csv_path)
        # csv entry is "This is a test","This is a translation"
        assert str(result) == r"\txt{This is a translation}"

    def test_translate_with_formula_manual_and_wildcard(self) -> None:
        """Test LatexTranslator with wildcard translation from CSV."""
        latex = r"\txt{This IS A TEST WITH A wildcard}"
        result = LatexTranslator(latex, "example_language", custom_csv=self.test_csv_path)
        # csv entry is "This ** wildcard","Different text ** here"
        assert str(result) == r"\txt{Different text IS A TEST WITH A here}"

    def test_translate_with_formula_manual_and_multiple_wildcard(self) -> None:
        """Test LatexTranslator with multiple wildcard translation from CSV."""
        latex = r"\txt{Wildcards CAN BE used MULTIPLE TIMES here AND AS OFTEN AS YOU want}"
        result = LatexTranslator(latex, "example_language", custom_csv=self.test_csv_path)
        # csv entry is "Wildcards ** used ** here ** want","Completely ** different ** text ** here"
        assert str(result) == r"\txt{Completely CAN BE different MULTIPLE TIMES text AND AS OFTEN AS YOU here}"

    def test_translate_with_comma_in_text(self) -> None:
        """Test LatexTranslator with comma in text from CSV."""
        latex = r"\txt{This quote contains, a comma}"
        result = LatexTranslator(latex, "example_language", custom_csv=self.test_csv_path)
        # csv entry is "This quote contains, a comma","Which is handled, correctly"
        assert str(result) == r"\txt{Which is handled, correctly}"

    def test_translate_with_special_characters(self) -> None:
        """Test LatexTranslator with special characters from CSV."""
        latex = r"\txt{Special characters: %$#& (╯°□°) ╯︵ ┻━┻}"
        result = LatexTranslator(latex, "example_language", custom_csv=self.test_csv_path)
        # csv entry is "Special characters: %$#& (╯°□°) ╯︵ ┻━┻","Works perfectly"
        assert str(result) == r"\txt{Works perfectly}"

    def test_not_translated_value(self) -> None:
        """Test LatexTranslator with special characters from CSV."""
        latex = r"This is true in all languages"
        result = LatexTranslator(latex, "example_language", custom_csv=self.test_csv_path)
        # csv entry is "This is true in all languages","-"
        assert str(result) == r"This is true in all languages"

    def test_translate_with_mismatched_wildcards(self) -> None:
        """Test LatexTranslator behavior when CSV entry has mismatched wildcard counts."""
        latex = r"\txt{Mismatched wildcard amount HERE}"
        result = LatexTranslator(latex, "example_language", custom_csv=self.test_csv_path)
        # csv entry is "Mismatched wildcard amount ** here","Mismatched wildcard amount ** ** not allowed"
        assert str(result) == r"\txt{Mismatched wildcard amount HERE}"

    def test_words_not_in_dictionary(self) -> None:
        """Test LatexTranslator with words that are not in dictionary (and so off topic that it will never be),
        such that it uses Google Translate.
        """
        example_latex = r"\txt{My favourite band is Ad Infinitum.}"
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_response = MagicMock()
            mock_response.text = "Mijn favoriete band is Ad Infinitum."
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [mock_response]
            mock_translator.return_value = mock_instance

            result = LatexTranslator(example_latex, "nl")
            assert str(result) == r"\txt{Mijn favoriete band is Ad Infinitum.}"

    def test_fake_language(self) -> None:
        """Test LatexTranslator with obscure language code, so that it uses Google Translate."""
        example_latex = r"\txt{This should return as just English}"
        result = LatexTranslator(example_latex, "not-a-real-language")
        assert str(result) == r"\txt{This should return as just English}"

    def test_conversion_of_decimal_comma(self) -> None:
        """Test LatexTranslator with conversion of decimal comma."""
        example_latex = r"\txt{$3.14$}"
        result = LatexTranslator(example_latex, "nl")
        assert str(result) == r"\txt{$3,14$}"

    def test_non_conversion_of_decimal_comma_in_text(self) -> None:
        """Test LatexTranslator with non-conversion of decimal comma in text."""
        example_latex = r"\txt{. . .}"
        result = LatexTranslator(example_latex, "nl")
        assert str(result) == r"\txt{. . .}"

    def test_combination_of_equation_and_text(self) -> None:
        """Test LatexTranslator with combination of equation and text."""
        example_latex = r"\txt{With formula 6.83:} \newline \txt{$E = mc^2 = 5.3 \cdot 10^{2} J$}"
        result_nl = LatexTranslator(example_latex, "nl")
        assert str(result_nl) == r"\txt{Met formule 6.83:} \newline \txt{$E = mc^2 = 5,3 \cdot 10^{2} J$}"

    def test_latex_with_multiple_text_blocks(self) -> None:
        """Test LatexTranslator with LaTeX containing multiple text blocks."""
        example_latex = r"\txt{Number one} \newline \txt{Number two}"
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_response1 = MagicMock()
            mock_response1.text = "Nummer één"
            mock_response2 = MagicMock()
            mock_response2.text = "Nummer twee"
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [mock_response1, mock_response2]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            assert str(result_nl) == r"\txt{Nummer één} \newline \txt{Nummer twee}"

    def test_nested_commands(self) -> None:
        """Test LatexTranslator with nested LaTeX commands."""
        example_latex = r"\txt{Normal text with }\textbf{bold text, }\textit{italic text}\textbf{\textit{ and both.}}"
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [
                MagicMock(text="Normale tekst met"),
                MagicMock(text="vetgedrukte tekst,"),
                MagicMock(text="cursieve tekst"),
                MagicMock(text="en beide."),
            ]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            assert str(result_nl) == r"\txt{Normale tekst met }\textbf{vetgedrukte tekst, }\textit{cursieve tekst}\textbf{\textit{ en beide.}}"

    def test_figure_caption(self) -> None:
        """Test LatexTranslator with figure caption translation."""
        example_latex = (
            r"\begin{figure}[h] \centering \includegraphics[width=0.4\textwidth]{path.png} \caption{This is the figure caption.} \end{figure}"
        )
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [MagicMock(text="Dit is het onderschrift van de figuur.")]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            expected = (
                r"\begin{figure}[h] \centering \includegraphics[width=0.4\textwidth]{path.png} "
                r"\caption{Dit is het onderschrift van de figuur.} \end{figure}"
            )
            assert str(result_nl) == expected

    def test_title_translation(self) -> None:
        """Test LatexTranslator with title translation."""
        example_latex = r"\title{This is the document title}"
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [MagicMock(text="Dit is de documenttitel")]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            assert str(result_nl) == r"\title{Dit is de documenttitel}"

    def test_section_translation(self) -> None:
        """Test LatexTranslator with section translation."""
        example_latex = r"\section{Introduction of the subject}"
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [MagicMock(text="Introductie van het onderwerp")]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            assert str(result_nl) == r"\section{Introductie van het onderwerp}"

    def test_subsection_translation(self) -> None:
        """Test LatexTranslator with subsection translation."""
        example_latex = r"\subsection{Background}"
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [MagicMock(text="Achtergrond")]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            assert str(result_nl) == r"\subsection{Achtergrond}"

    def test_subsubsection_translation(self) -> None:
        """Test LatexTranslator with subsubsection translation."""
        example_latex = r"\subsubsection{Part 1}"
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [MagicMock(text="Deel 1")]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            assert str(result_nl) == r"\subsubsection{Deel 1}"

    def test_table_translation(self) -> None:
        """Test LatexTranslator with table translation."""
        example_latex = (
            r"\begin{table}[h] \centering \begin{tabular}{lll} \toprule Header 1 & Header 2 & Header 3 with math $E=mc^2$ \\ "
            r"\midrule Row 1 Col 1 & Row 1 Col 2 with inline math $a^2 + b^2 = 25.0$ & Row 1 Col 3 \\ "
            r"Row 2 Col 1 & Row 2 Col 2 & Row 2 Col 3 \\ "
            r"Apple & Banana & Cherry \\ "
            r"Dog & Elephant & Frog \\ "
            r"Random text & More words & $x = y + z$ \\ "
            r"\bottomrule \end{tabular} \end{table}"
        )
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            # Now includes header translations (Header 1, Header 2, Header 3 with math)
            mock_instance.translate.return_value = [
                MagicMock(text="Kop 1"),
                MagicMock(text="Kop 2"),
                MagicMock(text="Kop 3 met wiskunde $E=mc^2$"),
                MagicMock(text="Rij 1 Kol 1"),
                MagicMock(text="Rij 1 Kol 2 met inline wiskunde $a^2 + b^2 = 25,0$"),
                MagicMock(text="Rij 1 Kol 3"),
                MagicMock(text="Rij 2 Kol 1"),
                MagicMock(text="Rij 2 Kol 2"),
                MagicMock(text="Rij 2 Kol 3"),
                MagicMock(text="Appel"),
                MagicMock(text="Banaan"),
                MagicMock(text="Kers"),
                MagicMock(text="Hond"),
                MagicMock(text="Olifant"),
                MagicMock(text="Kikker"),
                MagicMock(text="Random tekst"),
                MagicMock(text="Meer woorden"),
                MagicMock(text="$x = y + z$"),
            ]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            # Note: Math expressions are preserved inline, decimal commas converted
            expected = (
                r"\begin{table}[h] \centering \begin{tabular}{lll} \toprule Kop 1  &  Kop 2  &  Kop 3 met wiskunde $E=mc^2$ \\ "
                r"\midrule Rij 1 Kol 1  &  Rij 1 Kol 2 met inline wiskunde $a^2 + b^2 = 25,0$  &  Rij 1 Kol 3 \\ "
                r"Rij 2 Kol 1  &  Rij 2 Kol 2  &  Rij 2 Kol 3 \\ "
                r"Appel  &  Banaan  &  Kers \\ "
                r"Hond  &  Olifant  &  Kikker \\ "
                r"Random tekst  &  Meer woorden  &  $x = y + z$ \\ "
                r"\bottomrule \end{tabular} \end{table}"
            )
            assert str(result_nl) == expected

    def test_empty_table(self) -> None:
        """Test LatexTranslator with empty table translation."""
        example_latex = (
            r"\begin{table}[h] \centering \begin{tabular}{lll} \toprule Header 1 & Header 2 & Header 3 \\ "
            r"\midrule \\ \bottomrule \end{tabular} \end{table}"
        )
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            # Now includes header translations
            mock_instance.translate.return_value = [
                MagicMock(text="Kop 1"),
                MagicMock(text="Kop 2"),
                MagicMock(text="Kop 3"),
            ]
            mock_translator.return_value = mock_instance
            result_nl = LatexTranslator(example_latex, "nl")
            expected = (
                r"\begin{table}[h] \centering \begin{tabular}{lll} \toprule Kop 1  &  Kop 2  &  Kop 3 \\ "
                r"\midrule \\ \bottomrule \end{tabular} \end{table}"
            )
            assert str(result_nl) == expected

    def test_itemize_translation(self) -> None:
        """Test LatexTranslator with itemize translation."""
        example_latex = r"\begin{itemize} \item First \item Second thing \item Third \end{itemize}"
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [MagicMock(text="Eerst"), MagicMock(text="Tweede ding"), MagicMock(text="Derde")]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            assert str(result_nl) == r"\begin{itemize} \item Eerst \item Tweede ding \item Derde \end{itemize}"

    def test_enumerate_translation(self) -> None:
        """Test LatexTranslator with enumerate translation."""
        example_latex = r"\begin{enumerate} \item One \item Two \end{enumerate}"
        # Mock Google Translate for deterministic test
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [MagicMock(text="Een"), MagicMock(text="Twee")]
            mock_translator.return_value = mock_instance

            result_nl = LatexTranslator(example_latex, "nl")
            assert str(result_nl) == r"\begin{enumerate} \item Een \item Twee \end{enumerate}"

    def test_equation_translation(self) -> None:
        """Test LatexTranslator with equation translation."""
        example_latex = r"\begin{equation} E = mc^2 = 20.0 \tag{3.14} \end{equation}"
        result_nl = LatexTranslator(example_latex, "nl")
        assert str(result_nl) == r"\begin{equation} E = mc^2 = 20,0 \tag{3.14} \end{equation}"

    def test_non_english_source_language(self) -> None:
        """Test LatexTranslator with non-English source language using CSV."""
        # Create a temporary CSV with multiple languages
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="", encoding="utf-8") as f:
            f.write("en,nl,de,fr\n")
            f.write('"Hello","Hallo","Hallo","Bonjour"\n')
            f.write('"Goodbye","Tot ziens","Auf Wiedersehen","Au revoir"\n')
            temp_csv_path = f.name

        try:
            # Test translating from Dutch to German
            latex_nl = r"\txt{Hallo} and \txt{Tot ziens}"
            result_de = LatexTranslator(latex_nl, destination_language="de", source_language="nl", custom_csv=temp_csv_path)
            assert str(result_de) == r"\txt{Hallo} and \txt{Auf Wiedersehen}"

            # Test translating from French to English
            latex_fr = r"\txt{Bonjour} and \txt{Au revoir}"
            result_en = LatexTranslator(latex_fr, destination_language="en", source_language="fr", custom_csv=temp_csv_path)
            assert str(result_en) == r"\txt{Hello} and \txt{Goodbye}"

            # Test translating from German to French
            latex_de = r"\txt{Hallo} and \txt{Auf Wiedersehen}"
            result_fr = LatexTranslator(latex_de, destination_language="fr", source_language="de", custom_csv=temp_csv_path)
            assert str(result_fr) == r"\txt{Bonjour} and \txt{Au revoir}"
        finally:
            # Clean up temporary file
            os.unlink(temp_csv_path)

    def test_translation_network_error_graceful_fallback(self) -> None:
        """Test that network errors result in graceful fallback to original text."""
        latex = r"\txt{Untranslated phrase}"

        # Mock Translator to raise Exception (simulating network error)
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.side_effect = Exception("Connection failed")
            mock_translator.return_value = mock_instance

            result = LatexTranslator(latex, "nl")

            # Should return original text on failure
            assert str(result) == r"\txt{Untranslated phrase}"

    def test_translation_api_error_graceful_fallback(self) -> None:
        """Test that API errors result in graceful fallback to original text."""
        latex = r"\txt{Another untranslated phrase}"

        # Mock Translator to raise generic Exception (e.g., rate limit, API error)
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_instance = MagicMock()
            mock_instance.translate.side_effect = Exception("API rate limit exceeded")
            mock_translator.return_value = mock_instance

            result = LatexTranslator(latex, "nl")

            # Should return original text on failure
            assert str(result) == r"\txt{Another untranslated phrase}"

    def test_translation_success_with_mock(self) -> None:
        """Test successful translation with mocked Google Translate."""
        latex = r"\txt{Mocked translation test}"

        # Mock successful translation
        with patch("blueprints.utils.language.translate.Translator") as mock_translator:
            mock_response = MagicMock()
            mock_response.text = "Gemockte vertaling test"
            mock_instance = MagicMock()
            mock_instance.translate.return_value = [mock_response]
            mock_translator.return_value = mock_instance

            result = LatexTranslator(latex, "nl")

            assert str(result) == r"\txt{Gemockte vertaling test}"
