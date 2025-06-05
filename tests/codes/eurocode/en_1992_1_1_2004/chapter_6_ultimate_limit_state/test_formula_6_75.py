"""Testing formula 6.75 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_75 import Form6Dot75MaximumCompressiveStressLevel
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot75MaximumCompressiveStressLevel:
    """Validation for formula 6.75 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sigma_cd_max_equ = 10.0  # MPa
        f_cd_fat = 20.0  # MPa

        # Object to test
        formula = Form6Dot75MaximumCompressiveStressLevel(sigma_cd_max_equ=sigma_cd_max_equ, f_cd_fat=f_cd_fat)

        # Expected result, manually calculated
        manually_calculated_result = 0.5

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("sigma_cd_max_equ", "f_cd_fat"),
        [
            (-10.0, 20.0),  # sigma_cd_max_equ is negative
            (10.0, -20.0),  # f_cd_fat is negative
            (10.0, 0.0),  # f_cd_fat is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, sigma_cd_max_equ: float, f_cd_fat: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot75MaximumCompressiveStressLevel(sigma_cd_max_equ=sigma_cd_max_equ, f_cd_fat=f_cd_fat)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"E_{cd,max,equ} = \frac{\sigma_{cd,max,equ}}{f_{cd,fat}} = \frac{10.000}{20.000} = 0.500 \ -",
            ),
            ("short", r"E_{cd,max,equ} = 0.500 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_cd_max_equ = 10.0  # MPa
        f_cd_fat = 20.0  # MPa

        # Object to test
        latex = Form6Dot75MaximumCompressiveStressLevel(sigma_cd_max_equ=sigma_cd_max_equ, f_cd_fat=f_cd_fat).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
