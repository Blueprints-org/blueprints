"""Testing formula 5.46 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_46 import (
    Form5Dot46Part1TimeDependentForceLosses,
    Form5Dot46Part2TimeDependentStressLosses,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot46Part1TimeDependentForceLosses:
    """Validation for formula 5.46 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_p = 1000.0
        epsilon_cs = 0.0002
        e_p = 200000.0
        delta_sigma_pr = 100.0
        e_cm = 30000.0
        phi_t_t0 = 2.0
        sigma_c_qp = 10.0
        a_c = 5000.0
        i_c = 1000000.0
        z_cp = 200.0

        # Object to test
        formula = Form5Dot46Part1TimeDependentForceLosses(
            a_p=a_p,
            epsilon_cs=epsilon_cs,
            e_p=e_p,
            delta_sigma_pr=delta_sigma_pr,
            e_cm=e_cm,
            phi_t_t0=phi_t_t0,
            sigma_c_qp=sigma_c_qp,
            a_c=a_c,
            i_c=i_c,
            z_cp=z_cp,
        )

        # Expected result, manually calculated
        manually_calculated_result = 363.045762873

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_p", "epsilon_cs", "e_p", "delta_sigma_pr", "e_cm", "phi_t_t0", "sigma_c_qp", "a_c", "i_c", "z_cp"),
        [
            (-1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # a_p is negative
            (1000.0, -0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # epsilon_cs is negative
            (1000.0, 0.0002, -200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # e_p is negative
            (1000.0, 0.0002, 200000.0, -100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # delta_sigma_pr is negative
            (1000.0, 0.0002, 200000.0, 100.0, -30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # e_cm is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, -2.0, 10.0, 5000.0, 1000000.0, 200.0),  # phi_t_t0 is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, -10.0, 5000.0, 1000000.0, 200.0),  # sigma_c_qp is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, -5000.0, 1000000.0, 200.0),  # a_c is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, -1000000.0, 200.0),  # i_c is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, -200.0),  # z_cp is negative
            (0.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # a_p is zero
            (1000.0, 0.0002, 0.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # e_p is zero
            (1000.0, 0.0002, 200000.0, 100.0, 0.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # e_cm is zero
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 0.0, 1000000.0, 200.0),  # a_c is zero
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 0.0, 200.0),  # i_c is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        a_p: float,
        epsilon_cs: float,
        e_p: float,
        delta_sigma_pr: float,
        e_cm: float,
        phi_t_t0: float,
        sigma_c_qp: float,
        a_c: float,
        i_c: float,
        z_cp: float,
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot46Part1TimeDependentForceLosses(
                a_p=a_p,
                epsilon_cs=epsilon_cs,
                e_p=e_p,
                delta_sigma_pr=delta_sigma_pr,
                e_cm=e_cm,
                phi_t_t0=phi_t_t0,
                sigma_c_qp=sigma_c_qp,
                a_c=a_c,
                i_c=i_c,
                z_cp=z_cp,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta P_{c+s+r} = A_p \cdot \frac{\epsilon_{cs} \cdot E_p + 0.8 \cdot \Delta \sigma_{pr} + "
                r"\frac{E_p}{E_{cm}} \cdot \phi(t, t_0) \cdot \sigma_{c,QP}}{1 + \frac{E_p}{E_{cm}} \cdot \frac{A_p}{A_c} "
                r"\cdot \left(1 + \frac{A_c}{I_c} \cdot z_{cp}^2\right) \cdot \left(1 + 0.8 \cdot \phi(t, t_0)\right)}"
                r" = 1000.000 \cdot \frac{0.000200 \cdot 200000.000 + 0.800 \cdot 100.000 + \frac{200000.000}{30000.000} "
                r"\cdot 2.000 \cdot 10.000}{1 + \frac{200000.000}{30000.000} \cdot \frac{1000.000}{5000.000} "
                r"\cdot \left(1 + \frac{5000.000}{1000000.000} \cdot 200.000^2\right) "
                r"\cdot \left(1 + 0.800 \cdot 2.000\right)} = 363.046 \ N",
            ),
            ("short", r"\Delta P_{c+s+r} = 363.046 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_p = 1000.0
        epsilon_cs = 0.0002
        e_p = 200000.0
        delta_sigma_pr = 100.0
        e_cm = 30000.0
        phi_t_t0 = 2.0
        sigma_c_qp = 10.0
        a_c = 5000.0
        i_c = 1000000.0
        z_cp = 200.0

        # Object to test
        latex = Form5Dot46Part1TimeDependentForceLosses(
            a_p=a_p,
            epsilon_cs=epsilon_cs,
            e_p=e_p,
            delta_sigma_pr=delta_sigma_pr,
            e_cm=e_cm,
            phi_t_t0=phi_t_t0,
            sigma_c_qp=sigma_c_qp,
            a_c=a_c,
            i_c=i_c,
            z_cp=z_cp,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm5Dot46Part2TimeDependentStressLosses:
    """Validation for formula 5.46 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_p = 1000.0
        epsilon_cs = 0.0002
        e_p = 200000.0
        delta_sigma_pr = 100.0
        e_cm = 30000.0
        phi_t_t0 = 2.0
        sigma_c_qp = 10.0
        a_c = 5000.0
        i_c = 1000000.0
        z_cp = 200.0

        # Object to test
        formula = Form5Dot46Part2TimeDependentStressLosses(
            a_p=a_p,
            epsilon_cs=epsilon_cs,
            e_p=e_p,
            delta_sigma_pr=delta_sigma_pr,
            e_cm=e_cm,
            phi_t_t0=phi_t_t0,
            sigma_c_qp=sigma_c_qp,
            a_c=a_c,
            i_c=i_c,
            z_cp=z_cp,
        )

        # Expected result, manually calculated
        manually_calculated_result = 0.363045762873

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_p", "epsilon_cs", "e_p", "delta_sigma_pr", "e_cm", "phi_t_t0", "sigma_c_qp", "a_c", "i_c", "z_cp"),
        [
            (-1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # a_p is negative
            (1000.0, -0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # epsilon_cs is negative
            (1000.0, 0.0002, -200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # e_p is negative
            (1000.0, 0.0002, 200000.0, -100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # delta_sigma_pr is negative
            (1000.0, 0.0002, 200000.0, 100.0, -30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # e_cm is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, -2.0, 10.0, 5000.0, 1000000.0, 200.0),  # phi_t_t0 is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, -10.0, 5000.0, 1000000.0, 200.0),  # sigma_c_qp is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, -5000.0, 1000000.0, 200.0),  # a_c is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, -1000000.0, 200.0),  # i_c is negative
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, -200.0),  # z_cp is negative
            (0.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # a_p is zero
            (1000.0, 0.0002, 0.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # e_p is zero
            (1000.0, 0.0002, 200000.0, 100.0, 0.0, 2.0, 10.0, 5000.0, 1000000.0, 200.0),  # e_cm is zero
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 0.0, 1000000.0, 200.0),  # a_c is zero
            (1000.0, 0.0002, 200000.0, 100.0, 30000.0, 2.0, 10.0, 5000.0, 0.0, 200.0),  # i_c is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        a_p: float,
        epsilon_cs: float,
        e_p: float,
        delta_sigma_pr: float,
        e_cm: float,
        phi_t_t0: float,
        sigma_c_qp: float,
        a_c: float,
        i_c: float,
        z_cp: float,
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot46Part2TimeDependentStressLosses(
                a_p=a_p,
                epsilon_cs=epsilon_cs,
                e_p=e_p,
                delta_sigma_pr=delta_sigma_pr,
                e_cm=e_cm,
                phi_t_t0=phi_t_t0,
                sigma_c_qp=sigma_c_qp,
                a_c=a_c,
                i_c=i_c,
                z_cp=z_cp,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta \sigma_{p,c+s+r} = \frac{\epsilon_{cs} \cdot E_p + 0.8 \cdot \Delta \sigma_{pr} + "
                r"\frac{E_p}{E_{cm}} \cdot \phi(t, t_0) \cdot \sigma_{c,QP}}{1 + \frac{E_p}{E_{cm}} \cdot \frac{A_p}{A_c} "
                r"\cdot \left(1 + \frac{A_c}{I_c} \cdot z_{cp}^2\right) \cdot \left(1 + 0.8 \cdot \phi(t, t_0)\right)}"
                r" = \frac{0.000200 \cdot 200000.000 + 0.800 \cdot 100.000 + \frac{200000.000}{30000.000} "
                r"\cdot 2.000 \cdot 10.000}{1 + \frac{200000.000}{30000.000} \cdot \frac{1000.000}{5000.000} "
                r"\cdot \left(1 + \frac{5000.000}{1000000.000} \cdot 200.000^2\right) "
                r"\cdot \left(1 + 0.800 \cdot 2.000\right)} = 0.363 \ MPa",
            ),
            ("short", r"\Delta \sigma_{p,c+s+r} = 0.363 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_p = 1000.0
        epsilon_cs = 0.0002
        e_p = 200000.0
        delta_sigma_pr = 100.0
        e_cm = 30000.0
        phi_t_t0 = 2.0
        sigma_c_qp = 10.0
        a_c = 5000.0
        i_c = 1000000.0
        z_cp = 200.0

        # Object to test
        latex = Form5Dot46Part2TimeDependentStressLosses(
            a_p=a_p,
            epsilon_cs=epsilon_cs,
            e_p=e_p,
            delta_sigma_pr=delta_sigma_pr,
            e_cm=e_cm,
            phi_t_t0=phi_t_t0,
            sigma_c_qp=sigma_c_qp,
            a_c=a_c,
            i_c=i_c,
            z_cp=z_cp,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
