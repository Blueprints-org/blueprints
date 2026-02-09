"""Tests for CheckStrengthTensionClass1234 according to Eurocode 3."""

import pytest

from blueprints.checks.eurocode.steel.strength_tension import CheckStrengthTensionClass1234
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrengthTensionClass1234:
    """Tests for CheckStrengthTensionClass1234."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no normal force."""
        n = 0

        calc = CheckStrengthTensionClass1234(heb_steel_cross_section, n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0.0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthTensionClass1234(heb_steel_cross_section, n, gamma_m0=1.0)
        assert calc == calc_without_section_props

    def test_result_tension_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok tension load."""
        n = 355 * 14908 / 1.0 / 1e3 * 0.99

        calc = CheckStrengthTensionClass1234(heb_steel_cross_section, n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_tension_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok tension load."""
        n = 355 * 14908 / 1.0 / 1e3 * 1.01

        calc = CheckStrengthTensionClass1234(heb_steel_cross_section, n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_negative_tension(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for negative tension load (compression)."""
        n = -100

        calc = CheckStrengthTensionClass1234(heb_steel_cross_section, n, gamma_m0=1.0)
        with pytest.raises(ValueError):
            calc.calculation_formula()

    def test_report_tension(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test report output with summary flag for tension."""
        n = 100

        calc = CheckStrengthTensionClass1234(heb_steel_cross_section, n, gamma_m0=1.0)
        assert calc.report()
