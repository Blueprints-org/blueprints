"""Testing formula 8.41 of prEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_41 import Form8Dot41InclinationCompressionField
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot41InclinationCompressionField:
    """Validation for formula 8.41 from prEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("theta", "theta_min", "exp_result"),
        [
            (48.0, 21.8, False),
            (45.0, 21.8, True),
            (26.57, 21.8, True),
            (21.8, 21.8, True),
            (18.43, 21.8, False),
        ],
    )
    def test_evaluation(self, theta: float, theta_min: float, exp_result: bool) -> None:
        """Test the evaluation of the result."""
        form = Form8Dot41InclinationCompressionField(theta=theta, theta_min=theta_min)
        assert form == exp_result

    @pytest.mark.parametrize(
        ("theta", "theta_min"),
        [
            (-45.0, 21.8),  # negative lhs
            (0.0, 21.8),  # zero lhs
            (26.57, -45.0),  # negative rhs
            (26.57, 0),  # zero rhs
        ],
    )
    def test_raise_if_less_or_equal_to_zero(self, theta: float, theta_min: float) -> None:
        """Test if correct error is raised when provide arguments less or equal to zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot41InclinationCompressionField(theta=theta, theta_min=theta_min)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to 1 \le \cot \left( \theta \right) \le \cot \left( \theta_{\min} \right) \to 1 \le \cot \left( 26.57 \right) \le \cot \left( 21.80 \right) \to 1 \le 2.00 \le 2.50 \to OK",  # noqa: E501
            ),
            (
                "complete_with_units",
                r"CHECK \to 1 \le \cot \left( \theta \right) \le \cot \left( \theta_{\min} \right) \to 1 \le \cot \left( 26.57 ^\circ\right) \le \cot \left( 21.80 ^\circ\right) \to 1 \le 2.00 \le 2.50 \to OK",  # noqa: E501
            ),
            ("intermediate", r"1 \le 2.00 \le 2.50"),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representations of the formula."""
        # Example values
        theta = 26.57
        theta_min = 21.8

        # Create test object
        latex = Form8Dot41InclinationCompressionField(theta=theta, theta_min=theta_min).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "intermediate": latex.intermediate_result,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
