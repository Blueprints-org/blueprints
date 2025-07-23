"""Testing formula 11.2.2.3-2 from prEN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.pren_1995_1_1_2023.chapter_11_fasteners.formula_11_2_2_3_2 import (
    Form11Dot2Dot2Dot3Dash2WithdrawalStrengthDensityDependent,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm11Dot2Dot2Dot3Dash2WithdrawalStrengthDensityDependent:
    """Validation for formula 11.2.2.3-2 from prEN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("rho_k", "d", "expected_result"),
        [
            (350.0, 8.0, 13.195),  # 20 * (350/350)^0.8 * 8^(-0.2)
            (400.0, 10.0, 14.042), # 20 * (400/350)^0.8 * 10^(-0.2)
            (450.0, 6.0, 17.089),  # 20 * (450/350)^0.8 * 6^(-0.2)
        ],
        ids=["standard_density", "higher_density", "highest_density"],
    )
    def test_evaluation(
        self,
        rho_k: float,
        d: float,
        expected_result: float,
    ) -> None:
        """Test the evaluation of the result."""
        form_11_2_2_3_2 = Form11Dot2Dot2Dot3Dash2WithdrawalStrengthDensityDependent(
            rho_k=rho_k, d=d
        )
        assert form_11_2_2_3_2 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("rho_k", "d", "expectation"),
        [
            (350.0, 8.0, does_not_raise()),
            (-350.0, 8.0, pytest.raises(LessOrEqualToZeroError)),
            (350.0, -8.0, pytest.raises(LessOrEqualToZeroError)),
            (0.0, 8.0, pytest.raises(LessOrEqualToZeroError)),
            (350.0, 0.0, pytest.raises(LessOrEqualToZeroError)),
        ],
        ids=[
            "passes",
            "rho_k<0",
            "d<0",
            "rho_k=0",
            "d=0",
        ],
    )
    def test_raise_error_incorrect_args(
        self,
        rho_k: float,
        d: float,
        expectation: AbstractContextManager,
    ) -> None:
        """Test if errors are raised."""
        with expectation:
            assert (
                Form11Dot2Dot2Dot3Dash2WithdrawalStrengthDensityDependent(
                    rho_k=rho_k, d=d
                )
                is not None
            )

    @pytest.mark.parametrize(
        ("rho_k", "d", "rep_short", "rep_long"),
        [
            (
                350.0,
                8.0,
                r"f_{w,k} = 13.195 \ MPa",
                r"f_{w,k} = 20 \cdot \left(\frac{\rho_k}{350}\right)^{0.8} \cdot d^{-0.2} = 20 \cdot \left(\frac{350.000}{350}\right)^{0.8} \cdot 8.000^{-0.2} = 13.195 \ MPa",
            ),
            (
                400.0,
                10.0,
                r"f_{w,k} = 14.042 \ MPa",
                r"f_{w,k} = 20 \cdot \left(\frac{\rho_k}{350}\right)^{0.8} \cdot d^{-0.2} = 20 \cdot \left(\frac{400.000}{350}\right)^{0.8} \cdot 10.000^{-0.2} = 14.042 \ MPa",
            ),
        ],
        ids=["standard_case", "higher_density_case"],
    )
    def test_latex(
        self,
        rho_k: float,
        d: float,
        rep_short: str,
        rep_long: str,
    ) -> None:
        """Test the latex representation of the formula."""
        form_11_2_2_3_2_latex = Form11Dot2Dot2Dot3Dash2WithdrawalStrengthDensityDependent(
            rho_k=rho_k, d=d
        ).latex()
        assert form_11_2_2_3_2_latex.complete == rep_long
        assert form_11_2_2_3_2_latex.short == rep_short