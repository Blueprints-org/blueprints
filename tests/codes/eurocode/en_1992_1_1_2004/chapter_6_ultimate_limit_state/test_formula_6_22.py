"""Testing formula 6.22 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_22 import Form6Dot22CheckCrushingCompressionStruts
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot22CheckCrushingCompressionStruts:
    """Validation for formula 6.22 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 8.0  # MPA
        nu = 0.6  # dimensionless
        f_cd = 30.0  # MPA
        theta_f = 45.0  # DEG

        # Object to test
        formula = Form6Dot22CheckCrushingCompressionStruts(v_ed=v_ed, nu=nu, f_cd=f_cd, theta_f=theta_f)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("v_ed", "nu", "f_cd", "theta_f"),
        [
            (-8.0, 0.6, 30.0, 45.0),  # v_ed is negative
            (8.0, -0.6, 30.0, 45.0),  # nu is negative
            (8.0, 0.6, -30.0, 45.0),  # f_cd is negative
            (8.0, 0.6, 30.0, -45.0),  # theta_f is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, nu: float, f_cd: float, theta_f: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot22CheckCrushingCompressionStruts(v_ed=v_ed, nu=nu, f_cd=f_cd, theta_f=theta_f)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to v_{Ed} \leq \nu \cdot f_{cd} \cdot \sin(\theta_{f}) \cdot \cos(\theta_{f}) \to "
                r"8.000 \leq 0.600 \cdot 30.000 \cdot \sin(45.000) \cdot \cos(45.000) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 8.0  # MPa
        nu = 0.6  # dimensionless
        f_cd = 30.0  # MPA
        theta_f = 45.0  # DEG

        # Object to test

        latex = Form6Dot22CheckCrushingCompressionStruts(v_ed=v_ed, nu=nu, f_cd=f_cd, theta_f=theta_f).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
