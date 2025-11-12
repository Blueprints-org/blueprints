"""Testing formula 5.8 of EN 1993-1-1:2005."""

import numpy as np
import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_5_structural_analysis.formula_5_8 import Form5Dot8CheckSlenderness
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot8CheckSlenderness:
    """Validation for formula 5.8 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        lambda_bar = 1.0
        a = 1000.0
        f_y = 355.0
        n_ed = 100000.0

        # Object to test
        formula = Form5Dot8CheckSlenderness(lambda_bar=lambda_bar, a=a, f_y=f_y, n_ed=n_ed)

        # Expected result, manually calculated
        expected_result = True
        expected_unity_check = lambda_bar / (0.5 * np.sqrt(a * f_y / n_ed))

        assert formula == expected_result
        assert formula.unity_check == expected_unity_check

    @pytest.mark.parametrize(
        ("lambda_bar", "a", "f_y", "n_ed"),
        [
            (1.0, 1000.0, 355.0, -100000.0),  # n_ed is negative
            (1.0, 1000.0, 355.0, 0.0),  # n_ed is zero
        ],
    )
    def test_raise_error_when_invalid_values_less_or_equal_to_zero(self, lambda_bar: float, a: float, f_y: float, n_ed: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot8CheckSlenderness(
                lambda_bar=lambda_bar,
                a=a,
                f_y=f_y,
                n_ed=n_ed,
            )

    @pytest.mark.parametrize(
        ("lambda_bar", "a", "f_y", "n_ed"),
        [
            (-1.0, 1000.0, 355.0, 100000.0),  # lambda_bar is negative
            (1.0, -1000.0, 355.0, 100000.0),  # a is negative
            (1.0, 1000.0, -355.0, 100000.0),  # f_y is negative
        ],
    )
    def test_raise_error_when_negative(self, lambda_bar: float, a: float, f_y: float, n_ed: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form5Dot8CheckSlenderness(
                lambda_bar=lambda_bar,
                a=a,
                f_y=f_y,
                n_ed=n_ed,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \overline{\lambda} > 0.5 \sqrt{\frac{A \cdot f_{y}}{N_{Ed}}} "
                r"\right) \to \left( \overline{1.00} > 0.5 \sqrt{\frac{1000.00 \cdot 355.00}{100000.00}} \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        lambda_bar = 1.0
        a = 1000.0
        f_y = 355.0
        n_ed = 100000.0

        # Object to test
        latex = Form5Dot8CheckSlenderness(
            lambda_bar=lambda_bar,
            a=a,
            f_y=f_y,
            n_ed=n_ed,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
