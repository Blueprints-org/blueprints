"""Testing formula 6.55 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_55 import Form6Dot55DesignStrengthConcreteStruts
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot55DesignStrengthConcreteStruts:
    """Validation for formula 6.55 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_cd = 30.0  # MPa

        # Object to test
        formula = Form6Dot55DesignStrengthConcreteStruts(f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 30.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "f_cd",
        [
            -30.0,  # f_cd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot55DesignStrengthConcreteStruts(f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{Rd,max} = f_{cd} = 30.000 = 30.000 \ MPa",
            ),
            ("short", r"\sigma_{Rd,max} = 30.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cd = 30.0  # MPa

        # Object to test
        latex = Form6Dot55DesignStrengthConcreteStruts(f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
