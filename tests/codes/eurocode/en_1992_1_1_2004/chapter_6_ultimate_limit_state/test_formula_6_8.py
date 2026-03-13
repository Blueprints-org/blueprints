"""Testing formula 6.8 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_8 import Form6Dot8ShearResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot8ShearResistance:
    """Validation for formula 6.8 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sw = 100.0
        s = 200.0
        z = 300.0
        f_ywd = 400.0
        theta = 45.0

        # Object to test
        formula = Form6Dot8ShearResistance(a_sw=a_sw, s=s, z=z, f_ywd=f_ywd, theta=theta)

        # Expected result, manually calculated
        manually_calculated_result = 60000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_sw", "s", "z", "f_ywd", "theta"),
        [
            (-100.0, 200.0, 300.0, 400.0, 45.0),  # a_sw is negative
            (100.0, -200.0, 300.0, 400.0, 45.0),  # s is negative
            (100.0, 200.0, -300.0, 400.0, 45.0),  # z is negative
            (100.0, 200.0, 300.0, -400.0, 45.0),  # f_ywd is negative
            (100.0, 200.0, 300.0, 400.0, -45.0),  # theta is negative
            (100.0, 0.0, 300.0, 400.0, 45.0),  # s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_sw: float, s: float, z: float, f_ywd: float, theta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot8ShearResistance(a_sw=a_sw, s=s, z=z, f_ywd=f_ywd, theta=theta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{Rd,s} = \frac{A_{sw}}{s} \cdot z \cdot f_{ywd} \cdot \cot(\theta) = "
                r"\frac{100.000}{200.000} \cdot 300.000 \cdot 400.000 \cdot \cot(45.000) = 60000.000 \ N",
            ),
            ("short", r"V_{Rd,s} = 60000.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sw = 100.0
        s = 200.0
        z = 300.0
        f_ywd = 400.0
        theta = 45.0

        # Object to test
        latex = Form6Dot8ShearResistance(a_sw=a_sw, s=s, z=z, f_ywd=f_ywd, theta=theta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
