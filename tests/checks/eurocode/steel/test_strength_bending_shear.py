"""Tests for bending moment strength together with shear and torsion according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.strength_bending_shear import (
    CheckStrenghtBendingShearClass3IProfile,
)
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrenghtBendingShearClass3IProfile:
    """Tests for CheckStrenghtBendingShearClass3IProfile."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no bending moment."""
        cross_section, section_properties = heb_steel_cross_section
        calc = CheckStrenghtBendingShearClass3IProfile(cross_section, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrenghtBendingShearClass3IProfile(cross_section, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        assert pytest.approx(result.unity_check) == calc_without_section_props.result().unity_check

    def test_result_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok bending moment about y-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m = 613.3 * 0.99  # Applied bending moment in kNm
        m_x = 1  # Applied torsional moment in kNm
        v = 600  # Applied shear force in kN
        calc = CheckStrenghtBendingShearClass3IProfile(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
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
        calc = CheckStrenghtBendingShearClass3IProfile(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
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
        calc = CheckStrenghtBendingShearClass3IProfile(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        calc.report().to_word("bending_moment_strength.docx")
        calc = CheckStrenghtBendingShearClass3IProfile(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
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
        calc = CheckStrenghtBendingShearClass3IProfile(cross_section, m, m_x, v, axis_m="My", axis_v="Vz", section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_invalid_axis(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test ValueError is raised for invalid axis input."""
        cross_section, section_properties = heb_steel_cross_section
        with pytest.raises(ValueError):
            CheckStrenghtBendingShearClass3IProfile(
                cross_section, 100, 0, 0, axis_m="Ma", axis_v="Vz", section_properties=section_properties
            ).calculation_formula()
        with pytest.raises(ValueError):
            CheckStrenghtBendingShearClass3IProfile(
                cross_section, 100, 0, 0, axis_m="My", axis_v="Va", section_properties=section_properties
            ).calculation_formula()
        with pytest.raises(ValueError):
            CheckStrenghtBendingShearClass3IProfile(
                cross_section, 100, 0, 0, axis_m="Mz", axis_v="Vz", section_properties=section_properties
            ).calculation_formula()

    def test_check_wrong_profile(self, chs_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() raises TypeError for non-I-profile."""
        cross_section, section_properties = chs_steel_cross_section
        with pytest.raises(TypeError, match="The provided profile is not an I-profile"):
            CheckStrenghtBendingShearClass3IProfile(
                cross_section, m=100, m_x=0, v=1, axis_m="My", axis_v="Vz", section_properties=section_properties
            ).calculation_formula()
