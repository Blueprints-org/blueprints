"""Testing formula 5.41 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_41 import Form5Dot41MaxForceTendon
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot41MaxForceTendon:
    """Validation for formula 5.41 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_p = 1000.0  # mm^2
        k_1 = 0.8  # -
        f_pk = 1860.0  # MPa
        k_2 = 0.9  # -
        f_p0_1k = 1674.0  # MPa

        # Object to test
        formula = Form5Dot41MaxForceTendon(a_p=a_p, k_1=k_1, f_pk=f_pk, k_2=k_2, f_p0_1k=f_p0_1k)

        # Expected result, manually calculated
        manually_calculated_result = 1488000.0  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_p", "k_1", "f_pk", "k_2", "f_p0_1k"),
        [
            (-1000.0, 0.8, 1860.0, 0.9, 1674.0),  # a_p is negative
            (1000.0, -0.8, 1860.0, 0.9, 1674.0),  # k_1 is negative
            (1000.0, 0.8, -1860.0, 0.9, 1674.0),  # f_pk is negative
            (1000.0, 0.8, 1860.0, -0.9, 1674.0),  # k_2 is negative
            (1000.0, 0.8, 1860.0, 0.9, -1674.0),  # f_p0_1k is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_p: float, k_1: float, f_pk: float, k_2: float, f_p0_1k: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot41MaxForceTendon(a_p=a_p, k_1=k_1, f_pk=f_pk, k_2=k_2, f_p0_1k=f_p0_1k)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"P_{max} = A_{p} \cdot \min(k_1 \cdot f_{pk}, k_2 \cdot f_{p0.1k}) = "
                r"1000.000 \cdot \min(0.800 \cdot 1860.000, 0.900 \cdot 1674.000) = 1488000.000 \ N",
            ),
            ("short", r"P_{max} = 1488000.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_p = 1000.0  # mm^2
        k_1 = 0.8  # -
        f_pk = 1860.0  # MPa
        k_2 = 0.9  # -
        f_p0_1k = 1674.0  # MPa

        # Object to test
        latex = Form5Dot41MaxForceTendon(a_p=a_p, k_1=k_1, f_pk=f_pk, k_2=k_2, f_p0_1k=f_p0_1k).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
