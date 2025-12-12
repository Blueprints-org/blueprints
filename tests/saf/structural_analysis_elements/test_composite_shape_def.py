"""Tests for CompositeShapeDef SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.composite_shape_def import (
    CompositeShapeDef,
    PolygonContour,
)


class TestPolygonContourCreation:
    """Test PolygonContour NamedTuple creation."""

    def test_solid_polygon(self) -> None:
        """Test creating a solid polygon contour."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
            ),
            material_name="S235",
            is_opening=False,
        )
        assert contour.material_name == "S235"
        assert not contour.is_opening
        assert len(contour.coordinates) == 4

    def test_opening_polygon(self) -> None:
        """Test creating an opening polygon contour."""
        contour = PolygonContour(
            coordinates=(
                (-20.0, 100.0),
                (-20.0, 120.0),
                (20.0, 120.0),
                (20.0, 100.0),
            ),
            is_opening=True,
        )
        assert contour.is_opening
        assert contour.material_name == ""

    def test_polygon_default_values(self) -> None:
        """Test polygon with default values."""
        contour = PolygonContour(
            coordinates=(
                (0.0, 0.0),
                (0.0, 100.0),
                (100.0, 100.0),
                (100.0, 0.0),
            ),
        )
        assert contour.material_name == ""
        assert not contour.is_opening


class TestCompositeShapeDefValidInitialization:
    """Test valid initialization of CompositeShapeDef."""

    def test_simple_rectangular_shape(self) -> None:
        """Test simple rectangular composite shape."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        assert shape.name == "GEN_1"
        assert len(shape.polygons) == 1

    def test_shape_with_opening(self) -> None:
        """Test shape with solid polygon and opening."""
        solid = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        opening = PolygonContour(
            coordinates=(
                (-20.0, 100.0),
                (-20.0, 120.0),
                (20.0, 120.0),
                (20.0, 100.0),
                (-20.0, 100.0),
            ),
            is_opening=True,
        )
        shape = CompositeShapeDef(
            name="GEN_2",
            polygons=(solid, opening),
        )
        assert len(shape.polygons) == 2

    def test_shape_with_multiple_solids_and_openings(self) -> None:
        """Test shape with multiple solid polygons and openings."""
        solid1 = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        opening1 = PolygonContour(
            coordinates=(
                (-20.0, 100.0),
                (-20.0, 120.0),
                (20.0, 120.0),
                (20.0, 100.0),
                (-20.0, 100.0),
            ),
            is_opening=True,
        )
        solid2 = PolygonContour(
            coordinates=(
                (150.0, 50.0),
                (150.0, 150.0),
                (200.0, 150.0),
                (200.0, 50.0),
                (150.0, 50.0),
            ),
            material_name="C25/30",
        )
        shape = CompositeShapeDef(
            name="GEN_3",
            polygons=(solid1, opening1, solid2),
        )
        assert len(shape.polygons) == 3

    def test_triangular_polygon(self) -> None:
        """Test shape with triangular polygon (3 coordinates)."""
        contour = PolygonContour(
            coordinates=(
                (0.0, 0.0),
                (100.0, 0.0),
                (50.0, 100.0),
                (0.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="TRIANGLE",
            polygons=(contour,),
        )
        assert len(shape.polygons) == 1

    def test_hexagonal_polygon(self) -> None:
        """Test shape with hexagonal polygon."""
        contour = PolygonContour(
            coordinates=(
                (-50.0, 0.0),
                (-100.0, 50.0),
                (-100.0, 150.0),
                (-50.0, 200.0),
                (50.0, 200.0),
                (100.0, 150.0),
                (100.0, 50.0),
                (50.0, 0.0),
                (-50.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="HEXAGON",
            polygons=(contour,),
        )
        assert len(shape.polygons) == 1

    def test_maximum_polygons(self) -> None:
        """Test shape with maximum allowed polygons (99)."""
        polygons = []

        # Create solid first polygon
        solid_first = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        polygons.append(solid_first)

        # Create 98 opening polygons
        for i in range(1, 99):
            contour = PolygonContour(
                coordinates=(
                    (float(i * 10), 0.0),
                    (float(i * 10), 100.0),
                    (float(i * 10 + 50), 100.0),
                    (float(i * 10), 0.0),
                ),
                is_opening=True,
            )
            polygons.append(contour)

        shape = CompositeShapeDef(
            name="MAX_POLY",
            polygons=tuple(polygons),
        )
        assert len(shape.polygons) == 99

    def test_shape_with_uuid(self) -> None:
        """Test shape with UUID identifier."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
            id="12345678-1234-5678-1234-567812345678",
        )
        assert shape.id == "12345678-1234-5678-1234-567812345678"

    def test_different_material_references(self) -> None:
        """Test shape with multiple different material references."""
        steel = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 100.0),
                (0.0, 100.0),
                (0.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        concrete = PolygonContour(
            coordinates=(
                (0.0, 0.0),
                (0.0, 100.0),
                (100.0, 100.0),
                (100.0, 0.0),
                (0.0, 0.0),
            ),
            material_name="C25/30",
        )
        shape = CompositeShapeDef(
            name="COMPOSITE",
            polygons=(steel, concrete),
        )
        assert shape.polygons[0].material_name == "S235"
        assert shape.polygons[1].material_name == "C25/30"


class TestCompositeShapeDefValidation:
    """Test validation of CompositeShapeDef."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
            ),
            material_name="S235",
        )
        with pytest.raises(ValueError, match="name cannot be empty"):
            CompositeShapeDef(
                name="",
                polygons=(contour,),
            )

    def test_no_polygons_raises_error(self) -> None:
        """Test that empty polygons tuple raises ValueError."""
        with pytest.raises(ValueError, match="polygons must contain at least one"):
            CompositeShapeDef(
                name="GEN_1",
                polygons=(),
            )

    def test_too_many_polygons_raises_error(self) -> None:
        """Test that more than 99 polygons raises ValueError."""
        polygons = []
        for i in range(100):
            if i == 0:
                contour = PolygonContour(
                    coordinates=(
                        (-100.0, 0.0),
                        (-100.0, 200.0),
                        (100.0, 200.0),
                        (100.0, 0.0),
                    ),
                    material_name="S235",
                )
            else:
                contour = PolygonContour(
                    coordinates=(
                        (float(i * 10), 0.0),
                        (float(i * 10), 100.0),
                        (float(i * 10 + 50), 100.0),
                        (float(i * 10), 0.0),
                    ),
                    is_opening=True,
                )
            polygons.append(contour)

        with pytest.raises(ValueError, match="Maximum 99 polygons"):
            CompositeShapeDef(
                name="OVERFLOW",
                polygons=tuple(polygons),
            )

    def test_polygon_with_less_than_3_coordinates_raises_error(self) -> None:
        """Test that polygon with < 3 coordinates raises ValueError."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
            ),
            material_name="S235",
        )
        with pytest.raises(ValueError, match="at least 3 coordinates"):
            CompositeShapeDef(
                name="INVALID",
                polygons=(contour,),
            )

    def test_unclosed_polygon_raises_error(self) -> None:
        """Test that unclosed polygon raises ValueError."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
            ),
            material_name="S235",
        )
        with pytest.raises(ValueError, match="must be closed"):
            CompositeShapeDef(
                name="UNCLOSED",
                polygons=(contour,),
            )

    def test_solid_polygon_without_material_raises_error(self) -> None:
        """Test that solid polygon without material raises ValueError."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="",
        )
        with pytest.raises(ValueError, match="must have a material_name"):
            CompositeShapeDef(
                name="NO_MAT",
                polygons=(contour,),
            )

    def test_only_openings_raises_error(self) -> None:
        """Test that only opening polygons (no solid) raises ValueError."""
        opening1 = PolygonContour(
            coordinates=(
                (-20.0, 100.0),
                (-20.0, 120.0),
                (20.0, 120.0),
                (20.0, 100.0),
                (-20.0, 100.0),
            ),
            is_opening=True,
        )
        opening2 = PolygonContour(
            coordinates=(
                (30.0, 100.0),
                (30.0, 120.0),
                (70.0, 120.0),
                (70.0, 100.0),
                (30.0, 100.0),
            ),
            is_opening=True,
        )
        with pytest.raises(ValueError, match="At least one solid polygon"):
            CompositeShapeDef(
                name="ONLY_OPENINGS",
                polygons=(opening1, opening2),
            )

    def test_non_numeric_coordinates_raises_error(self) -> None:
        """Test that non-numeric coordinates raise ValueError."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                ("invalid", 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),  #  type: ignore[arg-type]
            material_name="S235",
        )
        with pytest.raises(ValueError, match="numeric values"):
            CompositeShapeDef(
                name="INVALID",
                polygons=(contour,),
            )


class TestCompositeShapeDefContourValidation:
    """Test contour string validation methods."""

    def test_validate_contour_string_valid(self) -> None:
        """Test valid contour string parsing."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        coords = shape.validate_contour_string("-100.0; 0.0|-100.0; 200.0|100.0; 200.0|100.0; 0.0|-100.0; 0.0")
        assert len(coords) == 5
        assert coords[0] == (-100.0, 0.0)

    def test_validate_contour_string_empty_raises_error(self) -> None:
        """Test that empty contour string raises ValueError."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        with pytest.raises(ValueError, match="cannot be empty"):
            shape.validate_contour_string("")

    def test_validate_contour_string_invalid_format_no_semicolon(self) -> None:
        """Test that missing semicolon raises ValueError."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        with pytest.raises(ValueError, match="Expected"):
            shape.validate_contour_string("-100.0, 0.0|-100.0; 200.0")

    def test_validate_contour_string_non_numeric_raises_error(self) -> None:
        """Test that non-numeric values raise ValueError."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        with pytest.raises(ValueError, match="non-numeric"):
            shape.validate_contour_string("abc; def|xyz; 123")

    def test_validate_contour_string_less_than_3_points(self) -> None:
        """Test that less than 3 coordinate pairs raises ValueError."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        with pytest.raises(ValueError, match="At least 3 coordinate pairs"):
            shape.validate_contour_string("-100.0; 0.0|-100.0; 200.0")


class TestCompositeShapeDefImmutability:
    """Test immutability of CompositeShapeDef."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        with pytest.raises(Exception):
            shape.name = "GEN_2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that shape can be used in sets."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        shape_set = {shape}
        assert shape in shape_set


class TestCompositeShapeDefEquality:
    """Test equality of CompositeShapeDef."""

    def test_equal_shapes(self) -> None:
        """Test that identical shapes are equal."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape1 = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        shape2 = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        assert shape1 == shape2

    def test_unequal_shapes_different_names(self) -> None:
        """Test that shapes with different names are not equal."""
        contour = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        shape1 = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour,),
        )
        shape2 = CompositeShapeDef(
            name="GEN_2",
            polygons=(contour,),
        )
        assert shape1 != shape2

    def test_unequal_shapes_different_polygons(self) -> None:
        """Test that shapes with different polygons are not equal."""
        contour1 = PolygonContour(
            coordinates=(
                (-100.0, 0.0),
                (-100.0, 200.0),
                (100.0, 200.0),
                (100.0, 0.0),
                (-100.0, 0.0),
            ),
            material_name="S235",
        )
        contour2 = PolygonContour(
            coordinates=(
                (-200.0, 0.0),
                (-200.0, 300.0),
                (200.0, 300.0),
                (200.0, 0.0),
                (-200.0, 0.0),
            ),
            material_name="S235",
        )
        shape1 = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour1,),
        )
        shape2 = CompositeShapeDef(
            name="GEN_1",
            polygons=(contour2,),
        )
        assert shape1 != shape2
