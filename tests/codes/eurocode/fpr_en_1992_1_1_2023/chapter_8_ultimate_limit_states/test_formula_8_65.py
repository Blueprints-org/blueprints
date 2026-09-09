"""Testing formula 8.65 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_65 import (
    Form8Dot65LongitudinalShearStressFlangeWebJunction,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot65LongitudinalShearStressFlangeWebJunction:
    """Validation for formula 8.65 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("delta_f_d", "h_f", "delta_x", "expected"),
        [
            (200000.0, 200.0, 2000.0, 0.5),  # 200000 over an area of 200 by 2000
            (0.0, 200.0, 2000.0, 0.0),  # no change of axial force over the length considered
            (200000.0, 100.0, 2000.0, 1.0),  # halving the flange thickness doubles the stress
        ],
    )
    def test_evaluation(self, delta_f_d: float, h_f: float, delta_x: float, expected: float) -> None:
        """Tests the evaluation of the result."""
        # Create object to test
        formula = Form8Dot65LongitudinalShearStressFlangeWebJunction(delta_f_d=delta_f_d, h_f=h_f, delta_x=delta_x)

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_raise_error_when_negative_values_are_given(self) -> None:
        """Test if error is raised for a change of axial force that is not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot65LongitudinalShearStressFlangeWebJunction(delta_f_d=-200000.0, h_f=200.0, delta_x=2000.0)

    @pytest.mark.parametrize(
        ("delta_f_d", "h_f", "delta_x"),
        [
            (200000.0, -200.0, 2000.0),  # h_f is negative
            (200000.0, 0.0, 2000.0),  # h_f is zero
            (200000.0, 200.0, -2000.0),  # delta_x is negative
            (200000.0, 200.0, 0.0),  # delta_x is zero
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, delta_f_d: float, h_f: float, delta_x: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot65LongitudinalShearStressFlangeWebJunction(delta_f_d=delta_f_d, h_f=h_f, delta_x=delta_x)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Ed} = \frac{\Delta F_d}{h_f \cdot \Delta x} = \frac{200000.000}{200.000 \cdot 2000.000} = 0.500 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Ed} = \frac{\Delta F_d}{h_f \cdot \Delta x} = "
                r"\frac{200000.000 \ N}{200.000 \ mm \cdot 2000.000 \ mm} = 0.500 \ MPa",
            ),
            ("short", r"\tau_{Ed} = 0.500 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot65LongitudinalShearStressFlangeWebJunction(delta_f_d=200000.0, h_f=200.0, delta_x=2000.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
