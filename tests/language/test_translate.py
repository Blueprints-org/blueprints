"""Tests for language translations."""

from blueprints.language.translate import Translate


class TestCalculateRotationAngle:
    """Tests for language translations in Blueprints."""

    def test_translate_with_formula_manual(self) -> None:
        """Test Translate with translation from CSV."""
        latex = r"\text{This is a test}"
        result = Translate(latex, "_test")
        assert str(result) == r"\text{This is a translation}"

    def test_translate_with_formula_manual_and_wildcard(self) -> None:
        """Test Translate with wildcard translation from CSV."""
        latex = r"\text{This IS A TEST WITH A wildcard}"
        result = Translate(latex, "_test")
        assert str(result) == r"\text{Different text |IS A TEST WITH A| here}"

    def test_translate_with_formula_manual_and_multiple_wildcard(self) -> None:
        """Test Translate with multiple wildcard translation from CSV."""
        latex = r"\text{Wildcards CAN BE used MULTIPLE TIMES here AND AS OFTEN AS YOU want}"
        result = Translate(latex, "_test")
        assert str(result) == r"\text{Completely |CAN BE| different |MULTIPLE TIMES| text |AND AS OFTEN AS YOU| here}"
