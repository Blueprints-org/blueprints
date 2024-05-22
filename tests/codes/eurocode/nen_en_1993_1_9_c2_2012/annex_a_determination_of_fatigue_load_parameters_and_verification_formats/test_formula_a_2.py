"""Testing formula A.1 from NEN-EN 1993-1-9+C2:2012: Annex A - Determination of fatigue load parameters and verification formats."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_1_9_c2_2012.annex_a_determination_of_fatigue_load_parameters_and_verification_formats.formula_a_2 import (
    FormADot2CriteriaBasedOnDamageAccumulation,
)
from blueprints.validations import NegativeValueError


class TestFormADot2CriteriaBasedOnDamageAccumulation:
    """Validation for formula A.2 from NEN-EN 1993-1-9+C2:2012."""

    def test_evaluation_if_ok(self) -> None:
        """Test the evaluation of the result."""
        # example values
        d_d = 0.8  # -

        form_a_1 = FormADot2CriteriaBasedOnDamageAccumulation(d_d=d_d)
        # manually calculated result
        manually_calculated_result = True

        assert form_a_1 == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    def test_evaluation_if_not_ok(self) -> None:
        """Test the evaluation of the result."""
        # example values
        d_d = 1.1  # -

        form_a_1 = FormADot2CriteriaBasedOnDamageAccumulation(d_d=d_d)
        # manually calculated result
        manually_calculated_result = False

        assert form_a_1 == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    def test_raise_error_if_negative_n_e(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for n_E."""
        d_d = -0.1  # -
        with pytest.raises(NegativeValueError):
            FormADot2CriteriaBasedOnDamageAccumulation(d_d=d_d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"OK? \rightarrow D_d \leq 1.0 \rightarrow 0.800 \leq 1.0 \rightarrow True",
            ),
            ("short", r"OK? \rightarrow True"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d_d = 0.8  # -

        # Object to test
        form_a_2_latex = FormADot2CriteriaBasedOnDamageAccumulation(d_d=d_d).latex()

        actual = {
            "complete": form_a_2_latex.complete,
            "short": form_a_2_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
