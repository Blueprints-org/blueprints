"""Testing formula 6.76 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_76 import Form6Dot76DesignFatigueStrengthConcrete
from blueprints.validations import LessOrEqualToZeroError


class TestForm6Dot76DesignFatigueStrengthConcrete:
    """Validation for formula 6.76 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        k_1 = 0.85
        beta_cc_t0 = 1.1
        f_cd = 3
        f_ck = 2

        # Object to test
        form_6_76 = Form6Dot76DesignFatigueStrengthConcrete(k_1=k_1, beta_cc_t0=beta_cc_t0, f_cd=f_cd, f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 2.78256  # KN

        assert form_6_76 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k_1", "beta_cc_t0", "f_cd", "f_ck"),
        [
            (-0.85, 1.1, 3, 2),
            (0.85, -1.1, 3, 2),
            (0.85, 1.1, -3, 2),
            (0.85, 1.1, 3, -2),
        ],
    )
    def test_raise_error_when_negative_theta_i_is_given(
        self,
        k_1: float,
        beta_cc_t0: float,
        f_cd: float,
        f_ck: float,
    ) -> None:
        """Test negative values for all arguments."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot76DesignFatigueStrengthConcrete(k_1=k_1, beta_cc_t0=beta_cc_t0, f_cd=f_cd, f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{cd,fat} = k_{1} \cdot β_{cc}(t_0) \cdot f_{cd} \cdot \left(1-\frac{f_{ck}}{250}\right) = "
                r"0.850 \cdot 1.100 \cdot 3.000 \cdot \left(1-\frac{2.000}{250}\right) = 2.783",
            ),
            ("short", r"f_{cd,fat} = 2.783"),
            (
                "string",
                r"f_{cd,fat} = k_{1} \cdot β_{cc}(t_0) \cdot f_{cd} \cdot \left(1-\frac{f_{ck}}{250}\right) = "
                r"0.850 \cdot 1.100 \cdot 3.000 \cdot \left(1-\frac{2.000}{250}\right) = 2.783",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_1 = 0.85
        beta_cc_t0 = 1.1
        f_cd = 3
        f_ck = 2

        # Object to test
        form_6_76_latex = Form6Dot76DesignFatigueStrengthConcrete(k_1=k_1, beta_cc_t0=beta_cc_t0, f_cd=f_cd, f_ck=f_ck).latex()

        actual = {"complete": form_6_76_latex.complete, "short": form_6_76_latex.short, "string": str(form_6_76_latex)}

        assert actual[representation] == expected, f"{representation} representation failed."
