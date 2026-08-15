"""Testing formula 8.57 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_56 import Form8Dot56StressInShearReinforcement
from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_57 import Form8Dot57AdditionalBendingMoment
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angles chosen so that their cotangents are round numbers, which keeps the hand calculations readable
THETA_COT_2 = 26.565051177078  # cot(theta) = 2
THETA_COT_0_5 = 63.434948822922  # cot(theta) = 0.5


class TestForm8Dot57AdditionalBendingMoment:
    """Validation for formula 8.57 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "x", "expected"),
        [
            # (2 - 0.002 * 435 * 2) * 400 * 300 * (600/2 - 200) = 0.26 * 400 * 300 * 100
            (2.0, 200.0, 3120000.0),
            # beyond half the distance to the load the lever turns negative
            (2.0, 400.0, -3120000.0),
            # below the contribution of the shear reinforcement the first bracket turns negative
            (1.0, 200.0, -8880000.0),
        ],
    )
    def test_evaluation(self, tau_ed: float, x: float, expected: float) -> None:
        """Tests the evaluation of the result, including the two cases where it turns negative."""
        # Create object to test
        formula = Form8Dot57AdditionalBendingMoment(
            tau_ed=tau_ed,
            rho_w=0.002,
            f_ywd=435.0,
            theta=THETA_COT_2,
            z=400.0,
            b_w=300.0,
            a=600.0,
            x=x,
        )

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_accepts_the_negative_stress_of_formula_8_56(self) -> None:
        r"""For [$\cot\theta < 1$] the standard requires f_ywd to be replaced by the stress of Formula (8.56),
        which carries no printed lower bound and is negative over much of its range. Guarding this argument
        against negative values would block the substitution the standard prescribes, so it is not guarded.
        """
        # 200000 * (0.5^2 * (0 + 0.001) - 0.001) = -150.0
        sigma_swd = Form8Dot56StressInShearReinforcement(e_s=200000.0, theta=THETA_COT_0_5, epsilon_x=0.0, f_ywd=435.0)

        formula = Form8Dot57AdditionalBendingMoment(
            tau_ed=2.0,
            rho_w=0.002,
            f_ywd=sigma_swd,
            theta=THETA_COT_0_5,
            z=400.0,
            b_w=300.0,
            a=600.0,
            x=200.0,
        )

        # (2 - 0.002 * -150 * 0.5) * 400 * 300 * (600/2 - 200) = 2.15 * 400 * 300 * 100
        assert formula == pytest.approx(expected=25800000.0, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_ed", "rho_w", "z", "b_w", "a", "x"),
        [
            (-2.0, 0.002, 400.0, 300.0, 600.0, 200.0),  # tau_ed is negative
            (2.0, -0.002, 400.0, 300.0, 600.0, 200.0),  # rho_w is negative
            (2.0, 0.002, -400.0, 300.0, 600.0, 200.0),  # z is negative
            (2.0, 0.002, 400.0, -300.0, 600.0, 200.0),  # b_w is negative
            (2.0, 0.002, 400.0, 300.0, -600.0, 200.0),  # a is negative
            (2.0, 0.002, 400.0, 300.0, 600.0, -200.0),  # x is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self,
        tau_ed: float,
        rho_w: float,
        z: float,
        b_w: float,
        a: float,
        x: float,
    ) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot57AdditionalBendingMoment(tau_ed=tau_ed, rho_w=rho_w, f_ywd=435.0, theta=THETA_COT_2, z=z, b_w=b_w, a=a, x=x)

    @pytest.mark.parametrize(
        "theta",
        [
            -THETA_COT_2,  # theta is negative
            0.0,  # theta is zero, for which the cotangent diverges
        ],
    )
    def test_raise_error_when_the_angle_is_less_or_equal_to_zero(self, theta: float) -> None:
        """Test if error is raised for an angle that is not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot57AdditionalBendingMoment(tau_ed=2.0, rho_w=0.002, f_ywd=435.0, theta=theta, z=400.0, b_w=300.0, a=600.0, x=200.0)

    def test_raise_error_when_the_angle_exceeds_90_degrees(self) -> None:
        """The angle is an inclination to the member axis, so it cannot pass 90 degrees."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot57AdditionalBendingMoment(tau_ed=2.0, rho_w=0.002, f_ywd=435.0, theta=120.0, z=400.0, b_w=300.0, a=600.0, x=200.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\Delta M_{Ed} = \left(\tau_{Ed} - \rho_w \cdot f_{ywd} \cdot \cot(\theta)\right) "
                    r"\cdot z \cdot b_w \cdot \left(\frac{a}{2} - x\right) = "
                    r"\left(2.000 - 0.002 \cdot 435.000 \cdot \cot(26.565)\right) "
                    r"\cdot 400.000 \cdot 300.000 \cdot \left(\frac{600.000}{2} - 200.000\right) = 3120000.000 \ Nmm"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\Delta M_{Ed} = \left(\tau_{Ed} - \rho_w \cdot f_{ywd} \cdot \cot(\theta)\right) "
                    r"\cdot z \cdot b_w \cdot \left(\frac{a}{2} - x\right) = "
                    r"\left(2.000 \ MPa - 0.002 \cdot 435.000 \ MPa \cdot \cot(26.565 ^\circ)\right) "
                    r"\cdot 400.000 \ mm \cdot 300.000 \ mm \cdot \left(\frac{600.000 \ mm}{2} - 200.000 \ mm\right) = 3120000.000 \ Nmm"
                ),
            ),
            ("short", r"\Delta M_{Ed} = 3120000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot57AdditionalBendingMoment(
            tau_ed=2.0,
            rho_w=0.002,
            f_ywd=435.0,
            theta=THETA_COT_2,
            z=400.0,
            b_w=300.0,
            a=600.0,
            x=200.0,
        ).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
