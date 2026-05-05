"""Testing formula 8.50 of prEN 1992-1-1:2023."""

import math

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_50 import (
    Form8Dot50AdditionalTensileForceDueToShear,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot50AdditionalTensileForceDueToShear:
    """Validation for formula 8.50 from prEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 1200e3
        theta = 21.8

        # Create object to test
        test_formula = Form8Dot50AdditionalTensileForceDueToShear(v_ed=v_ed, theta=theta)

        # Expected result, manually calculated
        manually_calculated_result = 1200e3 * (1 / math.tan(math.radians(theta)))  # N

        # Perform test by assert
        assert test_formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "theta"),
        [
            (-1000.0, 21.8),  # v_ed negative
        ],
    )
    def test_raise_error_when_negative_v_ed(self, v_ed: float, theta: float) -> None:
        """Test negative v_ed raises error."""
        with pytest.raises(NegativeValueError):
            Form8Dot50AdditionalTensileForceDueToShear(v_ed=v_ed, theta=theta)

    @pytest.mark.parametrize(
        ("v_ed", "theta"),
        [
            (1000.0, 0.0),  # theta zero
            (1000.0, -21.8),  # theta negative
        ],
    )
    def test_raise_error_when_invalid_theta(self, v_ed: float, theta: float) -> None:
        """Test zero or negative theta raises error."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot50AdditionalTensileForceDueToShear(v_ed=v_ed, theta=theta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"N_{Vd} = |V_{Ed}| \cdot \cot\theta = |1200000.000| \cdot \cot21.800 = 3000214.035 \ N"),
            ("short", r"N_{Vd} = 3000214.035 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 1200e3
        theta = 21.8

        # Object to test
        test_latex = Form8Dot50AdditionalTensileForceDueToShear(v_ed=v_ed, theta=theta).latex()

        actual = {
            "complete": test_latex.complete,
            "short": test_latex.short,
        }
        assert expected == actual[representation]
