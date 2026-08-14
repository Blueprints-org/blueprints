"""Tests for CheckStrengthCompressionClass123 according to Eurocode 3."""

import pytest

from blueprints.checks.eurocode.steel.strength_compression import CheckStrengthCompressionClass123
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrengthCompressionClass123:
    """Tests for CheckStrengthCompressionClass123."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no normal force."""
        n = 0
        calc = CheckStrengthCompressionClass123(heb_steel_cross_section, n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

    def test_result_compression_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok compression load."""
        n = -355 * 14908 / 1.0 / 1e3 * 0.99
        calc = CheckStrengthCompressionClass123(heb_steel_cross_section, n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_compression_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok compression load."""
        n = -355 * 14908 / 1.0 / 1e3 * 1.01
        calc = CheckStrengthCompressionClass123(heb_steel_cross_section, n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_positive_compression(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for for positive compression load (tension)."""
        n = 100
        with pytest.raises(ValueError):
            _ = CheckStrengthCompressionClass123(heb_steel_cross_section, n, gamma_m0=1.0)

    def test_report_compression(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test report output for compression."""
        n = -100
        calc = CheckStrengthCompressionClass123(heb_steel_cross_section, n, gamma_m0=1.0)
        assert calc.report()

    def test_source_docs(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test source_docs() method."""
        n = -100
        calc = CheckStrengthCompressionClass123(heb_steel_cross_section, n, gamma_m0=1.0)
        docs = calc.source_docs()
        assert isinstance(docs, list)
        assert len(docs) == 1
