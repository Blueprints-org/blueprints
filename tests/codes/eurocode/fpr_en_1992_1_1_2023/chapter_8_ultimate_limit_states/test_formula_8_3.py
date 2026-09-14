"""Testing formula 8.3 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_3 import (
    Form8Dot3AxialResistanceWithoutMoment,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot3AxialResistanceWithoutMoment:
    """Validation for formula 8.3 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_c = 200000.0
        f_cd = 20.0
        a_s = 5000.0
        f_yd = 435.0

        # Object to test
        formula = Form8Dot3AxialResistanceWithoutMoment(a_c=a_c, f_cd=f_cd, a_s=a_s, f_yd=f_yd)

        # Expected result, manually calculated: 200000 * 20 + 5000 * 435
        manually_calculated_result = 6175000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_c", "f_cd", "a_s", "f_yd"),
        [
            (-200000.0, 20.0, 5000.0, 435.0),  # a_c is negative
            (200000.0, -20.0, 5000.0, 435.0),  # f_cd is negative
            (200000.0, 20.0, -5000.0, 435.0),  # a_s is negative
            (200000.0, 20.0, 5000.0, -435.0),  # f_yd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_c: float, f_cd: float, a_s: float, f_yd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot3AxialResistanceWithoutMoment(a_c=a_c, f_cd=f_cd, a_s=a_s, f_yd=f_yd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"N_{Rd,0} = A_c \cdot f_{cd} + A_s \cdot f_{yd} = 200000.000 \cdot 20.000 + 5000.000 \cdot 435.000 = 6175000.000 \ N",
            ),
            (
                "complete_with_units",
                (
                    r"N_{Rd,0} = A_c \cdot f_{cd} + A_s \cdot f_{yd} = "
                    r"200000.000 \ mm^2 \cdot 20.000 \ MPa + 5000.000 \ mm^2 \cdot 435.000 \ MPa = 6175000.000 \ N"
                ),
            ),
            ("short", r"N_{Rd,0} = 6175000.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_c = 200000.0
        f_cd = 20.0
        a_s = 5000.0
        f_yd = 435.0

        # Object to test
        latex = Form8Dot3AxialResistanceWithoutMoment(a_c=a_c, f_cd=f_cd, a_s=a_s, f_yd=f_yd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
