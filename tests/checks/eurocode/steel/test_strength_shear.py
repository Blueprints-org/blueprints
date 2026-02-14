"""Tests for shear strength checks according to Eurocode 3."""

import pytest

from blueprints.checks.eurocode.steel.strength_shear import CheckStrengthShearClass12, CheckStrengthShearClass34
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrengthShearClass12:
    """Tests for CheckStrengthShearClass12."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no shear force."""
        v = 0
        calc = CheckStrengthShearClass12(heb_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

    def test_result_shear_ok(self, heb_steel_cross_section: SteelCrossSection, heb_welded_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok shear force."""
        v = 355 * 4.74 / 1.732 * 0.99
        calc = CheckStrengthShearClass12(heb_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        v = -v
        calc = CheckStrengthShearClass12(heb_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        v = 355 * 12.03 / 1.732 * 0.99
        calc = CheckStrengthShearClass12(heb_steel_cross_section, v, axis="Vy", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

        # Test with welded fabrication method
        v = 355 * 2.882 / 1.732 * 0.99
        calc = CheckStrengthShearClass12(heb_welded_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_shear_not_ok(self, heb_steel_cross_section: SteelCrossSection, heb_welded_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok shear force."""
        v = 355 * 4.74 / 1.732 * 1.01
        calc = CheckStrengthShearClass12(heb_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

        v = 355 * 12.03 / 1.732 * 1.01
        calc = CheckStrengthShearClass12(heb_steel_cross_section, v, axis="Vy", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

        # Test with welded fabrication method
        v = 355 * 2.882 / 1.732 * 1.01
        calc = CheckStrengthShearClass12(heb_welded_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

    def test_report_shear(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test report output for shear force."""
        v = 1
        calc = CheckStrengthShearClass12(heb_steel_cross_section, v, gamma_m0=1.0)
        assert calc.report()

    def test_check_wrong_profile(self, chs_steel_cross_section: SteelCrossSection) -> None:
        """Test check() raises TypeError for non-I-profile."""
        v = 1
        with pytest.raises(NotImplementedError):
            CheckStrengthShearClass12(chs_steel_cross_section, v, gamma_m0=1.0)


class TestCheckStrengthShearClass34:
    """Tests for CheckStrengthShearClass34."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test report output for shear force."""
        v = 0
        calc = CheckStrengthShearClass34(heb_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = CheckStrengthShearClass34(heb_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        assert calc == calc_without_section_props

    def test_result_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok shear force in Vz direction."""
        v = 1379 * 0.99
        calc = CheckStrengthShearClass34(heb_steel_cross_section, v, axis="Vy", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

        v = 607 * 0.99
        calc = CheckStrengthShearClass34(heb_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok shear force."""
        v = 1379 * 1.01
        calc = CheckStrengthShearClass34(heb_steel_cross_section, v, axis="Vy", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

        v = 607 * 1.01
        calc = CheckStrengthShearClass34(heb_steel_cross_section, v, axis="Vz", gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
