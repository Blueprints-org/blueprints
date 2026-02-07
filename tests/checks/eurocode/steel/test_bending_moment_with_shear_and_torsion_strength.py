"""Tests for bending moment strength according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.bending_moment_with_shear_and_torsion_strength import (
    BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck,
)
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestBendingMomentStrengthClass1And2Check:
    """Tests for BendingMomentStrengthClass1And2Check."""

    def test_result_none(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() returns True for no bending moment."""
        cross_section, section_properties = heb_steel_cross_section
        calc = BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(
            cross_section, axis_m="My", axis_v="Vz", section_properties=section_properties
        )
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

        calc_without_section_props = BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(
            cross_section, axis_m="My", axis_v="Vz", gamma_m0=1.0
        )
        assert pytest.approx(result.unity_check) == calc_without_section_props.result().unity_check

    def test_result_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok bending moment about y-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m = 613.3 * 0.99  # Applied bending moment in kNm
        mx = 1  # Applied torsional moment in kNm
        v = 600  # Applied shear force in kN
        calc = BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(
            cross_section, m, mx, v, axis_m="My", axis_v="Vz", section_properties=section_properties
        )
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok bending moment about y-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m = -613.3 * 1.01  # Applied bending moment in kNm
        mx = 1  # Applied torsional moment in kNm
        v = 600  # Applied shear force in kN
        calc = BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(
            cross_section, m, mx, v, axis_m="My", axis_v="Vz", section_properties=section_properties
        )
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_result_no_mx_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for ok bending moment about z-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m = 627.3 * 0.99
        mx = 0  # no torsional moment
        v = -600  # Applied shear force in kN
        calc = BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(cross_section, m, mx, v, axis_m="My", axis_v="Vz", gamma_m0=1.0)
        calc.report().to_word("bending_moment_strength.docx")
        calc = BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(
            cross_section, m, mx, v, axis_m="My", axis_v="Vz", section_properties=section_properties
        )
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_no_mx_not_ok(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test result() for not ok bending moment about z-axis."""
        cross_section, section_properties = heb_steel_cross_section
        m = -627.3 * 1.01
        mx = 0  # no torsional moment
        v = -600  # Applied shear force in kN
        calc = BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(
            cross_section, m, mx, v, axis_m="My", axis_v="Vz", section_properties=section_properties
        )
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_invalid_axis(self, heb_steel_cross_section: tuple[SteelCrossSection, SectionProperties]) -> None:
        """Test ValueError is raised for invalid axis input."""
        cross_section, section_properties = heb_steel_cross_section
        with pytest.raises(ValueError):
            BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(
                cross_section, 100, 0, 0, axis_m="Ma", axis_v="Vz", section_properties=section_properties
            ).calculation_formula()
        with pytest.raises(ValueError):
            BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(
                cross_section, 100, 0, 0, axis_m="My", axis_v="Va", section_properties=section_properties
            ).calculation_formula()
        with pytest.raises(ValueError):
            BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(
                cross_section, 100, 0, 0, axis_m="Mz", axis_v="Vz", section_properties=section_properties
            ).calculation_formula()
