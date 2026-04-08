"""Testing formula 8.47 of prEN-1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_47 import Form8Dot47StrainTensionChord
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot47StrainTensionChord:
    """Validation for formula 8.47 from prEN-1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_td = 800e3  # N
        a_st = 1257  # mm^2
        e_s = 200000.0  # MPa

        # Object to test
        formula = Form8Dot47StrainTensionChord(f_td=f_td, a_st=a_st, e_s=e_s)

        # Expected result, manually calculated
        manually_calculated_result = 0.003182  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_f_rd_is_negative(self) -> None:
        """Test negative f_rd value."""
        with pytest.raises(NegativeValueError):
            Form8Dot47StrainTensionChord(f_td=-800.0e3, a_st=1257.0, e_s=200000.0)

    @pytest.mark.parametrize(
        ("f_td", "a_st", "e_s"),
        [
            (800e3, 0.0, 200000.0),  # a_st is zero
            (800e3, -1257.0, 200000.0),  # a_st is negative
            (800e3, 1257.0, 0.0),  # e_s is zero
            (800e3, 1257.0, -200000.0),  # e_s is negative
        ],
    )
    def test_raise_error_when_a_st_or_e_s_invalid(self, f_td: float, a_st: float, e_s: float) -> None:
        """Test invalid values for a_st or e_s."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot47StrainTensionChord(f_td=f_td, a_st=a_st, e_s=e_s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\varepsilon_{xt} = \frac{F_{td}}{A_{st} \cdot E_s} = "
                r"\frac{800000.0000}{1257.0000 \cdot 200000.0000} = 0.0032",
            ),
            (
                "complete_with_units",
                r"\varepsilon_{xt} = \frac{F_{td}}{A_{st} \cdot E_s} = "
                r"\frac{800000.0000 \ N}{1257.0000 \ mm^2 \cdot 200000.0000 \ MPa} = 0.0032",
            ),
            ("short", r"\varepsilon_{xt} = 0.0032"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_td = 800e3  # N
        a_st = 1257.0  # mm^2
        e_s = 200000.0  # MPa

        # Object to test
        latex = Form8Dot47StrainTensionChord(f_td=f_td, a_st=a_st, e_s=e_s).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
