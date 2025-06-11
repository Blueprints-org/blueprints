"""Tests for Table3Dot1NominalValuesHotRolledStructuralSteel class."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import (
    SteelStandardGroup,
    SteelStrengthClass,
    Table3Dot1NominalValuesHotRolledStructuralSteel,
)
from blueprints.type_alias import MM, MPA


class TestTable3Dot1NominalValuesHotRolledStructuralSteel:
    """Tests for the Table3Dot1NominalValuesHotRolledStructuralSteel class."""

    def test_valid_initialization(self) -> None:
        """Test that valid parameters create the instance successfully."""
        # Test with common steel type and thickness
        steel = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 30)
        assert steel.steel_class == SteelStrengthClass.S355
        assert steel.thickness == 30

    def test_invalid_steel_class(self) -> None:
        """Test that an invalid steel class raises ValueError."""

        # Creating a mock steel class that doesn't exist in the data
        class MockSteelClass:
            pass

        with pytest.raises(ValueError) as excinfo:
            Table3Dot1NominalValuesHotRolledStructuralSteel(MockSteelClass(), 30)  # type: ignore[arg-type]

        assert "Invalid steel class" in str(excinfo.value)

    def test_invalid_thickness_negative(self) -> None:
        """Test that negative thickness raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, -5)

        assert "Thickness must be a positive number" in str(excinfo.value)

    def test_invalid_thickness_zero(self) -> None:
        """Test that zero thickness raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 0)

        assert "Thickness must be a positive number" in str(excinfo.value)

    def test_invalid_thickness_type(self) -> None:
        """Test that non-numeric thickness raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, "30 mm")  # type: ignore[arg-type]

        assert "Thickness must be a positive number" in str(excinfo.value)

    def test_fy_small_thickness(self) -> None:
        """Test yield strength for thickness ≤ 40 mm."""
        # Test standard steel type with thickness below 40 mm
        steel = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 40)
        assert steel.fy == 355

    def test_fy_large_thickness(self) -> None:
        """Test yield strength for thickness > 40 mm and ≤ 80 mm."""
        # Test standard steel type with thickness above 40 mm
        steel = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 50)
        assert steel.fy == 335

    def test_fy_boundary_thickness(self) -> None:
        """Test yield strength at the boundary (40 mm and 40.01mm)."""
        # Test at exactly 40 mm (should use the ≤40 mm values)
        steel_at_40 = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 40)
        assert steel_at_40.fy == 355

        # Test just above 40 mm (should use the >40 mm values)
        steel_above_40 = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 40.01)
        assert steel_above_40.fy == 335

    def test_fy_too_large_thickness(self) -> None:
        """Test yield strength for thickness > 80 mm raises error."""
        with pytest.raises(ValueError) as excinfo:
            _ = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 81).fy

        assert "exceeds maximum supported value of 80 mm" in str(excinfo.value)

    def test_fy_en10219_1_above_40mm(self) -> None:
        """Test that EN 10219-1 steels with thickness > 40 mm return ValueError for fy."""
        steel = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355_MH_MLH_10219_1, 50)
        with pytest.raises(ValueError):
            _ = steel.fy

    def test_fu_small_thickness(self) -> None:
        """Test ultimate tensile strength for thickness ≤ 40 mm."""
        # Test standard steel type with thickness below 40 mm
        steel = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 40)
        assert steel.fu == 490

    def test_fu_large_thickness(self) -> None:
        """Test ultimate tensile strength for thickness > 40 mm and ≤ 80 mm."""
        # Test standard steel type with thickness above 40 mm
        steel = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 50)
        assert steel.fu == 470

    def test_fu_too_large_thickness(self) -> None:
        """Test ultimate tensile strength for thickness > 80 mm raises error."""
        with pytest.raises(ValueError) as excinfo:
            _ = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 90).fu

        assert "exceeds maximum supported value of 80 mm" in str(excinfo.value)

    def test_fu_boundary_thickness(self) -> None:
        """Test ultimate tensile strength at the boundary (40 mm and 40.01mm)."""
        # Test at exactly 40 mm (should use the ≤40 mm values)
        steel_at_40 = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 40)
        assert steel_at_40.fu == 490

        # Test just above 40 mm (should use the >40 mm values)
        steel_above_40 = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 40.01)
        assert steel_above_40.fu == 470

    def test_fu_en10219_1_above_40mm(self) -> None:
        """Test that EN 10219-1 steels with thickness > 40 mm return ValueError for fu."""
        steel = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355_MH_MLH_10219_1, 50)

        with pytest.raises(ValueError):
            _ = steel.fu

    def test_steel_strength_class_display_name(self) -> None:
        """Test that steel strength classes have the correct display names."""
        assert SteelStrengthClass.S355.display_name == "S 355"
        assert SteelStrengthClass.S275_M_ML_10025_4.display_name == "S 275 M/ML"
        assert SteelStrengthClass.S460_NH_NLH_10219_1.display_name == "S 460 NH/NLH"

    def test_steel_strength_class_standard_group(self) -> None:
        """Test that steel strength classes belong to the correct standard group."""
        assert SteelStrengthClass.S355.standard_group == SteelStandardGroup.EN_10025_2
        assert SteelStrengthClass.S275_M_ML_10025_4.standard_group == SteelStandardGroup.EN_10025_4
        assert SteelStrengthClass.S355_MH_MLH_10219_1.standard_group == SteelStandardGroup.EN_10219_1

    @pytest.mark.parametrize(
        ("steel_class", "thickness", "expected_fy", "expected_fu"),
        [
            # EN 10025-2
            (SteelStrengthClass.S235, 30, 235, 360),
            (SteelStrengthClass.S235, 50, 215, 360),
            (SteelStrengthClass.S355, 35, 355, 490),
            (SteelStrengthClass.S355, 75, 335, 470),
            # EN 10025-3
            (SteelStrengthClass.S275_N_NL_10025_3, 20, 275, 390),
            (SteelStrengthClass.S275_N_NL_10025_3, 60, 255, 370),
            # EN 10025-4
            (SteelStrengthClass.S420_M_ML_10025_4, 10, 420, 520),
            (SteelStrengthClass.S420_M_ML_10025_4, 70, 390, 500),
            # EN 10025-5
            (SteelStrengthClass.S235_W_10025_5, 25, 235, 360),
            (SteelStrengthClass.S235_W_10025_5, 45, 215, 340),
            # EN 10025-6
            (SteelStrengthClass.S460_Q_QL_QL1_10025_6, 15, 460, 570),
            (SteelStrengthClass.S460_Q_QL_QL1_10025_6, 55, 440, 550),
            # EN 10210-1
            (SteelStrengthClass.S235_H_10210_1, 5, 235, 360),
            (SteelStrengthClass.S235_H_10210_1, 65, 215, 340),
        ],
    )
    def test_steel_strength_values(
        self,
        steel_class: SteelStrengthClass,
        thickness: MM,
        expected_fy: MPA,
        expected_fu: MPA,
    ) -> None:
        """Test that steel strength values match expected values for various classes and thicknesses."""
        steel = Table3Dot1NominalValuesHotRolledStructuralSteel(steel_class, thickness)
        assert steel.fy == expected_fy
        assert steel.fu == expected_fu

    def test_string_representation(self) -> None:
        """Test that __str__ returns the expected string format."""
        steel = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.S355, 30)
        expected_str = "S 355, t=30 mm, fy=355 N/mm², fu=490 N/mm²"
        assert str(steel) == expected_str
