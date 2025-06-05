"""Testing formula 5.22 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_22 import Form5Dot22FactorKc, Form5Dot22FactorKs
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot22FactorKs:
    """Validation for formula 5.22 (Ks) from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        rho = 0.003  # -

        # Object to test
        form_5_22_ks = Form5Dot22FactorKs(rho=rho)

        # Expected result, manually calculated
        manually_calculated_result = 1.0  # -

        assert form_5_22_ks == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_rho_is_less_than_0_002(self) -> None:
        """Test a value of rho less than 0.002."""
        # Example values
        rho = 0.001

        with pytest.raises(ValueError):
            Form5Dot22FactorKs(rho=rho)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"K_s = 1 = 1 = 1.000"),
            ("short", "K_s = 1.000"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        rho = 0.003  # -

        # Object to test
        form_5_22_ks_latex = Form5Dot22FactorKs(rho=rho).latex()

        actual = {
            "complete": form_5_22_ks_latex.complete,
            "short": form_5_22_ks_latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."


class TestForm5Dot22FactorKc:
    """Validation for formula 5.22 (Kc) from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        k1 = 0.8  # -
        k2 = 0.9  # -
        phi_ef = 2.0  # -
        rho = 0.003  # -

        # Object to test
        form_5_22_kc = Form5Dot22FactorKc(k1=k1, k2=k2, phi_ef=phi_ef, rho=rho)

        # Expected result, manually calculated
        manually_calculated_result = 0.24  # -

        assert form_5_22_kc == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_rho_is_less_than_0_002(self) -> None:
        """Test a value of rho less than 0.002."""
        # Example values
        rho = 0.001
        k1 = 0.8
        k2 = 0.9
        phi_ef = 2.0

        with pytest.raises(ValueError):
            Form5Dot22FactorKc(k1=k1, k2=k2, phi_ef=phi_ef, rho=rho)

    def test_raise_error_when_phi_ef_is_less_or_equal_to_zero(self) -> None:
        """Test a value of phi_ef less or equal to zero."""
        # Example values
        rho = 0.003
        k1 = 0.8
        k2 = 0.9
        phi_ef = 0.0

        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot22FactorKc(k1=k1, k2=k2, phi_ef=phi_ef, rho=rho)

    def test_raise_error_when_k1_is_negative(self) -> None:
        """Test a negative value for k1."""
        # Example values
        rho = 0.003
        k1 = -0.8
        k2 = 0.9
        phi_ef = 2.0

        with pytest.raises(NegativeValueError):
            Form5Dot22FactorKc(k1=k1, k2=k2, phi_ef=phi_ef, rho=rho)

    def test_raise_error_when_k2_is_negative(self) -> None:
        """Test a negative value for k2."""
        # Example values
        rho = 0.003
        k1 = 0.8
        k2 = -0.9
        phi_ef = 2.0

        with pytest.raises(NegativeValueError):
            Form5Dot22FactorKc(k1=k1, k2=k2, phi_ef=phi_ef, rho=rho)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"K_c = \frac{k_1 \cdot k_2}{1 + \phi_{ef}} = \frac{0.800 \cdot 0.900}{1 + 2.000} = 0.240"),
            ("short", r"K_c = 0.240"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k1 = 0.8  # -
        k2 = 0.9  # -
        phi_ef = 2.0  # -
        rho = 0.003  # -

        # Object to test
        form_5_22_kc_latex = Form5Dot22FactorKc(k1=k1, k2=k2, phi_ef=phi_ef, rho=rho).latex()

        actual = {
            "complete": form_5_22_kc_latex.complete,
            "short": form_5_22_kc_latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
