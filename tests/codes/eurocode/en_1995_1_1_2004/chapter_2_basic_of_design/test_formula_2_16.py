"""Testing formula 2.16 from EN 1995-1-1:2004: Chapter 2: Basis of design."""

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2004.chapter_2_basis_of_design.formula_2_16 import Form2Dot16DesignShearModulus
from blueprints.validations import LessOrEqualToZeroError


class TestForm2Dot16DesignShearModulus:
    """Validation for formula 2.16 from EN 1993-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        g_mean = 689.0  # MPA
        gamma_m = 1.3  # [-]

        formula = Form2Dot16DesignShearModulus(g_mean=g_mean, gamma_m=gamma_m)

        manually_calculated_result = 530.0  # MPA

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("g_mean", "gamma_m", "expected_exception"),
        [
            (-689.0, 1.3, LessOrEqualToZeroError),  # g_mean is negative
            (0.0, 1.3, LessOrEqualToZeroError),  # g_mean is zero
            (689.0, -1.3, LessOrEqualToZeroError),  # gamma_m is negative
            (689.0, 0.0, LessOrEqualToZeroError),  # gamma_m is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        g_mean: float,
        gamma_m: float,
        expected_exception: type[Exception],
    ) -> None:
        """Test invalid values."""
        with pytest.raises(expected_exception):
            Form2Dot16DesignShearModulus(g_mean=g_mean, gamma_m=gamma_m)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"G_d = \frac{G_{mean}}{\gamma_M} = \frac{689.000}{1.300} = 530.000 \ MPA",
            ),
            (
                "complete_with_units",
                r"G_d = \frac{G_{mean}}{\gamma_M} = \frac{689.000 \ MPA}{1.300} = 530.000 \ MPA",
            ),
            ("short", r"G_d = 530.000 \ MPA"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the LaTeX representation of the formula."""
        g_mean = 689.0  # MPA
        gamma_m = 1.3  # [-]

        latex = Form2Dot16DesignShearModulus(g_mean=g_mean, gamma_m=gamma_m).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
