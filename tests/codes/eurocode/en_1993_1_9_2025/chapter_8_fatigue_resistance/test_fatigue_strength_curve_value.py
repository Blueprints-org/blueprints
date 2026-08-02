"""Testing the fatigue strength curve value from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance."""

from typing import Literal

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_value import Form8FatigueStrengthCurveValue
from blueprints.validations import LessOrEqualToZeroError


class TestForm8FatigueStrengthCurveValue:
    """Validation for the fatigue strength curve value from EN 1993-1-9:2025."""

    @pytest.mark.parametrize(
        ("delta_sigma_ref", "n_ref", "n_target", "m", "point"),
        [
            (160.0, 2e6, 5e6, 3.0, "D"),  # Δσ_D = Δσ_C (N_C/N_D)^(1/m1)
            (117.889, 5e6, 1e8, 5.0, "L"),  # Δσ_L = Δσ_D (N_D/N_L)^(1/m2)
        ],
    )
    def test_evaluation(self, delta_sigma_ref: float, n_ref: float, n_target: float, m: float, point: Literal["D", "L"]) -> None:
        """Test the evaluation of the result for both reference points."""
        form = Form8FatigueStrengthCurveValue(delta_sigma_ref=delta_sigma_ref, n_ref=n_ref, n_target=n_target, m=m, point=point)
        manually_calculated_result = delta_sigma_ref * (n_ref / n_target) ** (1 / m)

        assert form == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    def test_d_point_matches_known_factor(self) -> None:
        """Δσ_D is 0.737·Δσ_C for the standard curve (N_C=2e6, N_D=5e6, m1=3)."""
        form = Form8FatigueStrengthCurveValue(delta_sigma_ref=160.0, n_ref=2e6, n_target=5e6, m=3.0, point="D")
        assert form / 160.0 == pytest.approx(expected=0.73681, rel=1e-4)

    def test_l_point_matches_known_factor(self) -> None:
        """Δσ_L is 0.405·Δσ_C for the standard curve, chaining D then L."""
        delta_sigma_d = Form8FatigueStrengthCurveValue(delta_sigma_ref=160.0, n_ref=2e6, n_target=5e6, m=3.0, point="D")
        delta_sigma_l = Form8FatigueStrengthCurveValue(delta_sigma_ref=delta_sigma_d, n_ref=5e6, n_target=1e8, m=5.0, point="L")
        assert delta_sigma_l / 160.0 == pytest.approx(expected=0.405, rel=1e-3)

    def test_raise_error_if_invalid_point(self) -> None:
        """Test that a ValueError is raised when point is not 'D' or 'L'."""
        with pytest.raises(ValueError, match="Invalid point"):
            Form8FatigueStrengthCurveValue(delta_sigma_ref=160.0, n_ref=2e6, n_target=5e6, m=3.0, point="X")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("delta_sigma_ref", "n_ref", "n_target", "m"),
        [
            (160.0, 0.0, 5e6, 3.0),  # n_ref <= 0
            (160.0, -2e6, 5e6, 3.0),  # n_ref < 0
            (160.0, 2e6, 0.0, 3.0),  # n_target <= 0
            (160.0, 2e6, 5e6, 0.0),  # m <= 0
            (160.0, 2e6, 5e6, -3.0),  # m < 0
            (0.0, 2e6, 5e6, 3.0),  # delta_sigma_ref <= 0 (zero reference strength gives a nonsensical zero strength)
            (-160.0, 2e6, 5e6, 3.0),  # delta_sigma_ref < 0
        ],
    )
    def test_raise_error_if_less_or_equal_to_zero(self, delta_sigma_ref: float, n_ref: float, n_target: float, m: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for non-positive cycle numbers, slope or reference strength."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8FatigueStrengthCurveValue(delta_sigma_ref=delta_sigma_ref, n_ref=n_ref, n_target=n_target, m=m, point="D")

    @pytest.mark.parametrize(
        ("point", "representation", "expected"),
        [
            (
                "D",
                "complete",
                r"\Delta\sigma_{D} = \Delta\sigma_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m_{1}} = "
                r"160.000 \left( \frac{2.0 \cdot 10^{6}}{5.0 \cdot 10^{6}} \right)^{1 / 3} = 117.889 \ MPa",
            ),
            ("D", "short", r"\Delta\sigma_{D} = 117.889 \ MPa"),
            (
                "L",
                "complete",
                r"\Delta\sigma_{L} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m_{2}} = "
                r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa",
            ),
            ("L", "short", r"\Delta\sigma_{L} = 64.754 \ MPa"),
        ],
    )
    def test_latex(self, point: Literal["D", "L"], representation: str, expected: str) -> None:
        """Test the latex representation of the formula for both reference points."""
        inputs = {
            "D": {"delta_sigma_ref": 160.0, "n_ref": 2e6, "n_target": 5e6, "m": 3.0},
            "L": {"delta_sigma_ref": 117.889, "n_ref": 5e6, "n_target": 1e8, "m": 5.0},
        }
        latex = Form8FatigueStrengthCurveValue(**inputs[point], point=point).latex()  # type: ignore[arg-type]

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
