"""Testing formula 5.17 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_17 import Form5Dot17EffectiveLengthBucklingLoad
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot17EffectiveLengthBucklingLoad:
    """Validation for formula 5.17 from EN 1992-1-1:2004."""

    @pytest.fixture
    def form_5_17(self) -> Form5Dot17EffectiveLengthBucklingLoad:
        """Setup and teardown for test."""
        return Form5Dot17EffectiveLengthBucklingLoad(ei=1_000_000, n_b=5)

    def test_evaluation(self, form_5_17: Form5Dot17EffectiveLengthBucklingLoad) -> None:
        """Test the evaluation of the result."""
        # Expected result, manually calculated
        manually_calculated_result = 1404.96  # M
        assert form_5_17 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("ei", "n_b"),
        [
            (-1_000_000, 5),
            (1_000_000, -5),
            (-1_000_000, -5),
        ],
    )
    def test_raise_error_when_zero_pars_are_given(self, ei: float, n_b: float) -> None:
        """Test zero values for ei, n_b."""
        with pytest.raises(NegativeValueError):
            Form5Dot17EffectiveLengthBucklingLoad(ei=ei, n_b=n_b)

    def test_raise_error_when_negative_pars_are_given(self) -> None:
        """Test negative values for ei, n_b."""
        ei = 1_000_000
        n_b = 0
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot17EffectiveLengthBucklingLoad(ei=ei, n_b=n_b)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"l_0 = \pi \cdot \sqrt{\frac{EI}{N_{b}}} = \pi \cdot \sqrt{\frac{1000000}{5}} = 1404.963",
            ),
            ("short", r"l_0 = 1404.963"),
        ],
    )
    def test_latex(self, form_5_17: Form5Dot17EffectiveLengthBucklingLoad, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        form_5_17_latex = form_5_17.latex()
        actual = {"complete": form_5_17_latex.complete, "short": form_5_17_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
