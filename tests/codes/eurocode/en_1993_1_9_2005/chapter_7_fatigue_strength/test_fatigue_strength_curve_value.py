"""Testing the fatigue strength curve value from EN 1993-1-9:2005: Chapter 7 - Fatigue strength."""

from typing import Literal

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import StressType
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve_value import Form7FatigueStrengthCurveValue
from blueprints.validations import LessOrEqualToZeroError


class TestForm7FatigueStrengthCurveValue:
    """Validation for the fatigue strength curve value from EN 1993-1-9:2005."""

    @pytest.mark.parametrize(
        ("delta_sigma_ref", "n_ref", "n_target", "m", "point", "stress_type"),
        [
            (160.0, 2e6, 5e6, 3.0, "D", StressType.DIRECT),  # Δσ_D = Δσ_C (N_C/N_D)^(1/m)
            (117.889, 5e6, 1e8, 5.0, "L", StressType.DIRECT),  # Δσ_L = Δσ_D (N_D/N_L)^(1/m)
            (100.0, 2e6, 1e8, 5.0, "L", StressType.SHEAR),  # Δτ_L = Δτ_C (N_C/N_L)^(1/m)
        ],
    )
    def test_evaluation(
        self, delta_sigma_ref: float, n_ref: float, n_target: float, m: float, point: Literal["D", "L"], stress_type: StressType
    ) -> None:
        """Test the evaluation of the result for all reference point variants."""
        form = Form7FatigueStrengthCurveValue(
            delta_sigma_ref=delta_sigma_ref, n_ref=n_ref, n_target=n_target, m=m, point=point, stress_type=stress_type
        )
        manually_calculated_result = delta_sigma_ref * (n_ref / n_target) ** (1 / m)

        assert form == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    def test_d_point_matches_known_factor(self) -> None:
        """Δσ_D is 0.737·Δσ_C for the direct stress curve (N_C=2e6, N_D=5e6, m=3), see 7.1(2)."""
        form = Form7FatigueStrengthCurveValue(delta_sigma_ref=160.0, n_ref=2e6, n_target=5e6, m=3.0, point="D", stress_type=StressType.DIRECT)
        assert form / 160.0 == pytest.approx(expected=0.737, rel=1e-3)

    def test_l_point_matches_known_factor(self) -> None:
        """Δσ_L is 0.549·Δσ_D for the direct stress curve (N_D=5e6, N_L=1e8, m=5), see 7.1(3)."""
        form = Form7FatigueStrengthCurveValue(delta_sigma_ref=117.889, n_ref=5e6, n_target=1e8, m=5.0, point="L", stress_type=StressType.DIRECT)
        assert form / 117.889 == pytest.approx(expected=0.549, rel=1e-3)

    def test_shear_l_point_matches_known_factor(self) -> None:
        """Δτ_L is 0.457·Δτ_C for the shear curve (N_C=2e6, N_L=1e8, m=5), see 7.1(2)."""
        form = Form7FatigueStrengthCurveValue(delta_sigma_ref=100.0, n_ref=2e6, n_target=1e8, m=5.0, point="L", stress_type=StressType.SHEAR)
        assert form / 100.0 == pytest.approx(expected=0.457, rel=1e-3)

    def test_raise_error_if_invalid_point(self) -> None:
        """Test that a ValueError is raised when point is not 'D' or 'L'."""
        with pytest.raises(ValueError, match="Invalid point"):
            Form7FatigueStrengthCurveValue(
                delta_sigma_ref=160.0,
                n_ref=2e6,
                n_target=5e6,
                m=3.0,
                point="X",  # type: ignore[arg-type]
                stress_type=StressType.DIRECT,
            )

    def test_raise_error_for_shear_d_point(self) -> None:
        """The shear curve (Figure 7.2) has no constant amplitude fatigue limit, so point 'D' is undefined for it."""
        with pytest.raises(ValueError, match="Invalid point"):
            Form7FatigueStrengthCurveValue(delta_sigma_ref=100.0, n_ref=2e6, n_target=1e8, m=5.0, point="D", stress_type=StressType.SHEAR)

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
            Form7FatigueStrengthCurveValue(
                delta_sigma_ref=delta_sigma_ref, n_ref=n_ref, n_target=n_target, m=m, point="D", stress_type=StressType.DIRECT
            )

    @pytest.mark.parametrize(
        ("point", "stress_type", "representation", "expected"),
        [
            (
                "D",
                StressType.DIRECT,
                "complete",
                r"\Delta\sigma_{D} = \Delta\sigma_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m} = "
                r"160.000 \left( \frac{2.0 \cdot 10^{6}}{5.0 \cdot 10^{6}} \right)^{1 / 3} = 117.889 \ MPa",
            ),
            ("D", StressType.DIRECT, "short", r"\Delta\sigma_{D} = 117.889 \ MPa"),
            (
                "L",
                StressType.DIRECT,
                "complete",
                r"\Delta\sigma_{L} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m} = "
                r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa",
            ),
            ("L", StressType.DIRECT, "short", r"\Delta\sigma_{L} = 64.754 \ MPa"),
            (
                "L",
                StressType.SHEAR,  # shear curve: the symbol switches from Δσ to Δτ and the reference point is C
                "complete",
                r"\Delta\tau_{L} = \Delta\tau_{C} \left( \frac{N_{C}}{N_{L}} \right)^{1 / m} = "
                r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 45.731 \ MPa",
            ),
            ("L", StressType.SHEAR, "short", r"\Delta\tau_{L} = 45.731 \ MPa"),
        ],
    )
    def test_latex(self, point: Literal["D", "L"], stress_type: StressType, representation: str, expected: str) -> None:
        """Test the latex representation of the formula for all reference point variants."""
        inputs = {
            ("D", StressType.DIRECT): {"delta_sigma_ref": 160.0, "n_ref": 2e6, "n_target": 5e6, "m": 3.0},
            ("L", StressType.DIRECT): {"delta_sigma_ref": 117.889, "n_ref": 5e6, "n_target": 1e8, "m": 5.0},
            ("L", StressType.SHEAR): {"delta_sigma_ref": 100.0, "n_ref": 2e6, "n_target": 1e8, "m": 5.0},
        }
        latex = Form7FatigueStrengthCurveValue(**inputs[(point, stress_type)], point=point, stress_type=stress_type).latex()  # type: ignore[arg-type]

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
