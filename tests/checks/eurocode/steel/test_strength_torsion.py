"""Tests for CheckStrengthStVenantTorsionClass1234 according to Eurocode 3."""

import pytest

from blueprints.checks.eurocode.steel.strength_torsion import CheckStrengthStVenantTorsionClass1234
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrengthStVenantTorsionClass1234:
    """Tests for CheckStrengthStVenantTorsionClass1234."""

    def test_result_none(self, unp_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no torsion."""
        m_x = 0
        calc = CheckStrengthStVenantTorsionClass1234(unp_steel_cross_section, m_x, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0.0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthStVenantTorsionClass1234(unp_steel_cross_section, m_x, gamma_m0=1.0)
        assert calc == calc_without_section_props

    def test_result_tension_ok(self, unp_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok tension load."""
        m_x = -0.3896 * 0.99
        calc = CheckStrengthStVenantTorsionClass1234(unp_steel_cross_section, m_x, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_tension_not_ok(self, unp_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok tension load."""
        m_x = 0.3896 * 1.01
        calc = CheckStrengthStVenantTorsionClass1234(unp_steel_cross_section, m_x, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_source_docs(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test source_docs() method."""
        m_x = 1
        calc = CheckStrengthStVenantTorsionClass1234(heb_steel_cross_section, m_x=1, gamma_m0=1.0)
        docs = calc.source_docs()
        assert isinstance(docs, list)
        assert len(docs) == 1