"""Testing formula 6.50 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_6_ultimate_limit_state.formula_6_50 import Form6Dot50ShearStressResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot50ShearStressResistance:
    """Validation for formula 6.50 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        c_rd_c = 0.18
        k = 1.5
        rho = 0.02
        f_ck = 30.0
        d = 500.0
        a = 300.0
        v_min = 0.035

        # Object to test
        formula = Form6Dot50ShearStressResistance(c_rd_c=c_rd_c, k=k, rho=rho, f_ck=f_ck, d=d, a=a, v_min=v_min)

        # Expected result, manually calculated
        manually_calculated_result = 3.52338087705  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("c_rd_c", "k", "rho", "f_ck", "d", "a", "v_min"),
        [
            (-0.18, 1.5, 0.02, 30.0, 500.0, 300.0, 0.035),  # c_rd_c is negative
            (0.18, -1.5, 0.02, 30.0, 500.0, 300.0, 0.035),  # k is negative
            (0.18, 1.5, -0.02, 30.0, 500.0, 300.0, 0.035),  # rho is negative
            (0.18, 1.5, 0.02, -30.0, 500.0, 300.0, 0.035),  # f_ck is negative
            (0.18, 1.5, 0.02, 30.0, -500.0, 300.0, 0.035),  # d is negative
            (0.18, 1.5, 0.02, 30.0, 500.0, -300.0, 0.035),  # a is negative
            (0.18, 1.5, 0.02, 30.0, 500.0, 300.0, -0.035),  # v_min is negative
            (0.18, 1.5, 0.02, 30.0, 500.0, 0.0, 0.035),  # a is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, c_rd_c: float, k: float, rho: float, f_ck: float, d: float, a: float, v_min: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot50ShearStressResistance(c_rd_c=c_rd_c, k=k, rho=rho, f_ck=f_ck, d=d, a=a, v_min=v_min)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Rd} = \max \left( C_{Rd,c} \cdot k \cdot \left( 100 \cdot \rho \cdot f_{ck} \right)^{\frac{1}{3}} "
                r"\cdot \frac{2 \cdot d}{a}, v_{min} \cdot \frac{2 \cdot d}{a} \right)"
                r" = \max \left( 0.180 \cdot 1.500 \cdot \left( 100 \cdot 0.020 \cdot 30.000 \right)^{\frac{1}{3}} \cdot "
                r"\frac{2 \cdot 500.000}{300.000}, 0.035 \cdot \frac{2 \cdot 500.000}{300.000} \right) = 3.523 MPa",
            ),
            ("short", r"v_{Rd} = 3.523 MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        c_rd_c = 0.18
        k = 1.5
        rho = 0.02
        f_ck = 30.0
        d = 500.0
        a = 300.0
        v_min = 0.035

        # Object to test
        latex = Form6Dot50ShearStressResistance(c_rd_c=c_rd_c, k=k, rho=rho, f_ck=f_ck, d=d, a=a, v_min=v_min).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
