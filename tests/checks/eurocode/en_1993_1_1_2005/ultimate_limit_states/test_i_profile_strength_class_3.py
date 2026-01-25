"""Tests for IProfileStrengthClass3.NormalForceCheck according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.i_profile_strength_class_3 import IProfileStrengthClass3
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestIProfileStrengthClass3:
    """Tests for IProfileStrengthClass3."""

    def test_check_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        cross_section, section_properties = heb_steel_cross_section
        calc = IProfileStrengthClass3(cross_section, gamma_m0=1.0, section_properties=section_properties)
        assert calc.report()

    def test_check_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        n = 1e6
        cross_section, section_properties = heb_steel_cross_section
        calc = IProfileStrengthClass3(cross_section, n=n, gamma_m0=1.0, section_properties=section_properties)
        assert calc.report()

    @pytest.mark.parametrize(
        ("n", "vy", "vz", "mx", "my", "mz"),
        [
            {"n": 0, "vy": 0, "vz": 0, "mx": 0, "my": 0, "mz": 0},  # none
            {"n": 1, "vy": 1, "vz": 1, "mx": 1, "my": 1, "mz": 1},  # all
            {"n": 1, "vy": 0, "vz": 0, "mx": 0, "my": 0, "mz": 0},  # only n tension
            {"n": -1, "vy": 0, "vz": 0, "mx": 0, "my": 0, "mz": 0},  # only n compression
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
    def test_report_only_single_force_permutations(
        self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties], n: float, vy: float, vz: float, mx: float, my: float, mz: float
    ) -> None:
        """Test report output for IProfileStrengthClass3 with 0 and 1 for all n, vy, vz, mx, my, mz."""
        cross_section, section_properties = heb_steel_cross_section
        calc = IProfileStrengthClass3(cross_section, n=n, v_y=vy, v_z=vz, m_x=mx, m_y=my, m_z=mz, gamma_m0=1.0, section_properties=section_properties)
        assert calc.result()
        assert calc.report()

    def test_check_wrong_profile(self, chs_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test check() raises TypeError for non-I-profile."""
        cross_section, section_properties = chs_steel_cross_section
        with pytest.raises(TypeError, match="The provided profile is not an I-profile"):
            IProfileStrengthClass3(cross_section, gamma_m0=1.0, section_properties=section_properties)
