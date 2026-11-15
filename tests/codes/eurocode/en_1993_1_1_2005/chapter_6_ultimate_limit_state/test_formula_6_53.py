"""Testing formula 6.53 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_53 import (
    Form6Dot53NonDimensionalSlendernessTorsionalBucklingClass4,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot53NonDimensionalSlendernessTorsionalBucklingClass4:
    """Validation for formula 6.53 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_eff = 4200.0
        f_y = 355.0
        n_cr = 2000000.0

        # Object to test
        formula = Form6Dot53NonDimensionalSlendernessTorsionalBucklingClass4(a_eff=a_eff, f_y=f_y, n_cr=n_cr)

        # Expected result, manually calculated
        # sqrt(4200 * 355 / 2000000) = sqrt(0.7455) = 0.863423
        manually_calculated_result = 0.863423  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_eff", "f_y", "n_cr"),
        [
            (-4200.0, 355.0, 2000000.0),  # a_eff is negative
            (4200.0, -355.0, 2000000.0),  # f_y is negative
            (4200.0, 355.0, 0.0),  # n_cr is zero
            (4200.0, 355.0, -2000000.0),  # n_cr is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_eff: float, f_y: float, n_cr: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot53NonDimensionalSlendernessTorsionalBucklingClass4(a_eff=a_eff, f_y=f_y, n_cr=n_cr)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\overline{\lambda}_T = \sqrt{\frac{A_{eff} \cdot f_y}{N_{cr}}} = "
                    r"\sqrt{\frac{4200.000 \cdot 355.000}{2000000.000}} = 0.863 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\overline{\lambda}_T = \sqrt{\frac{A_{eff} \cdot f_y}{N_{cr}}} = "
                    r"\sqrt{\frac{4200.000 \ mm^2 \cdot 355.000 \ MPa}{2000000.000 \ N}} = 0.863 \ -"
                ),
            ),
            ("short", r"\overline{\lambda}_T = 0.863 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_eff = 4200.0
        f_y = 355.0
        n_cr = 2000000.0

        # Object to test
        latex = Form6Dot53NonDimensionalSlendernessTorsionalBucklingClass4(a_eff=a_eff, f_y=f_y, n_cr=n_cr).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
