"""Tests for CompressionStrengthClass123Check according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.compression_strength import CompressionStrengthClass123Check
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCompressionStrengthClass123Check:
    """Tests for CompressionStrengthClass123Check."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no normal force."""
        cross_section, section_properties = heb_steel_cross_section
        n = 0
        calc = CompressionStrengthClass123Check(cross_section, n, gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CompressionStrengthClass123Check(cross_section, n, gamma_m0=1.0)
        assert pytest.approx(result.unity_check) == calc_without_section_props.result().unity_check

    def test_result_compression_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok compression load."""
        cross_section, section_properties = heb_steel_cross_section
        n = -355 * 14908 / 1.0 / 1e3 * 0.99
        calc = CompressionStrengthClass123Check(cross_section, n, gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_compression_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok compression load."""
        cross_section, section_properties = heb_steel_cross_section
        n = -355 * 14908 / 1.0 / 1e3 * 1.01
        calc = CompressionStrengthClass123Check(cross_section, n, gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_positive_compression(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for for positive compression load (tension)."""
        cross_section, section_properties = heb_steel_cross_section
        n = 100
        calc = CompressionStrengthClass123Check(cross_section, n, gamma_m0=1.0, section_properties=section_properties)
        with pytest.raises(ValueError):
            calc.calculation_formula()
