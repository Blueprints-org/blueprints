"""Testing formula 5.43 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_43 import Form5Dot43InitialPrestressForce
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot43InitialPrestressForce:
    """Validation for formula 5.43 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_p = 1000.0  # mm^2
        k_7 = 0.75  # -
        f_pk = 1860.0  # MPa
        k_8 = 0.85  # -
        f_p0_1k = 1674.0  # MPa

        # Object to test
        formula = Form5Dot43InitialPrestressForce(a_p=a_p, k_7=k_7, f_pk=f_pk, k_8=k_8, f_p0_1k=f_p0_1k)

        # Expected result, manually calculated
        manually_calculated_result = 1395000.0  # N

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_p", "k_7", "f_pk", "k_8", "f_p0_1k"),
        [
            (-1000.0, 0.75, 1860.0, 0.85, 1674.0),  # a_p is negative
            (1000.0, -0.75, 1860.0, 0.85, 1674.0),  # k_7 is negative
            (1000.0, 0.75, -1860.0, 0.85, 1674.0),  # f_pk is negative
            (1000.0, 0.75, 1860.0, -0.85, 1674.0),  # k_8 is negative
            (1000.0, 0.75, 1860.0, 0.85, -1674.0),  # f_p0_1k is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_p: float, k_7: float, f_pk: float, k_8: float, f_p0_1k: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot43InitialPrestressForce(a_p=a_p, k_7=k_7, f_pk=f_pk, k_8=k_8, f_p0_1k=f_p0_1k)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"P_{m0}(x) = A_{p} \cdot \min \left(k_7 \cdot f_{pk} ; k_8 \cdot f_{p0.1k} \right) = "
                r"1000.000 \cdot \min \left(0.750 \cdot 1860.000 ; 0.850 \cdot 1674.000 \right) = 1395000.000 N",
            ),
            ("short", r"P_{m0}(x) = 1395000.000 N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_p = 1000.0  # mm^2
        k_7 = 0.75  # -
        f_pk = 1860.0  # MPa
        k_8 = 0.85  # -
        f_p0_1k = 1674.0  # MPa

        # Object to test
        latex = Form5Dot43InitialPrestressForce(a_p=a_p, k_7=k_7, f_pk=f_pk, k_8=k_8, f_p0_1k=f_p0_1k).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
