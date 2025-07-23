"""Testing formula 11.2.2.3-1 from prEN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.pren_1995_1_1_2023.chapter_11_fasteners.formula_11_2_2_3_1 import (
    Form11Dot2Dot2Dot3Dash1WithdrawalCapacityScrew,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm11Dot2Dot2Dot3Dash1WithdrawalCapacityScrew:
    """Validation for formula 11.2.2.3-1 from prEN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("d_head_ef", "l_ef", "rho_k", "f_w_k", "expected_result"),
        [
            (10.0, 50.0, 350.0, 4.0, 6.283),  # π * 10 * 50 * 4 / 1000
            (8.0, 40.0, 400.0, 3.5, 3.518),   # π * 8 * 40 * 3.5 / 1000
            (12.0, 60.0, 450.0, 5.0, 11.310), # π * 12 * 60 * 5 / 1000
        ],
        ids=["standard_screw", "smaller_screw", "larger_screw"],
    )
    def test_evaluation(
        self,
        d_head_ef: float,
        l_ef: float,
        rho_k: float,
        f_w_k: float,
        expected_result: float,
    ) -> None:
        """Test the evaluation of the result."""
        form_11_2_2_3_1 = Form11Dot2Dot2Dot3Dash1WithdrawalCapacityScrew(
            d_head_ef=d_head_ef, l_ef=l_ef, rho_k=rho_k, f_w_k=f_w_k
        )
        assert form_11_2_2_3_1 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("d_head_ef", "l_ef", "rho_k", "f_w_k", "expectation"),
        [
            (10.0, 50.0, 350.0, 4.0, does_not_raise()),
            (-10.0, 50.0, 350.0, 4.0, pytest.raises(LessOrEqualToZeroError)),
            (10.0, -50.0, 350.0, 4.0, pytest.raises(LessOrEqualToZeroError)),
            (10.0, 50.0, -350.0, 4.0, pytest.raises(LessOrEqualToZeroError)),
            (10.0, 50.0, 350.0, -4.0, pytest.raises(LessOrEqualToZeroError)),
            (0.0, 50.0, 350.0, 4.0, pytest.raises(LessOrEqualToZeroError)),
        ],
        ids=[
            "passes",
            "d_head_ef<0",
            "l_ef<0",
            "rho_k<0",
            "f_w_k<0",
            "d_head_ef=0",
        ],
    )
    def test_raise_error_incorrect_args(
        self,
        d_head_ef: float,
        l_ef: float,
        rho_k: float,
        f_w_k: float,
        expectation: AbstractContextManager,
    ) -> None:
        """Test if errors are raised."""
        with expectation:
            assert (
                Form11Dot2Dot2Dot3Dash1WithdrawalCapacityScrew(
                    d_head_ef=d_head_ef, l_ef=l_ef, rho_k=rho_k, f_w_k=f_w_k
                )
                is not None
            )

    @pytest.mark.parametrize(
        ("d_head_ef", "l_ef", "rho_k", "f_w_k", "rep_short", "rep_long"),
        [
            (
                10.0,
                50.0,
                350.0,
                4.0,
                r"F_{w,Rd} = 6.283 \ kN",
                r"F_{w,Rd} = \pi \cdot d_{head,ef} \cdot l_{ef} \cdot f_{w,k} = \pi \cdot 10.000 \cdot 50.000 \cdot 4.000 = 6.283 \ kN",
            ),
            (
                8.0,
                40.0,
                400.0,
                3.5,
                r"F_{w,Rd} = 3.518 \ kN",
                r"F_{w,Rd} = \pi \cdot d_{head,ef} \cdot l_{ef} \cdot f_{w,k} = \pi \cdot 8.000 \cdot 40.000 \cdot 3.500 = 3.518 \ kN",
            ),
        ],
        ids=["standard_case", "smaller_case"],
    )
    def test_latex(
        self,
        d_head_ef: float,
        l_ef: float,
        rho_k: float,
        f_w_k: float,
        rep_short: str,
        rep_long: str,
    ) -> None:
        """Test the latex representation of the formula."""
        form_11_2_2_3_1_latex = Form11Dot2Dot2Dot3Dash1WithdrawalCapacityScrew(
            d_head_ef=d_head_ef, l_ef=l_ef, rho_k=rho_k, f_w_k=f_w_k
        ).latex()
        assert form_11_2_2_3_1_latex.complete == rep_long
        assert form_11_2_2_3_1_latex.short == rep_short