"""Testing formula 6.18 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_18 import Form6Dot18AdditionalTensileForce
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot18AdditionalTensileForce:
    """Validation for formula 6.18 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 100.0
        theta = 30.0
        alpha = 45.0

        # Object to test
        formula = Form6Dot18AdditionalTensileForce(v_ed=v_ed, theta=theta, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 36.6025403784  # kN

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "theta", "alpha"),
        [
            (-100.0, 30.0, 45.0),  # v_ed is negative
            (100.0, -30.0, 45.0),  # theta is negative
            (100.0, 30.0, -45.0),  # alpha is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, theta: float, alpha: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot18AdditionalTensileForce(v_ed=v_ed, theta=theta, alpha=alpha)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta F_{td} = 0.5 \cdot V_{Ed} \cdot \left(\cot(\theta) - \cot(\alpha)\right) "
                r"= 0.5 \cdot 100.000 \cdot \left(\cot(30.000) - \cot(45.000)\right) = 36.603 \ kN",
            ),
            ("short", r"\Delta F_{td} = 36.603 \ kN"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 100.0
        theta = 30.0
        alpha = 45.0

        # Object to test
        latex = Form6Dot18AdditionalTensileForce(v_ed=v_ed, theta=theta, alpha=alpha).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
