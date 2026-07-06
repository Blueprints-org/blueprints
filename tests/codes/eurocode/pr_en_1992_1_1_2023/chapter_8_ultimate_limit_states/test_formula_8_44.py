"""Testing formula 8.44 of prEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_44 import Form8Dot44StressCompressionField
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot44StressCompressionField:
    """Validation for formula 8.44 from prEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "theta", "nu", "f_cd", "exp_result"),
        [
            (2.0, 45.0, 0.5, 20.0, 4.0),  # Calculated result below upper limit
            (5.0, 45.0, 0.5, 20.0, 10.0),  # Calculated result above upper limit --> capped at limit
            (5.0, 21.8, 0.5, 20.0, 10.0),  # Calculated result different angle above upper limit --> capped at limit
        ],
    )
    def test_evaluation(self, tau_ed: float, theta: float, nu: float, f_cd: float, exp_result: float) -> None:
        """Tests the evaluation of the result."""
        formula = Form8Dot44StressCompressionField(tau_ed=tau_ed, theta=theta, nu=nu, f_cd=f_cd)
        assert formula == exp_result

    @pytest.mark.parametrize(
        ("tau_ed", "theta", "nu", "f_cd"),
        [
            (-2.0, 45.0, 0.5, 20.0),  # tau_Ed is negative
            (2.0, 45.0, -0.5, 20.0),  # nu is negative
            (2.0, 45.0, 0.5, -20.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, tau_ed: float, theta: float, nu: float, f_cd: float) -> None:
        """Test invalid values for tau_ed, nu and f_cd."""
        with pytest.raises(NegativeValueError):
            Form8Dot44StressCompressionField(tau_ed=tau_ed, theta=theta, nu=nu, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("tau_ed", "theta", "nu", "f_cd"),
        [
            (2.0, 0.0, 0.5, 20.0),  # theta is zero
            (2.0, -45.0, 0.5, 20.0),  # theta is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero_values_are_given(self, tau_ed: float, theta: float, nu: float, f_cd: float) -> None:
        """Test invalid values for theta."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot44StressCompressionField(tau_ed=tau_ed, theta=theta, nu=nu, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{cd} = \tau_{Ed} \cdot \left( \cot \left( \theta \right) + \tan \left( \theta \right) \right) \leq \nu \cdot f_{cd} "
                r"= 2.00 \cdot \left( \cot \left( 21.80 \right) + \tan \left( 21.80 \right) \right) "
                r"\leq 0.50 \cdot 20.00 = 5.80 \leq 10.00 = 5.80 \ MPa",
            ),
            (
                "complete_with_units",
                r"\sigma_{cd} = \tau_{Ed} \cdot \left( \cot \left( \theta \right) + \tan \left( \theta \right) \right) \leq \nu \cdot f_{cd} "
                r"= 2.00 \ MPa \cdot \left( \cot \left( 21.80 ^\circ \right) + \tan \left( 21.80 ^\circ \right) \right) "
                r"\leq 0.50 \cdot 20.00 \ MPa = 5.80 \leq 10.00 = 5.80 \ MPa",
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
        latex = Form8Dot44StressCompressionField(tau_ed=tau_ed, theta=theta, nu=nu, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "intermediate": latex.intermediate_result,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
