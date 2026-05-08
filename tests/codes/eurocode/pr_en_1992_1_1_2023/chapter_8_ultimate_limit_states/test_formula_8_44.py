"""Testing formula 8.44 of prEN 1992-1-1:2023."""

from typing import ClassVar

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_44 import Form8Dot44StressCompressionField
from blueprints.validations import NegativeValueError


class TestForm8Dot44StressCompressionField:
    """Validation for formula 8.44 from prEN 1992-1-1:2023."""

    testdata: ClassVar[list[tuple[float, float, float, float, float]]] = [
        (2.0, 45.0, 0.5, 20.0, 4.0),
        (5.0, 45.0, 0.5, 20.0, 10.0),
        (5.0, 21.8, 0.5, 20.0, 10.0),
    ]

    @pytest.mark.parametrize("tau_ed,theta,nu,f_cd,exp_result", testdata)  # noqa: PT006
    def test_evaluation(
        self,
        tau_ed: float,
        theta: float,
        nu: float,
        f_cd: float,
        exp_result: float,
    ) -> None:
        """Tests the evaluation of the result."""
        formula = Form8Dot44StressCompressionField(
            tau_ed=tau_ed,
            theta=theta,
            nu=nu,
            f_cd=f_cd,
        )
        assert formula == exp_result

    @pytest.mark.parametrize(
        ("tau_ed", "theta", "nu", "f_cd"),
        [
            (-5.0, 33.69, 0.6, 16.7),  # tau_ed is negative
            (5.0, -33.69, 0.6, 16.7),  # theta is negative
            (5.0, 33.69, -0.6, 16.7),  # nu is negative
        ],
    )
    def test_raise_error_when_negative_values_given(
        self,
        tau_ed: float,
        theta: float,
        nu: float,
        f_cd: float,
    ) -> None:
        """Test invalid values that should raise NegativeValueError."""
        with pytest.raises(NegativeValueError):
            Form8Dot44StressCompressionField(
                tau_ed=tau_ed,
                theta=theta,
                nu=nu,
                f_cd=f_cd,
            )

    @pytest.mark.parametrize(
        ("tau_ed", "theta", "nu", "f_cd"),
        [
            (-2.0, 45.0, 0.5, 20.0),  # tau_Ed is negative
            (2.0, -45.0, 0.5, 20.0),  # theta is negative
            (2.0, 45.0, -0.5, 20.0),  # nu is negative
            (2.0, 45.0, 0.5, -20.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_invalid_args(
        self,
        tau_ed: float,
        theta: float,
        nu: float,
        f_cd: float,
    ) -> None:
        """Test invalid values for tau_ed, cot_theta, tan_theta, nu and f_cd."""
        with pytest.raises(NegativeValueError):
            Form8Dot44StressCompressionField(
                tau_ed=tau_ed,
                theta=theta,
                nu=nu,
                f_cd=f_cd,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{cd} = \tau_{Ed} \cdot \left( \cot \left( \theta \right) + \tan \left( \theta \right) \right) \leq \nu \cdot f_{cd} = 2.00 \cdot \left( \cot \left( 21.80 \right) + \tan \left( 21.80 \right) \right) \leq 0.50 \cdot 20.00 = 5.80 \leq 10.00 = 5.80 \ MPa",  # noqa: E501
            ),
            (
                "complete_with_units",
                r"\sigma_{cd} = \tau_{Ed} \cdot \left( \cot \left( \theta \right) + \tan \left( \theta \right) \right) \leq \nu \cdot f_{cd} = 2.00 \ MPa \cdot \left( \cot \left( 21.80 ^\circ \right) + \tan \left( 21.80 ^\circ \right) \right) \leq 0.50 \cdot 20.00 \ MPa = 5.80 \leq 10.00 = 5.80 \ MPa",  # noqa: E501
            ),
            ("intermediate", r"5.80 \leq 10.00"),
            ("short", r"\sigma_{cd} = 5.80 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_ed = 2.0  # MPa
        theta = 21.8  # deg
        nu = 0.5  # dimensionless
        f_cd = 20.0  # MPa

        # Object to test
        latex = Form8Dot44StressCompressionField(
            tau_ed=tau_ed,
            theta=theta,
            nu=nu,
            f_cd=f_cd,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "intermediate": latex.intermediate_result,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
