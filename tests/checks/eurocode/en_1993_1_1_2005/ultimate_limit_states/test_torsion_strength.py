"""Tests for TorsionStrengthCheck according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.torsion_strength import TorsionStrengthCheck
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestTorsionStrengthCheck:
    """Tests for TorsionStrengthCheck."""

    def test_result_none(self, unp_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no torsion."""
        mx = 0
        cross_section, section_properties = unp_steel_cross_section
        calc = TorsionStrengthCheck(cross_section, mx, gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0.0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = TorsionStrengthCheck(cross_section, mx, gamma_m0=1.0)
        assert calc == calc_without_section_props

    def test_result_tension_ok(self, unp_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok tension load."""
        mx = -0.3896 * 0.99
        cross_section, section_properties = unp_steel_cross_section
        calc = TorsionStrengthCheck(cross_section, mx, gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_tension_not_ok(self, unp_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok tension load."""
        mx = 0.3896 * 1.01
        cross_section, section_properties = unp_steel_cross_section
        calc = TorsionStrengthCheck(cross_section, mx, gamma_m0=1.0, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()
