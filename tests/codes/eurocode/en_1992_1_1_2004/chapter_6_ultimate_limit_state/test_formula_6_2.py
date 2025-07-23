"""Testing formula 6.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_2 import (
    Form6Dot2aSub1ThicknessFactor,
    Form6Dot2aSub2RebarRatio,
    Form6Dot2ShearResistance,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot2ShearResistance:
    """Validation for formula 6.2a from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        c_rd_c = 0.18
        k = 1.0
        rho_l = 0.02
        f_ck = 30.0
        k_1 = 0.15
        sigma_cp = 1.0
        b_w = 300.0
        d = 500.0
        v_min = 0.035

        # Object to test
        formula = Form6Dot2ShearResistance(c_rd_c=c_rd_c, k=k, rho_l=rho_l, f_ck=f_ck, k_1=k_1, sigma_cp=sigma_cp, b_w=b_w, d=d, v_min=v_min)

        # Expected result, manually calculated
        manually_calculated_result = 128201.426312

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("c_rd_c", "k", "rho_l", "f_ck", "k_1", "sigma_cp", "b_w", "d", "v_min"),
        [
            (-0.18, 1.0, 0.02, 30.0, 0.15, 1.0, 300.0, 500.0, 0.035),  # c_rd_c is negative
            (0.18, -1.0, 0.02, 30.0, 0.15, 1.0, 300.0, 500.0, 0.035),  # k is negative
            (0.18, 1.0, -0.02, 30.0, 0.15, 1.0, 300.0, 500.0, 0.035),  # rho_l is negative
            (0.18, 1.0, 0.02, -30.0, 0.15, 1.0, 300.0, 500.0, 0.035),  # f_ck is negative
            (0.18, 1.0, 0.02, 30.0, -0.15, 1.0, 300.0, 500.0, 0.035),  # k_1 is negative
            (0.18, 1.0, 0.02, 30.0, 0.15, -1.0, 300.0, 500.0, 0.035),  # sigma_cp is negative
            (0.18, 1.0, 0.02, 30.0, 0.15, 1.0, -300.0, 500.0, 0.035),  # b_w is negative
            (0.18, 1.0, 0.02, 30.0, 0.15, 1.0, 300.0, -500.0, 0.035),  # d is negative
            (0.18, 1.0, 0.02, 30.0, 0.15, 1.0, 300.0, 500.0, -0.035),  # v_min is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, c_rd_c: float, k: float, rho_l: float, f_ck: float, k_1: float, sigma_cp: float, b_w: float, d: float, v_min: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot2ShearResistance(c_rd_c=c_rd_c, k=k, rho_l=rho_l, f_ck=f_ck, k_1=k_1, sigma_cp=sigma_cp, b_w=b_w, d=d, v_min=v_min)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{Rd,c} = \max(C_{Rd,c} \cdot k \cdot \left(100 \cdot \rho_l \cdot f_{ck}\right)^{1/3} + "
                r"k_1 \cdot \sigma_{cp}, v_{min} + k_1 \cdot \sigma_{cp}) \cdot b_w \cdot d"
                r" = \max(0.180 \cdot 1.000 \cdot \left(100 \cdot 0.020 \cdot 30.000\right)^{1/3} + 0.150 \cdot "
                r"1.000, 0.035 + 0.150 \cdot 1.000) \cdot 300.000 \cdot 500.000 = 128201.426 \ N",
            ),
            ("short", r"V_{Rd,c} = 128201.426 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        c_rd_c = 0.18
        k = 1.0
        rho_l = 0.02
        f_ck = 30.0
        k_1 = 0.15
        sigma_cp = 1.0
        b_w = 300.0
        d = 500.0
        v_min = 0.035

        # Object to test
        latex = Form6Dot2ShearResistance(c_rd_c=c_rd_c, k=k, rho_l=rho_l, f_ck=f_ck, k_1=k_1, sigma_cp=sigma_cp, b_w=b_w, d=d, v_min=v_min).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot2aSub1ThicknessFactor:
    """Validation for formula 6.2aSub1 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d = 500.0

        # Object to test
        formula = Form6Dot2aSub1ThicknessFactor(d=d)

        # Expected result, manually calculated
        manually_calculated_result = 1.63245553203

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d"),
        [
            (-500.0),  # d is negative
            (0.0),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot2aSub1ThicknessFactor(d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k = \min(1 + \sqrt{\frac{200}{d}}, 2.0) = \min(1 + \sqrt{\frac{200}{500.000}}, 2.0) = 1.632 \ -",
            ),
            ("short", r"k = 1.632 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d = 500.0

        # Object to test
        latex = Form6Dot2aSub1ThicknessFactor(d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot2aSub2RebarRatio:
    """Validation for formula 6.2aSub2 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sl = 1500.0
        b_w = 300.0
        d = 500.0

        # Object to test
        formula = Form6Dot2aSub2RebarRatio(a_sl=a_sl, b_w=b_w, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 0.01

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_sl", "b_w", "d"),
        [
            (-1500.0, 300.0, 500.0),  # A_sl is negative
            (1500.0, -300.0, 500.0),  # b_w is negative
            (1500.0, 0.0, 500.0),  # b_w is zero
            (1500.0, 300.0, -500.0),  # d is negative
            (1500.0, 300.0, 0.0),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_sl: float, b_w: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot2aSub2RebarRatio(a_sl=a_sl, b_w=b_w, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_l = \min( \frac{A_{sl}}{b_w \cdot d}, 0.02) = \min( \frac{1500.000}{300.000 \cdot 500.000}, 0.02) = 0.010 \ -",
            ),
            ("short", r"\rho_l = 0.010 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sl = 1500.0
        b_w = 300.0
        d = 500.0

        # Object to test
        latex = Form6Dot2aSub2RebarRatio(a_sl=a_sl, b_w=b_w, d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
