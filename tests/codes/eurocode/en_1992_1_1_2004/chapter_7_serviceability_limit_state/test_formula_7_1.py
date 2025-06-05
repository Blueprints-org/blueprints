"""Testing formula 7.1 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_1 import Form7Dot1MinReinforcingSteel
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot1MinReinforcingSteel:
    """Validation for formula 7.1 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        k_c = 1.0
        k = 0.65
        f_ct_eff = 2.9
        a_ct = 1000.0
        sigma_s = 435.0

        # Object to test
        formula = Form7Dot1MinReinforcingSteel(k_c=k_c, k=k, f_ct_eff=f_ct_eff, a_ct=a_ct, sigma_s=sigma_s)

        # Expected result, manually calculated
        manually_calculated_result = 4.333  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k_c", "k", "f_ct_eff", "a_ct", "sigma_s"),
        [
            (-1.0, 0.65, 2.9, 1000.0, 435.0),  # k_c is negative
            (1.0, -0.65, 2.9, 1000.0, 435.0),  # k is negative
            (1.0, 0.65, -2.9, 1000.0, 435.0),  # f_ct_eff is negative
            (1.0, 0.65, 2.9, -1000.0, 435.0),  # a_ct is negative
            (1.0, 0.65, 2.9, 1000.0, -435.0),  # sigma_s is negative
            (1.0, 0.65, 2.9, 1000.0, 0.0),  # sigma_s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, k_c: float, k: float, f_ct_eff: float, a_ct: float, sigma_s: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot1MinReinforcingSteel(k_c=k_c, k=k, f_ct_eff=f_ct_eff, a_ct=a_ct, sigma_s=sigma_s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_{s,min} = \frac{k_c \cdot k \cdot f_{ct,eff} \cdot A_{ct}}{\sigma_s} = "
                r"\frac{1.000 \cdot 0.650 \cdot 2.900 \cdot 1000.000}{435.000} = 4.333 \ mm^2",
            ),
            ("short", r"A_{s,min} = 4.333 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_c = 1.0
        k = 0.65
        f_ct_eff = 2.9
        a_ct = 1000.0
        sigma_s = 435.0

        # Object to test
        latex = Form7Dot1MinReinforcingSteel(k_c=k_c, k=k, f_ct_eff=f_ct_eff, a_ct=a_ct, sigma_s=sigma_s).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
