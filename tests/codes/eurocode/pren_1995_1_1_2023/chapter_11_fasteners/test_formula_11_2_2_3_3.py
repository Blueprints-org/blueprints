"""Testing formula 11.2.2.3-3 from prEN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.pren_1995_1_1_2023.chapter_11_fasteners.formula_11_2_2_3_3 import (
    Form11Dot2Dot2Dot3Dash3DesignWithdrawalResistance,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm11Dot2Dot2Dot3Dash3DesignWithdrawalResistance:
    """Validation for formula 11.2.2.3-3 from prEN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("f_w_rk", "k_mod", "gamma_m", "expected_result"),
        [
            (10.0, 0.9, 1.3, 6.923),  # (0.9 * 10.0) / 1.3
            (15.0, 0.8, 1.2, 10.0),   # (0.8 * 15.0) / 1.2
            (8.0, 1.0, 1.3, 6.154),   # (1.0 * 8.0) / 1.3
        ],
        ids=["standard_case", "higher_load", "unity_k_mod"],
    )
    def test_evaluation(
        self,
        f_w_rk: float,
        k_mod: float,
        gamma_m: float,
        expected_result: float,
    ) -> None:
        """Test the evaluation of the result."""
        form_11_2_2_3_3 = Form11Dot2Dot2Dot3Dash3DesignWithdrawalResistance(
            f_w_rk=f_w_rk, k_mod=k_mod, gamma_m=gamma_m
        )
        assert form_11_2_2_3_3 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("f_w_rk", "k_mod", "gamma_m", "expectation"),
        [
            (10.0, 0.9, 1.3, does_not_raise()),
            (-10.0, 0.9, 1.3, pytest.raises(LessOrEqualToZeroError)),
            (10.0, -0.9, 1.3, pytest.raises(LessOrEqualToZeroError)),
            (10.0, 0.9, -1.3, pytest.raises(LessOrEqualToZeroError)),
            (0.0, 0.9, 1.3, pytest.raises(LessOrEqualToZeroError)),
            (10.0, 0.0, 1.3, pytest.raises(LessOrEqualToZeroError)),
            (10.0, 0.9, 0.0, pytest.raises(LessOrEqualToZeroError)),
        ],
        ids=[
            "passes",
            "f_w_rk<0",
            "k_mod<0",
            "gamma_m<0",
            "f_w_rk=0",
            "k_mod=0",
            "gamma_m=0",
        ],
    )
    def test_raise_error_incorrect_args(
        self,
        f_w_rk: float,
        k_mod: float,
        gamma_m: float,
        expectation: AbstractContextManager,
    ) -> None:
        """Test if errors are raised."""
        with expectation:
            assert (
                Form11Dot2Dot2Dot3Dash3DesignWithdrawalResistance(
                    f_w_rk=f_w_rk, k_mod=k_mod, gamma_m=gamma_m
                )
                is not None
            )

    @pytest.mark.parametrize(
        ("f_w_rk", "k_mod", "gamma_m", "rep_short", "rep_long"),
        [
            (
                10.0,
                0.9,
                1.3,
                r"F_{w,Rd} = 6.923 \ kN",
                r"F_{w,Rd} = \frac{k_{mod} \cdot F_{w,Rk}}{\gamma_M} = \frac{0.900 \cdot 10.000}{1.300} = 6.923 \ kN",
            ),
            (
                15.0,
                0.8,
                1.2,
                r"F_{w,Rd} = 10.000 \ kN",
                r"F_{w,Rd} = \frac{k_{mod} \cdot F_{w,Rk}}{\gamma_M} = \frac{0.800 \cdot 15.000}{1.200} = 10.000 \ kN",
            ),
        ],
        ids=["standard_case", "higher_load_case"],
    )
    def test_latex(
        self,
        f_w_rk: float,
        k_mod: float,
        gamma_m: float,
        rep_short: str,
        rep_long: str,
    ) -> None:
        """Test the latex representation of the formula."""
        form_11_2_2_3_3_latex = Form11Dot2Dot2Dot3Dash3DesignWithdrawalResistance(
            f_w_rk=f_w_rk, k_mod=k_mod, gamma_m=gamma_m
        ).latex()
        assert form_11_2_2_3_3_latex.complete == rep_long
        assert form_11_2_2_3_3_latex.short == rep_short