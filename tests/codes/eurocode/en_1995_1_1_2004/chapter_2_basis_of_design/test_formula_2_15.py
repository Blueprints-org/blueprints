"""Testing formula 2.15 from EN 1995-1-1:2004: Chapter 2: Basis of design."""

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2004.chapter_2_basis_of_design.formula_2_15 import Form2Dot15DesignModulusElasticity
from blueprints.validations import LessOrEqualToZeroError


class TestForm2Dot15DesignModulusElasticity:
    """Validation for formula 2.15 from EN 1995-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        e_mean = 13000.0  # MPA
        gamma_m = 1.3  # [-]

        formula = Form2Dot15DesignModulusElasticity(e_mean=e_mean, gamma_m=gamma_m)

        manually_calculated_result = 10000.0  # MPA

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("e_mean", "gamma_m", "expected_exception"),
        [
            (-13000.0, 1.3, LessOrEqualToZeroError),  # e_mean is negative
            (0.0, 1.3, LessOrEqualToZeroError),  # e_mean is zero
            (13000.0, -1.3, LessOrEqualToZeroError),  # gamma_m is negative
            (13000.0, 0.0, LessOrEqualToZeroError),  # gamma_m is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        e_mean: float,
        gamma_m: float,
        expected_exception: type[Exception],
    ) -> None:
        """Test invalid values."""
        with pytest.raises(expected_exception):
            Form2Dot15DesignModulusElasticity(e_mean=e_mean, gamma_m=gamma_m)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"E_d = \frac{E_{mean}}{\gamma_M} = \frac{13000.000}{1.300} = 10000.000 \ MPA",
            ),
            (
                "complete_with_units",
                r"E_d = \frac{E_{mean}}{\gamma_M} = \frac{13000.000 \ MPA}{1.300} = 10000.000 \ MPA",
            ),
            ("short", r"E_d = 10000.000 \ MPA"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the LaTeX representation of the formula."""
        e_mean = 13000.0  # MPA
        gamma_m = 1.3  # [-]

        latex = Form2Dot15DesignModulusElasticity(e_mean=e_mean, gamma_m=gamma_m).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
