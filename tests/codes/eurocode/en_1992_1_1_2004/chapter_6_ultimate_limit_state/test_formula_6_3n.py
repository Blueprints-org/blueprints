"""Testing formula 6.3N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_3n import Form6Dot3nShearCapacityWithoutRebar
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot3nShearCapacityWithoutRebar:
    """Validation for formula 6.3N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        k = 1.0
        f_ck = 30.0

        # Object to test
        formula = Form6Dot3nShearCapacityWithoutRebar(k=k, f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.19170289512

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k", "f_ck"),
        [
            (-1.0, 30.0),  # k is negative
            (1.0, -30.0),  # f_ck is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, k: float, f_ck: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot3nShearCapacityWithoutRebar(k=k, f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{min} = 0.035 \cdot k^{3/2} \cdot f_{ck}^{1/2} = 0.035 \cdot 1.000^{3/2} \cdot 30.000^{1/2} = 0.192 \ MPa",
            ),
            ("short", r"v_{min} = 0.192 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k = 1.0
        f_ck = 30.0

        # Object to test
        latex = Form6Dot3nShearCapacityWithoutRebar(k=k, f_ck=f_ck).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
