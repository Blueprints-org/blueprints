"""Testing formula 8.25 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_25 import (
    Form8Dot25EffectiveDepthFromPrincipalShearForce,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot25EffectiveDepthFromPrincipalShearForce:
    """Validation for formula 8.25 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d_x = 300.0
        d_y = 250.0
        alpha_v = 21.801409  # degrees, following formula 8.26 for v_ed_x = 100.0 and v_ed_y = 40.0

        # Object to test
        formula = Form8Dot25EffectiveDepthFromPrincipalShearForce(d_x=d_x, d_y=d_y, alpha_v=alpha_v)

        # Expected result, manually calculated
        manually_calculated_result = 293.103448  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("alpha_v", "expected"),
        [
            (0.0, 300.0),  # principal shear force along the x-axis, so d equals d_x
            (45.0, 275.0),  # equal shear in both directions, matching 0.5 * (d_x + d_y) of formula 8.23
            (90.0, 250.0),  # principal shear force along the y-axis, so d equals d_y
        ],
    )
    def test_evaluation_at_characteristic_angles(self, alpha_v: float, expected: float) -> None:
        """Tests the evaluation of the result at the angles with an exact outcome."""
        # Example values
        d_x = 300.0
        d_y = 250.0

        formula = Form8Dot25EffectiveDepthFromPrincipalShearForce(d_x=d_x, d_y=d_y, alpha_v=alpha_v)

        assert formula == pytest.approx(expected=expected, rel=1e-9)

    @pytest.mark.parametrize(
        ("d_x", "d_y", "alpha_v"),
        [
            (-300.0, 250.0, 45.0),  # d_x is negative
            (300.0, -250.0, 45.0),  # d_y is negative
            (300.0, 250.0, -45.0),  # alpha_v is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d_x: float, d_y: float, alpha_v: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot25EffectiveDepthFromPrincipalShearForce(d_x=d_x, d_y=d_y, alpha_v=alpha_v)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"d = d_x \cdot \cos^2(\alpha_v) + d_y \cdot \sin^2(\alpha_v) = "
                    r"300.000 \cdot \cos^2(45.000) + 250.000 \cdot \sin^2(45.000) = 275.000 \ mm"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"d = d_x \cdot \cos^2(\alpha_v) + d_y \cdot \sin^2(\alpha_v) = "
                    r"300.000 \ mm \cdot \cos^2(45.000 \ degrees) + 250.000 \ mm \cdot \sin^2(45.000 \ degrees) = 275.000 \ mm"
                ),
            ),
            ("short", r"d = 275.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d_x = 300.0
        d_y = 250.0
        alpha_v = 45.0

        # Object to test
        latex = Form8Dot25EffectiveDepthFromPrincipalShearForce(d_x=d_x, d_y=d_y, alpha_v=alpha_v).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y", "expected_alpha_v"),
        [
            (100.0, 57.735, 30.0),
            (100.0, 100.0, 45.0),
            (-100.0, -57.735, 30.0),  # the angle is taken on the magnitudes
        ],
    )
    def test_angle_from_the_shear_forces(self, v_ed_x: float, v_ed_y: float, expected_alpha_v: float) -> None:
        """Leaving out the angle has Formula (8.26) supply it from the two shear forces."""
        formula = Form8Dot25EffectiveDepthFromPrincipalShearForce(d_x=450.0, d_y=350.0, v_ed_x=v_ed_x, v_ed_y=v_ed_y)
        directly = Form8Dot25EffectiveDepthFromPrincipalShearForce(d_x=450.0, d_y=350.0, alpha_v=expected_alpha_v)

        assert formula.alpha_v == pytest.approx(expected=expected_alpha_v, rel=1e-6)
        assert float(formula) == pytest.approx(expected=float(directly), rel=1e-6)

    def test_raise_error_when_neither_the_angle_nor_the_shear_forces_are_given(self) -> None:
        """One of the two ways of supplying the angle is required."""
        with pytest.raises(ValueError, match="must be given"):
            Form8Dot25EffectiveDepthFromPrincipalShearForce(d_x=450.0, d_y=350.0)

    def test_raise_error_when_the_shear_force_in_the_x_direction_is_zero(self) -> None:
        """Formula (8.26) divides by it, so zero leaves the angle undefined."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot25EffectiveDepthFromPrincipalShearForce(d_x=450.0, d_y=350.0, v_ed_x=0.0, v_ed_y=57.735)

    def test_raise_error_when_the_angle_exceeds_90_degrees(self) -> None:
        """Formula (8.26) is an arctangent of two magnitudes, so it can never exceed 90 degrees."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot25EffectiveDepthFromPrincipalShearForce(d_x=450.0, d_y=350.0, alpha_v=120.0)
