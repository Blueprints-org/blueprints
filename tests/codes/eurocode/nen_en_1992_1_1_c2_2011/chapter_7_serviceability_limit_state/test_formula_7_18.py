"""Testing formula 7.18 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_18 import Form7Dot18DeformationParameter
from blueprints.validations import NegativeValueError


class TestForm7Dot18DeformationParameter:
    """Validation for formula 7.18 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        zeta = 1 / 3.0
        alpha_ll = 1.4
        alpha_l = 0.8

        # Object to test
        formula = Form7Dot18DeformationParameter(zeta=zeta, alpha_ll=alpha_ll, alpha_l=alpha_l)

        # Expected result, manually calculated
        manually_calculated_result = 1.0  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("zeta", "alpha_ll", "alpha_l"),
        [
            (-0.5, 1.2, 0.8),  # zeta is negative
            (0.5, -1.2, 0.8),  # alpha_ll is negative
            (0.5, 1.2, -0.8),  # alpha_l is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, zeta: float, alpha_ll: float, alpha_l: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form7Dot18DeformationParameter(zeta=zeta, alpha_ll=alpha_ll, alpha_l=alpha_l)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\alpha = \zeta \cdot \alpha_{II} + (1 - \zeta) \cdot \alpha_{I} = "
                r"0.500 \cdot 1.200 + (1 - 0.500) \cdot 0.800 = 1.000 \ -",
            ),
            ("short", r"\alpha = 1.000 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        zeta = 0.5
        alpha_ll = 1.2
        alpha_l = 0.8

        # Object to test
        latex = Form7Dot18DeformationParameter(zeta=zeta, alpha_ll=alpha_ll, alpha_l=alpha_l).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
