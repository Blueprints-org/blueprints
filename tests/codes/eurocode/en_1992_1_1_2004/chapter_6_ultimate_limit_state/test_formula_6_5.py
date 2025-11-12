"""Testing formula 6.5 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_5 import Form6Dot5ShearForceCheck
from blueprints.validations import NegativeValueError


class TestForm6Dot5ShearForceCheck:
    """Validation for formula 6.5 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 1.4e6  # N
        b_w = 300.0  # MM
        d = 500.0  # MM
        nu = 0.6  # DIMENSIONLESS
        f_cd = 30.0  # MPA

        # Object to test
        formula = Form6Dot5ShearForceCheck(v_ed=v_ed, b_w=b_w, d=d, nu=nu, f_cd=f_cd)

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("v_ed", "b_w", "d", "nu", "f_cd"),
        [
            (-100.0, 300.0, 500.0, 0.6, 30.0),  # v_ed is negative
            (100.0, -300.0, 500.0, 0.6, 30.0),  # b_w is negative
            (100.0, 300.0, -500.0, 0.6, 30.0),  # d is negative
            (100.0, 300.0, 500.0, -0.6, 30.0),  # nu is negative
            (100.0, 300.0, 500.0, 0.6, -30.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, b_w: float, d: float, nu: float, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot5ShearForceCheck(v_ed=v_ed, b_w=b_w, d=d, nu=nu, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to V_{Ed} \leq 0.5 \cdot b_w \cdot d \cdot \nu \cdot f_{cd} \to 1400000.000 \leq "
                r"0.5 \cdot 300.000 \cdot 500.000 \cdot 0.600 \cdot 30.000 \to \text{Not OK}",
            ),
            ("short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 1.4e6  # N
        b_w = 300.0  # MM
        d = 500.0  # MM
        nu = 0.6  # DIMENSIONLESS
        f_cd = 30.0  # MPA

        # Object to test
        latex = Form6Dot5ShearForceCheck(v_ed=v_ed, b_w=b_w, d=d, nu=nu, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
