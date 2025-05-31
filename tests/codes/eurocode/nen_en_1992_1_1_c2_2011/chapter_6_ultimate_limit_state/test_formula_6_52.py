"""Testing formula 6.52 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_52 import (
    Form6Dot52PunchingShearResistance,
    Form6Dot52Sub1EffectiveYieldStrength,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot52PunchingShearResistance:
    """Validation for formula 6.52 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_rd_c = 1.5  # MPa
        d = 200.0  # mm
        s_r = 150.0  # mm
        a_sw = 1000.0  # mm^2
        f_ywd_ef = 500.0  # MPa
        u_1 = 400.0  # mm
        alpha = 45.0  # degrees

        # Object to test
        formula = Form6Dot52PunchingShearResistance(v_rd_c=v_rd_c, d=d, s_r=s_r, a_sw=a_sw, f_ywd_ef=f_ywd_ef, u_1=u_1, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 9.96383476483  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_rd_c", "d", "s_r", "a_sw", "f_ywd_ef", "u_1", "alpha"),
        [
            (-1.5, 200.0, 150.0, 1000.0, 500.0, 400.0, 45.0),  # v_rd_c is negative
            (1.5, -200.0, 150.0, 1000.0, 500.0, 400.0, 45.0),  # d is negative
            (1.5, 200.0, -150.0, 1000.0, 500.0, 400.0, 45.0),  # s_r is negative
            (1.5, 200.0, 150.0, -1000.0, 500.0, 400.0, 45.0),  # a_sw is negative
            (1.5, 200.0, 150.0, 1000.0, -500.0, 400.0, 45.0),  # f_ywd_ef is negative
            (1.5, 200.0, 150.0, 1000.0, 500.0, -400.0, 45.0),  # u_1 is negative
            (1.5, 200.0, 150.0, 1000.0, 500.0, 400.0, -45.0),  # alpha is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, v_rd_c: float, d: float, s_r: float, a_sw: float, f_ywd_ef: float, u_1: float, alpha: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot52PunchingShearResistance(v_rd_c=v_rd_c, d=d, s_r=s_r, a_sw=a_sw, f_ywd_ef=f_ywd_ef, u_1=u_1, alpha=alpha)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Rd,cs} = 0.75 \cdot v_{Rd,c} + 1.5 \cdot \frac{ d}{s_r} \cdot A_{sw} \cdot "
                r"f_{ywd,ef} \cdot \frac{1}{u_{1} \cdot d} \cdot \sin(\alpha) = "
                r"0.75 \cdot 1.500 + 1.5 \cdot \frac{ 200.000}{150.000} \cdot 1000.000 \cdot 500.000 "
                r"\cdot \frac{1}{400.000 \cdot 200.000} \cdot \sin(45.000) = 9.964 \ MPa",
            ),
            ("short", r"v_{Rd,cs} = 9.964 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_rd_c = 1.5  # MPa
        d = 200.0  # mm
        s_r = 150.0  # mm
        a_sw = 1000.0  # mm^2
        f_ywd_ef = 500.0  # MPa
        u_1 = 400.0  # mm
        alpha = 45.0  # degrees

        # Object to test
        latex = Form6Dot52PunchingShearResistance(v_rd_c=v_rd_c, d=d, s_r=s_r, a_sw=a_sw, f_ywd_ef=f_ywd_ef, u_1=u_1, alpha=alpha).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot52Sub1EffectiveYieldStrength:
    """Validation for formula 6.52sub1 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d = 500.0
        f_ywd = 400.0

        # Object to test
        formula = Form6Dot52Sub1EffectiveYieldStrength(d=d, f_ywd=f_ywd)

        # Expected result, manually calculated
        manually_calculated_result = 375  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d", "f_ywd"),
        [
            (-500.0, 400.0),  # d is negative
            (500.0, -400.0),  # f_ywd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d: float, f_ywd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot52Sub1EffectiveYieldStrength(d=d, f_ywd=f_ywd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{ywd,ef} = \min\left(250 + 0.25 \cdot d, f_{ywd}\right) = \min\left(250 + 0.25 \cdot 500.000, 400.000\right) = 375.000 \ MPa",
            ),
            ("short", r"f_{ywd,ef} = 375.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d = 500.0
        f_ywd = 400.0

        # Object to test
        latex = Form6Dot52Sub1EffectiveYieldStrength(d=d, f_ywd=f_ywd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
