"""Testing formula 7.4 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_4 import Form7Dot4MeanStressConcrete
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot4MeanStressConcrete:
    """Validation for formula 7.4 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 1000.0  # N
        b = 200.0  # mm
        h = 300.0  # mm

        # Object to test
        formula = Form7Dot4MeanStressConcrete(n_ed=n_ed, b=b, h=h)

        # Expected result, manually calculated
        manually_calculated_result = 1000 / 200 / 300  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed", "b", "h"),
        [
            (-1000.0, 200.0, 300.0),  # n_ed is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given_negative(self, n_ed: float, b: float, h: float) -> None:
        """Test invalid values for negative n_ed."""
        with pytest.raises(NegativeValueError):
            Form7Dot4MeanStressConcrete(n_ed=n_ed, b=b, h=h)

    @pytest.mark.parametrize(
        ("n_ed", "b", "h"),
        [
            (1000.0, 0.0, 300.0),  # b is zero
            (1000.0, 200.0, 0.0),  # h is zero
            (1000.0, -200.0, 300.0),  # b is negative
            (1000.0, 200.0, -300.0),  # h is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given_zero_or_negative(self, n_ed: float, b: float, h: float) -> None:
        """Test invalid values for zero or negative b and h."""
        with pytest.raises(LessOrEqualToZeroError):
            Form7Dot4MeanStressConcrete(n_ed=n_ed, b=b, h=h)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_c = \frac{N_{Ed}}{b \cdot h} = \frac{1000.000}{200.000 \cdot 300.000} = 0.017 \ MPa",
            ),
            ("short", r"\sigma_c = 0.017 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 1000.0
        b = 200.0
        h = 300.0

        # Object to test
        latex = Form7Dot4MeanStressConcrete(n_ed=n_ed, b=b, h=h).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
