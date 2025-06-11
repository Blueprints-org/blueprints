"""Testing formula A.1 from EN 1993-1-9:2005: Annex A - Determination of fatigue load parameters and verification formats."""

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2005.annex_a_determination_of_fatigue_load_parameters_and_verification_formats.formula_a_2 import (
    FormADot2CriteriaBasedOnDamageAccumulation,
)
from blueprints.validations import NegativeValueError


class TestFormADot2CriteriaBasedOnDamageAccumulation:
    """Validation for formula A.2 from EN 1993-1-9:2005."""

    @pytest.mark.parametrize(
        ("d_d", "result_manual"),
        [
            (0.8, True),
            (1.1, False),
        ],
    )
    def test_evaluation(self, d_d: float, result_manual: bool) -> None:
        """Test the evaluation of the result."""
        assert FormADot2CriteriaBasedOnDamageAccumulation(d_d=d_d) == result_manual

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
                r"CHECK \rightarrow D_d \leq 1.0 \rightarrow 0.800 \leq 1.0 \rightarrow OK",
            ),
            ("short", r"CHECK \rightarrow OK"),
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
