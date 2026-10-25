"""Testing formula NB.NB.7 of NEN-EN 1993-1-1:2006."""

import pytest

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006.chapter_NB_NB_critical_buckling_moment.formula_nb_nb_7 import (
    FormNBDotNB7ReductionFactorKred,
)


class TestFormNBDotNB7ReductionFactorKred:
    """Validation for formula NB.NB.7 from NEN-EN 1993-1-1:2006."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Object to test
        formula = FormNBDotNB7ReductionFactorKred()

        # Expected result, manually calculated
        manually_calculated_result = 1.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_{red} = 1 = 1 = 1.000 \ -",
            ),
            (
                "complete_with_units",
                r"k_{red} = 1 = 1 = 1.000 \ -",
            ),
            ("short", r"k_{red} = 1.000 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = FormNBDotNB7ReductionFactorKred().latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
