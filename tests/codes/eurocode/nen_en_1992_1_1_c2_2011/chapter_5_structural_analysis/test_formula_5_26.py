"""Testing formula 5.26 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_26 import Form5Dot26FactorKc, Form5Dot26FactorKs
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot26FactorKs:
    """Validation for formula 5.26 (Factor Ks) from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        rho = 0.02  # -

        # Object to test
        form_5_26_ks = Form5Dot26FactorKs(rho=rho)

        # Expected result, manually calculated
        manually_calculated_result = 0.0

        assert form_5_26_ks == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_rho_is_less_than_0_01(self) -> None:
        """Test a value for rho less than 0.01."""
        # Example values
        rho = 0.009

        with pytest.raises(ValueError):
            Form5Dot26FactorKs(rho=rho)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"K_s = 0 = 0 = 0.000"),
            ("short", "K_s = 0.000"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        rho = 0.02  # -

        # Object to test
        form_5_26_ks_latex = Form5Dot26FactorKs(rho=rho).latex()

        actual = {
            "complete": form_5_26_ks_latex.complete,
            "short": form_5_26_ks_latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."


class TestForm5Dot26FactorKc:
    """Validation for formula 5.26 (Factor Kc) from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_ef = 2.0  # -
        rho = 0.02  # -

        # Object to test
        form_5_26_kc = Form5Dot26FactorKc(phi_ef=phi_ef, rho=rho)

        # Expected result, manually calculated
        manually_calculated_result = 0.15

        assert form_5_26_kc == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_rho_is_less_or_equal_to_0_01(self) -> None:
        """Test a value for rho less than or equal to 0.01."""
        # Example values
        phi_ef = 2.0
        rho = 0.01

        with pytest.raises(ValueError):
            Form5Dot26FactorKc(phi_ef=phi_ef, rho=rho)

    def test_raise_error_when_phi_ef_is_less_or_equal_to_zero(self) -> None:
        """Test a value for phi_ef less than or equal to zero."""
        # Example values
        phi_ef = 0.0
        rho = 0.02

        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot26FactorKc(phi_ef=phi_ef, rho=rho)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"K_c = \frac{0.3}{1 + 0.5 \cdot \phi_{ef}} = \frac{0.3}{1 + 0.5 \cdot 2.000} = 0.150"),
            ("short", "K_c = 0.150"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        phi_ef = 2.0  # -
        rho = 0.02  # -

        # Object to test
        form_5_26_kc_latex = Form5Dot26FactorKc(phi_ef=phi_ef, rho=rho).latex()

        actual = {
            "complete": form_5_26_kc_latex.complete,
            "short": form_5_26_kc_latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
