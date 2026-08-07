"""Testing formula 8.70 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_70 import (
    Form8Dot70CheckCrushingOfCompressionFieldInFlange,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot70CheckCrushingOfCompressionFieldInFlange:
    """Validation for formula 8.70 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "expected"),
        [
            (3.0, True),  # the compression field is not crushed
            (6.0, False),  # the compression field is crushed
        ],
    )
    def test_evaluation(self, tau_ed: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        # Example values
        cot_theta_f = 1.2
        nu = 0.5
        f_cd = 20.0

        # Object to test
        formula = Form8Dot70CheckCrushingOfCompressionFieldInFlange(
            tau_ed=tau_ed,
            cot_theta_f=cot_theta_f,
            nu=nu,
            f_cd=f_cd,
        )

        assert bool(formula) is expected

    def test_compressive_stress(self) -> None:
        """Tests the compressive stress in the compression field."""
        # Object to test
        formula = Form8Dot70CheckCrushingOfCompressionFieldInFlange(
            tau_ed=3.0,
            cot_theta_f=1.2,
            nu=0.5,
            f_cd=20.0,
        )

        # Expected result, manually calculated: 3.0 * (1.2 + 1 / 1.2)
        manually_calculated_result = 6.1  # MPa

        assert formula.lhs == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_compressive_strength(self) -> None:
        """Tests the compressive strength of the compression field."""
        # Object to test
        formula = Form8Dot70CheckCrushingOfCompressionFieldInFlange(
            tau_ed=3.0,
            cot_theta_f=1.2,
            nu=0.5,
            f_cd=20.0,
        )

        # Expected result, manually calculated: 0.5 * 20.0
        manually_calculated_result = 10.0  # MPa

        assert formula.rhs == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_ed", "cot_theta_f", "nu", "f_cd"),
        [
            (-3.0, 1.2, 0.5, 20.0),  # tau_ed is negative
            (3.0, -1.2, 0.5, 20.0),  # cot_theta_f is negative
            (3.0, 0.0, 0.5, 20.0),  # cot_theta_f is zero
            (3.0, 1.2, -0.5, 20.0),  # nu is negative
            (3.0, 1.2, 0.0, 20.0),  # nu is zero
            (3.0, 1.2, 0.5, -20.0),  # f_cd is negative
            (3.0, 1.2, 0.5, 0.0),  # f_cd is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_ed: float, cot_theta_f: float, nu: float, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot70CheckCrushingOfCompressionFieldInFlange(
                tau_ed=tau_ed,
                cot_theta_f=cot_theta_f,
                nu=nu,
                f_cd=f_cd,
            )

    @pytest.mark.parametrize(
        ("tau_ed", "representation", "expected"),
        [
            (
                3.0,
                "complete",
                (
                    r"CHECK \to \sigma_{cd} = \tau_{Ed} \left(\cot(\theta_f) + \tan(\theta_f)\right) \leq \nu \cdot f_{cd} \to "
                    r"6.100 = 3.000 \left(1.200 + 0.833\right) \leq 0.500 \cdot 20.000 \to OK"
                ),
            ),
            (
                3.0,
                "complete_with_units",
                (
                    r"CHECK \to \sigma_{cd} = \tau_{Ed} \left(\cot(\theta_f) + \tan(\theta_f)\right) \leq \nu \cdot f_{cd} \to "
                    r"6.100 \ MPa = 3.000 \ MPa \left(1.200 + 0.833\right) \leq 0.500 \cdot 20.000 \ MPa \to OK"
                ),
            ),
            (3.0, "short", r"CHECK \to OK"),
            (6.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, tau_ed: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot70CheckCrushingOfCompressionFieldInFlange(
            tau_ed=tau_ed,
            cot_theta_f=1.2,
            nu=0.5,
            f_cd=20.0,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
