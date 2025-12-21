"""Tests for SteelIProfileStrengthClass3.NormalForceCheck according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.strength.steel_i_profile_strength_class_3 import SteelIProfileStrengthClass3
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile


class TestSteelIProfileStrengthClass3:
    """Tests for SteelIProfileStrengthClass3."""

    def test_check(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_force_1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=0, vy=0, vz=0, mx=0, my=0, mz=0
        )
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_force_1d, gamma_m0=1.0)
        check = calc.check()
        assert check.is_ok is True
        assert len(calc.latex()) > 0

    def test_latex_all(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test latex output for SteelIProfileStrengthClass3."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_force_1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=1, vy=1, vz=1, mx=1, my=1, mz=1
        )
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_force_1d, gamma_m0=1.0)
        check = calc.check()
        latex_output = calc.latex()
        assert check.is_ok is True
        assert len(latex_output) > 0

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
    def test_latex_only_single_force_permutations(
        self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties], forces_kwargs: dict[str, float]
    ) -> None:
        """Test latex output for SteelIProfileStrengthClass3 with 0 and 1 for all n, vy, vz, mx, my, mz."""
        (heb_profile, heb_properties) = heb_profile_and_properties

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
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_force_1d, gamma_m0=1.0)
        check = calc.check()
        latex_output = calc.latex()
        assert check.is_ok is True
        assert len(latex_output) > 0

    def test_removal_slashes_at_start(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        r"""Test that latex output does not start with '\newline'."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_force_1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", mz=1
        )
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_force_1d, gamma_m0=1.0)
        latex_output = calc.latex()
        assert latex_output[:8] != r"\newline"

    def test_latex_wrong_format(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test that wrong format raises ValueError."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_force_1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", mz=1
        )
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_force_1d, gamma_m0=1.0)

        with pytest.raises(ValueError):
            calc.latex(latex_format="table")
