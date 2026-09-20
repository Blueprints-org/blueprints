"""Testing formula 8.102 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_102 import (
    Form8Dot102CoefficientAccountingForAxialForcesTwoDirections,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot102CoefficientAccountingForAxialForcesTwoDirections:
    """Validation for formula 8.102 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        k_pp_x = 1.2
        k_pp_y = 0.9

        # Object to test
        formula = Form8Dot102CoefficientAccountingForAxialForcesTwoDirections(k_pp_x=k_pp_x, k_pp_y=k_pp_y)

        # Expected result, manually calculated
        manually_calculated_result = 1.039230  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k_pp_x", "k_pp_y"),
        [
            (-1.2, 0.9),  # k_pp_x is negative
            (1.2, -0.9),  # k_pp_y is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, k_pp_x: float, k_pp_y: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot102CoefficientAccountingForAxialForcesTwoDirections(k_pp_x=k_pp_x, k_pp_y=k_pp_y)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_{pp} = \sqrt{k_{pp,x} \cdot k_{pp,y}} = \sqrt{1.200 \cdot 0.900} = 1.039 \ -",
            ),
            (
                "complete_with_units",
                r"k_{pp} = \sqrt{k_{pp,x} \cdot k_{pp,y}} = \sqrt{1.200 \cdot 0.900} = 1.039 \ -",
            ),
            ("short", r"k_{pp} = 1.039 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_pp_x = 1.2
        k_pp_y = 0.9

        # Object to test
        latex = Form8Dot102CoefficientAccountingForAxialForcesTwoDirections(k_pp_x=k_pp_x, k_pp_y=k_pp_y).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
