"""Testing formula 6.65 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_65 import Form6Dot65ConcreteCompressionStrut
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot65ConcreteCompressionStrut:
    """Validation for formula 6.65 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        theta = 30.0

        # Object to test
        formula = Form6Dot65ConcreteCompressionStrut(theta=theta)

        # Expected result, manually calculated
        manually_calculated_result = 37.228865915079  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "theta",
        [
            -30.0,  # theta is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, theta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot65ConcreteCompressionStrut(theta=theta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\theta_{fat} = \tan^{-1}\left(\min\left(\sqrt{\tan(\theta)}, 1\right)\right)"
                r" = \tan^{-1}\left(\min\left(\sqrt{\tan(30.000)}, 1\right)\right) = 37.229 \ degrees",
            ),
            ("short", r"\theta_{fat} = 37.229 \ degrees"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta = 30.0

        # Object to test
        latex = Form6Dot65ConcreteCompressionStrut(theta=theta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
