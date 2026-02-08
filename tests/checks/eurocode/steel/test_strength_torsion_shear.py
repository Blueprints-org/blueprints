"""Tests for torsion with shear strength according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.strength_torsion_shear import CheckStrengthTorsionShearClass1234IProfile
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrengthTorsionShearClass1234IProfile:
    """Tests for CheckStrengthTorsionShearClass1234IProfile, using St. Venant torsion."""

    def test_result_none_v(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 0
        mx = 1
        calc = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vz", gamma_m0=1.0)
        assert calc == calc_without_section_props

    def test_result_none_mx(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no shear force."""
        cross_section, section_properties = heb_steel_cross_section
        mx = 0
        v = 1
        calc = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

    def test_result_shear_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 585.023 * 0.99
        mx = 10
        calc = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

        v = -v
        calc = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        v = 1482.833 * 0.99
        calc = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vy", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        v = 355.277 * 0.99
        object.__setattr__(cross_section, "fabrication_method", "welded")
        calc = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_shear_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok shear force."""
        cross_section, section_properties = heb_steel_cross_section
        object.__setattr__(cross_section, "fabrication_method", "rolled")
        v = 585.023 * 1.01
        mx = 10
        calc = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

        v = 1482.833 * 1.01
        calc = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vy", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

        v = 355.277 * 1.01
        object.__setattr__(cross_section, "fabrication_method", "welded")
        calc = CheckStrengthTorsionShearClass1234IProfile(cross_section, mx, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

    def test_check_wrong_profile(self, chs_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() raises TypeError for non-I-profile."""
        cross_section, section_properties = chs_steel_cross_section
        with pytest.raises(TypeError, match="The provided profile is not an I-profile"):
            CheckStrengthTorsionShearClass1234IProfile(cross_section, mx=10, v=1, gamma_m0=1.0, section_properties=section_properties)
