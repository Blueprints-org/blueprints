"""Testing formula 6.44 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_44 import (
    Form6Dot44CombinedCompressionBendingClass4CrossSections,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm6Dot44CombinedCompressionBendingClass4CrossSections:
    """Validation for formula 6.44 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 50000.0  # N
        a_eff = 2000.0  # mm^2
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # -
        m_y_ed = 5000000.0  # Nmm
        e_ny = 10.0  # mm
        w_eff_y_min = 50000.0  # mm^3
        m_z_ed = 3000000.0  # Nmm
        e_nz = 8.0  # mm
        w_eff_z_min = 40000.0  # mm^3

        # Object to test
        formula = Form6Dot44CombinedCompressionBendingClass4CrossSections(
            n_ed=n_ed,
            a_eff=a_eff,
            f_y=f_y,
            gamma_m0=gamma_m0,
            m_y_ed=m_y_ed,
            e_ny=e_ny,
            w_eff_y_min=w_eff_y_min,
            m_z_ed=m_z_ed,
            e_nz=e_nz,
            w_eff_z_min=w_eff_z_min,
        )

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result
        # Unity check calculation
        n_rd = a_eff * f_y / gamma_m0
        m_y_rd = w_eff_y_min * f_y / gamma_m0
        m_z_rd = w_eff_z_min * f_y / gamma_m0
        expected_unity = n_ed / n_rd + (m_y_ed + n_ed * e_ny) / m_y_rd + (m_z_ed + n_ed * e_nz) / m_z_rd
        assert formula.unity_check == pytest.approx(expected_unity)

    @pytest.mark.parametrize(
        ("n_ed", "a_eff", "f_y", "gamma_m0", "m_y_ed", "e_ny", "w_eff_y_min", "m_z_ed", "e_nz", "w_eff_z_min"),
        [
            (50000.0, 0.0, 355.0, 1.0, 5000000.0, 10.0, 50000.0, 3000000.0, 8.0, 40000.0),  # a_eff is zero
            (50000.0, -2000.0, 355.0, 1.0, 5000000.0, 10.0, 50000.0, 3000000.0, 8.0, 40000.0),  # a_eff is negative
            (50000.0, 2000.0, 355.0, 0.0, 5000000.0, 10.0, 50000.0, 3000000.0, 8.0, 40000.0),  # gamma_m0 is zero
            (50000.0, 2000.0, 355.0, -1.0, 5000000.0, 10.0, 50000.0, 3000000.0, 8.0, 40000.0),  # gamma_m0 is negative
            (50000.0, 2000.0, 355.0, 1.0, 5000000.0, 10.0, 0.0, 3000000.0, 8.0, 40000.0),  # w_eff_y_min is zero
            (50000.0, 2000.0, 355.0, 1.0, 5000000.0, 10.0, -50000.0, 3000000.0, 8.0, 40000.0),  # w_eff_y_min is negative
            (50000.0, 2000.0, 355.0, 1.0, 5000000.0, 10.0, 50000.0, 3000000.0, 8.0, 0.0),  # w_eff_z_min is zero
            (50000.0, 2000.0, 355.0, 1.0, 5000000.0, 10.0, 50000.0, 3000000.0, 8.0, -40000.0),  # w_eff_z_min is negative
            (50000.0, 2000.0, -355.0, 1.0, 5000000.0, 10.0, 50000.0, 3000000.0, 8.0, 40000.0),  # f_y is negative
            (50000.0, 2000.0, 0.0, 1.0, 5000000.0, 10.0, 50000.0, 3000000.0, 8.0, 40000.0),  # f_y is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        n_ed: float,
        a_eff: float,
        f_y: float,
        gamma_m0: float,
        m_y_ed: float,
        e_ny: float,
        w_eff_y_min: float,
        m_z_ed: float,
        e_nz: float,
        w_eff_z_min: float,
    ) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot44CombinedCompressionBendingClass4CrossSections(
                n_ed=n_ed,
                a_eff=a_eff,
                f_y=f_y,
                gamma_m0=gamma_m0,
                m_y_ed=m_y_ed,
                e_ny=e_ny,
                w_eff_y_min=w_eff_y_min,
                m_z_ed=m_z_ed,
                e_nz=e_nz,
                w_eff_z_min=w_eff_z_min,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{N_{Ed}}{A_{eff} \cdot f_y / \gamma_{M0}} + "
                r"\frac{M_{y,Ed} + N_{Ed} \cdot e_{Ny}}{W_{eff,y,min} \cdot f_y / \gamma_{M0}} + "
                r"\frac{M_{z,Ed} + N_{Ed} \cdot e_{Nz}}{W_{eff,z,min} \cdot f_y / \gamma_{M0}} \leq 1 \to "
                r"\frac{50000.000}{2000.000 \cdot 355.000 / 1.000} + "
                r"\frac{5000000.000 + 50000.000 \cdot 10.000}{50000.000 \cdot 355.000 / 1.000} + "
                r"\frac{3000000.000 + 50000.000 \cdot 8.000}{40000.000 \cdot 355.000 / 1.000} \leq 1 \to OK",
            ),
            ("short", r"CHECK \to OK"),
            (
                "complete_with_units",
                r"CHECK \to \frac{N_{Ed}}{A_{eff} \cdot f_y / \gamma_{M0}} + "
                r"\frac{M_{y,Ed} + N_{Ed} \cdot e_{Ny}}{W_{eff,y,min} \cdot f_y / \gamma_{M0}} + "
                r"\frac{M_{z,Ed} + N_{Ed} \cdot e_{Nz}}{W_{eff,z,min} \cdot f_y / \gamma_{M0}} \leq 1 \to "
                r"\frac{50000.000 \ N}{2000.000 \ mm^2 \cdot 355.000 \ MPa / 1.000} + "
                r"\frac{5000000.000 \ Nmm + 50000.000 \ N \cdot 10.000 \ mm}{50000.000 \ mm^3 \cdot 355.000 \ MPa / 1.000} + "
                r"\frac{3000000.000 \ Nmm + 50000.000 \ N \cdot 8.000 \ mm}{40000.000 \ mm^3 \cdot 355.000 \ MPa / 1.000} \leq 1 \to OK",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 50000.0  # N
        a_eff = 2000.0  # mm^2
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # -
        m_y_ed = 5000000.0  # Nmm
        e_ny = 10.0  # mm
        w_eff_y_min = 50000.0  # mm^3
        m_z_ed = 3000000.0  # Nmm
        e_nz = 8.0  # mm
        w_eff_z_min = 40000.0  # mm^3

        # Object to test
        latex = Form6Dot44CombinedCompressionBendingClass4CrossSections(
            n_ed=n_ed,
            a_eff=a_eff,
            f_y=f_y,
            gamma_m0=gamma_m0,
            m_y_ed=m_y_ed,
            e_ny=e_ny,
            w_eff_y_min=w_eff_y_min,
            m_z_ed=m_z_ed,
            e_nz=e_nz,
            w_eff_z_min=w_eff_z_min,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
            "complete_with_units": latex.complete_with_units,
        }

        assert expected == actual[representation], f"{representation} representation failed."
