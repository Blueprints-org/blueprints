"""Tests for bending moment strength together with shear and torsion according to Eurocode 3."""

import numpy as np
import pytest

from blueprints.checks.eurocode.steel.strength_bending_shear import (
    CheckStrengthBendingShearClass3,
    CheckStrengthBendingShearClass12,
)
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection

# Factor chosen in such a way that it reduces 50% of strength according to 1993-1-1 6.29
# That way, the test values from test_strength_bending.py and test_strength_shear.py can be used to test the combined check.
FACTOR_SHEAR = (np.sqrt(0.5) + 1.0) / 2.0


class TestCheckStrengthBendingShearClass12:
    """Tests for CheckStrengthBendingShearClass12."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no bending moment."""
        cross_section = heb_steel_cross_section
        calc = CheckStrengthBendingShearClass12(cross_section, axis_m="My", axis_v="Vz")
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthBendingShearClass12(cross_section, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        assert pytest.approx(result.unity_check) == calc_without_section_props.result().unity_check

    def test_source_docs_and_calculation_formula(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test source_docs() method."""
        calc = CheckStrengthBendingShearClass12(heb_steel_cross_section, axis_m="My", axis_v="Vz")
        docs = calc.source_docs()
        assert isinstance(docs, list)
        assert len(docs) == 1
        assert calc.calculation_formula() == {}

    def test_result_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about y-axis."""
        cross_section = heb_steel_cross_section
        m_x = 10  # Applied torsional moment in kNm
        v = 587.8 * FACTOR_SHEAR  # Applied shear force in kN
        m = 355 * 1.869 * 0.5 * 0.99
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.01) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.01) == 1 / 0.99
        assert calc.report()

    def test_result_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about y-axis."""
        cross_section = heb_steel_cross_section
        m_x = 10  # Applied torsional moment in kNm
        v = 587.8 * FACTOR_SHEAR  # Applied shear force in kN
        m = 355 * 1.869 * 0.5 * 1.01
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz")
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.01) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.01) == 1 / 1.01
        assert calc.report()

    def test_result_no_m_x_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about z-axis."""
        cross_section = heb_steel_cross_section
        m_x = 0  # no torsional moment
        v = -355 * 4.74 / 1.732 * FACTOR_SHEAR  # Applied shear force in kN
        m = 355 * 1.869 * 0.5 * 0.99
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.01) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.01) == 1 / 0.99
        assert calc.report()

    def test_result_no_m_x_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about z-axis."""
        cross_section = heb_steel_cross_section
        m_x = 0  # no torsional moment
        v = -355 * 4.74 / 1.732 * FACTOR_SHEAR  # Applied shear force in kN
        m = 355 * 1.869 * 0.5 * 1.01
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz")
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.01) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.01) == 1 / 1.01
        assert calc.report()

    def test_invalid_axis(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test ValueError is raised for invalid axis input."""
        cross_section = heb_steel_cross_section
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass12(cross_section, 100, 0, 0, axis_m="Ma", axis_v="Vz").calculation_formula()
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass12(cross_section, 100, 0, 0, axis_m="My", axis_v="Va").calculation_formula()
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass12(cross_section, 100, 0, 0, axis_m="Mz", axis_v="Vz").calculation_formula()


class TestCheckStrengthBendingShearClass3:
    """Tests for CheckStrengthBendingShearClass3."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no bending moment."""
        cross_section = heb_steel_cross_section

        calc = CheckStrengthBendingShearClass3(cross_section, axis_m="My", axis_v="Vz")
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthBendingShearClass3(cross_section, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        assert pytest.approx(result.unity_check) == calc_without_section_props.result().unity_check

    def test_result_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about y-axis."""
        cross_section = heb_steel_cross_section

        m = 180 * 0.99
        v = 410 * 0.99  # Applied shear force in kN
        m_x = 10 * 0.99  # Applied torsional moment in kNm
        calc = CheckStrengthBendingShearClass3(cross_section, m, m_x, v, axis_m="Mz", axis_v="Vy")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.01) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.01) == 1 / 0.99
        assert calc.report()

    def test_result_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about y-axis."""
        cross_section = heb_steel_cross_section

        m = 180 * 1.01
        v = 410 * 1.01  # Applied shear force in kN
        m_x = 10 * 1.01  # Applied torsional moment in kNm
        calc = CheckStrengthBendingShearClass3(cross_section, m, m_x, v, axis_m="Mz", axis_v="Vy")
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.01) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.01) == 1 / 1.01
        assert calc.report()

    def test_result_no_m_x_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about z-axis."""
        cross_section = heb_steel_cross_section

        m = 203 * 0.99
        v = 450 * 0.99  # Applied shear force in kN
        m_x = 0
        calc = CheckStrengthBendingShearClass3(cross_section, m, m_x, v, axis_m="Mz", axis_v="Vy")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.01) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.01) == 1 / 0.99
        assert calc.report()

    def test_result_no_m_x_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about z-axis."""
        cross_section = heb_steel_cross_section

        m = 203 * 1.01
        v = 450 * 1.01  # Applied shear force in kN
        m_x = 0
        calc = CheckStrengthBendingShearClass3(cross_section, m, m_x, v, axis_m="Mz", axis_v="Vy")
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.01) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.01) == 1 / 1.01
        assert calc.report()

    def test_invalid_axis(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test ValueError is raised for invalid axis input."""
        cross_section = heb_steel_cross_section
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass3(cross_section, 100, 0, 0, axis_m="Ma", axis_v="Vz").calculation_formula()
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass3(cross_section, 100, 0, 0, axis_m="My", axis_v="Va").calculation_formula()
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass3(cross_section, 100, 0, 0, axis_m="Mz", axis_v="Vz").calculation_formula()
