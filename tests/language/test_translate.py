"""Tests for language translations."""

import os

from blueprints.language.translate import TranslateLatex


class TestTranslateLatex:
    """Tests for language translations in Blueprints."""

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        # Path to the test CSV file
        self.test_csv_path = os.path.join(os.path.dirname(__file__), "example_language.csv")

    def test_translate_with_formula_manual(self) -> None:
        """Test TranslateLatex with translation from CSV."""
        latex = r"\txt{This is a test}"
        result = TranslateLatex(latex, "example_language", custom_csv_path=self.test_csv_path)
        # csv entry is "This is a test","This is a translation"
        assert str(result) == r"\txt{This is a translation}"

    def test_translate_with_formula_manual_and_wildcard(self) -> None:
        """Test TranslateLatex with wildcard translation from CSV."""
        latex = r"\txt{This IS A TEST WITH A wildcard}"
        result = TranslateLatex(latex, "example_language", custom_csv_path=self.test_csv_path)
        # csv entry is "This ** wildcard","Different text ** here"
        assert str(result) == r"\txt{Different text IS A TEST WITH A here}"

    def test_translate_with_formula_manual_and_multiple_wildcard(self) -> None:
        """Test TranslateLatex with multiple wildcard translation from CSV."""
        latex = r"\txt{Wildcards CAN BE used MULTIPLE TIMES here AND AS OFTEN AS YOU want}"
        result = TranslateLatex(latex, "example_language", custom_csv_path=self.test_csv_path)
        # csv entry is "Wildcards ** used ** here ** want","Completely ** different ** text ** here"
        assert str(result) == r"\txt{Completely CAN BE different MULTIPLE TIMES text AND AS OFTEN AS YOU here}"

    def test_translate_with_comma_in_text(self) -> None:
        """Test TranslateLatex with comma in text from CSV."""
        latex = r"\txt{This quote contains, a comma}"
        result = TranslateLatex(latex, "example_language", custom_csv_path=self.test_csv_path)
        # csv entry is "This quote contains, a comma","Which is handled, correctly"
        assert str(result) == r"\txt{Which is handled, correctly}"

    def test_translate_with_special_characters(self) -> None:
        """Test TranslateLatex with special characters from CSV."""
        latex = r"\txt{Special characters: %$#& (╯°□°) ╯︵ ┻━┻}"
        result = TranslateLatex(latex, "example_language", custom_csv_path=self.test_csv_path)
        # csv entry is "Special characters: %$#& (╯°□°) ╯︵ ┻━┻","Works perfectly"
        assert str(result) == r"\txt{Works perfectly}"

    def test_not_translated_value(self) -> None:
        """Test TranslateLatex with special characters from CSV."""
        latex = r"This is true in all languages"
        result = TranslateLatex(latex, "example_language", custom_csv_path=self.test_csv_path)
        # csv entry is "This is true in all languages","-"
        assert str(result) == r"This is true in all languages"

    def test_translate_with_mismatched_wildcards(self) -> None:
        """Test TranslateLatex behavior when CSV entry has mismatched wildcard counts."""
        latex = r"\txt{Mismatched wildcard amount HERE}"
        result = TranslateLatex(latex, "example_language", custom_csv_path=self.test_csv_path)
        # csv entry is "Mismatched wildcard amount ** here","Mismatched wildcard amount ** ** not allowed"
        assert str(result) == r"\txt{Mismatched wildcard amount HERE}"

    def test_words_not_in_dictionary(self) -> None:
        """Test TranslateLatex with words that are not in dictionary (and so off topic that it will never be),
        such that it uses Google Translate.
        """
        example_latex = r"\txt{My favourite band is Ad Infinitum.}"
        if not TranslateLatex(example_latex, "nl").translation_failed:
            result = TranslateLatex(example_latex, "nl")
            assert str(result) == r"\txt{Mijn favoriete band is Ad Infinitum.}"

    def test_fake_language(self) -> None:
        """Test TranslateLatex with obscure language code, so that it uses Google Translate."""
        example_latex = r"\txt{This should return as just English}"
        result = TranslateLatex(example_latex, "not-a-real-language")
        assert str(result) == r"\txt{This should return as just English}"

    def test_conversion_of_decimal_comma(self) -> None:
        """Test TranslateLatex with conversion of decimal comma."""
        example_latex = r"3.14"
        result = TranslateLatex(example_latex, "nl")
        assert str(result) == r"3,14"

    def test_non_conversion_of_decimal_comma_in_text(self) -> None:
        """Test TranslateLatex with non-conversion of decimal comma in text."""
        example_latex = r"\txt{. . .}"
        result = TranslateLatex(example_latex, "nl")
        assert str(result) == r"\txt{. . .}"

    def test_combination_of_equation_and_text(self) -> None:
        """Test TranslateLatex with combination of equation and text."""
        example_latex = r"\txt{With formula 6.83:} \newline E = mc^2 = 5.3 \cdot 10^{2} J"
        result_nl = TranslateLatex(example_latex, "nl")
        assert str(result_nl) == r"\txt{Met formule 6.83:} \newline E = mc^2 = 5,3 \cdot 10^{2} J"

    def test_latex_with_multiple_text_blocks(self) -> None:
        """Test TranslateLatex with LaTeX containing multiple text blocks."""
        example_latex = r"\txt{Number one} \newline \txt{Number two}"
        if not TranslateLatex(example_latex, "nl").translation_failed:
            result_nl = TranslateLatex(example_latex, "nl")
            assert str(result_nl) == r"\txt{Nummer één} \newline \txt{Nummer twee}"

    def test_nested_commands(self) -> None:
        """Test TranslateLatex with nested LaTeX commands."""
        example_latex = r"\txt{Normal text with }\textbf{bold text, }\textit{italic text}\textbf{\textit{ and both.}}"
        if not TranslateLatex(example_latex, "nl").translation_failed:
            result_nl = TranslateLatex(example_latex, "nl")
            assert str(result_nl) == r"\txt{Normale tekst met }\textbf{vetgedrukte tekst, }\textit{cursieve tekst}\textbf{\textit{ en beide.}}"
