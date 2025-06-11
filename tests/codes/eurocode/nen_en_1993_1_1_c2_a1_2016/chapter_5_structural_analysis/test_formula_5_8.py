"""Testing formula 5.8 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_5_structural_analysis.formula_5_8 import Form5Dot8CheckSlenderness
from blueprints.validations import LessOrEqualToZeroError


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

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("lambda_bar", "a", "f_y", "n_ed"),
        [
            (-1.0, 1000.0, 355.0, 100000.0),  # lambda_bar is negative
            (1.0, -1000.0, 355.0, 100000.0),  # a is negative
            (1.0, 1000.0, -355.0, 100000.0),  # f_y is negative
            (1.0, 1000.0, 355.0, -100000.0),  # n_ed is negative
            (0.0, 1000.0, 355.0, 100000.0),  # lambda_bar is zero
            (1.0, 0.0, 355.0, 100000.0),  # a is zero
            (1.0, 1000.0, 0.0, 100000.0),  # f_y is zero
            (1.0, 1000.0, 355.0, 0.0),  # n_ed is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, lambda_bar: float, a: float, f_y: float, n_ed: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot8CheckSlenderness(lambda_bar, a, f_y, n_ed)

    def test_latex(self) -> None:
        """Test the latex representation of the formula."""
        # Example values
        lambda_bar = 1.0
        a = 1000.0
        f_y = 355.0
        n_ed = 100000.0

        # Object to test
        formula = Form5Dot8CheckSlenderness(lambda_bar=lambda_bar, a=a, f_y=f_y, n_ed=n_ed)
        latex = formula.latex()

        expected_equation = r"\left( \lambda_{bar} > 0.5 \sqrt{\frac{A \cdot f_{y}}{N_{Ed}}} \right)"
        expected_numeric_equation = r"\left( 1.00 > 0.5 \sqrt{\frac{1000.00 \cdot 355.00}{100000.00}} \right)"
        expected_result = "OK"

        assert latex.equation == expected_equation
        assert latex.numeric_equation == expected_numeric_equation
        assert latex.result == expected_result
