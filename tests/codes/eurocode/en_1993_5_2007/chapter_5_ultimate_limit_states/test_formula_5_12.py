"""Testing formula 5.12 of EN 1993-5:2007."""

import pytest

from blueprints.codes.eurocode.en_1993_5_2007.chapter_5_ultimate_limit_states.formula_5_12 import Form5Dot12ElasticCriticalLoad
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot12ElasticCriticalLoad:
    """Validation for formula 5.12 from EN 1993-5:2007."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        e = 210000  # MPA
        i = 5000  # MM4
        beta_d = 1.0  # DIMENSIONLESS
        l = 1000  # MM  # noqa: E741

        # Object to test
        formula = Form5Dot12ElasticCriticalLoad(e=e, i=i, beta_d=beta_d, l=l)

        # Expected result, manually calculated
        manually_calculated_result = 10363.1  # N

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("e", "i", "beta_d", "l"),
        [
            (-210000, 5000, 1.0, 1000),  # e is negative
            (210000, -5000, 1.0, 1000),  # i is negative
            (210000, 5000, -1.0, 1000),  # beta_d is negative
            (210000, 5000, 1.0, -1000),  # l is negative
            (210000, 5000, 1.0, 0),  # l is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, e: float, i: float, beta_d: float, l: float) -> None:  # noqa: E741
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot12ElasticCriticalLoad(e=e, i=i, beta_d=beta_d, l=l)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"N_{cr} = \frac{E \cdot I \cdot \beta_D \cdot \pi^2}{l^2} = "
                r"\frac{210000.000 \cdot 5000.000 \cdot 1.000 \cdot \pi^2}{1000.000^2} = 10363.085 \ N",
            ),
            ("short", r"N_{cr} = 10363.085 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        e = 210000  # MPA
        i = 5000  # MM4
        beta_d = 1.0  # DIMENSIONLESS
        l = 1000  # MM  # noqa: E741

        # Object to test
        latex = Form5Dot12ElasticCriticalLoad(e=e, i=i, beta_d=beta_d, l=l).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
