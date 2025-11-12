"""Testing formula 6.11a/b/cN of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_11abcn import (
    Form6Dot11abcnCompressionChordCoefficient,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot11abcnCompressionChordCoefficient:
    """Validation for formula 6.11a/b/cN from EN 1992-1-1:2004."""

    def test_evaluation_below_0_25(self) -> None:
        """Tests the evaluation of the result for sigma_cp/f_cd < 0.25."""
        # Example values
        sigma_cp = 5.0
        f_cd = 30.0

        # Object to test
        formula = Form6Dot11abcnCompressionChordCoefficient(sigma_cp=sigma_cp, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 1 + 1 / 6.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_between_0_25_and_0_5(self) -> None:
        """Tests the evaluation of the result for 0.25 <= sigma_cp/f_cd <= 0.5."""
        # Example values
        sigma_cp = 10.0
        f_cd = 30.0

        # Object to test
        formula = Form6Dot11abcnCompressionChordCoefficient(sigma_cp=sigma_cp, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 1.25

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_above_0_5(self) -> None:
        """Tests the evaluation of the result for sigma_cp/f_cd > 0.5."""
        # Example values
        sigma_cp = 20.0
        f_cd = 30.0

        # Object to test
        formula = Form6Dot11abcnCompressionChordCoefficient(sigma_cp=sigma_cp, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 5 / 6.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("sigma_cp", "f_cd"),
        [
            (-5.0, 30.0),  # sigma_cp is negative
            (0.0, 30.0),  # sigma_cp is zero
            (5.0, -30.0),  # f_cd is negative
            (5.0, 0.0),  # f_cd is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, sigma_cp: float, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot11abcnCompressionChordCoefficient(sigma_cp=sigma_cp, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\alpha_{cw} = \begin{cases} 1 + \frac{\sigma_{cp}}{f_{cd}} & \text{if } 0 \lt \sigma_{cp} \leq 0.25 f_{cd} "
                r"\\ 1.25 & \text{if } 0.25 f_{cd} \lt \sigma_{cp} \leq 0.5 f_{cd} \\ 2.5 \left(1 - \frac{\sigma_{cp}}{f_{cd}}\right) "
                r"& \text{if } \sigma_{cp} \gt 0.5 f_{cd} \end{cases} = "
                r"\begin{cases} 1 + \frac{5.000}{30.000} & \text{if } 0 \lt 5.000 \leq 0.25 \cdot 30.000 \\ 1.250 & \text{if } "
                r"0.25 \cdot 30.000 \lt 5.000 \leq 0.5 \cdot 30.000 \\ 2.5 \left(1 - \frac{5.000}{30.000}\right) & \text{if } "
                r"5.000 \gt 0.5 \cdot 30.000 \end{cases} = 1.167 \ -",
            ),
            ("short", r"\alpha_{cw} = 1.167 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_cp = 5.0
        f_cd = 30.0

        # Object to test
        latex = Form6Dot11abcnCompressionChordCoefficient(sigma_cp=sigma_cp, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
