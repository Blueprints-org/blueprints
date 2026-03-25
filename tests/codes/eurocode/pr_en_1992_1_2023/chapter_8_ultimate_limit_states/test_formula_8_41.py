"""Testing formula 8.41 of prEN 1992-1-1:2023."""

from typing import ClassVar

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_41 import Form8Dot41InclinationCompressionField
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot41InclinationCompressionField:
    """Validation for formula 8.41 from prEN 1992-1-1:2023."""

    testdata: ClassVar[list[tuple[float, float, bool]]] = [
        (0.9, 2.5, False),
        (1.0, 2.5, True),
        (2.0, 2.5, True),
        (2.5, 2.5, True),
        (3.0, 2.5, False),
    ]

    @pytest.mark.parametrize("cot_theta,cot_theta_min,exp_result", testdata)  # noqa: PT006
    def test_evaluation(self, cot_theta: float, cot_theta_min: float, exp_result: bool) -> None:
        """Test the evaluation of the result."""
        form = Form8Dot41InclinationCompressionField(cot_theta=cot_theta, cot_theta_min=cot_theta_min)
        assert form == exp_result

    @pytest.mark.parametrize(
        ("cot_theta", "cot_theta_min"),
        [
            (-1.0, 2.5),  # negative lhs
            (0.0, 2.5),  # zero lhs
            (2.0, -1.0),  # negative rhs
            (2.0, 0),  # zero rhs
        ],
    )
    def test_raise_if_less_or_equal_to_zero(self, cot_theta: float, cot_theta_min: float) -> None:
        """Test if correct error is raised when provide arguments less or equal to zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot41InclinationCompressionField(cot_theta=cot_theta, cot_theta_min=cot_theta_min)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"CHECK \to 1 \le \cot \theta \le \cot \theta_{\min} \to 1 \le 2.00 \le 2.50 \to OK"),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representations of the formula."""
        # Example values
        cot_theta = 2.0
        cot_theta_min = 2.5

        # Create test object
        latex = Form8Dot41InclinationCompressionField(cot_theta=cot_theta, cot_theta_min=cot_theta_min).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert expected == actual[representation], f"{representation} representation failed."
