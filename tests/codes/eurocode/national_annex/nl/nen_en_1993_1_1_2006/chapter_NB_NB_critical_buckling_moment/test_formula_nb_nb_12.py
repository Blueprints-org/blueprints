"""Testing formula NB.NB.12 of NEN-EN 1993-1-1:2006."""

import pytest

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006.chapter_NB_NB_critical_buckling_moment.formula_nb_nb_12 import (
    FormNBDotNB12ParameterS,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestFormNBDotNB12ParameterS:
    """Validation for formula NB.NB.12 from NEN-EN 1993-1-1:2006."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        e = 210000.0
        i_w = 8000000000.0
        g = 81000.0
        i_t = 200000.0

        # Object to test
        formula = FormNBDotNB12ParameterS(e=e, i_w=i_w, g=g, i_t=i_t)

        # Expected result, manually calculated
        manually_calculated_result = 322.030594

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("e", "i_w", "g", "i_t"),
        [
            (-210000.0, 8000000000.0, 81000.0, 200000.0),  # e is negative
            (210000.0, -8000000000.0, 81000.0, 200000.0),  # i_w is negative
            (210000.0, 8000000000.0, 0.0, 200000.0),  # g is zero
            (210000.0, 8000000000.0, -81000.0, 200000.0),  # g is negative
            (210000.0, 8000000000.0, 81000.0, 0.0),  # i_t is zero
            (210000.0, 8000000000.0, 81000.0, -200000.0),  # i_t is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, e: float, i_w: float, g: float, i_t: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            FormNBDotNB12ParameterS(e=e, i_w=i_w, g=g, i_t=i_t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"S = \sqrt{\frac{E \cdot I_w}{G \cdot I_t}} = "
                r"\sqrt{\frac{210000.000 \cdot 8000000000.000}{81000.000 \cdot 200000.000}} = 322.031 \ mm",
            ),
            (
                "complete_with_units",
                r"S = \sqrt{\frac{E \cdot I_w}{G \cdot I_t}} = "
                r"\sqrt{\frac{210000.000 \ MPa \cdot 8000000000.000 \ mm^6}{81000.000 \ MPa \cdot 200000.000 \ mm^4}} = 322.031 \ mm",
            ),
            ("short", r"S = 322.031 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        e = 210000.0
        i_w = 8000000000.0
        g = 81000.0
        i_t = 200000.0

        # Object to test
        latex = FormNBDotNB12ParameterS(e=e, i_w=i_w, g=g, i_t=i_t).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
