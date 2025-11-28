"""Tests for language translations."""

from blueprints.language.translate import TranslateLatex


class TestTranslateLatex:
    """Tests for language translations in Blueprints."""

    def test_translate_with_formula_manual(self) -> None:
        """Test TranslateLatex with translation from CSV."""
        latex = r"\text{This is a test}"
        result = TranslateLatex(latex, "test")
        assert str(result) == r"\text{This is a translation}"

    def test_translate_with_formula_manual_and_wildcard(self) -> None:
        """Test TranslateLatex with wildcard translation from CSV."""
        latex = r"\text{This IS A TEST WITH A wildcard}"
        result = TranslateLatex(latex, "test")
        assert str(result) == r"\text{Different text IS A TEST WITH A here}"

    def test_translate_with_formula_manual_and_multiple_wildcard(self) -> None:
        """Test TranslateLatex with multiple wildcard translation from CSV."""
        latex = r"\text{Wildcards CAN BE used MULTIPLE TIMES here AND AS OFTEN AS YOU want}"
        result = TranslateLatex(latex, "test")
        assert str(result) == r"\text{Completely CAN BE different MULTIPLE TIMES text AND AS OFTEN AS YOU here}"

    def test_translate_with_comma_in_text(self) -> None:
        """Test TranslateLatex with comma in text from CSV."""
        latex = r"\text{This quote contains, a comma}"
        result = TranslateLatex(latex, "test")
        assert str(result) == r"\text{Which is handled, correctly}"

    def test_translate_with_special_characters(self) -> None:
        """Test TranslateLatex with special characters from CSV."""
        latex = r"\text{Special characters: %$#& (╯°□°) ╯︵ ┻━┻}"
        result = TranslateLatex(latex, "test")
        assert str(result) == r"\text{Works perfectly}"

    def test_translate_with_mismatched_wildcards(self) -> None:
        """Test TranslateLatex with mismatched wildcard counts in CSV (usually continues to Google Translate, but test language does not exist)."""
        latex = r"\text{Mismatched wildcard amount HERE}"
        result = TranslateLatex(latex, "test")
        assert str(result) == r"\text{Mismatched wildcard amount HERE}"

    def test_word_thats_not_in_dictionary(self) -> None:
        """Test TranslateLatex with word that's not in dictionary, so that it used Google Translate."""
        example_latex = r"\text{My favourite band is Ad Infinitum.}"
        result = TranslateLatex(example_latex, "nl")
        assert str(result) == r"\text{Mijn favoriete band is Ad Infinitum.}"

    def test_fake_language(self) -> None:
        """Test TranslateLatex with obscure language code, so that it used Google Translate."""
        example_latex = r"\text{This should return as just English}"
        result = TranslateLatex(example_latex, "not+a+real+language")
        assert str(result) == r"\text{This should return as just English}"

    def test_convertion_of_decimal_comma(self) -> None:
        """Test TranslateLatex with conversion of decimal comma."""
        example_latex = r"3.14"
        result = TranslateLatex(example_latex, "nl")
        assert str(result) == r"3,14"

    def test_non_conversion_of_decimal_comma_in_text(self) -> None:
        """Test TranslateLatex with non-conversion of decimal comma in text."""
        example_latex = r"\text{. . .}"
        result = TranslateLatex(example_latex, "nl")
        assert str(result) == r"\text{. . .}"

    def test_combination_of_equation_and_text(self) -> None:
        """Test TranslateLatex with combination of equation and text."""
        example_latex = r"\text{With formula 6.83:} \\ E = mc^2 = 5.3 \cdot 10^{2} J"
        result_nl = TranslateLatex(example_latex, "nl")
        assert str(result_nl) == r"\text{Met formule 6.83:} \\ E = mc^2 = 5,3 \cdot 10^{2} J"

    def test_latex_with_multiple_text_blocks(self) -> None:
        """Test TranslateLatex with LaTeX containing multiple text blocks."""
        example_latex = r"\text{Number one} \\ \text{Number two}"
        result_nl = TranslateLatex(example_latex, "nl")
        assert str(result_nl) == r"\text{Nummer één} \\ \text{Nummer twee}"
