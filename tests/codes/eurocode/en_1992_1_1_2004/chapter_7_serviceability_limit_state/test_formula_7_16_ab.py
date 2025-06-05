"""Testing formula 7.16.a and 7.16.b of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_16_ab import (
    Form7Dot16abSpanDepthRatio,
    Form7Dot16ReferenceReinforcementRatio,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot16abSpanDepthRatio:
    """Validation for formula 7.16a/b from EN 1992-1-1:2004."""

    def test_evaluation_rho_less_than_rho_0(self) -> None:
        """Tests the evaluation of the result when rho <= rho_0."""
        # Example values
        capital_k = 1.0
        f_ck = 30.0
        rho = 0.001
        rho_0 = 0.002
        rho_prime = 0.0005

        # Object to test
        formula = Form7Dot16abSpanDepthRatio(capital_k=capital_k, f_ck=f_ck, rho=rho, rho_0=rho_0, rho_prime=rho_prime)

        # Expected result, manually calculated
        manually_calculated_result = 44.9587985653203

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_rho_greater_than_rho_0(self) -> None:
        """Tests the evaluation of the result when rho > rho_0."""
        # Example values
        capital_k = 1.0
        f_ck = 30.0
        rho = 0.003
        rho_0 = 0.002
        rho_prime = 0.0005

        # Object to test
        formula = Form7Dot16abSpanDepthRatio(capital_k=capital_k, f_ck=f_ck, rho=rho, rho_0=rho_0, rho_prime=rho_prime)

        # Expected result, manually calculated
        manually_calculated_result = 17.80088842235581

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("capital_k", "f_ck", "rho", "rho_0", "rho_prime"),
        [
            (-1.0, 30.0, 0.001, 0.002, 0.0),  # capital_k is negative
            (1.0, -30.0, 0.001, 0.002, 0.0),  # f_ck is negative
            (1.0, 30.0, -0.001, 0.002, 0.0),  # rho is negative
            (1.0, 30.0, 0.001, -0.002, 0.0),  # rho_0 is negative
            (1.0, 30.0, 0.001, 0.002, -0.001),  # rho_prime is negative
            (1.0, 30.0, 0.0, 0.002, 0.0),  # rho is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, capital_k: float, f_ck: float, rho: float, rho_0: float, rho_prime: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot16abSpanDepthRatio(capital_k=capital_k, f_ck=f_ck, rho=rho, rho_0=rho_0, rho_prime=rho_prime)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\frac{l}{d} = \begin{cases} K \cdot \left[11 + 1.5 \cdot \sqrt{f_{ck}} \cdot "
                r"\frac{\rho_0}{\rho} + 3.2 \cdot \sqrt{f_{ck}} \cdot \left(\frac{\rho_0}{\rho} - 1\right)^{3/2}\right] & "
                r"\text{if } \rho \leq \rho_0 \\ K \cdot \left[11 + 1.5 \cdot \sqrt{f_{ck}} \cdot "
                r"\frac{\rho_0}{\rho - \rho'} + \frac{1}{12} \cdot \sqrt{f_{ck}} \cdot \sqrt{\frac{\rho'}"
                r"{\rho_0}}\right] & \text{if } \rho > \rho_0 \end{cases} = "
                r"\begin{cases} 1.000 \cdot \left[11 + 1.5 \cdot \sqrt{30.000} \cdot \frac{0.0020}{0.0010} + "
                r"3.2 \cdot \sqrt{30.000} \cdot \left(\frac{0.0020}{0.0010} - 1\right)^{3/2}\right] & "
                r"\text{if } 0.0010 \leq 0.0020 \\ 1.000 \cdot \left[11 + 1.5 \cdot \sqrt{30.000} "
                r"\cdot \frac{0.0020}{0.0010 - 0.0005} + \frac{1}{12} \cdot \sqrt{30.000} \cdot "
                r"\sqrt{\frac{0.0005}{0.0020}}\right] & \text{if } 0.0010 > 0.0020 \end{cases} = 44.959 \ -",
            ),
            ("short", r"\frac{l}{d} = 44.959 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        capital_k = 1.0
        f_ck = 30.0
        rho = 0.0010
        rho_0 = 0.0020
        rho_prime = 0.0005

        # Object to test
        latex = Form7Dot16abSpanDepthRatio(capital_k=capital_k, f_ck=f_ck, rho=rho, rho_0=rho_0, rho_prime=rho_prime).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm7Dot16ReferenceReinforcementRatio:
    """Validation for reference reinforcement ratio calculation from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        f_ck = 30.0

        formula = Form7Dot16ReferenceReinforcementRatio(f_ck=f_ck)
        manually_calculated_result = 0.00547722557  # Example manually calculated result

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "f_ck",
        [
            -30.0,  # f_ck is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_ck: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form7Dot16ReferenceReinforcementRatio(f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_0 = \sqrt{f_{ck}} \cdot 10^{-3}"
                r" = \sqrt{30.000} \cdot 10^{-3} = 0.005477 \ -",
            ),
            ("short", r"\rho_0 = 0.005477 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        f_ck = 30.0

        latex = Form7Dot16ReferenceReinforcementRatio(f_ck=f_ck).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
