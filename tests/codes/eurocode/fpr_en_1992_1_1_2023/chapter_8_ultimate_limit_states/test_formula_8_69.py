"""Testing formula 8.69 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_69 import (
    Form8Dot69CheckTransverseReinforcementInFlange,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot69CheckTransverseReinforcementInFlange:
    """Validation for formula 8.69 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "expected"),
        [
            (1.5, True),  # the reinforcement carries the shear stress
            (3.4974, True),  # exactly on the boundary, which the standard includes
            (4.0, False),  # the reinforcement does not carry the shear stress
        ],
    )
    def test_evaluation(self, tau_ed: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sf = 201.0
        s_f = 150.0
        h_f = 200.0
        f_yd = 435.0
        cot_theta_f = 1.2

        # Object to test
        formula = Form8Dot69CheckTransverseReinforcementInFlange(
            tau_ed=tau_ed,
            a_sf=a_sf,
            s_f=s_f,
            h_f=h_f,
            f_yd=f_yd,
            cot_theta_f=cot_theta_f,
        )

        assert bool(formula) is expected

    def test_right_hand_side(self) -> None:
        """Tests the shear stress that the transverse reinforcement can carry."""
        # Object to test
        formula = Form8Dot69CheckTransverseReinforcementInFlange(
            tau_ed=1.5,
            a_sf=201.0,
            s_f=150.0,
            h_f=200.0,
            f_yd=435.0,
            cot_theta_f=1.2,
        )

        # Expected result, manually calculated: 201 / (150 * 200) * 435 * 1.2
        manually_calculated_result = 3.4974  # MPa

        assert formula.rhs == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_ed", "a_sf", "s_f", "h_f", "f_yd", "cot_theta_f"),
        [
            (-1.5, 201.0, 150.0, 200.0, 435.0, 1.2),  # tau_ed is negative
            (1.5, -201.0, 150.0, 200.0, 435.0, 1.2),  # a_sf is negative
            (1.5, 201.0, -150.0, 200.0, 435.0, 1.2),  # s_f is negative
            (1.5, 201.0, 0.0, 200.0, 435.0, 1.2),  # s_f is zero
            (1.5, 201.0, 150.0, -200.0, 435.0, 1.2),  # h_f is negative
            (1.5, 201.0, 150.0, 0.0, 435.0, 1.2),  # h_f is zero
            (1.5, 201.0, 150.0, 200.0, -435.0, 1.2),  # f_yd is negative
            (1.5, 201.0, 150.0, 200.0, 435.0, -1.2),  # cot_theta_f is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        tau_ed: float,
        a_sf: float,
        s_f: float,
        h_f: float,
        f_yd: float,
        cot_theta_f: float,
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot69CheckTransverseReinforcementInFlange(
                tau_ed=tau_ed,
                a_sf=a_sf,
                s_f=s_f,
                h_f=h_f,
                f_yd=f_yd,
                cot_theta_f=cot_theta_f,
            )

    @pytest.mark.parametrize(
        ("tau_ed", "representation", "expected"),
        [
            (
                1.5,
                "complete",
                (
                    r"CHECK \to \tau_{Ed} \leq \frac{A_{sf}}{s_f \cdot h_f} \cdot f_{yd} \cdot \cot(\theta_f) \to "
                    r"1.500 \leq \frac{201.000}{150.000 \cdot 200.000} \cdot 435.000 \cdot 1.200 \to OK"
                ),
            ),
            (
                1.5,
                "complete_with_units",
                (
                    r"CHECK \to \tau_{Ed} \leq \frac{A_{sf}}{s_f \cdot h_f} \cdot f_{yd} \cdot \cot(\theta_f) \to "
                    r"1.500 \ MPa \leq \frac{201.000 \ mm^2}{150.000 \ mm \cdot 200.000 \ mm} \cdot 435.000 \ MPa \cdot 1.200 \to OK"
                ),
            ),
            (1.5, "short", r"CHECK \to OK"),
            (4.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, tau_ed: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot69CheckTransverseReinforcementInFlange(
            tau_ed=tau_ed,
            a_sf=201.0,
            s_f=150.0,
            h_f=200.0,
            f_yd=435.0,
            cot_theta_f=1.2,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
