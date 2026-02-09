"""Tests for CheckStrengthIProfileClass3 according to Eurocode 3."""

import pytest

from blueprints.checks.eurocode.steel.strength_i_profile import CheckStrengthIProfileClass3
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrengthIProfileClass3:
    """Tests for CheckStrengthIProfileClass3."""

    def test_check_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test check() returns True for no normal force."""
        calc = CheckStrengthIProfileClass3(heb_steel_cross_section, gamma_m0=1.0)
        assert calc.result().is_ok

    def test_check_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test check() returns False for large force."""
        n = 1e6

        calc = CheckStrengthIProfileClass3(heb_steel_cross_section, n=n, gamma_m0=1.0)
        assert not calc.result().is_ok
        assert calc.report()

    @pytest.mark.parametrize(
        ("n", "vy", "vz", "mx", "my", "mz"),
        [
            (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),  # none
            (1.0, 1.0, 1.0, 1.0, 1.0, 1.0),  # all
            (1.0, 0.0, 0.0, 0.0, 0.0, 0.0),  # only n tension
            (-1.0, 0.0, 0.0, 0.0, 0.0, 0.0),  # only n compression
            (0.0, 1.0, 0.0, 0.0, 0.0, 0.0),  # only vy
            (0.0, 0.0, 1.0, 0.0, 0.0, 0.0),  # only vz
            (0.0, 0.0, 0.0, 1.0, 0.0, 0.0),  # only mx
            (0.0, 0.0, 0.0, 0.0, 1.0, 0.0),  # only my
            (0.0, 0.0, 0.0, 0.0, 0.0, 1.0),  # only mz
            (0.0, 0.0, 0.0, 0.0, 1.0, 1.0),  # my and mz
            (0.0, 1.0, 1.0, 0.0, 1.0, 1.0),  # my, mz and vy, vz
            (1.0, 0.0, 0.0, 0.0, 1.0, 0.0),  # n and my
            (1.0, 0.0, 0.0, 0.0, 0.0, 1.0),  # n and mz
        ],
    )
    def test_permutations(self, heb_steel_cross_section: SteelCrossSection, n: float, vy: float, vz: float, mx: float, my: float, mz: float) -> None:
        """Test report output for CheckStrengthIProfileClass3 with 0 and 1 for all n, vy, vz, mx, my, mz."""
        calc = CheckStrengthIProfileClass3(heb_steel_cross_section, n=n, v_y=vy, v_z=vz, m_x=mx, m_y=my, m_z=mz, gamma_m0=1.0)
        assert calc.result()
        assert calc.report()

    def test_check_wrong_profile(self, chs_steel_cross_section: SteelCrossSection) -> None:
        """Test check() raises TypeError for non-I-profile."""
        with pytest.raises(TypeError, match="The provided profile is not an I-profile"):
            CheckStrengthIProfileClass3(chs_steel_cross_section, gamma_m0=1.0)

    def test_ignoring_checks(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test ignore_checks works."""
        n = 1e6

        calc = CheckStrengthIProfileClass3(
            heb_steel_cross_section,
            n=n,
            gamma_m0=1.0,
            ignore_checks=["tension"],
        )
        assert calc.result().is_ok
