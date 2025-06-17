"""Testing formula 7.11 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_11 import Form7Dot11MaximumCrackSpacing
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot11MaximumCrackSpacing:
    """Validation for formula 7.11 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        k_3 = 0.8
        c = 30.0
        k_1 = 0.5
        k_2 = 1.0
        k_4 = 0.6
        diam = 16.0
        rho_p_eff = 0.02

        # Object to test
        formula = Form7Dot11MaximumCrackSpacing(k_3=k_3, c=c, k_1=k_1, k_2=k_2, k_4=k_4, diam=diam, rho_p_eff=rho_p_eff)

        # Expected result, manually calculated
        manually_calculated_result = 264.000  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k_3", "c", "k_1", "k_2", "k_4", "diam", "rho_p_eff"),
        [
            (-0.8, 30.0, 0.5, 1.0, 0.6, 16.0, 0.02),  # k_3 is negative
            (0.8, -30.0, 0.5, 1.0, 0.6, 16.0, 0.02),  # c is negative
            (0.8, 30.0, -0.5, 1.0, 0.6, 16.0, 0.02),  # k_1 is negative
            (0.8, 30.0, 0.5, -1.0, 0.6, 16.0, 0.02),  # k_2 is negative
            (0.8, 30.0, 0.5, 1.0, -0.6, 16.0, 0.02),  # k_4 is negative
            (0.8, 30.0, 0.5, 1.0, 0.6, -16.0, 0.02),  # diam is negative
            (0.8, 30.0, 0.5, 1.0, 0.6, 16.0, 0.0),  # rho_p_eff is zero
            (0.8, 30.0, 0.5, 1.0, 0.6, 16.0, -0.02),  # rho_p_eff is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, k_3: float, c: float, k_1: float, k_2: float, k_4: float, diam: float, rho_p_eff: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot11MaximumCrackSpacing(k_3=k_3, c=c, k_1=k_1, k_2=k_2, k_4=k_4, diam=diam, rho_p_eff=rho_p_eff)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"s_{r,max} = k_3 \cdot c + k_1 \cdot k_2 \cdot k_4 \cdot \frac{⌀}{\rho_{p,eff}} = "
                r"0.800 \cdot 30.000 + 0.500 \cdot 1.000 \cdot 0.600 \cdot \frac{16.000}{0.020} = 264.000 \ mm",
            ),
            ("short", r"s_{r,max} = 264.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_3 = 0.8
        c = 30.0
        k_1 = 0.5
        k_2 = 1.0
        k_4 = 0.6
        diam = 16.0
        rho_p_eff = 0.02

        # Object to test
        latex = Form7Dot11MaximumCrackSpacing(k_3=k_3, c=c, k_1=k_1, k_2=k_2, k_4=k_4, diam=diam, rho_p_eff=rho_p_eff).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
