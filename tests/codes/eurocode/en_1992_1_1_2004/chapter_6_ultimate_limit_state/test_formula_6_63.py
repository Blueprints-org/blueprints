"""Testing formula 6.63 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_63 import Form6Dot63ConcentratedResistanceForce
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot63ConcentratedResistanceForce:
    """Validation for formula 6.63 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_c0 = 300.0
        a_c1 = 400.0
        f_cd = 30.0

        # Object to test
        formula = Form6Dot63ConcentratedResistanceForce(a_c0=a_c0, a_c1=a_c1, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 10392.304845413264  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_c0", "a_c1", "f_cd"),
        [
            (-300.0, 400.0, 30.0),  # a_c0 is negative
            (300.0, -400.0, 30.0),  # a_c1 is negative
            (300.0, 400.0, -30.0),  # f_cd is negative
            (0.0, 400.0, 30.0),  # a_c0 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_c0: float, a_c1: float, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot63ConcentratedResistanceForce(a_c0=a_c0, a_c1=a_c1, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{Rdu} = \min \left( A_{c0} \cdot f_{cd} \cdot \sqrt{\frac{A_{c1}}{A_{c0}}}, 3 \cdot f_{cd} \cdot A_{c0} \right) = "
                r"\min \left( 300.000 \cdot 30.000 \cdot \sqrt{\frac{400.000}{300.000}}, 3 \cdot 30.000 \cdot 300.000 \right) = 10392.305 \ N",
            ),
            ("short", r"F_{Rdu} = 10392.305 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_c0 = 300.0
        a_c1 = 400.0
        f_cd = 30.0

        # Object to test
        latex = Form6Dot63ConcentratedResistanceForce(a_c0=a_c0, a_c1=a_c1, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
