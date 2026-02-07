"""Tests for PlasticShearStrengthIProfileCheck according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.shear_strength import PlasticShearStrengthIProfileCheck
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestPlasticShearStrengthIProfileCheck:
    """Tests for PlasticShearStrengthIProfileCheck."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 0
        calc = PlasticShearStrengthIProfileCheck(cross_section, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = PlasticShearStrengthIProfileCheck(cross_section, v, axis="Vz", gamma_m0=1.0)
        assert calc == calc_without_section_props

    def test_result_shear_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 355 * 4.74 / 1.732 * 0.99
        calc = PlasticShearStrengthIProfileCheck(cross_section, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        v = -v
        calc = PlasticShearStrengthIProfileCheck(cross_section, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        v = 355 * 12.03 / 1.732 * 0.99
        calc = PlasticShearStrengthIProfileCheck(cross_section, v, axis="Vy", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        v = 355 * 2.882 / 1.732 * 0.99
        object.__setattr__(cross_section, "fabrication_method", "welded")
        calc = PlasticShearStrengthIProfileCheck(cross_section, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_shear_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok shear force."""
        cross_section, section_properties = heb_steel_cross_section
        object.__setattr__(cross_section, "fabrication_method", "rolled")
        v = 355 * 4.74 / 1.732 * 1.01
        calc = PlasticShearStrengthIProfileCheck(cross_section, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

        v = 355 * 12.03 / 1.732 * 1.01
        calc = PlasticShearStrengthIProfileCheck(cross_section, v, axis="Vy", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

        v = 355 * 2.882 / 1.732 * 1.01
        object.__setattr__(cross_section, "fabrication_method", "welded")
        calc = PlasticShearStrengthIProfileCheck(cross_section, v, axis="Vz", gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

    def test_report_shear(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test report output for shear force."""
        cross_section, section_properties = heb_steel_cross_section
        v = 1
        calc = PlasticShearStrengthIProfileCheck(cross_section, v, gamma_m0=1.0, section_properties=section_properties)
        assert calc.report()

    def test_check_wrong_profile(self, chs_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() raises TypeError for non-I-profile."""
        cross_section, section_properties = chs_steel_cross_section
        v = 1
        with pytest.raises(TypeError, match="The provided profile is not an I-profile"):
            PlasticShearStrengthIProfileCheck(cross_section, v, gamma_m0=1.0, section_properties=section_properties)
