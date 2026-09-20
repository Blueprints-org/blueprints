"""Testing formula 8.12 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_12 import (
    Form8Dot12ConfinementStressRectangularSingleConfinement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot12ConfinementStressRectangularSingleConfinement:
    """Validation for formula 8.12 from FprEN 1992-1-1:2023."""

    def test_evaluation_bcsy_governs(self) -> None:
        """Tests the evaluation of the result where b_csy governs the max."""
        # Example values
        a_s_conf = 100.0
        f_yd = 500.0
        b_csx = 300.0
        b_csy = 400.0
        s = 150.0

        # Object to test
        formula = Form8Dot12ConfinementStressRectangularSingleConfinement(a_s_conf=a_s_conf, f_yd=f_yd, b_csx=b_csx, b_csy=b_csy, s=s)

        # Expected result, manually calculated: 2 * 100 * 500 / (max(300, 400) * 150)
        manually_calculated_result = 1.6666666666666667

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_bcsx_governs(self) -> None:
        """Tests the evaluation of the result where b_csx governs the max."""
        # Example values
        a_s_conf = 100.0
        f_yd = 500.0
        b_csx = 400.0
        b_csy = 300.0
        s = 150.0

        # Object to test
        formula = Form8Dot12ConfinementStressRectangularSingleConfinement(a_s_conf=a_s_conf, f_yd=f_yd, b_csx=b_csx, b_csy=b_csy, s=s)

        # Expected result, manually calculated: 2 * 100 * 500 / (max(400, 300) * 150)
        manually_calculated_result = 1.6666666666666667

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_s_conf", "f_yd"),
        [
            (-100.0, 500.0),  # a_s_conf is negative
            (100.0, -500.0),  # f_yd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, a_s_conf: float, f_yd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot12ConfinementStressRectangularSingleConfinement(a_s_conf=a_s_conf, f_yd=f_yd, b_csx=300.0, b_csy=400.0, s=150.0)

    @pytest.mark.parametrize(
        ("b_csx", "b_csy", "s"),
        [
            (-300.0, 400.0, 150.0),  # b_csx is negative
            (300.0, -400.0, 150.0),  # b_csy is negative
            (300.0, 400.0, -150.0),  # s is negative
            (300.0, 400.0, 0.0),  # s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, b_csx: float, b_csy: float, s: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot12ConfinementStressRectangularSingleConfinement(a_s_conf=100.0, f_yd=500.0, b_csx=b_csx, b_csy=b_csy, s=s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\sigma_{c2d} = \frac{2 \cdot A_{s,conf} \cdot f_{yd}}{\max\left(b_{csx}, b_{csy}\right) \cdot s} = "
                    r"\frac{2 \cdot 100.000 \cdot 500.000}{\max\left(300.000, 400.000\right) \cdot 150.000} = 1.667 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\sigma_{c2d} = \frac{2 \cdot A_{s,conf} \cdot f_{yd}}{\max\left(b_{csx}, b_{csy}\right) \cdot s} = "
                    r"\frac{2 \cdot 100.000 \ mm^2 \cdot 500.000 \ MPa}"
                    r"{\max\left(300.000 \ mm, 400.000 \ mm\right) \cdot 150.000 \ mm} = 1.667 \ MPa"
                ),
            ),
            ("short", r"\sigma_{c2d} = 1.667 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_s_conf = 100.0
        f_yd = 500.0
        b_csx = 300.0
        b_csy = 400.0
        s = 150.0

        # Object to test
        latex = Form8Dot12ConfinementStressRectangularSingleConfinement(a_s_conf=a_s_conf, f_yd=f_yd, b_csx=b_csx, b_csy=b_csy, s=s).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
