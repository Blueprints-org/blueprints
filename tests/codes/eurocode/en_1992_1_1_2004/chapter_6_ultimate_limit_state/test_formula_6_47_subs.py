"""Testing formula 6.47 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_47_subs import (
    SubForm6Dot47FactorK,
    SubForm6Dot47FactorRhoL,
    SubForm6Dot47FactorSigmaCp,
    SubForm6Dot47FactorSigmaCy,
    SubForm6Dot47FactorSigmaCz,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestSubForm6Dot47FactorK:
    """Validation for sub-formula 1 of formula 6.47 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d = 500.0

        # Object to test
        formula = SubForm6Dot47FactorK(d=d)

        # Expected result, manually calculated
        manually_calculated_result = 1.632455532033676  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d"),
        [
            (-500.0),  # d is negative
            (0.0),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            SubForm6Dot47FactorK(d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k = \min \left( 1 + \sqrt{\frac{200}{d}}, 2.0 \right) = "
                r"\min \left( 1 + \sqrt{\frac{200}{500.000}}, 2.0 \right) = 1.632 \ -",
            ),
            ("short", r"k = 1.632 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d = 500.0

        # Object to test
        latex = SubForm6Dot47FactorK(d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestSubForm6Dot47FactorRhoL:
    """Validation for sub-formula 2 of formula 6.47 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        rho_ly = 0.02
        rho_lz = 0.03

        # Object to test
        formula = SubForm6Dot47FactorRhoL(rho_ly=rho_ly, rho_lz=rho_lz)

        # Expected result, manually calculated
        manually_calculated_result = 0.02  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("rho_ly", "rho_lz"),
        [
            (-0.02, 0.03),  # rho_ly is negative
            (0.02, -0.03),  # rho_lz is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, rho_ly: float, rho_lz: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            SubForm6Dot47FactorRhoL(rho_ly=rho_ly, rho_lz=rho_lz)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_l = \min \left( \sqrt{\rho_{ly} \cdot \rho_{lz}}, 0.02 \right) = "
                r"\min \left( \sqrt{0.020 \cdot 0.030}, 0.02 \right) = 0.020 \ -",
            ),
            ("short", r"\rho_l = 0.020 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        rho_ly = 0.02
        rho_lz = 0.03

        # Object to test
        latex = SubForm6Dot47FactorRhoL(rho_ly=rho_ly, rho_lz=rho_lz).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestSubForm6Dot47FactorSigmaCp:
    """Validation for sub-formula 3 of formula 6.47 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sigma_cy = 1.0
        sigma_cz = 2.0

        # Object to test
        formula = SubForm6Dot47FactorSigmaCp(sigma_cy=sigma_cy, sigma_cz=sigma_cz)

        # Expected result, manually calculated
        manually_calculated_result = 1.5  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("sigma_cy", "sigma_cz"),
        [
            (-1.0, 2.0),  # sigma_cy is negative
            (1.0, -2.0),  # sigma_cz is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, sigma_cy: float, sigma_cz: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            SubForm6Dot47FactorSigmaCp(sigma_cy=sigma_cy, sigma_cz=sigma_cz)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{cp} = \frac{\sigma_{cy} + \sigma_{cz}}{2} = " r"\frac{1.000 + 2.000}{2} = 1.500 \ MPa",
            ),
            ("short", r"\sigma_{cp} = 1.500 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_cy = 1.0
        sigma_cz = 2.0

        # Object to test
        latex = SubForm6Dot47FactorSigmaCp(sigma_cy=sigma_cy, sigma_cz=sigma_cz).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestSubForm6Dot47FactorSigmaCy:
    """Validation for sub-formula 4 of formula 6.47 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed_y = 1000.0
        a_cy = 500.0

        # Object to test
        formula = SubForm6Dot47FactorSigmaCy(n_ed_y=n_ed_y, a_cy=a_cy)

        # Expected result, manually calculated
        manually_calculated_result = 2.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed_y", "a_cy"),
        [
            (-1000.0, 500.0),  # n_ed_y is negative
            (1000.0, -500.0),  # a_cy is negative
            (1000.0, 0.0),  # a_cy is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed_y: float, a_cy: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            SubForm6Dot47FactorSigmaCy(n_ed_y=n_ed_y, a_cy=a_cy)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{cy} = \frac{N_{Ed,y}}{A_{cy}} = " r"\frac{1000.000}{500.000} = 2.000 \ MPa",
            ),
            ("short", r"\sigma_{cy} = 2.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed_y = 1000.0
        a_cy = 500.0

        # Object to test
        latex = SubForm6Dot47FactorSigmaCy(n_ed_y=n_ed_y, a_cy=a_cy).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestSubForm6Dot47FactorSigmaCz:
    """Validation for sub-formula 5 of formula 6.47 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed_z = 2000.0
        a_cz = 1000.0

        # Object to test
        formula = SubForm6Dot47FactorSigmaCz(n_ed_z=n_ed_z, a_cz=a_cz)

        # Expected result, manually calculated
        manually_calculated_result = 2.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed_z", "a_cz"),
        [
            (-2000.0, 1000.0),  # n_ed_z is negative
            (2000.0, -1000.0),  # a_cz is negative
            (2000.0, 0.0),  # a_cz is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed_z: float, a_cz: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            SubForm6Dot47FactorSigmaCz(n_ed_z=n_ed_z, a_cz=a_cz)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{cz} = \frac{N_{Ed,z}}{A_{cz}} = " r"\frac{2000.000}{1000.000} = 2.000 \ MPa",
            ),
            ("short", r"\sigma_{cz} = 2.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed_z = 2000.0
        a_cz = 1000.0

        # Object to test
        latex = SubForm6Dot47FactorSigmaCz(n_ed_z=n_ed_z, a_cz=a_cz).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
