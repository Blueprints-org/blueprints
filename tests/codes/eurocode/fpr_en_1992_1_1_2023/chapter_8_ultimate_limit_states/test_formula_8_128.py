"""Testing formula 8.128 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_128 import (
    Form8Dot128EccentricallyLoadedArea,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot128EccentricallyLoadedArea:
    """Validation for formula 8.128 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_0 = 300.0
        e_a = 20.0
        b_0 = 400.0
        e_b = 25.0

        # Object to test
        formula = Form8Dot128EccentricallyLoadedArea(a_0=a_0, e_a=e_a, b_0=b_0, e_b=e_b)

        # Expected result, manually calculated: (300 - 2 * 20) * (400 - 2 * 25) = 260 * 350
        manually_calculated_result = 91000.0

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
            Form8Dot128EccentricallyLoadedArea(a_0=a_0, e_a=20.0, b_0=b_0, e_b=25.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"A_{c0,red} = \left(a_0 - 2 \cdot e_a\right) \cdot \left(b_0 - 2 \cdot e_b\right) = "
                    r"\left(300.000 - 2 \cdot 20.000\right) \cdot \left(400.000 - 2 \cdot 25.000\right) = 91000.000 \ mm^2"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"A_{c0,red} = \left(a_0 - 2 \cdot e_a\right) \cdot \left(b_0 - 2 \cdot e_b\right) = "
                    r"\left(300.000 \ mm - 2 \cdot 20.000 \ mm\right) \cdot \left(400.000 \ mm - 2 \cdot 25.000 \ mm\right) = "
                    r"91000.000 \ mm^2"
                ),
            ),
            ("short", r"A_{c0,red} = 91000.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_0 = 300.0
        e_a = 20.0
        b_0 = 400.0
        e_b = 25.0

        # Object to test
        latex = Form8Dot128EccentricallyLoadedArea(a_0=a_0, e_a=e_a, b_0=b_0, e_b=e_b).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
