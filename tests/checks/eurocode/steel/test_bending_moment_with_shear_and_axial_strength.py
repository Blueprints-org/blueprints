"""Tests for bending moment strength together with axial force according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.bending_moment_with_shear_and_axial_strength import BendingShearAxialStrengthClass3IProfileCheck
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestBendingShearAxialStrengthClass3IProfileCheck:
    """Tests for BendingShearAxialStrengthClass3IProfileCheck."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no loading."""
        cross_section, section_properties = heb_steel_cross_section
        calc = BendingShearAxialStrengthClass3IProfileCheck(cross_section, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = BendingShearAxialStrengthClass3IProfileCheck(cross_section, gamma_m0=1.0)
        assert pytest.approx(result.unity_check) == calc_without_section_props.result().unity_check

    def test_result_ok_combined_loading(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok combined loading (My, Mz, N)."""
        cross_section, section_properties = heb_steel_cross_section
        n = 1000 * 0.99  # Applied axial force in kN
        v_y = 1111 * 0.99  # Applied shear force in y-direction in kN
        v_z = 50 * 0.99  # Applied shear force in z-direction in kN
        m_x = 10 * 0.99  # Applied torsional moment in kNm
        m_y = 100 * 0.99  # Applied bending moment around y-axis in kNm
        m_z = 80 * 0.99  # Applied bending moment around z-axis in kNm
        calc = BendingShearAxialStrengthClass3IProfileCheck(
            cross_section, m_y=m_y, m_z=m_z, n=n, v_y=v_y, v_z=v_z, m_x=m_x, section_properties=section_properties
        )
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_not_ok_combined_loading(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok combined loading (excessive moments and axial force)."""
        cross_section, section_properties = heb_steel_cross_section
        n = 1000 * 1.01  # Applied axial force in kN
        v_y = 1111 * 1.01  # Applied shear force in y-direction in kN
        v_z = 50 * 1.01  # Applied shear force in z-direction in kN
        m_x = 10 * 1.01  # Applied torsional moment in kNm
        m_y = 100 * 1.01  # Applied bending moment around y-axis in kNm
        m_z = 80 * 1.01  # Applied bending moment around z-axis in kNm
        calc = BendingShearAxialStrengthClass3IProfileCheck(
            cross_section, m_y=m_y, m_z=m_z, n=n, v_y=v_y, v_z=v_z, m_x=m_x, section_properties=section_properties
        )
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_negative_moments(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() handles negative moment values correctly (absolute values used)."""
        cross_section, section_properties = heb_steel_cross_section
        n = -1000 * 0.99  # Applied axial force in kN
        v_y = -1111 * 0.99  # Applied shear force in y-direction in kN
        v_z = -50 * 0.99  # Applied shear force in z-direction in kN
        m_x = -10 * 0.99  # Applied torsional moment in kNm
        m_y = -100 * 0.99  # Applied bending moment around y-axis in kNm
        m_z = -80 * 0.99  # Applied bending moment around z-axis in kNm
        calc = BendingShearAxialStrengthClass3IProfileCheck(
            cross_section, m_y=m_y, m_z=m_z, n=n, v_y=v_y, v_z=v_z, m_x=m_x, section_properties=section_properties
        )
        result = calc.result()
        assert result.is_ok is True
        assert calc.report()

    def test_check_wrong_profile(self, chs_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() raises TypeError for non-I-profile."""
        cross_section, section_properties = chs_steel_cross_section
        n = 1  # Applied axial force in kN
        v_y = 1  # Applied shear force in y-direction in kN
        v_z = 1  # Applied shear force in z-direction in kN
        m_x = 1  # Applied torsional moment in kNm
        m_y = 1  # Applied bending moment around y-axis in kNm
        m_z = 1  # Applied bending moment around z-axis in kNm
        with pytest.raises(TypeError, match="The provided profile is not an I-profile"):
            BendingShearAxialStrengthClass3IProfileCheck(
                cross_section, m_y=m_y, m_z=m_z, n=n, v_y=v_y, v_z=v_z, m_x=m_x, section_properties=section_properties
            )
