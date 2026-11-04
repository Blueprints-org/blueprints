"""Testing formula 8.127 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_127 import (
    Form8Dot127ConcentricallyLoadedArea,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot127ConcentricallyLoadedArea:
    """Validation for formula 8.127 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_0 = 300.0
        b_0 = 400.0

        # Object to test
        formula = Form8Dot127ConcentricallyLoadedArea(a_0=a_0, b_0=b_0)

        # Expected result, manually calculated: 300 * 400
        manually_calculated_result = 120000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_0", "b_0"),
        [
            (-300.0, 400.0),  # a_0 is negative
            (300.0, -400.0),  # b_0 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_0: float, b_0: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot127ConcentricallyLoadedArea(a_0=a_0, b_0=b_0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"A_{c0} = a_0 \cdot b_0 = 300.000 \cdot 400.000 = 120000.000 \ mm^2"),
            (
                "complete_with_units",
                r"A_{c0} = a_0 \cdot b_0 = 300.000 \ mm \cdot 400.000 \ mm = 120000.000 \ mm^2",
            ),
            ("short", r"A_{c0} = 120000.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_0 = 300.0
        b_0 = 400.0

        # Object to test
        latex = Form8Dot127ConcentricallyLoadedArea(a_0=a_0, b_0=b_0).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
