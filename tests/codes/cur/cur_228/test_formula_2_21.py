"""Test for formula 2.21 from CUR 228."""

import pytest

from blueprints.codes.cur.cur_228.formula_2_21 import Form2Dot21ModulusHorizontalSubgrade
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm2Dot21ModulusHorizontalSubgrade:
    """Validation for formula 2.21 from CUR 228."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        r = 0.5  # m
        e_p = 2.47  # kN/m²
        alpha = 1 / 3  # -
        form_2_21 = Form2Dot21ModulusHorizontalSubgrade(r=r, e_p=e_p, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 9.187357198

        assert form_2_21 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("r", "alpha"),
        [
            (-0.6, -0.33),
            (0.2, -0.33),
            (0.2, 0.0),
            (0.0, 0.0),
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, r: float, alpha: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form2Dot21ModulusHorizontalSubgrade(r=r, e_p=500, alpha=alpha)

    @pytest.mark.parametrize(
        ("e_p"),
        [
            (-500.0),
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, e_p: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form2Dot21ModulusHorizontalSubgrade(r=0.4, e_p=e_p, alpha=0.33)

    @pytest.mark.parametrize(
        ("r"),
        [
            (0.2),
            (0.29),
        ],
    )
    def test_raise_error_when_invalid_diameter_values_are_given(self, r: float) -> None:
        """Test invalid values."""
        with pytest.raises(ValueError):
            Form2Dot21ModulusHorizontalSubgrade(r=r, e_p=500, alpha=0.33)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    "k_{h} = \\frac{1}{3 \\cdot E_{p}} \\cdot \\left[1.3 \\cdot R_{0} \\left( 2.65 \\frac{R}{R_0}\\right)^\\alpha + \\alpha \\cdot  "
                    "R \\right] = \\frac{1}{3 \\cdot 2.5} \\cdot\\left[1.3 \\cdot 0.3 \\left( 2.65 \\cdot \\frac{0.5}{0.3}\\right)^{0.33}+ 0.33 "
                    "\\cdot 0.5\\right] = 9.19 \\ kN/m^3"
                ),
            ),
            ("short", r"k_{h} = 9.19 \ kN/m^3"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        r = 0.5  # m
        e_p = 2.47  # kN/m²
        alpha = 1 / 3  # -

        # Object to test
        form_2_1_a_latex = Form2Dot21ModulusHorizontalSubgrade(r=r, e_p=e_p, alpha=alpha).latex()

        actual = {"complete": form_2_1_a_latex.complete, "short": form_2_1_a_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
