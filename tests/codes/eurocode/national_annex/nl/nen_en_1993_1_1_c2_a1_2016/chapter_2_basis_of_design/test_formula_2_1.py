"""Testing formula 2.1 of NEN-EN 1993-1-1+C2+A1:2016."""

import pytest

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_c2_a1_2016.chapter_2_basis_of_design.formula_2_1 import (
    Form2Dot1DesignResistance,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm2Dot1DesignResistance:
    """Validation for formula 2.1 from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        r_k = 355.0
        gamma_m = 1.1

        # Object to test
        formula = Form2Dot1DesignResistance(r_k=r_k, gamma_m=gamma_m)

        # Expected result, manually calculated
        manually_calculated_result = 322.727272727  # R_k / gamma_M = 355.0 / 1.1

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("r_k", "gamma_m"),
        [
            (355.0, 0.0),  # gamma_m is zero
            (355.0, -1.1),  # gamma_m is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, r_k: float, gamma_m: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form2Dot1DesignResistance(r_k=r_k, gamma_m=gamma_m)

    def test_evaluation_negative_r_k(self) -> None:
        """Tests that a negative r_k evaluates correctly without raising an error."""
        formula = Form2Dot1DesignResistance(r_k=-355.0, gamma_m=1.1)
        assert formula == pytest.approx(expected=-322.727272727, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"R_d = \frac{R_k}{\gamma_M} = \frac{355.000}{1.100} = 322.727",
            ),
            (
                "complete_with_units",
                r"R_d = \frac{R_k}{\gamma_M} = \frac{355.000}{1.100} = 322.727",
            ),
            ("short", r"R_d = 322.727"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        r_k = 355.0
        gamma_m = 1.1

        # Object to test
        latex = Form2Dot1DesignResistance(r_k=r_k, gamma_m=gamma_m).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
