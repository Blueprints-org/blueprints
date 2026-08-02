"""Testing the fatigue life curve value from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance."""

from typing import Literal

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_life_curve_value import Form8FatigueLifeCurveValue
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import StressType
from blueprints.validations import LessOrEqualToZeroError


class TestForm8FatigueLifeCurveValue:
    """Validation for the fatigue life curve value from EN 1993-1-9:2025."""

    @pytest.mark.parametrize(
        ("delta_sigma_ref", "n_ref", "m", "delta_sigma_r", "point"),
        [
            (160.0, 2e6, 3.0, 201.587, "C"),  # N_R = N_C (Δσ_C/Δσ_R)^m1
            (117.889, 5e6, 5.0, 89.343, "D"),  # N_R = N_D (Δσ_D/Δσ_R)^m2
        ],
    )
    def test_evaluation(self, delta_sigma_ref: float, n_ref: float, m: float, delta_sigma_r: float, point: Literal["C", "D"]) -> None:
        """Test the evaluation of the result for both branches."""
        form = Form8FatigueLifeCurveValue(
            delta_sigma_ref=delta_sigma_ref, n_ref=n_ref, m=m, delta_sigma_r=delta_sigma_r, point=point, stress_type=StressType.NORMAL
        )
        manually_calculated_result = n_ref * (delta_sigma_ref / delta_sigma_r) ** m

        assert form == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    def test_reference_stress_maps_to_reference_cycles(self) -> None:
        """Feeding the reference strength back (Δσ_R = Δσ_ref) returns the reference cycle number N_ref."""
        form = Form8FatigueLifeCurveValue(delta_sigma_ref=160.0, n_ref=2e6, m=3.0, delta_sigma_r=160.0, point="C", stress_type=StressType.NORMAL)
        assert form == pytest.approx(expected=2e6, rel=1e-9)

    def test_raise_error_if_invalid_point(self) -> None:
        """Test that a ValueError is raised when point is not 'C' or 'D'."""
        with pytest.raises(ValueError, match="Invalid point"):
            Form8FatigueLifeCurveValue(delta_sigma_ref=160.0, n_ref=2e6, m=3.0, delta_sigma_r=160.0, point="X", stress_type=StressType.NORMAL)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("delta_sigma_ref", "n_ref", "m", "delta_sigma_r"),
        [
            (160.0, 0.0, 3.0, 160.0),  # n_ref <= 0
            (160.0, -2e6, 3.0, 160.0),  # n_ref < 0
            (160.0, 2e6, 0.0, 160.0),  # m <= 0
            (160.0, 2e6, -3.0, 160.0),  # m < 0
            (160.0, 2e6, 3.0, 0.0),  # delta_sigma_r <= 0 (would divide by zero)
            (160.0, 2e6, 3.0, -160.0),  # delta_sigma_r < 0
            (0.0, 2e6, 3.0, 160.0),  # delta_sigma_ref <= 0 (zero reference strength gives a nonsensical N_R = 0)
            (-160.0, 2e6, 3.0, 160.0),  # delta_sigma_ref < 0
        ],
    )
    def test_raise_error_if_less_or_equal_to_zero(self, delta_sigma_ref: float, n_ref: float, m: float, delta_sigma_r: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive cycle number, slope, applied stress range or reference strength."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8FatigueLifeCurveValue(
                delta_sigma_ref=delta_sigma_ref, n_ref=n_ref, m=m, delta_sigma_r=delta_sigma_r, point="C", stress_type=StressType.NORMAL
            )

    @pytest.mark.parametrize(
        ("point", "stress_type", "inputs", "representation", "expected"),
        [
            (
                "C",
                StressType.NORMAL,
                {"delta_sigma_ref": 160.0, "n_ref": 2e6, "m": 3.0, "delta_sigma_r": 201.587},
                "complete",
                r"N_{R} = N_{C} \left( \frac{\Delta\sigma_{C}}{\Delta\sigma_{R}} \right)^{m_{1}} = "
                r"2.0 \cdot 10^{6} \left( \frac{160.000}{201.587} \right)^{3} = 1000005",
            ),
            (
                "D",
                StressType.NORMAL,
                {"delta_sigma_ref": 117.889, "n_ref": 5e6, "m": 5.0, "delta_sigma_r": 89.343},
                "complete",
                r"N_{R} = N_{D} \left( \frac{\Delta\sigma_{D}}{\Delta\sigma_{R}} \right)^{m_{2}} = "
                r"5.0 \cdot 10^{6} \left( \frac{117.889}{89.343} \right)^{5} = 20000174",
            ),
            (
                "C",
                StressType.SHEAR,
                {"delta_sigma_ref": 100.0, "n_ref": 2e6, "m": 5.0, "delta_sigma_r": 114.870},
                "complete",
                r"N_{R} = N_{C} \left( \frac{\Delta\tau_{C}}{\Delta\tau_{R}} \right)^{m_{1}} = "
                r"2.0 \cdot 10^{6} \left( \frac{100.000}{114.870} \right)^{5} = 999993",
            ),
            (
                "C",
                StressType.NORMAL,
                {"delta_sigma_ref": 160.0, "n_ref": 2e6, "m": 3.0, "delta_sigma_r": 201.587},
                "short",
                r"N_{R} = 1000005",
            ),
        ],
    )
    def test_latex(self, point: Literal["C", "D"], stress_type: StressType, inputs: dict[str, float], representation: str, expected: str) -> None:
        """Test the latex representation on both branches, including the Δσ (normal) vs Δτ (shear) symbol switch."""
        latex = Form8FatigueLifeCurveValue(**inputs, point=point, stress_type=stress_type).latex()  # type: ignore[arg-type]

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
