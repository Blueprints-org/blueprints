"""Testing formula 6.15 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_15 import Form6Dot15ShearReinforcementResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot15ShearReinforcementResistance:
    """Validation for formula 6.15 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sw_max = 1000.0  # mm²
        f_ywd = 500.0  # MPa
        b_w = 300.0  # mm
        s = 200.0  # mm
        alpha_cw = 1.0  # dimensionless
        nu_1 = 0.6  # dimensionless
        f_cd = 30.0  # MPa
        alpha = 45.0  # degrees

        # Object to test
        formula = Form6Dot15ShearReinforcementResistance(
            a_sw_max=a_sw_max,
            f_ywd=f_ywd,
            b_w=b_w,
            s=s,
            alpha_cw=alpha_cw,
            nu_1=nu_1,
            f_cd=f_cd,
            alpha=alpha,
        )

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("a_sw_max", "f_ywd", "b_w", "s", "alpha_cw", "nu_1", "f_cd", "alpha"),
        [
            (-1000.0, 500.0, 300.0, 200.0, 1.0, 0.6, 30.0, 45.0),  # a_sw_max is negative
            (1000.0, -500.0, 300.0, 200.0, 1.0, 0.6, 30.0, 45.0),  # f_ywd is negative
            (1000.0, 500.0, -300.0, 200.0, 1.0, 0.6, 30.0, 45.0),  # b_w is negative
            (1000.0, 500.0, 300.0, -200.0, 1.0, 0.6, 30.0, 45.0),  # s is negative
            (1000.0, 500.0, 300.0, 200.0, -1.0, 0.6, 30.0, 45.0),  # alpha_cw is negative
            (1000.0, 500.0, 300.0, 200.0, 1.0, -0.6, 30.0, 45.0),  # nu_1 is negative
            (1000.0, 500.0, 300.0, 200.0, 1.0, 0.6, -30.0, 45.0),  # f_cd is negative
            (1000.0, 500.0, 300.0, 200.0, 1.0, 0.6, 30.0, -45.0),  # alpha is negative
            (1000.0, 500.0, 0.0, 200.0, 1.0, 0.6, 30.0, 45.0),  # b_w is zero
            (1000.0, 500.0, 300.0, 0.0, 1.0, 0.6, 30.0, 45.0),  # s is zero
            (1000.0, 500.0, 300.0, 200.0, 1.0, 0.6, 30.0, 0.0),  # alpha is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, a_sw_max: float, f_ywd: float, b_w: float, s: float, alpha_cw: float, nu_1: float, f_cd: float, alpha: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot15ShearReinforcementResistance(
                a_sw_max=a_sw_max,
                f_ywd=f_ywd,
                b_w=b_w,
                s=s,
                alpha_cw=alpha_cw,
                nu_1=nu_1,
                f_cd=f_cd,
                alpha=alpha,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{A_{sw,max} \cdot f_{ywd}}{b_{w} \cdot s} \leq \frac{\frac{1}{2} \cdot \alpha_{cw} "
                r"\cdot \nu_{1} \cdot f_{cd}}{\sin(\alpha)} \to "
                r"\frac{1000.000 \cdot 500.000}{300.000 \cdot 200.000} \leq \frac{\frac{1}{2} \cdot 1.000 "
                r"\cdot 0.600 \cdot 30.000}{\sin(45.000)} \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sw_max = 1000.0  # mm²
        f_ywd = 500.0  # MPa
        b_w = 300.0  # mm
        s = 200.0  # mm
        alpha_cw = 1.0  # dimensionless
        nu_1 = 0.6  # dimensionless
        f_cd = 30.0  # MPa
        alpha = 45.0  # degrees

        # Object to test
        latex = Form6Dot15ShearReinforcementResistance(
            a_sw_max=a_sw_max,
            f_ywd=f_ywd,
            b_w=b_w,
            s=s,
            alpha_cw=alpha_cw,
            nu_1=nu_1,
            f_cd=f_cd,
            alpha=alpha,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
