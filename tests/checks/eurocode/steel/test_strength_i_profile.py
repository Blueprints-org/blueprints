"""Tests for CheckStrengthIProfileClass3.NormalForceCheck according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.strength_i_profile import CheckStrengthIProfileClass3
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrengthIProfileClass3:
    """Tests for CheckStrengthIProfileClass3."""

    def test_check_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        cross_section, section_properties = heb_steel_cross_section

        calc = CheckStrengthIProfileClass3(cross_section, gamma_m0=1.0, section_properties=section_properties)
        assert calc.result().is_ok

    def test_check_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        n = 1e6
        cross_section, section_properties = heb_steel_cross_section
        calc = CheckStrengthIProfileClass3(cross_section, n=n, gamma_m0=1.0, section_properties=section_properties)
        assert not calc.result().is_ok
        assert calc.report()

    def test_check_no_section_properties(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() works without provided section properties."""
        cross_section, _ = heb_steel_cross_section
        calc_without_section_props = CheckStrengthIProfileClass3(cross_section, gamma_m0=1.0)
        assert calc_without_section_props.result()

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
    def test_permutations(
        self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties], n: float, vy: float, vz: float, mx: float, my: float, mz: float
    ) -> None:
        """Test report output for CheckStrengthIProfileClass3 with 0 and 1 for all n, vy, vz, mx, my, mz."""
        cross_section, section_properties = heb_steel_cross_section
        calc = CheckStrengthIProfileClass3(
            cross_section, n=n, v_y=vy, v_z=vz, m_x=mx, m_y=my, m_z=mz, gamma_m0=1.0, section_properties=section_properties
        )
        assert calc.result()
        assert calc.report()

    def test_check_wrong_profile(self, chs_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() raises TypeError for non-I-profile."""
        cross_section, section_properties = chs_steel_cross_section
        with pytest.raises(TypeError, match="The provided profile is not an I-profile"):
            CheckStrengthIProfileClass3(cross_section, gamma_m0=1.0, section_properties=section_properties)

    def test_ignoring_checks(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test ignore_checks works."""
        n = 1e6
        cross_section, section_properties = heb_steel_cross_section
        calc = CheckStrengthIProfileClass3(
            cross_section,
            n=n,
            gamma_m0=1.0,
            section_properties=section_properties,
            ignore_checks=["tension"],
        )
        assert calc.result().is_ok
