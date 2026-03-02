"""Testing formula 8.27 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_27 import Form8Dot27CheckShearBucklingResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot27CheckShearBucklingResistance:
    """Validation for formula 8.27 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        h_w = 500.0
        t_w = 5.0
        epsilon = 1.0
        eta = 1.0

        # Object to test
        formula = Form8Dot27CheckShearBucklingResistance(h_w=h_w, t_w=t_w, epsilon=epsilon, eta=eta)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("h_w", "t_w", "epsilon", "eta"),
        [
            (-500.0, 5.0, 1.0, 1.0),  # h_w is negative
            (500.0, 5.0, -1.0, 1.0),  # epsilon is negative
            (500.0, -5.0, 1.0, 1.0),  # t_w is negative
            (500.0, 5.0, 1.0, -1.0),  # eta is negative
            (500.0, 5.0, 1.0, 0.0),  # eta is less than or equal to zero
            (500.0, 0.0, 1.0, 1.0),  # t_w is less than or equal to zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, h_w: float, t_w: float, epsilon: float, eta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot27CheckShearBucklingResistance(h_w=h_w, t_w=t_w, epsilon=epsilon, eta=eta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{h_w}{t_w} > 72 \cdot \frac{\epsilon}{\eta} \right) \to "
                r"\left( \frac{500.000}{5.000} > 72 \cdot \frac{1.000}{1.000} \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        h_w = 500.0
        t_w = 5.0
        epsilon = 1.0
        eta = 1.0

        # Object to test
        latex = Form8Dot27CheckShearBucklingResistance(h_w=h_w, t_w=t_w, epsilon=epsilon, eta=eta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
