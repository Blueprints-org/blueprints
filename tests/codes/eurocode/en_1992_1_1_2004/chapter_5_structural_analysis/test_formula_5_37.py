"""Testing formula 5.37 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_37 import Form5Dot37CreepFactor
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot37CreepFactor:
    """Validation for formula 5.37 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_ck = 30.0
        lambda_ = 2.0
        phi_ef = 1.5

        # Object to test
        formula = Form5Dot37CreepFactor(f_ck=f_ck, lambda_=lambda_, phi_ef=phi_ef)

        # Expected result, manually calculated
        manually_calculated_result = 1.730

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_ck", "lambda_", "phi_ef"),
        [
            (-30.0, 2.0, 1.5),  # f_ck is negative
            (30.0, -2.0, 1.5),  # lambda_ is negative
            (30.0, 2.0, -1.5),  # phi_ef is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_ck: float, lambda_: float, phi_ef: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot37CreepFactor(f_ck=f_ck, lambda_=lambda_, phi_ef=phi_ef)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"K_{\phi} = \max\left(1 + \left(0.35 + \frac{f_{ck}}{200} - \frac{\lambda}{150}\right) \cdot \phi_{ef}; 1\right) "
                r"= \max\left(1 + \left(0.35 + \frac{30.000}{200} - \frac{2.000}{150}\right) \cdot 1.500; 1\right) = 1.730 \ -",
            ),
            ("short", r"K_{\phi} = 1.730 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 30.0
        lambda_ = 2.0
        phi_ef = 1.5

        # Object to test
        latex = Form5Dot37CreepFactor(f_ck=f_ck, lambda_=lambda_, phi_ef=phi_ef).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
