"""Tests for bending moment strength together with shear and torsion according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.strength_bending_shear import (
    CheckStrengthBendingShearClass3,
    CheckStrengthBendingShearClass12,
)
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.unit_conversion import KNM_TO_NMM


class TestCheckStrengthBendingShearClass12:
    """Tests for CheckStrengthBendingShearClass12."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no bending moment."""
        cross_section, section_properties = heb_steel_cross_section
        calc = CheckStrengthBendingShearClass12(cross_section, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthBendingShearClass12(cross_section, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        assert pytest.approx(result.unity_check) == calc_without_section_props.result().unity_check

    def test_result_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok bending moment about y-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m_x = 1  # Applied torsional moment in kNm
        v = 600  # Applied shear force in kN
        resistance = CheckStrengthBendingShearClass12(
            cross_section, m_x=m_x, v=v, axis_m="My", axis_v="Vz", section_properties=section_properties
        ).calculation_formula()["resistance"]
        m = float(resistance) / KNM_TO_NMM * 0.99
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok bending moment about y-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m_x = 1  # Applied torsional moment in kNm
        v = 600  # Applied shear force in kN
        resistance = CheckStrengthBendingShearClass12(
            cross_section, m_x=m_x, v=v, axis_m="My", axis_v="Vz", section_properties=section_properties
        ).calculation_formula()["resistance"]
        m = -float(resistance) / KNM_TO_NMM * 1.01
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_result_no_m_x_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok bending moment about z-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m_x = 0  # no torsional moment
        v = -600  # Applied shear force in kN
        resistance = CheckStrengthBendingShearClass12(
            cross_section, m_x=m_x, v=v, axis_m="My", axis_v="Vz", section_properties=section_properties
        ).calculation_formula()["resistance"]
        m = float(resistance) / KNM_TO_NMM * 0.99
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        calc.report().to_word("bending_moment_strength.docx")
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_no_m_x_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok bending moment about z-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m_x = 0  # no torsional moment
        v = -600  # Applied shear force in kN
        resistance = CheckStrengthBendingShearClass12(
            cross_section, m_x=m_x, v=v, axis_m="My", axis_v="Vz", section_properties=section_properties
        ).calculation_formula()["resistance"]
        m = -float(resistance) / KNM_TO_NMM * 1.01
        calc = CheckStrengthBendingShearClass12(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_invalid_axis(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test ValueError is raised for invalid axis input."""
        cross_section, section_properties = heb_steel_cross_section
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass12(
                cross_section, 100, 0, 0, axis_m="Ma", axis_v="Vz", section_properties=section_properties
            ).calculation_formula()
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass12(
                cross_section, 100, 0, 0, axis_m="My", axis_v="Va", section_properties=section_properties
            ).calculation_formula()
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass12(
                cross_section, 100, 0, 0, axis_m="Mz", axis_v="Vz", section_properties=section_properties
            ).calculation_formula()


class TestCheckStrengthBendingShearClass3:
    """Tests for CheckStrengthBendingShearClass3."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no bending moment."""
        cross_section, section_properties = heb_steel_cross_section
        calc = CheckStrengthBendingShearClass3(cross_section, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthBendingShearClass3(cross_section, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        assert pytest.approx(result.unity_check) == calc_without_section_props.result().unity_check

    def test_result_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok bending moment about y-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m = 613.3 * 0.99  # Applied bending moment in kNm
        m_x = 1  # Applied torsional moment in kNm
        v = 600  # Applied shear force in kN
        calc = CheckStrengthBendingShearClass3(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok bending moment about y-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m = -613.3 * 1.01  # Applied bending moment in kNm
        m_x = 1  # Applied torsional moment in kNm
        v = 600  # Applied shear force in kN
        calc = CheckStrengthBendingShearClass3(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_result_no_m_x_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok bending moment about z-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m = 627.3 * 0.99
        m_x = 0  # no torsional moment
        v = -600  # Applied shear force in kN
        calc = CheckStrengthBendingShearClass3(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        calc.report().to_word("bending_moment_strength.docx")
        calc = CheckStrengthBendingShearClass3(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_no_m_x_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok bending moment about z-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m = -627.3 * 1.01
        m_x = 0  # no torsional moment
        v = -600  # Applied shear force in kN
        calc = CheckStrengthBendingShearClass3(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_invalid_axis(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test ValueError is raised for invalid axis input."""
        cross_section, section_properties = heb_steel_cross_section
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass3(
                cross_section, 100, 0, 0, axis_m="Ma", axis_v="Vz", section_properties=section_properties
            ).calculation_formula()
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass3(
                cross_section, 100, 0, 0, axis_m="My", axis_v="Va", section_properties=section_properties
            ).calculation_formula()
        with pytest.raises(ValueError):
            CheckStrengthBendingShearClass3(
                cross_section, 100, 0, 0, axis_m="Mz", axis_v="Vz", section_properties=section_properties
            ).calculation_formula()
