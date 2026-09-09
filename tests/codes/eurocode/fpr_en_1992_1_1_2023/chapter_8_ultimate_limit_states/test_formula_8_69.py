"""Testing formula 8.69 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_69 import (
    Form8Dot69CheckTransverseReinforcementInFlange,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angle chosen so that its cotangent is a round number, which keeps the hand calculations readable
THETA_F_COT_1_2 = 39.805571092265  # cot(theta_f) = 1.2


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
        theta_f = THETA_F_COT_1_2

        # Object to test
        formula = Form8Dot69CheckTransverseReinforcementInFlange(
            tau_ed=tau_ed,
            a_sf=a_sf,
            s_f=s_f,
            h_f=h_f,
            f_yd=f_yd,
            theta_f=theta_f,
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
            theta_f=THETA_F_COT_1_2,
        )

        # Expected result, manually calculated: 201 / (150 * 200) * 435 * 1.2
        manually_calculated_result = 3.4974  # MPa

        assert formula.rhs == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_ed", "a_sf", "s_f", "h_f", "f_yd", "theta_f"),
        [
            (-1.5, 201.0, 150.0, 200.0, 435.0, THETA_F_COT_1_2),  # tau_ed is negative
            (1.5, -201.0, 150.0, 200.0, 435.0, THETA_F_COT_1_2),  # a_sf is negative
            (1.5, 201.0, -150.0, 200.0, 435.0, THETA_F_COT_1_2),  # s_f is negative
            (1.5, 201.0, 0.0, 200.0, 435.0, THETA_F_COT_1_2),  # s_f is zero
            (1.5, 201.0, 150.0, -200.0, 435.0, THETA_F_COT_1_2),  # h_f is negative
            (1.5, 201.0, 150.0, 0.0, 435.0, THETA_F_COT_1_2),  # h_f is zero
            (1.5, 201.0, 150.0, 200.0, -435.0, THETA_F_COT_1_2),  # f_yd is negative
            (1.5, 201.0, 150.0, 200.0, 0.0, THETA_F_COT_1_2),  # f_yd is zero
            (1.5, 201.0, 150.0, 200.0, 435.0, -THETA_F_COT_1_2),  # theta_f is negative
            (1.5, 201.0, 150.0, 200.0, 435.0, 0.0),  # theta_f is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        tau_ed: float,
        a_sf: float,
        s_f: float,
        h_f: float,
        f_yd: float,
        theta_f: float,
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot69CheckTransverseReinforcementInFlange(
                tau_ed=tau_ed,
                a_sf=a_sf,
                s_f=s_f,
                h_f=h_f,
                f_yd=f_yd,
                theta_f=theta_f,
            )

    def test_raise_error_when_theta_f_exceeds_90_degrees(self) -> None:
        """The angle is an inclination to the member axis, so it cannot pass 90 degrees."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot69CheckTransverseReinforcementInFlange(
                tau_ed=1.5,
                a_sf=201.0,
                s_f=150.0,
                h_f=200.0,
                f_yd=435.0,
                theta_f=120.0,
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
            theta_f=THETA_F_COT_1_2,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
