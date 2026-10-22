"""Testing formula 8.78 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_78 import (
    Form8Dot78MinimumInterfaceReinforcementAlongEdge,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot78MinimumInterfaceReinforcementAlongEdge:
    """Validation for formula 8.78 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        t_min = 60.0
        f_ctm = 2.9
        f_yk = 500.0

        # Object to test
        formula = Form8Dot78MinimumInterfaceReinforcementAlongEdge(t_min=t_min, f_ctm=f_ctm, f_yk=f_yk)

        # Expected result, manually calculated: 60 * 2.9 / 500
        manually_calculated_result = 0.348  # mm^2/mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("t_min", "f_ctm", "f_yk"),
        [
            (-60.0, 2.9, 500.0),  # t_min is negative
            (60.0, -2.9, 500.0),  # f_ctm is negative
            (60.0, 2.9, -500.0),  # f_yk is negative
            (60.0, 2.9, 0.0),  # f_yk is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, t_min: float, f_ctm: float, f_yk: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot78MinimumInterfaceReinforcementAlongEdge(t_min=t_min, f_ctm=f_ctm, f_yk=f_yk)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a_{s,min} = \frac{t_{min} \cdot f_{ctm}}{f_{yk}} = \frac{60.000 \cdot 2.900}{500.000} = 0.348 \ mm^2/mm",
            ),
            (
                "complete_with_units",
                (
                    r"a_{s,min} = \frac{t_{min} \cdot f_{ctm}}{f_{yk}} = "
                    r"\frac{60.000 \ mm \cdot 2.900 \ MPa}{500.000 \ MPa} = 0.348 \ mm^2/mm"
                ),
            ),
            ("short", r"a_{s,min} = 0.348 \ mm^2/mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t_min = 60.0
        f_ctm = 2.9
        f_yk = 500.0

        # Object to test
        latex = Form8Dot78MinimumInterfaceReinforcementAlongEdge(t_min=t_min, f_ctm=f_ctm, f_yk=f_yk).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
