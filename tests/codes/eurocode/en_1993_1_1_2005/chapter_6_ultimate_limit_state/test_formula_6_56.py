"""Testing formula 6.56 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_56 import (
    Form6Dot56LateralTorsionalIntermediateFactor,
    Form6Dot56NonDimensionalSlendernessLT,
    Form6Dot56ReductionFactorLateralTorsionalBuckling,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot56NonDimensionalSlendernessLT:
    """Validation for formula 6.56 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        w_y = 500000.0
        f_y = 355.0
        m_cr = 100000000.0

        # Object to test
        formula = Form6Dot56NonDimensionalSlendernessLT(w_y=w_y, f_y=f_y, m_cr=m_cr)

        # Expected result, manually calculated
        manually_calculated_result = 1.332291259  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("w_y", "f_y", "m_cr"),
        [
            (-500000.0, 355.0, 100000000.0),  # w_y is negative
            (500000.0, -355.0, 100000000.0),  # f_y is negative
            (500000.0, 355.0, 0.0),  # m_cr is zero
            (500000.0, 355.0, -100000000.0),  # m_cr is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, w_y: float, f_y: float, m_cr: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot56NonDimensionalSlendernessLT(w_y=w_y, f_y=f_y, m_cr=m_cr)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\overline{\lambda}_{LT} = \sqrt{\frac{W_y \cdot f_y}{M_{cr}}} = "
                r"\sqrt{\frac{500000.000 \cdot 355.000}{100000000.000}} = 1.332",
            ),
            (
                "complete_with_units",
                r"\overline{\lambda}_{LT} = \sqrt{\frac{W_y \cdot f_y}{M_{cr}}} = "
                r"\sqrt{\frac{500000.000 \ mm^3 \cdot 355.000 \ MPa}{100000000.000 \ Nmm}} = 1.332",
            ),
            ("short", r"\overline{\lambda}_{LT} = 1.332"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        w_y = 500000.0
        f_y = 355.0
        m_cr = 100000000.0

        # Object to test
        latex = Form6Dot56NonDimensionalSlendernessLT(w_y=w_y, f_y=f_y, m_cr=m_cr).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot56LateralTorsionalIntermediateFactor:
    """Validation for formula 6.56 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        alpha_lt = 0.34
        lambda_bar_lt = 0.8

        # Object to test
        formula = Form6Dot56LateralTorsionalIntermediateFactor(alpha_lt=alpha_lt, lambda_bar_lt=lambda_bar_lt)

        # Expected result, manually calculated
        manually_calculated_result = 0.922  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("alpha_lt", "lambda_bar_lt"),
        [
            (-0.34, 0.8),  # alpha_lt is negative
            (0.34, -0.8),  # lambda_bar_lt is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, alpha_lt: float, lambda_bar_lt: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot56LateralTorsionalIntermediateFactor(alpha_lt=alpha_lt, lambda_bar_lt=lambda_bar_lt)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Phi_{LT} = 0.5 \cdot \left[ 1 + \alpha_{LT} \cdot \left( \overline{\lambda}_{LT} - 0.2 \right) + "
                r"\overline{\lambda}_{LT}^2 \right] = "
                r"0.5 \cdot \left[ 1 + 0.340 \cdot \left( 0.800 - 0.2 \right) + 0.800^2 \right] = 0.922",
            ),
            (
                "complete_with_units",
                r"\Phi_{LT} = 0.5 \cdot \left[ 1 + \alpha_{LT} \cdot \left( \overline{\lambda}_{LT} - 0.2 \right) + "
                r"\overline{\lambda}_{LT}^2 \right] = 0.5 \cdot \left[ 1 + 0.340 \cdot \left( 0.800 - 0.2 \right) + "
                r"0.800^2 \right] = 0.922",
            ),
            ("short", r"\Phi_{LT} = 0.922"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        alpha_lt = 0.34
        lambda_bar_lt = 0.8

        # Object to test
        latex = Form6Dot56LateralTorsionalIntermediateFactor(alpha_lt=alpha_lt, lambda_bar_lt=lambda_bar_lt).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot56ReductionFactorLateralTorsionalBuckling:
    """Validation for formula 6.56 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        phi_lt = 0.922
        lambda_bar_lt = 0.8

        # Object to test
        formula = Form6Dot56ReductionFactorLateralTorsionalBuckling(phi_lt=phi_lt, lambda_bar_lt=lambda_bar_lt)

        # Expected result, manually calculated
        manually_calculated_result = 0.724518  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("phi_lt", "lambda_bar_lt"),
        [
            (0.0, 0.8),  # phi_lt is zero
            (-0.922, 0.8),  # phi_lt is negative
            (0.922, -0.8),  # lambda_bar_lt is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, phi_lt: float, lambda_bar_lt: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot56ReductionFactorLateralTorsionalBuckling(phi_lt=phi_lt, lambda_bar_lt=lambda_bar_lt)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\chi_{LT} = \frac{1}{\Phi_{LT} + \sqrt{\Phi_{LT}^2 - \overline{\lambda}_{LT}^2}} = "
                r"\frac{1}{0.922 + \sqrt{0.922^2 - 0.800^2}} = 0.724",
            ),
            (
                "complete_with_units",
                r"\chi_{LT} = \frac{1}{\Phi_{LT} + \sqrt{\Phi_{LT}^2 - \overline{\lambda}_{LT}^2}} = "
                r"\frac{1}{0.922 + \sqrt{0.922^2 - 0.800^2}} = 0.724",
            ),
            ("short", r"\chi_{LT} = 0.724"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        phi_lt = 0.922
        lambda_bar_lt = 0.8

        # Object to test
        latex = Form6Dot56ReductionFactorLateralTorsionalBuckling(phi_lt=phi_lt, lambda_bar_lt=lambda_bar_lt).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
