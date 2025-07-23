"""Testing formula 5.42 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_42 import Form5Dot42ConcreteCompressiveStress
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot42ConcreteCompressiveStress:
    """Validation for formula 5.42 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sigma_c = 10.0  # MPa
        f_ck_t = 30.0  # MPa

        # Object to test
        formula = Form5Dot42ConcreteCompressiveStress(sigma_c=sigma_c, f_ck_t=f_ck_t)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("sigma_c", "f_ck_t"),
        [
            (-10.0, 30.0),  # sigma_c is negative
            (10.0, -30.0),  # f_ck_t is negative
            (0.0, 30.0),  # sigma_c is zero
            (10.0, 0.0),  # f_ck_t is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, sigma_c: float, f_ck_t: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot42ConcreteCompressiveStress(sigma_c=sigma_c, f_ck_t=f_ck_t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \sigma_{c} \leq 0.6 \cdot f_{ck}(t) \to 10.000 \leq 0.6 \cdot 30.000 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_c = 10.0  # MPa
        f_ck_t = 30.0  # MPa

        # Object to test
        latex = Form5Dot42ConcreteCompressiveStress(sigma_c=sigma_c, f_ck_t=f_ck_t).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
