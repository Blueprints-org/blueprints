"""Test for formula 2.22 from CUR 228."""

import pytest

from blueprints.codes.cur.cur_228.formula_2_22 import Form2Dot22ModulusHorizontalSubgrade
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm2Dot22ModulusHorizontalSubgrade:
    """Validation for formula 2.22 from CUR 228."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        r = 0.2  # m
        e_p = 2.47  # kN/m²
        alpha = 1 / 3  # -
        form_2_22 = Form2Dot22ModulusHorizontalSubgrade(r=r, e_p=e_p, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 17.00760939

        assert form_2_22 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_r_is_higher_then_0_3(self) -> None:
        """Tests if an ValueError is raised when r > 0.3."""
        # Example values
        r = 0.5  # m
        e_p = 2.47  # kN/m²
        alpha = 1 / 3  # -

        with pytest.raises(ValueError):
            Form2Dot22ModulusHorizontalSubgrade(r=r, e_p=e_p, alpha=alpha)

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
            Form2Dot22ModulusHorizontalSubgrade(r=r, e_p=500, alpha=alpha)

    @pytest.mark.parametrize(
        ("e_p"),
        [
            (-500.0),
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, e_p: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form2Dot22ModulusHorizontalSubgrade(r=0.2, e_p=e_p, alpha=0.33)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    "k_{h} = \\frac{2 \\cdot R}{E_{p}} \\cdot \\frac{4 \\cdot 2.65^{\\alpha} + 3 "
                    "\\alpha}{18} = \\frac{2 \\cdot 0.20}{2.47} \\cdot \\frac{4 \\cdot "
                    "2.65^{0.33} + 3 \\cdot 0.33}{18} = 17.01 \\ kN/m^3"
                ),
            ),
            ("short", r"k_{h} = 17.01 \ kN/m^3"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        r = 0.2  # m
        e_p = 2.47  # kN/m²
        alpha = 1 / 3  # -

        # Object to test
        form_2_1_a_latex = Form2Dot22ModulusHorizontalSubgrade(r=r, e_p=e_p, alpha=alpha).latex()

        actual = {"complete": form_2_1_a_latex.complete, "short": form_2_1_a_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
