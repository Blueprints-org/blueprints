"""Testing formula 8.1 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_1 import (
    Form8Dot1MinimumDesignMoment,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot1MinimumDesignMoment:
    """Validation for formula 8.1 from FprEN 1992-1-1:2023."""

    def test_evaluation_expression_governs(self) -> None:
        """Tests the evaluation of the result where h / 30 governs."""
        # Example values
        n_ed = 500000.0
        h = 900.0

        # Object to test
        formula = Form8Dot1MinimumDesignMoment(n_ed=n_ed, h=h)

        # Expected result, manually calculated: 500000 * max(900 / 30, 20) = 500000 * 30
        manually_calculated_result = 15000000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_bound_governs(self) -> None:
        """Tests the evaluation of the result where the bound of 20 mm governs."""
        # Example values
        n_ed = 500000.0
        h = 300.0

        # Object to test
        formula = Form8Dot1MinimumDesignMoment(n_ed=n_ed, h=h)

        # Expected result, manually calculated: 500000 * max(300 / 30, 20) = 500000 * 20
        manually_calculated_result = 10000000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_negative_axial_force(self) -> None:
        """Tests the evaluation of the result when the axial force is given as a negative value."""
        # Example values
        n_ed = -500000.0
        h = 900.0

        # Object to test
        formula = Form8Dot1MinimumDesignMoment(n_ed=n_ed, h=h)

        # Expected result, manually calculated: |-500000| * max(900 / 30, 20) = 500000 * 30
        manually_calculated_result = 15000000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "h",
        [
            -900.0,  # h is negative
            0.0,  # h is zero
        ],
    )
    def test_raise_error_when_h_is_less_or_equal_to_zero(self, h: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot1MinimumDesignMoment(n_ed=500000.0, h=h)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"M_{Ed,min} = \left|N_{Ed}\right| \cdot \max\left(\frac{h}{30}, 20\right) = "
                    r"\left|500000.000\right| \cdot \max\left(\frac{900.000}{30}, 20\right) = 15000000.000 \ Nmm"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"M_{Ed,min} = \left|N_{Ed}\right| \cdot \max\left(\frac{h}{30}, 20\right) = "
                    r"\left|500000.000 \ N\right| \cdot \max\left(\frac{900.000 \ mm}{30}, 20\right) = 15000000.000 \ Nmm"
                ),
            ),
            ("short", r"M_{Ed,min} = 15000000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 500000.0
        h = 900.0

        # Object to test
        latex = Form8Dot1MinimumDesignMoment(n_ed=n_ed, h=h).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
