"""Tests for language translations."""

from blueprints.language.translate import Translate


class TestCalculateRotationAngle:
    """Tests for language translations in Blueprints."""

    def test_translate_with_formula_manual(self) -> None:
        """Test Translate with translation from CSV."""
        latex = r"\text{This is a test}"
        result = Translate(latex, "nl")
        assert str(result) == r"\text{Dit is een test}"

    def test_translate_with_formula_manual_and_wildcard(self) -> None:
        """Test Translate with wildcard translation from CSV."""
        latex = r"\text{With formula this should not be translated:}"
        result = Translate(latex, "nl")
        assert str(result) == r"\text{Met formule this should not be translated:}"
