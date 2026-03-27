"""Testing formula 8.42 of prEN 1992-1-1:2023."""

import pytest
from typing import ClassVar

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_42 import (
    Form8Dot42ShearStressResistanceReinforcement,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot42ShearStressResistanceReinforcement:
    """Validation for formula 8.42 from prEN 1992-1-1:2023."""

    testdata: ClassVar[list[tuple[float, float, float, float]]] = [
        (0.3e-2, 435., 1.0, 1.305),
        (0.3e-2, 435., 2.5, 3.262),
    ]

    @pytest.mark.parametrize("rho_w,f_ywd,cot_theta,exp_result", testdata)  # noqa: PT006
    def test_evaluation(self, rho_w: float, f_ywd: float, cot_theta: float, exp_result: float) -> None:
        """Test the evaluation of the result."""
        form = Form8Dot42ShearStressResistanceReinforcement(rho_w=rho_w, f_ywd=f_ywd, cot_theta=cot_theta)
        assert form == pytest.approx(expected=exp_result, rel=1e-3)

    @pytest.mark.parametrize(
        ("rho_w", "f_ywd", "cot_theta"),
        [
            (-0.3e-2, 435., 1.0),  # rho_w is negative
            (0.3e-2, -435., 1.0),  # f_ywd is negative
            (0.3e-2, 435., -1.0),  # cot_theta is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, rho_w: float, f_ywd: float, cot_theta: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot42ShearStressResistanceReinforcement(rho_w=rho_w, f_ywd=f_ywd, cot_theta=cot_theta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Rd,sy} = \rho_w \cdot f_{ywd} \cdot \cot \theta = 0.003 \cdot 435.000 \cdot 2.500 = 3.262 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Rd,sy} = \rho_w \cdot f_{ywd} \cdot \cot \theta = 0.003 \cdot 435.000 \ MPa \cdot 2.500 = 3.262 \ MPa",
            ),
            ("short", r"\tau_{Rd,sy} = 3.262 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        rho_w = 0.3e-2
        f_ywd = 435.
        cot_theta = 2.5

        # Object to test
        latex = Form8Dot42ShearStressResistanceReinforcement(rho_w=rho_w, f_ywd=f_ywd, cot_theta=cot_theta).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
