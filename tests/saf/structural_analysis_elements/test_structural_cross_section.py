"""Tests for StructuralCrossSection SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_cross_section import (
    CrossSectionType,
    FormCode,
    ShapeType,
    StructuralCrossSection,
)


class TestStructuralCrossSectionValidInitialization:
    """Test valid initialization of StructuralCrossSection."""

    def test_general_cross_section(self) -> None:
        """Test General type cross-section."""
        cs = StructuralCrossSection(
            name="GEN_1",
            material="Steel",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
        )
        assert cs.name == "GEN_1"
        assert cs.cross_section_type == CrossSectionType.GENERAL
        assert cs.profile == "GEN_1"

    def test_parametric_cross_section(self) -> None:
        """Test Parametric type cross-section."""
        cs = StructuralCrossSection(
            name="CS_RECT",
            material="S235",
            cross_section_type=CrossSectionType.PARAMETRIC,
            shape=ShapeType.RECTANGULAR,
            parameters="200; 100",
        )
        assert cs.cross_section_type == CrossSectionType.PARAMETRIC
        assert cs.shape == ShapeType.RECTANGULAR

    def test_manufactured_cross_section(self) -> None:
        """Test Manufactured type cross-section."""
        cs = StructuralCrossSection(
            name="HEB180",
            material="S235",
            cross_section_type=CrossSectionType.MANUFACTURED,
            profile="HEB180",
            form_code=FormCode.HOT_ROLLED,
        )
        assert cs.cross_section_type == CrossSectionType.MANUFACTURED
        assert cs.form_code == FormCode.HOT_ROLLED

    def test_compound_cross_section(self) -> None:
        """Test Compound type cross-section."""
        cs = StructuralCrossSection(
            name="COMPOUND_1",
            material="S235;C25/30",
            cross_section_type=CrossSectionType.COMPOUND,
            shape=ShapeType.T_SECTION,
            parameters="100; 200; 300",
        )
        assert cs.cross_section_type == CrossSectionType.COMPOUND

    def test_cross_section_with_all_geometric_properties(self) -> None:
        """Test cross-section with all geometric properties."""
        cs = StructuralCrossSection(
            name="HEB180",
            material="S235",
            cross_section_type=CrossSectionType.MANUFACTURED,
            profile="HEB180",
            form_code=FormCode.HOT_ROLLED,
            a=0.065,
            iy=0.000682,
            iz=0.003831,
            it=0.0000591,
            iw=0.00015548,
            wply=0.007638,
            wplz=0.010727,
        )
        assert cs.a == 0.065
        assert cs.iy == 0.000682
        assert cs.iz == 0.003831

    def test_cross_section_with_description_id(self) -> None:
        """Test cross-section with manufacturer description ID."""
        cs = StructuralCrossSection(
            name="HEB180",
            material="S235",
            cross_section_type=CrossSectionType.MANUFACTURED,
            profile="HEB180",
            form_code=FormCode.HOT_ROLLED,
            description_id=2,
        )
        assert cs.description_id == 2

    def test_cross_section_with_uuid(self) -> None:
        """Test cross-section with UUID identifier."""
        cs = StructuralCrossSection(
            name="CS1",
            material="S235",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
            id="6bbd256e-0225-4ee5-91e5-c7ef791a33cb",
        )
        assert cs.id == "6bbd256e-0225-4ee5-91e5-c7ef791a33cb"

    def test_cross_section_multiple_materials(self) -> None:
        """Test cross-section with multiple materials."""
        cs = StructuralCrossSection(
            name="COMPOSITE",
            material="S235;C25/30;S355",
            cross_section_type=CrossSectionType.COMPOUND,
            shape=ShapeType.CUSTOM,
            parameters="100;200",
        )
        assert "S235" in cs.material
        assert "C25/30" in cs.material

    def test_i_section_parametric(self) -> None:
        """Test parametric I-section."""
        cs = StructuralCrossSection(
            name="I_SECTION",
            material="S235",
            cross_section_type=CrossSectionType.PARAMETRIC,
            shape=ShapeType.I_SECTION,
            parameters="100; 50; 200; 150",
        )
        assert cs.shape == ShapeType.I_SECTION

    def test_circular_parametric(self) -> None:
        """Test parametric circular section."""
        cs = StructuralCrossSection(
            name="CIRCLE",
            material="S235",
            cross_section_type=CrossSectionType.PARAMETRIC,
            shape=ShapeType.CIRCULAR,
            parameters="100",
        )
        assert cs.shape == ShapeType.CIRCULAR

    def test_cold_formed_manufactured(self) -> None:
        """Test cold formed manufactured cross-section."""
        cs = StructuralCrossSection(
            name="CHS_100",
            material="S235",
            cross_section_type=CrossSectionType.MANUFACTURED,
            profile="CHS100x3",
            form_code=FormCode.COLD_FORMED,
        )
        assert cs.form_code == FormCode.COLD_FORMED


class TestStructuralCrossSectionValidation:
    """Test validation of StructuralCrossSection."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralCrossSection(
                name="",
                material="S235",
                cross_section_type=CrossSectionType.GENERAL,
                profile="GEN_1",
            )

    def test_empty_material_raises_error(self) -> None:
        """Test that empty material raises ValueError."""
        with pytest.raises(ValueError, match="material cannot be empty"):
            StructuralCrossSection(
                name="CS1",
                material="",
                cross_section_type=CrossSectionType.GENERAL,
                profile="GEN_1",
            )

    def test_parametric_missing_shape_raises_error(self) -> None:
        """Test that Parametric without shape raises ValueError."""
        with pytest.raises(ValueError, match="shape must be specified"):
            StructuralCrossSection(
                name="CS_RECT",
                material="S235",
                cross_section_type=CrossSectionType.PARAMETRIC,
                parameters="200; 100",
            )

    def test_parametric_missing_parameters_raises_error(self) -> None:
        """Test that Parametric without parameters raises ValueError."""
        with pytest.raises(ValueError, match="parameters must be specified"):
            StructuralCrossSection(
                name="CS_RECT",
                material="S235",
                cross_section_type=CrossSectionType.PARAMETRIC,
                shape=ShapeType.RECTANGULAR,
            )

    def test_manufactured_missing_form_code_raises_error(self) -> None:
        """Test that Manufactured without form_code raises ValueError."""
        with pytest.raises(ValueError, match="form_code must be specified"):
            StructuralCrossSection(
                name="HEB180",
                material="S235",
                cross_section_type=CrossSectionType.MANUFACTURED,
                profile="HEB180",
            )

    def test_general_missing_profile_raises_error(self) -> None:
        """Test that General without profile raises ValueError."""
        with pytest.raises(ValueError, match="profile must be specified"):
            StructuralCrossSection(
                name="GEN_1",
                material="Steel",
                cross_section_type=CrossSectionType.GENERAL,
            )

    def test_compound_missing_shape_raises_error(self) -> None:
        """Test that Compound without shape raises ValueError."""
        with pytest.raises(ValueError, match="shape must be specified"):
            StructuralCrossSection(
                name="COMPOUND_1",
                material="S235;C25/30",
                cross_section_type=CrossSectionType.COMPOUND,
                parameters="100;200",
            )

    def test_compound_missing_parameters_raises_error(self) -> None:
        """Test that Compound without parameters raises ValueError."""
        with pytest.raises(ValueError, match="parameters must be specified"):
            StructuralCrossSection(
                name="COMPOUND_1",
                material="S235;C25/30",
                cross_section_type=CrossSectionType.COMPOUND,
                shape=ShapeType.T_SECTION,
            )

    def test_negative_area_raises_error(self) -> None:
        """Test that negative area raises ValueError."""
        with pytest.raises(ValueError, match="a must be non-negative"):
            StructuralCrossSection(
                name="CS1",
                material="S235",
                cross_section_type=CrossSectionType.GENERAL,
                profile="GEN_1",
                a=-0.075,
            )

    def test_negative_iy_raises_error(self) -> None:
        """Test that negative iy raises ValueError."""
        with pytest.raises(ValueError, match="iy must be non-negative"):
            StructuralCrossSection(
                name="CS1",
                material="S235",
                cross_section_type=CrossSectionType.GENERAL,
                profile="GEN_1",
                iy=-0.000641,
            )

    def test_negative_iz_raises_error(self) -> None:
        """Test that negative iz raises ValueError."""
        with pytest.raises(ValueError, match="iz must be non-negative"):
            StructuralCrossSection(
                name="CS1",
                material="S235",
                cross_section_type=CrossSectionType.GENERAL,
                profile="GEN_1",
                iz=-0.013319,
            )

    def test_negative_it_raises_error(self) -> None:
        """Test that negative it raises ValueError."""
        with pytest.raises(ValueError, match="it must be non-negative"):
            StructuralCrossSection(
                name="CS1",
                material="S235",
                cross_section_type=CrossSectionType.GENERAL,
                profile="GEN_1",
                it=-0.0000591,
            )

    def test_negative_iw_raises_error(self) -> None:
        """Test that negative iw raises ValueError."""
        with pytest.raises(ValueError, match="iw must be non-negative"):
            StructuralCrossSection(
                name="CS1",
                material="S235",
                cross_section_type=CrossSectionType.GENERAL,
                profile="GEN_1",
                iw=-0.00015548,
            )

    def test_negative_wply_raises_error(self) -> None:
        """Test that negative wply raises ValueError."""
        with pytest.raises(ValueError, match="wply must be non-negative"):
            StructuralCrossSection(
                name="CS1",
                material="S235",
                cross_section_type=CrossSectionType.GENERAL,
                profile="GEN_1",
                wply=-0.007638,
            )

    def test_negative_wplz_raises_error(self) -> None:
        """Test that negative wplz raises ValueError."""
        with pytest.raises(ValueError, match="wplz must be non-negative"):
            StructuralCrossSection(
                name="CS1",
                material="S235",
                cross_section_type=CrossSectionType.GENERAL,
                profile="GEN_1",
                wplz=-0.010727,
            )

    def test_zero_area_valid(self) -> None:
        """Test that zero area is valid (edge case)."""
        cs = StructuralCrossSection(
            name="CS1",
            material="S235",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
            a=0.0,
        )
        assert cs.a == 0.0


class TestEnums:
    """Test enum values."""

    def test_cross_section_type_values(self) -> None:
        """Test CrossSectionType enum values."""
        assert CrossSectionType.GENERAL.value == "General"
        assert CrossSectionType.PARAMETRIC.value == "Parametric"
        assert CrossSectionType.MANUFACTURED.value == "Manufactured"
        assert CrossSectionType.COMPOUND.value == "Compound"

    def test_shape_type_values(self) -> None:
        """Test ShapeType enum values."""
        assert ShapeType.T_SECTION.value == "T Section"
        assert ShapeType.I_SECTION.value == "I Section"
        assert ShapeType.RECTANGULAR.value == "Rectangular"
        assert ShapeType.CIRCULAR.value == "Circular"

    def test_form_code_values(self) -> None:
        """Test FormCode enum values."""
        assert FormCode.HOT_ROLLED.value == "1"
        assert FormCode.COLD_FORMED.value == "2"


class TestStructuralCrossSectionImmutability:
    """Test immutability of StructuralCrossSection."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        cs = StructuralCrossSection(
            name="CS1",
            material="S235",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
        )
        with pytest.raises(Exception):
            cs.name = "CS2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that cross-section can be used in sets."""
        cs = StructuralCrossSection(
            name="CS1",
            material="S235",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
        )
        cs_set = {cs}
        assert cs in cs_set


class TestStructuralCrossSectionEquality:
    """Test equality of StructuralCrossSection."""

    def test_equal_cross_sections(self) -> None:
        """Test that identical cross-sections are equal."""
        cs1 = StructuralCrossSection(
            name="CS1",
            material="S235",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
        )
        cs2 = StructuralCrossSection(
            name="CS1",
            material="S235",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
        )
        assert cs1 == cs2

    def test_unequal_cross_sections_different_names(self) -> None:
        """Test that cross-sections with different names are not equal."""
        cs1 = StructuralCrossSection(
            name="CS1",
            material="S235",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
        )
        cs2 = StructuralCrossSection(
            name="CS2",
            material="S235",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
        )
        assert cs1 != cs2

    def test_unequal_cross_sections_different_types(self) -> None:
        """Test that cross-sections with different types are not equal."""
        cs1 = StructuralCrossSection(
            name="CS1",
            material="S235",
            cross_section_type=CrossSectionType.GENERAL,
            profile="GEN_1",
        )
        cs2 = StructuralCrossSection(
            name="CS1",
            material="S235",
            cross_section_type=CrossSectionType.PARAMETRIC,
            shape=ShapeType.RECTANGULAR,
            parameters="200; 100",
        )
        assert cs1 != cs2
