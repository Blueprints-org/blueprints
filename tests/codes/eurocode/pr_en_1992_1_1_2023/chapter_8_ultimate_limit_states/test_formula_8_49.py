"""Testing formula 8.49 of prEN 1992-1-2:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_49 import Form8Dot49StrainCompressionChordInTension
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot49StrainCompressionChordInTension:
    """Validation for formula 8.49 from prEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_cd = 800e3  # N
        a_sc = 1257.0  # mm^2
        e_s = 200000.0  # MPa

        # Object to test
        formula = Form8Dot49StrainCompressionChordInTension(f_cd=f_cd, a_sc=a_sc, e_s=e_s)

        # Expected result, manually calculated
        manually_calculated_result = 0.003182  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_sc", "e_s"),
        [
            (0.0, 200000.0),  # a_sc is zero
            (-1257.0, 200000.0),  # a_sc is negative
            (1257.0, 0.0),  # e_s is zero
            (1257.0, -200000.0),  # e_s is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_sc: float, e_s: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot49StrainCompressionChordInTension(f_cd=800e3, a_sc=a_sc, e_s=e_s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\varepsilon_{xc} = \frac{|F_{cd}|}{A_{sc} \cdot E_s} = "
                r"\frac{800000.0000}{1257.0000 \cdot 200000.0000} = 0.0032 \ -",
            ),
            (
                "complete_with_units",
                r"\varepsilon_{xc} = \frac{|F_{cd}|}{A_{sc} \cdot E_s} = "
                r"\frac{800000.0000 \ N}{1257.0000 \ mm^2 \cdot 200000.0000 \ MPa} = 0.0032 \ -",
            ),
            ("short", r"\varepsilon_{xc} = 0.0032 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cd = 800e3  # N
        a_sc = 1257.0  # mm^2
        e_s = 200000.0  # MPa

        # Object to test
        latex = Form8Dot49StrainCompressionChordInTension(f_cd=f_cd, a_sc=a_sc, e_s=e_s).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
