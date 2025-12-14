"""Tests for StructuralMaterial SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_material import (
    MaterialType,
    StructuralMaterial,
)


class TestStructuralMaterialValidInitialization:
    """Test valid initialization of StructuralMaterial."""

    def test_steel_material_minimal(self) -> None:
        """Test minimal steel material definition."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
        )
        assert material.name == "S235"
        assert material.material_type == MaterialType.STEEL
        assert material.quality == "S235"

    def test_steel_material_complete(self) -> None:
        """Test complete steel material with all properties."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
            subtype="Hot rolled",
            unit_mass=7850.0,
            e_modulus=210000.0,
            g_modulus=81000.0,
            poisson_coefficient=0.3,
            thermal_expansion=1.2e-5,
            design_properties="Fy|235;Fu|360",
        )
        assert material.subtype == "Hot rolled"
        assert material.unit_mass == 7850.0
        assert material.e_modulus == 210000.0
        assert material.g_modulus == 81000.0
        assert material.poisson_coefficient == 0.3

    def test_concrete_material(self) -> None:
        """Test concrete material definition."""
        material = StructuralMaterial(
            name="C25/30",
            material_type=MaterialType.CONCRETE,
            quality="C25/30",
            unit_mass=2400.0,
            e_modulus=31000.0,
            poisson_coefficient=0.2,
            design_properties="fck|25;fcm|33",
        )
        assert material.material_type == MaterialType.CONCRETE
        assert material.quality == "C25/30"
        assert material.e_modulus == 31000.0

    def test_timber_material(self) -> None:
        """Test timber material definition."""
        material = StructuralMaterial(
            name="C24",
            material_type=MaterialType.TIMBER,
            quality="C24",
            unit_mass=420.0,
            e_modulus=11000.0,
            g_modulus=690.0,
        )
        assert material.material_type == MaterialType.TIMBER

    def test_aluminium_material(self) -> None:
        """Test aluminium material definition."""
        material = StructuralMaterial(
            name="6061-T6",
            material_type=MaterialType.ALUMINIUM,
            quality="6061-T6",
            unit_mass=2700.0,
            e_modulus=69000.0,
        )
        assert material.material_type == MaterialType.ALUMINIUM

    def test_masonry_material(self) -> None:
        """Test masonry material definition."""
        material = StructuralMaterial(
            name="Brick",
            material_type=MaterialType.MASONRY,
            quality="M15",
            unit_mass=1500.0,
        )
        assert material.material_type == MaterialType.MASONRY

    def test_other_material_type(self) -> None:
        """Test other material type."""
        material = StructuralMaterial(
            name="Custom",
            material_type=MaterialType.OTHER,
            quality="Custom",
        )
        assert material.material_type == MaterialType.OTHER

    def test_material_with_uuid(self) -> None:
        """Test material with UUID identifier."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
            id="12345678-1234-5678-1234-567812345678",
        )
        assert material.id == "12345678-1234-5678-1234-567812345678"

    def test_material_with_single_design_property(self) -> None:
        """Test material with single design property."""
        material = StructuralMaterial(
            name="S355",
            material_type=MaterialType.STEEL,
            quality="S355",
            design_properties="Fy|355",
        )
        assert material.design_properties == "Fy|355"

    def test_material_with_multiple_design_properties(self) -> None:
        """Test material with multiple design properties."""
        material = StructuralMaterial(
            name="S355",
            material_type=MaterialType.STEEL,
            quality="S355",
            design_properties="Fy|355;Fu|510;Elongation|15",
        )
        assert material.design_properties == "Fy|355;Fu|510;Elongation|15"

    def test_material_with_spaces_in_design_properties(self) -> None:
        """Test material with spaces in design properties."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
            design_properties="Yield Strength|235 ; Ultimate Strength|360",
        )
        assert "Yield Strength" in material.design_properties

    def test_poisson_coefficient_boundary_zero(self) -> None:
        """Test Poisson coefficient at boundary (0)."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
            poisson_coefficient=0.0,
        )
        assert material.poisson_coefficient == 0.0

    def test_poisson_coefficient_boundary_max(self) -> None:
        """Test Poisson coefficient at boundary (0.5)."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
            poisson_coefficient=0.5,
        )
        assert material.poisson_coefficient == 0.5

    def test_material_cold_formed_steel(self) -> None:
        """Test cold formed steel."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
            subtype="Cold formed",
            unit_mass=7850.0,
        )
        assert material.subtype == "Cold formed"


class TestStructuralMaterialValidation:
    """Test validation of StructuralMaterial."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralMaterial(
                name="",
                material_type=MaterialType.STEEL,
                quality="S235",
            )

    def test_empty_quality_raises_error(self) -> None:
        """Test that empty quality raises ValueError."""
        with pytest.raises(ValueError, match="quality cannot be empty"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="",
            )

    def test_negative_e_modulus_raises_error(self) -> None:
        """Test that negative e_modulus raises ValueError."""
        with pytest.raises(ValueError, match="e_modulus must be positive"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                e_modulus=-210000.0,
            )

    def test_zero_e_modulus_raises_error(self) -> None:
        """Test that zero e_modulus raises ValueError."""
        with pytest.raises(ValueError, match="e_modulus must be positive"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                e_modulus=0.0,
            )

    def test_negative_g_modulus_raises_error(self) -> None:
        """Test that negative g_modulus raises ValueError."""
        with pytest.raises(ValueError, match="g_modulus must be positive"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                g_modulus=-81000.0,
            )

    def test_poisson_coefficient_below_zero_raises_error(self) -> None:
        """Test that Poisson coefficient < 0 raises ValueError."""
        with pytest.raises(ValueError, match="poisson_coefficient must be between"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                poisson_coefficient=-0.1,
            )

    def test_poisson_coefficient_above_max_raises_error(self) -> None:
        """Test that Poisson coefficient > 0.5 raises ValueError."""
        with pytest.raises(ValueError, match="poisson_coefficient must be between"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                poisson_coefficient=0.6,
            )

    def test_negative_thermal_expansion_raises_error(self) -> None:
        """Test that negative thermal_expansion raises ValueError."""
        with pytest.raises(ValueError, match="thermal_expansion must be positive"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                thermal_expansion=-1.2e-5,
            )

    def test_zero_thermal_expansion_raises_error(self) -> None:
        """Test that zero thermal_expansion raises ValueError."""
        with pytest.raises(ValueError, match="thermal_expansion must be positive"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                thermal_expansion=0.0,
            )

    def test_negative_unit_mass_raises_error(self) -> None:
        """Test that negative unit_mass raises ValueError."""
        with pytest.raises(ValueError, match="unit_mass must be positive"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                unit_mass=-7850.0,
            )

    def test_zero_unit_mass_raises_error(self) -> None:
        """Test that zero unit_mass raises ValueError."""
        with pytest.raises(ValueError, match="unit_mass must be positive"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                unit_mass=0.0,
            )

    def test_invalid_design_properties_missing_pipe(self) -> None:
        """Test that design properties without pipe raises ValueError."""
        with pytest.raises(ValueError, match="Invalid design property format"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                design_properties="Fy355",
            )

    def test_invalid_design_properties_multiple_pipes(self) -> None:
        """Test that design properties with multiple pipes raises ValueError."""
        with pytest.raises(ValueError, match="Invalid design property format"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                design_properties="Fy|355|extra",
            )

    def test_invalid_design_properties_empty_label(self) -> None:
        """Test that design properties with empty label raises ValueError."""
        with pytest.raises(ValueError, match="Label and value cannot be empty"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                design_properties="|355",
            )

    def test_invalid_design_properties_empty_value(self) -> None:
        """Test that design properties with empty value raises ValueError."""
        with pytest.raises(ValueError, match="Label and value cannot be empty"):
            StructuralMaterial(
                name="S235",
                material_type=MaterialType.STEEL,
                quality="S235",
                design_properties="Fy|",
            )

    def test_valid_design_properties_with_semicolon_in_multiple(self) -> None:
        """Test valid multiple design properties separated by semicolons."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
            design_properties="Fy|235;Fu|360;E|210000",
        )
        assert material.design_properties == "Fy|235;Fu|360;E|210000"

    def test_valid_design_properties_with_empty_pairs(self) -> None:
        """Test that empty pairs in design properties are skipped."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
            design_properties="Fy|235;;Fu|360",
        )
        assert material.design_properties == "Fy|235;;Fu|360"


class TestEnums:
    """Test enum values."""

    def test_material_type_values(self) -> None:
        """Test MaterialType enum values."""
        assert MaterialType.CONCRETE.value == "Concrete"
        assert MaterialType.STEEL.value == "Steel"
        assert MaterialType.TIMBER.value == "Timber"
        assert MaterialType.ALUMINIUM.value == "Aluminium"
        assert MaterialType.MASONRY.value == "Masonry"
        assert MaterialType.OTHER.value == "Other"


class TestStructuralMaterialImmutability:
    """Test immutability of StructuralMaterial."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
        )
        with pytest.raises(Exception):
            material.name = "S355"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that material can be used in sets."""
        material = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
        )
        material_set = {material}
        assert material in material_set


class TestStructuralMaterialEquality:
    """Test equality of StructuralMaterial."""

    def test_equal_materials(self) -> None:
        """Test that identical materials are equal."""
        mat1 = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
        )
        mat2 = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
        )
        assert mat1 == mat2

    def test_unequal_materials_different_names(self) -> None:
        """Test that materials with different names are not equal."""
        mat1 = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
        )
        mat2 = StructuralMaterial(
            name="S355",
            material_type=MaterialType.STEEL,
            quality="S355",
        )
        assert mat1 != mat2

    def test_unequal_materials_different_types(self) -> None:
        """Test that materials with different types are not equal."""
        mat1 = StructuralMaterial(
            name="S235",
            material_type=MaterialType.STEEL,
            quality="S235",
        )
        mat2 = StructuralMaterial(
            name="S235",
            material_type=MaterialType.CONCRETE,
            quality="S235",
        )
        assert mat1 != mat2
