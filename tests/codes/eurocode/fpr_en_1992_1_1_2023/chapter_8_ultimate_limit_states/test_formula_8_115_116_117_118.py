"""Testing formulas 8.115, 8.116, 8.117 and 8.118 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_115_116_117_118 import (
    Form8Dot115To118StrengthReductionFactorCrossedByTie,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot115To118StrengthReductionFactorCrossedByTie:
    """Validation for formulas 8.115, 8.116, 8.117 and 8.118 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("theta_cs", "expected"),
        [
            (20.0, 0.4),  # lower boundary of the first range
            (25.0, 0.4),  # inside the first range
            (29.999, 0.4),  # just below the second boundary
            (30.0, 0.55),  # lower boundary of the second range
            (35.0, 0.55),  # inside the second range
            (39.999, 0.55),  # just below the third boundary
            (40.0, 0.7),  # lower boundary of the third range
            (50.0, 0.7),  # inside the third range
            (59.999, 0.7),  # just below the fourth boundary
            (60.0, 0.85),  # lower boundary of the fourth range
            (75.0, 0.85),  # inside the fourth range
            (89.999, 0.85),  # just below the upper boundary
        ],
    )
    def test_evaluation(self, theta_cs: float, expected: float) -> None:
        """Tests the evaluation of the result."""
        assert Form8Dot115To118StrengthReductionFactorCrossedByTie(theta_cs=theta_cs) == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        "theta_cs",
        [
            0.0,  # zero
            -5.0,  # negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, theta_cs: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot115To118StrengthReductionFactorCrossedByTie(theta_cs=theta_cs)

    @pytest.mark.parametrize(
        "theta_cs",
        [
            10.0,  # below the range covered by the formulas
            90.0,  # at the excluded upper boundary
            95.0,  # above the range covered by the formulas
        ],
    )
    def test_raise_error_when_theta_cs_outside_covered_range(self, theta_cs: float) -> None:
        """Test values of theta_cs outside the range covered by formulas (8.115) to (8.118)."""
        with pytest.raises(ValueError, match="outside the range covered by formulas"):
            Form8Dot115To118StrengthReductionFactorCrossedByTie(theta_cs=theta_cs)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\nu = \begin{cases} 0.4 & \text{if } 20^\circ \leq \theta_{cs} < 30^\circ \\ "
                    r"0.55 & \text{if } 30^\circ \leq \theta_{cs} < 40^\circ \\ "
                    r"0.7 & \text{if } 40^\circ \leq \theta_{cs} < 60^\circ \\ "
                    r"0.85 & \text{if } 60^\circ \leq \theta_{cs} < 90^\circ \end{cases} = "
                    r"\begin{cases} 0.4 & \text{if } 20^\circ \leq 45.000 < 30^\circ \\ "
                    r"0.55 & \text{if } 30^\circ \leq 45.000 < 40^\circ \\ "
                    r"0.7 & \text{if } 40^\circ \leq 45.000 < 60^\circ \\ "
                    r"0.85 & \text{if } 60^\circ \leq 45.000 < 90^\circ \end{cases} = 0.700 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\nu = \begin{cases} 0.4 & \text{if } 20^\circ \leq \theta_{cs} < 30^\circ \\ "
                    r"0.55 & \text{if } 30^\circ \leq \theta_{cs} < 40^\circ \\ "
                    r"0.7 & \text{if } 40^\circ \leq \theta_{cs} < 60^\circ \\ "
                    r"0.85 & \text{if } 60^\circ \leq \theta_{cs} < 90^\circ \end{cases} = "
                    r"\begin{cases} 0.4 & \text{if } 20^\circ \leq 45.000 ^\circ < 30^\circ \\ "
                    r"0.55 & \text{if } 30^\circ \leq 45.000 ^\circ < 40^\circ \\ "
                    r"0.7 & \text{if } 40^\circ \leq 45.000 ^\circ < 60^\circ \\ "
                    r"0.85 & \text{if } 60^\circ \leq 45.000 ^\circ < 90^\circ \end{cases} = 0.700 \ -"
                ),
            ),
            ("short", r"\nu = 0.700 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example value
        theta_cs = 45.0

        # Object to test
        latex = Form8Dot115To118StrengthReductionFactorCrossedByTie(theta_cs=theta_cs).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
