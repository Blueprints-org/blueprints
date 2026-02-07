"""Tests for bending moment strength together with axial force according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.bending_moment_with_axial_strength import BendingMomentWithAxialStrengthClass3Check
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestBendingMomentWithAxialStrengthClass3Check:
    """Tests for BendingMomentWithAxialStrengthClass3Check."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no loading."""
        cross_section, section_properties = heb_steel_cross_section
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = BendingMomentWithAxialStrengthClass3Check(cross_section, gamma_m0=1.0)
        assert pytest.approx(result.unity_check) == calc_without_section_props.result().unity_check

    def test_result_ok_combined_loading(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok combined loading (My, Mz, N)."""
        cross_section, section_properties = heb_steel_cross_section
        my = 100 * 0.99  # Applied bending moment around y-axis in kNm
        mz = 130.37 * 0.99  # Applied bending moment around z-axis in kNm
        n = 1000 * 0.99  # Applied axial force (tension) in kN
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, my=my, mz=mz, n=n, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_not_ok_combined_loading(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok combined loading (excessive moments and axial force)."""
        cross_section, section_properties = heb_steel_cross_section
        my = 100 * 1.01  # Applied bending moment around y-axis in kNm
        mz = 130.37 * 1.01  # Applied bending moment around z-axis in kNm
        n = 1000 * 1.01  # Applied axial force (tension) in kN
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, my=my, mz=mz, n=n, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_result_ok_my_only(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok bending moment My only."""
        cross_section, section_properties = heb_steel_cross_section
        my = 200  # Applied bending moment around y-axis in kNm
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, my=my, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True

    def test_result_ok_mz_only(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok bending moment Mz only."""
        cross_section, section_properties = heb_steel_cross_section
        mz = 100  # Applied bending moment around z-axis in kNm
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, mz=mz, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True

    def test_result_ok_tension(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok tension force only."""
        cross_section, section_properties = heb_steel_cross_section
        n = 1000  # Applied tensile axial force in kN
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, n=n, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True

    def test_result_ok_compression(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok compression force only."""
        cross_section, section_properties = heb_steel_cross_section
        n = -1000  # Applied compressive axial force in kN
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, n=n, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check < 1.0

    def test_result_my_and_tension(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for combined My and tension."""
        cross_section, section_properties = heb_steel_cross_section
        my = 150
        n = 800
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, my=my, n=n, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert calc.report()

    def test_result_mz_and_compression(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for combined Mz and compression."""
        cross_section, section_properties = heb_steel_cross_section
        mz = 80
        n = -600
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, mz=mz, n=n, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert calc.report()

    def test_negative_moments(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() handles negative moment values correctly (absolute values used)."""
        cross_section, section_properties = heb_steel_cross_section
        my = -100
        mz = -50
        n = -500
        calc = BendingMomentWithAxialStrengthClass3Check(cross_section, my=my, mz=mz, n=n, section_properties=section_properties)
        result = calc.result()
        assert result.is_ok is True
        assert calc.report()
