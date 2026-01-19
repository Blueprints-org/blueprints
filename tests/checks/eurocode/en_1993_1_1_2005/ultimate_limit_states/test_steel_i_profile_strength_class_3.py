"""Tests for SteelIProfileStrengthClass3.NormalForceCheck according to Eurocode 3."""

import pytest

from blueprints.checks.eurocode.en_1993_1_1_2005.ultimate_limit_states.steel_i_profile_strength_class_3 import SteelIProfileStrengthClass3
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestSteelIProfileStrengthClass3:
    """Tests for SteelIProfileStrengthClass3."""

    def test_check(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test check() returns True for no normal force."""
        result_internal_force_1d = ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1")
        calc = SteelIProfileStrengthClass3(heb_steel_cross_section, result_internal_force_1d, gamma_m0=1.0)
        assert calc.report()

    def test_latex_all(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test latex output for SteelIProfileStrengthClass3."""
        result_internal_force_1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=1, vy=1, vz=1, mx=1, my=1, mz=1
        )
        calc = SteelIProfileStrengthClass3(heb_steel_cross_section, result_internal_force_1d, gamma_m0=1.0)
        assert calc.report()

    @pytest.mark.parametrize(
        "forces_kwargs",
        [
            {"n": 0, "vy": 0, "vz": 0, "mx": 0, "my": 0, "mz": 0},  # none
            {"n": 1, "vy": 1, "vz": 1, "mx": 1, "my": 1, "mz": 1},  # all
            {"n": 1, "vy": 0, "vz": 0, "mx": 0, "my": 0, "mz": 0},  # only n
            {"n": 0, "vy": 1, "vz": 0, "mx": 0, "my": 0, "mz": 0},  # only vy
            {"n": 0, "vy": 0, "vz": 1, "mx": 0, "my": 0, "mz": 0},  # only vz
            {"n": 0, "vy": 0, "vz": 0, "mx": 1, "my": 0, "mz": 0},  # only mx
            {"n": 0, "vy": 0, "vz": 0, "mx": 0, "my": 1, "mz": 0},  # only my
            {"n": 0, "vy": 0, "vz": 0, "mx": 0, "my": 0, "mz": 1},  # only mz
            {"n": 0, "vy": 0, "vz": 0, "mx": 0, "my": 1, "mz": 1},  # my and mz
            {"n": 0, "vy": 1, "vz": 1, "mx": 0, "my": 1, "mz": 1},  # my, mz and vy, vz
            {"n": 1, "vy": 0, "vz": 0, "mx": 0, "my": 1, "mz": 0},  # n and my
            {"n": 1, "vy": 0, "vz": 0, "mx": 0, "my": 0, "mz": 1},  # n and mz
        ],
    )
    def test_report_only_single_force_permutations(self, heb_steel_cross_section: SteelCrossSection, forces_kwargs: dict[str, float]) -> None:
        """Test report output for SteelIProfileStrengthClass3 with 0 and 1 for all n, vy, vz, mx, my, mz."""
        result_internal_force_1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=forces_kwargs["n"],
            vy=forces_kwargs["vy"],
            vz=forces_kwargs["vz"],
            mx=forces_kwargs["mx"],
            my=forces_kwargs["my"],
            mz=forces_kwargs["mz"],
        )
        calc = SteelIProfileStrengthClass3(heb_steel_cross_section, result_internal_force_1d, gamma_m0=1.0)
        assert calc.result()
        assert calc.report()

    def test_check_wrong_profile(self, chs_steel_cross_section: SteelCrossSection) -> None:
        """Test check() returns True for no normal force."""
        result_internal_force_1d = ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1")
        calc = SteelIProfileStrengthClass3(chs_steel_cross_section, result_internal_force_1d, gamma_m0=1.0)
        assert calc.report()
