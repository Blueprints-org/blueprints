"""Testing formula 5.34 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_34 import Form5Dot34Curvature
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot34Curvature:
    """Validation for formula 5.34 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        k_r = 0.8
        k_phi = 1.2
        f_yd = 500.0
        e_s = 200000.0
        d = 300.0

        # Object to test
        formula = Form5Dot34Curvature(k_r=k_r, k_phi=k_phi, f_yd=f_yd, e_s=e_s, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 0.0000177777777777777777  # 1/mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    @pytest.mark.parametrize(
        ("k_r", "k_phi", "f_yd", "e_s", "d"),
        [
            (-0.8, 1.2, 500.0, 200000.0, 300.0),  # k_r is negative
            (0.8, -1.2, 500.0, 200000.0, 300.0),  # k_phi is negative
            (0.8, 1.2, -500.0, 200000.0, 300.0),  # f_yd is negative
            (0.8, 1.2, 500.0, -200000.0, 300.0),  # e_s is negative
            (0.8, 1.2, 500.0, 200000.0, -300.0),  # d is negative
            (0.8, 1.2, 0.0, 200000.0, 300.0),  # f_yd is zero
            (0.8, 1.2, 500.0, 0.0, 300.0),  # e_s is zero
            (0.8, 1.2, 500.0, 200000.0, 0.0),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, k_r: float, k_phi: float, f_yd: float, e_s: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot34Curvature(k_r=k_r, k_phi=k_phi, f_yd=f_yd, e_s=e_s, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\frac{1}{r} = K_r \cdot K_\phi \cdot \frac{f_{yd}}{E_s \cdot 0.45 \cdot d} "
                r"= 0.800 \cdot 1.200 \cdot \frac{500.000}{200000.000 \cdot 0.45 \cdot 300.000} = 0.000018 \ 1/mm",
            ),
            ("short", r"\frac{1}{r} = 0.000018 \ 1/mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_r = 0.8
        k_phi = 1.2
        f_yd = 500.0
        e_s = 200000.0
        d = 300.0

        # Object to test
        latex = Form5Dot34Curvature(k_r=k_r, k_phi=k_phi, f_yd=f_yd, e_s=e_s, d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
