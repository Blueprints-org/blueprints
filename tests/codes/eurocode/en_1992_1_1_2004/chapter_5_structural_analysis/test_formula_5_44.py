"""Testing formula 5.44 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_44 import Form5Dot44PrestressLoss
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot44PrestressLoss:
    """Validation for formula 5.44 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_p = 1000.0  # mm^2
        e_p = 200000.0  # MPa
        j = [1, 2]  # dimensionless
        delta_sigma_c_t = [10.0, 20.0]  # MPa
        e_cm_t = [30000.0, 30000.0]  # MPa

        # Object to test
        formula = Form5Dot44PrestressLoss(a_p=a_p, e_p=e_p, j=j, delta_sigma_c_t=delta_sigma_c_t, e_cm_t=e_cm_t)

        # Expected result, manually calculated
        manually_calculated_result = 1e6 / 3.0  # N

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_p", "e_p", "j", "delta_sigma_c_t", "e_cm_t"),
        [
            (-1000.0, 200000.0, [1, 2], [10.0, 20.0], [30000.0, 30000.0]),  # a_p is negative
            (1000.0, -200000.0, [1, 2], [10.0, 20.0], [30000.0, 30000.0]),  # e_p is negative
            (1000.0, 200000.0, [-1, 2], [10.0, 20.0], [30000.0, 30000.0]),  # j contains negative value
            (1000.0, 200000.0, [1, 2], [-10.0, 20.0], [30000.0, 30000.0]),  # delta_sigma_c_t contains negative value
            (1000.0, 200000.0, [1, 2], [10.0, 20.0], [-30000.0, 30000.0]),  # e_cm_t contains negative value
            (1000.0, 200000.0, [1, 2], [10.0, 20.0], [0.0, 30000.0]),  # e_cm_t contains zero value
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_p: float, e_p: float, j: list, delta_sigma_c_t: list, e_cm_t: list) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot44PrestressLoss(a_p=a_p, e_p=e_p, j=j, delta_sigma_c_t=delta_sigma_c_t, e_cm_t=e_cm_t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta P_{el} = A_{p} \cdot E_{p} \cdot \sum_{i=1}^{n} \frac{j_{i} \cdot \Delta \sigma_{c,i}(t)}{E_{cm,i}(t)} = "
                r"1000.000 \cdot 200000.000 \cdot \left( \frac{1 \cdot 10.000}{30000.000} + \frac{2 \cdot 20.000}{30000.000} \right) = "
                r"333333.333 \ N",
            ),
            ("short", r"\Delta P_{el} = 333333.333 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_p = 1000.0  # mm^2
        e_p = 200000.0  # MPa
        j = [1, 2]  # dimensionless
        delta_sigma_c_t = [10.0, 20.0]  # MPa
        e_cm_t = [30000.0, 30000.0]  # MPa

        # Object to test
        latex = Form5Dot44PrestressLoss(a_p=a_p, e_p=e_p, j=j, delta_sigma_c_t=delta_sigma_c_t, e_cm_t=e_cm_t).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
