"""Tests for NormalForceClass123Check according to Eurocode 3."""

import pytest

from blueprints.checks.eurocode.en_1993_1_1_2005.ultimate_limit_states.normal_force import NormalForceClass123
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestSteelIProfileStrengthClass3NormalForce:
    """Tests for NormalForceClass123."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no normal force."""
        result_internal_force_1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=0
        )
        calc = NormalForceClass123(heb_steel_cross_section, result_internal_force_1d, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided is None
        assert result.required is None
        assert calc.report()

    def test_result_tension_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok tension load."""
        load_tension = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=355 * 14908 / 1.0 / 1e3 * 0.99
        )  # 99% of capacity
        calc = NormalForceClass123(heb_steel_cross_section, load_tension, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_tension_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok tension load."""
        load_tension = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=355 * 14908 / 1.0 / 1e3 * 1.01
        )  # 101% of capacity
        calc = NormalForceClass123(heb_steel_cross_section, load_tension, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_result_compression_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok compression load."""
        load_compression = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=-355 * 14908 / 1.0 / 1e3 * 0.99
        )  # 99% of capacity
        calc = NormalForceClass123(heb_steel_cross_section, load_compression, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_compression_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok compression load."""
        load_compression = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=-355 * 14908 / 1.0 / 1e3 * 1.01
        )  # 101% of capacity
        calc = NormalForceClass123(heb_steel_cross_section, load_compression, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

    def test_report_compression(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test long report output."""
        load_compression = ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=-100)
        calc = NormalForceClass123(heb_steel_cross_section, load_compression, gamma_m0=1.0)
        assert calc.report()

    def test_report_tension(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test report output with summary flag for tension."""
        load_tension = ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=100)
        calc = NormalForceClass123(heb_steel_cross_section, load_tension, gamma_m0=1.0)
        assert calc.report()
