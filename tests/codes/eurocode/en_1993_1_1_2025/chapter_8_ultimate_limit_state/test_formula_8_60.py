"""Testing formula 8.60 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_60 import (
    Form8Dot60ReducedYieldStrength,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot60ReducedYieldStrength:
    """Validation for formula 8.60 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        rho = 0.25
        f_y = 355.0

        # Object to test
        formula = Form8Dot60ReducedYieldStrength(rho=rho, f_y=f_y)

        # Expected result, manually calculated
        # result = (1 - 0.25) * 355 = 266.25
        manually_calculated_result = 266.25  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("rho", "f_y"),
        [
            (-0.25, 355.0),  # rho is negative
            (0.25, -355.0),  # f_y is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, rho: float, f_y: float) -> None:
        """Test negative values."""
        with pytest.raises(NegativeValueError):
            Form8Dot60ReducedYieldStrength(rho=rho, f_y=f_y)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{y,red} = (1 - \rho) \cdot f_y = (1 - 0.250) \cdot 355.000 = 266.250 \ MPa",
            ),
            (
                "complete_with_units",
                r"f_{y,red} = (1 - \rho) \cdot f_y = (1 - 0.250) \cdot 355.000 \ MPa = 266.250 \ MPa",
            ),
            ("short", r"f_{y,red} = 266.250 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        rho = 0.25
        f_y = 355.0

        # Object to test
        latex = Form8Dot60ReducedYieldStrength(rho=rho, f_y=f_y).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
