"""Testing formula NB.NB.8 of NEN-EN 1993-1-1:2006."""

import pytest

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006.chapter_NB_NB_critical_buckling_moment.formula_nb_nb_8 import (
    FormNBDotNB8ReductionFactorKred,
)
from blueprints.validations import NegativeValueError


class TestFormNBDotNB8ReductionFactorKred:
    """Validation for formula NB.NB.8 from NEN-EN 1993-1-1:2006."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        alpha = 1000.0

        # Object to test
        formula = FormNBDotNB8ReductionFactorKred(alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 0.976

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_result_one(self) -> None:
        """Tests the evaluation of the result if it is limited to 1."""
        # Example values
        alpha = 0.0

        # Object to test
        formula = FormNBDotNB8ReductionFactorKred(alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 1.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "alpha",
        [
            -1000.0,  # alpha is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, alpha: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            FormNBDotNB8ReductionFactorKred(alpha=alpha)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_{red} = \min\left(\left(\left(-5.4 \cdot 10^{-5} \cdot \alpha\right) + 1.03\right), 1\right) = "
                r"\min\left(\left(\left(-5.4 \cdot 10^{-5} \cdot 1000.000\right) + 1.03\right), 1\right) = 0.976 \ -",
            ),
            (
                "complete_with_units",
                r"k_{red} = \min\left(\left(\left(-5.4 \cdot 10^{-5} \cdot \alpha\right) + 1.03\right), 1\right) = "
                r"\min\left(\left(\left(-5.4 \cdot 10^{-5} \cdot 1000.000\right) + 1.03\right), 1\right) = 0.976 \ -",
            ),
            ("short", r"k_{red} = 0.976 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        alpha = 1000.0

        # Object to test
        latex = FormNBDotNB8ReductionFactorKred(alpha=alpha).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
