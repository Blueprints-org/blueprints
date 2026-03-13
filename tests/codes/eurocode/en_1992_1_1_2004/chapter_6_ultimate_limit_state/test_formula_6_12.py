"""Testing formula 6.12 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_12 import (
    Form6Dot12CheckMaxEffectiveCrossSectionalAreaShearReinf,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot12CheckMaxEffectiveCrossSectionalAreaShearReinf:
    """Validation for formula 6.12 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sw_max = 100.0  # mm²
        f_ywd = 400.0  # MPa
        b_w = 300.0  # mm
        s = 200.0  # mm
        alpha_cw = 1.0  # dimensionless
        nu_1 = 0.6  # dimensionless
        f_cd = 30.0  # MPa

        # Object to test
        formula = Form6Dot12CheckMaxEffectiveCrossSectionalAreaShearReinf(
            a_sw_max=a_sw_max,
            f_ywd=f_ywd,
            b_w=b_w,
            s=s,
            alpha_cw=alpha_cw,
            nu_1=nu_1,
            f_cd=f_cd,
        )

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("a_sw_max", "f_ywd", "b_w", "s", "alpha_cw", "nu_1", "f_cd"),
        [
            (-100.0, 400.0, 300.0, 200.0, 1.0, 0.6, 30.0),  # a_sw_max is negative
            (100.0, -400.0, 300.0, 200.0, 1.0, 0.6, 30.0),  # f_ywd is negative
            (100.0, 400.0, -300.0, 200.0, 1.0, 0.6, 30.0),  # b_w is negative
            (100.0, 400.0, 300.0, -200.0, 1.0, 0.6, 30.0),  # s is negative
            (100.0, 400.0, 300.0, 200.0, -1.0, 0.6, 30.0),  # alpha_cw is negative
            (100.0, 400.0, 300.0, 200.0, 1.0, -0.6, 30.0),  # nu_1 is negative
            (100.0, 400.0, 300.0, 200.0, 1.0, 0.6, -30.0),  # f_cd is negative
            (100.0, 400.0, 0.0, 200.0, 1.0, 0.6, 30.0),  # b_w is zero
            (100.0, 400.0, 300.0, 0.0, 1.0, 0.6, 30.0),  # s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, a_sw_max: float, f_ywd: float, b_w: float, s: float, alpha_cw: float, nu_1: float, f_cd: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot12CheckMaxEffectiveCrossSectionalAreaShearReinf(
                a_sw_max=a_sw_max,
                f_ywd=f_ywd,
                b_w=b_w,
                s=s,
                alpha_cw=alpha_cw,
                nu_1=nu_1,
                f_cd=f_cd,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{A_{sw,max} \cdot f_{ywd}}{b_{w} \cdot s} \leq \frac{1}{2} \cdot \alpha_{cw} \cdot \nu_{1} \cdot f_{cd} \to "
                r"\frac{100.000 \cdot 400.000}{300.000 \cdot 200.000} \leq \frac{1}{2} \cdot 1.000 \cdot 0.600 \cdot 30.000 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sw_max = 100.0  # mm²
        f_ywd = 400.0  # MPa
        b_w = 300.0  # mm
        s = 200.0  # mm
        alpha_cw = 1.0  # dimensionless
        nu_1 = 0.6  # dimensionless
        f_cd = 30.0  # MPa

        # Object to test
        latex = Form6Dot12CheckMaxEffectiveCrossSectionalAreaShearReinf(
            a_sw_max=a_sw_max,
            f_ywd=f_ywd,
            b_w=b_w,
            s=s,
            alpha_cw=alpha_cw,
            nu_1=nu_1,
            f_cd=f_cd,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
