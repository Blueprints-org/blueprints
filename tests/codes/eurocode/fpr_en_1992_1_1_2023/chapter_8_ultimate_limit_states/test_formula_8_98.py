"""Testing formula 8.98 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_98 import (
    Form8Dot98DistanceToPointOfContraflexure,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot98DistanceToPointOfContraflexure:
    """Validation for formula 8.98 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result when the expression governs."""
        # Example values
        a_p_x = 1200.0
        a_p_y = 800.0
        d_v = 200.0

        # Object to test
        formula = Form8Dot98DistanceToPointOfContraflexure(a_p_x=a_p_x, a_p_y=a_p_y, d_v=d_v)

        # Expected result, manually calculated
        manually_calculated_result = 979.795897  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_lower_bound_governs(self) -> None:
        """Tests the evaluation of the result when the lower bound of d_v governs."""
        # Example values, with a_p_x and a_p_y small enough for the expression to fall below d_v
        formula = Form8Dot98DistanceToPointOfContraflexure(a_p_x=50.0, a_p_y=80.0, d_v=200.0)

        # Expected result, manually calculated: the expression yields 63.245553, so the lower bound d_v governs
        manually_calculated_result = 200.0  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_p_x", "a_p_y", "d_v"),
        [
            (-1200.0, 800.0, 200.0),  # a_p_x is negative
            (1200.0, -800.0, 200.0),  # a_p_y is negative
            (1200.0, 800.0, -200.0),  # d_v is negative
            (1200.0, 800.0, 0.0),  # d_v is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_p_x: float, a_p_y: float, d_v: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot98DistanceToPointOfContraflexure(a_p_x=a_p_x, a_p_y=a_p_y, d_v=d_v)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a_p = \max\left(\sqrt{a_{p,x} \cdot a_{p,y}}, d_v\right) = \max\left(\sqrt{1200.000 \cdot 800.000}, 200.000\right) = 979.796 \ mm",
            ),
            (
                "complete_with_units",
                (
                    r"a_p = \max\left(\sqrt{a_{p,x} \cdot a_{p,y}}, d_v\right) = "
                    r"\max\left(\sqrt{1200.000 \ mm \cdot 800.000 \ mm}, 200.000 \ mm\right) = 979.796 \ mm"
                ),
            ),
            ("short", r"a_p = 979.796 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_p_x = 1200.0
        a_p_y = 800.0
        d_v = 200.0

        # Object to test
        latex = Form8Dot98DistanceToPointOfContraflexure(a_p_x=a_p_x, a_p_y=a_p_y, d_v=d_v).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
