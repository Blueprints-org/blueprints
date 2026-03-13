"""Testing formula 6.73 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_73 import Form6Dot73StressRatio
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot73StressRatio:
    """Validation for formula 6.73 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        e_cd_min_equ = 10.0
        e_cd_max_equ = 20.0

        # Object to test
        formula = Form6Dot73StressRatio(e_cd_min_equ=e_cd_min_equ, e_cd_max_equ=e_cd_max_equ)

        # Expected result, manually calculated
        manually_calculated_result = 0.5

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("e_cd_min_equ", "e_cd_max_equ"),
        [
            (-10.0, 20.0),  # e_cd_min_equ is negative
            (10.0, -20.0),  # e_cd_max_equ is negative
            (10.0, 0.0),  # e_cd_max_equ is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, e_cd_min_equ: float, e_cd_max_equ: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot73StressRatio(e_cd_min_equ=e_cd_min_equ, e_cd_max_equ=e_cd_max_equ)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"R_{equ} = \frac{E_{cd,min,equ}}{E_{cd,max,equ}} = \frac{10.000}{20.000} = 0.500",
            ),
            ("short", r"R_{equ} = 0.500"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        e_cd_min_equ = 10.0
        e_cd_max_equ = 20.0

        # Object to test
        latex = Form6Dot73StressRatio(e_cd_min_equ=e_cd_min_equ, e_cd_max_equ=e_cd_max_equ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
