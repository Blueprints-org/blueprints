"""Testing formula 6.19 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_19 import Form6Dot19CheckShearForce
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot19CheckShearForce:
    """Validation for formula 6.19 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 100000  # N
        a_sw = 200.0  # mm²
        f_ywd = 400.0  # MPa
        alpha = 45.0  # degrees

        # Object to test
        formula = Form6Dot19CheckShearForce(v_ed=v_ed, a_sw=a_sw, f_ywd=f_ywd, alpha=alpha)

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("v_ed", "a_sw", "f_ywd", "alpha"),
        [
            (-100.0, 200.0, 400.0, 45.0),  # v_ed is negative
            (100.0, -200.0, 400.0, 45.0),  # a_sw is negative
            (100.0, 200.0, -400.0, 45.0),  # f_ywd is negative
            (100.0, 200.0, 400.0, -45.0),  # alpha is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, a_sw: float, f_ywd: float, alpha: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot19CheckShearForce(v_ed=v_ed, a_sw=a_sw, f_ywd=f_ywd, alpha=alpha)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to V_{Ed} \leq A_{sw} \cdot f_{ywd} \cdot \sin(\alpha) \to"
                r" 100000.000 \leq 200.000 \cdot 400.000 \cdot \sin(45.000) \to \text{Not OK}",
            ),
            ("short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 100000  # N
        a_sw = 200.0  # mm²
        f_ywd = 400.0  # MPa
        alpha = 45.0  # degrees

        # Object to test
        latex = Form6Dot19CheckShearForce(v_ed=v_ed, a_sw=a_sw, f_ywd=f_ywd, alpha=alpha).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
