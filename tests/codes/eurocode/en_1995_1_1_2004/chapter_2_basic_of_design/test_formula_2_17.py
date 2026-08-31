"""Testing formula 2.17 from EN 1995-1-1:2004: Chapter 2: Basis of design."""

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2004.chapter_2_basis_of_design.formula_2_17 import Form2Dot17DesignValueResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm2Dot17DesignValueResistance:
    """Validation for formula 2.1 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        r_k = 260.0  # N
        gamma_m = 1.3  # [-]
        k_mod = 0.50  # [-]

        formula = Form2Dot17DesignValueResistance(r_k=r_k, gamma_m=gamma_m, k_mod=k_mod)

        manually_calculated_result = 100.0  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("r_k", "gamma_m", "k_mod", "expected_exception"),
        [
            (-260.0, 1.3, 0.50, NegativeValueError),  # r_k is negative
            (260.0, -1.3, 0.50, LessOrEqualToZeroError),  # gamma_m is negative
            (260.0, 0.0, 0.50, LessOrEqualToZeroError),  # gamma_m is zero
            (260.0, 1.3, -0.50, LessOrEqualToZeroError),  # k_mod is negative
            (260.0, 1.3, 0.0, LessOrEqualToZeroError),  # k_mod is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        r_k: float,
        gamma_m: float,
        k_mod: float,
        expected_exception: type[Exception],
    ) -> None:
        """Test invalid values."""
        with pytest.raises(expected_exception):
            Form2Dot17DesignValueResistance(r_k=r_k, gamma_m=gamma_m, k_mod=k_mod)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"R_{d} = k_{mod}*\frac{R_k}{\gamma_M} = 0.500*\frac{260.000}{1.300} = 100.000 \ N",
            ),
            (
                "complete_with_units",
                r"R_{d} = k_{mod}*\frac{R_k}{\gamma_M} = 0.500*\frac{260.000 \ N}{1.300} = 100.000 \ N",
            ),
            ("short", r"R_{d} = 100.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the LaTeX representation of the formula."""
        r_k = 260.0  # N
        gamma_m = 1.3  # [-]
        k_mod = 0.50  # [-]

        latex = Form2Dot17DesignValueResistance(r_k=r_k, gamma_m=gamma_m, k_mod=k_mod).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
