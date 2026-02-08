"""Tests for torsion with shear strength according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.strength_torsion_shear import CheckStrengthTorsionShearClass12IProfile, CheckStrengthTorsionShearClass34
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrengthTorsionShearClass12IProfile:
    """Tests for CheckStrengthTorsionShearClass12IProfile, using St. Venant torsion, for class 1 and 2 I-profiles."""

    def test_result_none_v(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 0
        m_x = 1
        calc = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no torsional moment."""
        cross_section, section_properties = heb_steel_cross_section
        m_x = 0
        v = 0
        calc = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vz", gamma_m0=1.0)
        assert calc == calc_without_section_props

    def test_result_shear_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 585.023 * 0.99
        m_x = 10
        calc = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

        v = -v
        calc = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        v = 1482.833 * 0.99
        calc = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vy", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        v = 355.277 * 0.99
        object.__setattr__(cross_section, "fabrication_method", "welded")
        calc = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_shear_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok shear force."""
        cross_section, section_properties = heb_steel_cross_section
        object.__setattr__(cross_section, "fabrication_method", "hot-rolled")
        v = 585.023 * 1.01
        m_x = 10
        calc = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

        v = 1482.833 * 1.01
        calc = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vy", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

        v = 355.277 * 1.01
        object.__setattr__(cross_section, "fabrication_method", "welded")
        calc = CheckStrengthTorsionShearClass12IProfile(cross_section, m_x, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

    def test_check_wrong_profile(self, chs_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() raises TypeError for non-I-profile."""
        cross_section, section_properties = chs_steel_cross_section
        with pytest.raises(TypeError, match="The provided profile is not an I-profile"):
            CheckStrengthTorsionShearClass12IProfile(cross_section, m_x=10, v=1, gamma_m0=1.0, section_properties=section_properties)


class TestCheckStrengthTorsionShearClass34:
    """Tests for TestCheckStrengthTorsionShearClass34, using St. Venant torsion, for class 3 and 4."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 0
        m_x = 0
        calc = CheckStrengthTorsionShearClass34(cross_section, m_x, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthTorsionShearClass34(cross_section, m_x, v, axis="Vz", gamma_m0=1.0)
        assert calc == calc_without_section_props

    def test_result_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 690 * 0.99
        m_x = 7.66 * 0.99
        calc = CheckStrengthTorsionShearClass34(cross_section, m_x, v, axis="Vy", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 690 * 1.01
        m_x = 7.66 * 1.01
        calc = CheckStrengthTorsionShearClass34(cross_section, m_x, v, axis="Vy", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()
