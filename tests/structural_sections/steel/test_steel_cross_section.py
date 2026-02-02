"""Test the SteelCrossSection class."""

import pytest
from shapely.geometry import Point

from blueprints.structural_sections.steel.steel_cross_section import FabricationMethod, SteelCrossSection


class TestSteelCrossSection:
    """Test suite for the SteelCrossSection class."""

    def test_name(self, steel_cross_section_hot_formed: SteelCrossSection) -> None:
        """Test that the SteelCrossSection name works correctly."""
        assert steel_cross_section_hot_formed.profile.name == "IPE100"

    def test_area(self, steel_cross_section_hot_formed: SteelCrossSection) -> None:
        """Test that the SteelCrossSection area works correctly."""
        assert steel_cross_section_hot_formed.profile.area == pytest.approx(1032.6, 1e-3)

    def test_perimeter(self, steel_cross_section_hot_formed: SteelCrossSection) -> None:
        """Test that the SteelCrossSection perimeter works correctly."""
        assert steel_cross_section_hot_formed.profile.perimeter == pytest.approx(399.762, 1e-3)

    def test_centroid(self, steel_cross_section_hot_formed: SteelCrossSection) -> None:
        """Test that the SteelCrossSection centroid works correctly."""
        assert steel_cross_section_hot_formed.profile.centroid.equals_exact(Point(0.0, 0.0), 1e-3)

    def test_yield_strength(self, steel_cross_section_hot_formed: SteelCrossSection) -> None:
        """Test that the SteelCrossSection yield strength is calculated correctly."""
        expected_yield_strength: float = 275.0  # MPa for S275 steel
        assert steel_cross_section_hot_formed.yield_strength == pytest.approx(expected_yield_strength, 1e-3)

    def test_ultimate_strength(self, steel_cross_section_hot_formed: SteelCrossSection) -> None:
        """Test that the SteelCrossSection ultimate strength is calculated correctly."""
        expected_ultimate_strength: float = 430.0  # MPa for S275 steel
        assert steel_cross_section_hot_formed.ultimate_strength == pytest.approx(expected_ultimate_strength, 1e-3)

    def test_just_ok_yield_strength(self, thick_40_mm_flange_i_profile: SteelCrossSection) -> None:
        """Test that the SteelCrossSection yield strength is calculated correctly."""
        expected_yield_strength: float = 275.0  # MPa for S275 steel
        assert thick_40_mm_flange_i_profile.yield_strength == pytest.approx(expected_yield_strength, 1e-3)

    def test_just_ok_ultimate_strength(self, thick_40_mm_flange_i_profile: SteelCrossSection) -> None:
        """Test that the SteelCrossSection ultimate strength is calculated correctly."""
        expected_ultimate_strength: float = 430.0  # MPa for S275 steel
        assert thick_40_mm_flange_i_profile.ultimate_strength == pytest.approx(expected_ultimate_strength, 1e-3)

    def test_reduced_yield_strength(self, thick_41_mm_flange_i_profile: SteelCrossSection) -> None:
        """Test that the SteelCrossSection yield strength is calculated correctly."""
        expected_yield_strength: float = 255.0  # MPa for S275 steel
        assert thick_41_mm_flange_i_profile.yield_strength == pytest.approx(expected_yield_strength, 1e-3)

    def test_reduced_ultimate_strength(self, thick_41_mm_flange_i_profile: SteelCrossSection) -> None:
        """Test that the SteelCrossSection ultimate strength is calculated correctly."""
        expected_ultimate_strength: float = 410.0  # MPa for S275 steel
        assert thick_41_mm_flange_i_profile.ultimate_strength == pytest.approx(expected_ultimate_strength, 1e-3)

    def test_weight_per_meter(self, steel_cross_section_hot_formed: SteelCrossSection) -> None:
        """Test that the SteelCrossSection weight per meter is calculated correctly."""
        expected_weight: float = steel_cross_section_hot_formed.profile.area * steel_cross_section_hot_formed.material.density * 1e-6
        assert steel_cross_section_hot_formed.weight_per_meter == pytest.approx(expected_weight, 1e-3)

    def test_default_fabrication_method_hot_rolled(self, steel_cross_section_hot_formed: SteelCrossSection) -> None:
        """Test that the SteelCrossSection fabrication method is set correctly for hot-rolled profiles."""
        assert steel_cross_section_hot_formed.fabrication_method == FabricationMethod.HOT_ROLLED

    def test_default_fabrication_method_hot_rolled_corroded(self, steel_cross_section_corroded: SteelCrossSection) -> None:
        """Test that the SteelCrossSection fabrication method is set correctly for hot-rolled profiles with corrosion."""
        assert steel_cross_section_corroded.fabrication_method == FabricationMethod.HOT_ROLLED

    def test_default_fabrication_method_cold_formed(self, steel_cross_section_cold_formed: SteelCrossSection) -> None:
        """Test that the SteelCrossSection fabrication method is set correctly for cold-formed profiles."""
        assert steel_cross_section_cold_formed.fabrication_method == FabricationMethod.COLD_FORMED

    def test_default_fabrication_method_cold_formed_corroded(self, steel_cross_section_cold_formed_corroded: SteelCrossSection) -> None:
        """Test that the SteelCrossSection fabrication method is set correctly for cold-formed profiles with corrosion."""
        assert steel_cross_section_cold_formed_corroded.fabrication_method == FabricationMethod.COLD_FORMED

    def test_default_fabrication_method_welded(self, steel_cross_section_welded: SteelCrossSection) -> None:
        """Test that the SteelCrossSection fabrication method is set correctly for welded profiles."""
        assert steel_cross_section_welded.fabrication_method == FabricationMethod.WELDED

    def test_default_fabrication_method_welded_corroded(self, steel_cross_section_welded_corroded: SteelCrossSection) -> None:
        """Test that the SteelCrossSection fabrication method is set correctly for welded profiles with corrosion."""
        assert steel_cross_section_welded_corroded.fabrication_method == FabricationMethod.WELDED

    def test_default_fabrication_method_not_set(self, steel_cross_section_fabrication_not_set: SteelCrossSection) -> None:
        """Test that the SteelCrossSection fabrication method is set correctly when not set."""
        assert steel_cross_section_fabrication_not_set.fabrication_method is None
