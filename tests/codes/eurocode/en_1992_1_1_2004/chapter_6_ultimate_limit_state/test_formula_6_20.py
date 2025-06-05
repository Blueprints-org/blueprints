"""Testing formula 6.20 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_20 import Form6Dot20LongitudinalShearStress
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot20LongitudinalShearStress:
    """Validation for formula 6.20 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        delta_f_d = 100000.0  # N
        h_f = 200.0  # mm
        delta_x = 500.0  # mm

        # Object to test
        formula = Form6Dot20LongitudinalShearStress(delta_f_d=delta_f_d, h_f=h_f, delta_x=delta_x)

        # Expected result, manually calculated
        manually_calculated_result = 1.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("delta_f_d", "h_f", "delta_x"),
        [
            (-100000.0, 200.0, 500.0),  # delta_f_d is negative
            (100000.0, -200.0, 500.0),  # h_f is negative
            (100000.0, 200.0, -500.0),  # delta_x is negative
            (100000.0, 200.0, 0.0),  # delta_x is zero
            (100000.0, 0.0, 500.0),  # h_f is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, delta_f_d: float, h_f: float, delta_x: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot20LongitudinalShearStress(delta_f_d=delta_f_d, h_f=h_f, delta_x=delta_x)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Ed} = \frac{\Delta F_{d}}{h_{f} \cdot \Delta x} = \frac{100000.000}{200.000 \cdot 500.000} = 1.000 \ MPa",
            ),
            ("short", r"v_{Ed} = 1.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        delta_f_d = 100000.0  # N
        h_f = 200.0  # mm
        delta_x = 500.0  # mm

        # Object to test
        latex = Form6Dot20LongitudinalShearStress(delta_f_d=delta_f_d, h_f=h_f, delta_x=delta_x).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
