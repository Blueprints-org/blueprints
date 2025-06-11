"""Testing formula 6.77 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_77 import Form6Dot77FatigueVerification
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot77FatigueVerification:
    """Validation for formula 6.77 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sigma_c_max = 15.0
        sigma_c_min = 5.0
        f_cd_fat = 20.0
        f_ck = 30.0

        # Object to test
        formula = Form6Dot77FatigueVerification(
            sigma_c_max=sigma_c_max,
            sigma_c_min=sigma_c_min,
            f_cd_fat=f_cd_fat,
            f_ck=f_ck,
        )

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("sigma_c_max", "sigma_c_min", "f_cd_fat", "f_ck"),
        [
            (-15.0, 5.0, 20.0, 30.0),  # sigma_c_max is negative
            (15.0, -5.0, 20.0, 30.0),  # sigma_c_min is negative
            (15.0, 5.0, -20.0, 30.0),  # f_cd_fat is negative
            (15.0, 5.0, 20.0, -30.0),  # f_ck is negative
            (15.0, 5.0, 0.0, 30.0),  # f_cd_fat is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, sigma_c_max: float, sigma_c_min: float, f_cd_fat: float, f_ck: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot77FatigueVerification(
                sigma_c_max=sigma_c_max,
                sigma_c_min=sigma_c_min,
                f_cd_fat=f_cd_fat,
                f_ck=f_ck,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{\sigma_{c,max}}{f_{cd,fat}} \leq \min\left(0.5 + 0.45 \cdot \frac{\sigma_{c,min}}{f_{cd,fat}}, "
                r"\begin{cases} 0.9 & \text{if } f_{ck} \leq 50 \\ 0.8 & \text{if } f_{ck} > 50 \end{cases}\right) \to "
                r"\frac{15.000}{20.000} \leq \min\left(0.5 + 0.45 \cdot \frac{5.000}{20.000}, \begin{cases} 0.9 & "
                r"\text{if } 30.000 \leq 50 \\ 0.8 & \text{if } 30.000 > 50 \end{cases}\right) \to \text{Not OK}",
            ),
            ("short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_c_max = 15.0
        sigma_c_min = 5.0
        f_cd_fat = 20.0
        f_ck = 30.0

        # Object to test
        latex = Form6Dot77FatigueVerification(
            sigma_c_max=sigma_c_max,
            sigma_c_min=sigma_c_min,
            f_cd_fat=f_cd_fat,
            f_ck=f_ck,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
