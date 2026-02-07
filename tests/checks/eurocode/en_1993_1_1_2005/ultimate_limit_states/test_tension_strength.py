"""Tests for TensionStrengthCheck according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.tension_strength import TensionStrengthCheck
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestTensionStrengthCheck:
    """Tests for TensionStrengthCheck."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no normal force."""
        n = 0
        cross_section, section_properties = heb_steel_cross_section
        calc = TensionStrengthCheck(cross_section, n, gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0.0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = TensionStrengthCheck(cross_section, n, gamma_m0=1.0)
        assert calc == calc_without_section_props

    def test_result_tension_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok tension load."""
        n = 355 * 14908 / 1.0 / 1e3 * 0.99
        cross_section, section_properties = heb_steel_cross_section
        calc = TensionStrengthCheck(cross_section, n, gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_tension_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok tension load."""
        n = 355 * 14908 / 1.0 / 1e3 * 1.01
        cross_section, section_properties = heb_steel_cross_section
        calc = TensionStrengthCheck(cross_section, n, gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_negative_tension(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for negative tension load (compression)."""
        n = -100
        cross_section, section_properties = heb_steel_cross_section
        calc = TensionStrengthCheck(cross_section, n, gamma_m0=1.0, section_properties=section_properties)
        with pytest.raises(ValueError):
            calc.calculation_formula()

    def test_report_tension(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test report output with summary flag for tension."""
        n = 100
        cross_section, section_properties = heb_steel_cross_section
        calc = TensionStrengthCheck(cross_section, n, gamma_m0=1.0, section_properties=section_properties)
        assert calc.report()
