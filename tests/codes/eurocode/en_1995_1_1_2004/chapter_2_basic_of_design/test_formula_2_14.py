"""Testing formula 2.14 from EN 1995-1-1:2004: Chapter 2: Basis of design."""

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2004.chapter_2_basis_of_design.formula_2_14 import Form2Dot14DesignValueStrength
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm2Dot14DesignValueStrength:
    """Validation for formula 2.14 from EN 1995-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        x_k = 26.0  # MPA
        gamma_m = 1.3  # [-]
        k_mod = 0.50  # [-]

        formula = Form2Dot14DesignValueStrength(x_k=x_k, gamma_m=gamma_m, k_mod=k_mod)

        manually_calculated_result = 10.0  # MPA

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("x_k", "gamma_m", "k_mod", "expected_exception"),
        [
            (-26.0, 1.3, 0.50, NegativeValueError),  # x_k is negative
            (26.0, -1.3, 0.50, LessOrEqualToZeroError),  # gamma_m is negative
            (26.0, 0.0, 0.50, LessOrEqualToZeroError),  # gamma_m is zero
            (26.0, 1.3, -0.50, LessOrEqualToZeroError),  # k_mod is negative
            (26.0, 1.3, 0.0, LessOrEqualToZeroError),  # k_mod is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        x_k: float,
        gamma_m: float,
        k_mod: float,
        expected_exception: type[Exception],
    ) -> None:
        """Test invalid values."""
        with pytest.raises(expected_exception):
            Form2Dot14DesignValueStrength(x_k=x_k, gamma_m=gamma_m, k_mod=k_mod)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"X_d = k_{mod} \cdot \frac{X_k}{\gamma_M} = 0.500 \cdot \frac{26.000}{1.300} = 10.000 \ MPA",
            ),
            (
                "complete_with_units",
                r"X_d = k_{mod} \cdot \frac{X_k}{\gamma_M} = 0.500 \cdot \frac{26.000 \ MPA}{1.300} = 10.000 \ MPA",
            ),
            ("short", r"X_d = 10.000 \ MPA"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the LaTeX representation of the formula."""
        x_k = 26.0  # MPA
        gamma_m = 1.3  # [-]
        k_mod = 0.50  # [-]

        latex = Form2Dot14DesignValueStrength(x_k=x_k, gamma_m=gamma_m, k_mod=k_mod).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
