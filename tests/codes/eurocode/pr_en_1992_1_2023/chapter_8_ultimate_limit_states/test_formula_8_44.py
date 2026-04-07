"""Testing formula 8.44 of prEN 1992-1-1:2023."""

from typing import ClassVar

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_44 import Form8Dot44StressCompressionField
from blueprints.validations import NegativeValueError


class TestForm8Dot44StressCompressionField:
    """Validation for formula 8.44 from prEN 1992-1-1:2023."""

    testdata: ClassVar[list[tuple[float, float, float, float, float, float]]] = [
        (2.0, 1.0, 1.0, 0.5, 20.0, 4.0),
        (5.0, 1.0, 1.0, 0.5, 20.0, 10.0),
        (5.0, 2.5, 0.4, 0.5, 20.0, 10.0),
    ]

    @pytest.mark.parametrize("tau_ed,cot_theta,tan_theta,nu,f_cd,exp_result", testdata)  # noqa: PT006
    def test_evaluation(
        self,
        tau_ed: float,
        cot_theta: float,
        tan_theta: float,
        nu: float,
        f_cd: float,
        exp_result: bool,
    ) -> None:
        """Tests the evaluation of the result."""
        formula = Form8Dot44StressCompressionField(
            tau_ed=tau_ed,
            cot_theta=cot_theta,
            tan_theta=tan_theta,
            nu=nu,
            f_cd=f_cd,
        )
        assert formula == exp_result

    @pytest.mark.parametrize(
        ("tau_ed", "cot_theta", "tan_theta", "nu", "f_cd"),
        [
            (-5.0, 1.5, 0.5, 0.6, 16.7),  # tau_ed is negative
            (5.0, -1.5, 0.5, 0.6, 16.7),  # cot_theta is negative
            (5.0, 1.5, -0.5, 0.6, 16.7),  # tan_theta is negative
            (5.0, 1.5, 0.5, -0.6, 16.7),  # nu is negative
        ],
    )
    def test_raise_error_when_negative_values_given(
        self,
        tau_ed: float,
        cot_theta: float,
        tan_theta: float,
        nu: float,
        f_cd: float,
    ) -> None:
        """Test invalid values that should raise NegativeValueError."""
        with pytest.raises(NegativeValueError):
            Form8Dot44StressCompressionField(
                tau_ed=tau_ed,
                cot_theta=cot_theta,
                tan_theta=tan_theta,
                nu=nu,
                f_cd=f_cd,
            )

    @pytest.mark.parametrize(
        ("tau_ed", "cot_theta", "tan_theta", "nu", "f_cd"),
        [
            (-2.0, 1.0, 1.0, 0.5, 20.0),  # tau_Ed is negative
            (2.0, -1.0, 1.0, 0.5, 20.0),  # cot_theta is negative
            (2.0, 1.0, -1.0, 0.5, 20.0),  # tan_theta is negative
            (2.0, 1.0, 1.0, -0.5, 20.0),  # nu is negative
            (2.0, 1.0, 1.0, 0.5, -20.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_invalid_args(
        self,
        tau_ed: float,
        cot_theta: float,
        tan_theta: float,
        nu: float,
        f_cd: float,
    ) -> None:
        """Test invalid values for tau_ed, cot_theta, tan_theta, nu and f_cd."""
        with pytest.raises(NegativeValueError):
            Form8Dot44StressCompressionField(
                tau_ed=tau_ed,
                cot_theta=cot_theta,
                tan_theta=tan_theta,
                nu=nu,
                f_cd=f_cd,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{Rd} = \tau_{Ed} \cdot (\cot \theta + \tan \theta) \leq \nu \cdot f_{cd} = 2.00 \cdot (2.50 + 0.40) \leq 0.50 \cdot 20.00 = 5.80 \leq 10.00 = 5.80 \ MPa",  # noqa: E501
            ),
            (
                "complete_with_units",
                r"\sigma_{Rd} = \tau_{Ed} \cdot (\cot \theta + \tan \theta) \leq \nu \cdot f_{cd} = 2.00 \ MPa \cdot (2.50 + 0.40) \leq 0.50 \cdot 20.00 \ MPa = 5.80 \leq 10.00 = 5.80 \ MPa",  # noqa: E501
            ),
            ("short", r"\sigma_{Rd} = 5.80 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_ed = 2.0  # MPa
        cot_theta = 2.5  # dimensionless
        tan_theta = 0.4  # dimensionless
        nu = 0.5  # dimensionless
        f_cd = 20.0  # MPa

        # Object to test
        latex = Form8Dot44StressCompressionField(
            tau_ed=tau_ed,
            cot_theta=cot_theta,
            tan_theta=tan_theta,
            nu=nu,
            f_cd=f_cd,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
