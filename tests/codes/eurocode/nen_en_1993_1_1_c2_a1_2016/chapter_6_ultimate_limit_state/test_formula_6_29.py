"""Testing formula 6.29 of NEN-EN 1993-1-1+A1:2016."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_29 import Form6Dot29ReducedYieldStrength
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot29ReducedYieldStrength:
    """Validation for formula 6.29 from NEN-EN 1993-1-1+A1:2016."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        rho = 0.75
        f_y = 355.0  # MPa

        # Object to test
        formula = Form6Dot29ReducedYieldStrength(rho=rho, f_y=f_y)

        # Expected result, manually calculated
        manually_calculated_result = 88.75  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("rho", "f_y"),
        [
            (-0.75, 355.0),  # rho is negative
            (0.75, -355.0),  # f_y is negative
            (1.75, 355.0),  # one_minus_rho is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, rho: float, f_y: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot29ReducedYieldStrength(rho=rho, f_y=f_y)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{y,red} = (1 - \rho) \cdot f_y = (1 - 0.750) \cdot 355.000 = 88.750 \ MPa",
            ),
            (
                "complete_with_units",
                r"f_{y,red} = (1 - \rho) \cdot f_y = (1 - 0.750) \cdot 355.000 \ MPa = 88.750 \ MPa",
            ),
            ("short", r"f_{y,red} = 88.750 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        rho = 0.75
        f_y = 355.0  # MPa

        # Object to test
        latex = Form6Dot29ReducedYieldStrength(rho=rho, f_y=f_y).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
