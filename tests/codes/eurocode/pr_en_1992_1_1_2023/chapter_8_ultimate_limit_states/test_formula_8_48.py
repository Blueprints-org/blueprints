"""Testing formula 8.48 of prEN 1992-1-2:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_48 import (
    Form8Dot48StrainCompressionChordInCompression,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot48StrainCompressionChordInCompression:
    """Validation for formula 8.48 from prEN 1992-1-2:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_cd = 800e3  # N
        a_cc = 200000  # mm^2
        e_c = 10000.0  # MPa

        # Object to test
        formula = Form8Dot48StrainCompressionChordInCompression(f_cd=f_cd, a_cc=a_cc, e_c=e_c)

        # Expected result, manually calculated
        manually_calculated_result = -0.0004  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_cd", "a_cc", "e_c"),
        [
            (-800e3, 200000.0, 10000.0),  # f_cd is negative
            (800e3, 0.0, 10000.0),  # a_cc is zero
            (800e3, -200000.0, 10000.0),  # a_cc is negative
            (800e3, 200000.0, 0.0),  # e_c is zero
            (800e3, 200000.0, -10000.0),  # e_c is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_cd: float, a_cc: float, e_c: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot48StrainCompressionChordInCompression(f_cd=f_cd, a_cc=a_cc, e_c=e_c)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\varepsilon_{xc} = \frac{-F_{cd}}{A_{cc} \cdot E_c} = "
                r"\frac{-800000.0000}{200000.0000 \cdot 10000.0000} = -0.0004 \ -",
            ),
            (
                "complete_with_units",
                r"\varepsilon_{xc} = \frac{-F_{cd}}{A_{cc} \cdot E_c} = "
                r"\frac{-800000.0000 \ N}{200000.0000 \ mm^2 \cdot 10000.0000 \ MPa} = -0.0004 \ -",
            ),
            ("short", r"\varepsilon_{xc} = -0.0004 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cd = 800e3  # N
        a_cc = 200000.0  # mm^2
        e_c = 10000.0  # MPa

        # Object to test
        latex = Form8Dot48StrainCompressionChordInCompression(f_cd=f_cd, a_cc=a_cc, e_c=e_c).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
