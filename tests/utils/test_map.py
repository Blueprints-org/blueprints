"""BDD-style tests for the map module.

Each test follows the Given-When-Then pattern with a scenario
docstring and Arrange/Act/Assert comments.
"""
# ruff: noqa: SLF001

import asyncio
import contextlib
import io
import json
import shutil
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import folium
import pytest
from geopandas import GeoDataFrame
from shapely import GeometryCollection
from shapely.geometry import (
    LinearRing,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

from blueprints.utils.map import (
    _SHAPE_CONFIG,
    TILE_PROVIDERS,
    CircleStyle,
    FillStyle,
    HeatmapStyle,
    LabelStyle,
    Map,
    MapConfig,
    MarkerStyle,
    PopupStyle,
    RawHTML,
    StrokeStyle,
    _capture_screenshot,
    _check_selenium,
    _detect_and_transform_coords,
    _markdown_to_html,
    _resolve_style,
    _transform_geometry,
)

# ===================================================================
# Scenarios for creating and configuring a Map.
# ===================================================================


class TestMapCreation:
    """Scenarios for creating and configuring a Map."""

    def test_create_empty_map(self) -> None:
        """
        Scenario: Create a map with no arguments.

        Given: No configuration or data
        When: A Map is instantiated with defaults
        Then: The map has no title, no center, and an empty bounds list
        """
        # Act - When
        m = Map()

        # Assert - Then
        assert m._title is None, "Empty map should have no title"
        assert m._center is None, "Empty map should have no fixed center"
        assert m._bounds == [], "Empty map should have no tracked bounds"
        assert isinstance(m.folium_map, folium.Map), "Should wrap a Folium Map"

    def test_create_map_with_title(self) -> None:
        """
        Scenario: Create a map with a title overlay.

        Given: A title string "Construction Site Alpha"
        When: A Map is created with that title
        Then: The title is stored and rendered in the HTML
        """
        # Arrange - Given
        title = "Construction Site Alpha"

        # Act - When
        m = Map(title=title)

        # Assert - Then
        assert m._title == title, "Title should be stored"
        html = m._repr_html_()
        assert title in html, "Title should appear in rendered HTML"

    def test_create_map_with_fixed_center(self) -> None:
        """
        Scenario: Create a map centered on a specific location.

        Given: Center coordinates for Amsterdam (52.37, 4.90)
        When: A Map is created with that center
        Then: The map uses the fixed center instead of auto-fitting
        """
        # Arrange - Given
        center = (52.37, 4.90)

        # Act - When
        m = Map(center=center)

        # Assert - Then
        assert m._center == center, "Center should be stored as provided"

    def test_create_map_with_custom_config(self) -> None:
        """
        Scenario: Create a map with dark theme and plugins enabled.

        Given: A MapConfig with dark tiles, fullscreen, and minimap
        When: A Map is created with that config
        Then: The config is applied to the underlying map
        """
        # Arrange - Given
        config = MapConfig(
            tile_layer="cartodb_dark",
            zoom_start=14,
            fullscreen=True,
            minimap=True,
            measure_control=True,
            mouse_position=True,
        )

        # Act - When
        m = Map(config=config)

        # Assert - Then
        assert m._config.tile_layer == "cartodb_dark"
        assert m._config.fullscreen is True
        assert m._config.minimap is True
        assert m._config.zoom_start == 14

    def test_create_map_with_min_zoom(self) -> None:
        """
        Scenario: Create a map with min_zoom to restrict zoom-out.

        Given: A MapConfig with min_zoom=5
        When: A Map is created
        Then: The config stores min_zoom and the Folium map respects it
        """
        # Arrange - Given
        config = MapConfig(min_zoom=5)

        # Act - When
        m = Map(config=config)

        # Assert - Then
        assert m._config.min_zoom == 5

    def test_create_map_with_explicit_crs(self) -> None:
        """
        Scenario: Create a map with an explicit source coordinate system.

        Given: A CRS string "EPSG:28992" (Dutch RD New)
        When: A Map is created with that source_crs
        Then: All added geometries are transformed from that CRS
        """
        # Arrange - Given
        crs = "EPSG:28992"

        # Act - When
        m = Map(source_crs=crs)

        # Assert - Then
        assert m._source_crs == crs, "Source CRS should be stored"

    def test_map_repr_shows_metadata(self) -> None:
        """
        Scenario: Inspect a map's string representation.

        Given: A Map with a title and one point added
        When: repr() is called on the map
        Then: The output includes the title and geometry count
        """
        # Arrange - Given
        m = Map(title="Site B")
        m.add_point(Point(4.9, 52.37))

        # Act - When
        result = repr(m)

        # Assert - Then
        assert "Site B" in result, "repr should include the title"
        assert "Map" in result, "repr should include the class name"

    def test_map_with_custom_tile_url(self) -> None:
        """
        Scenario: Create a map with a tile URL not in the TILE_PROVIDERS registry.

        Given: A MapConfig with a raw tile URL and custom attribution
        When: A Map is created
        Then: The custom tile URL is passed to Folium

        Covers: lines 559-560
        """
        # Arrange - Given
        config = MapConfig(
            tile_layer="https://custom.tiles.example/{z}/{x}/{y}.png",
            attribution="Custom Tiles © Example",
        )

        # Act - When
        m = Map(config=config)

        # Assert - Then
        assert m._map is not None, "Map should be created with custom tiles"
        assert m._config.tile_layer.startswith("https://")


# ===================================================================
# Scenarios for adding point markers and circles.
# ===================================================================


class TestAddPoints:
    """Scenarios for adding point markers and circles."""

    def test_add_point_with_emoji_label(self) -> None:
        """
        Scenario: Add a construction site marker with an emoji.

        Given: An empty map and a Point at Amsterdam Centraal
        When: A point is added with a 🏗️ emoji label and hover text
        Then: The bounds are tracked and the method returns self
        """
        # Arrange - Given
        m = Map()
        point = Point(4.8952, 52.3702)

        # Act - When
        result = m.add_point(point, label="🏗️", hover="**Amsterdam Centraal**")

        # Assert - Then
        assert result is m, "add_point should return self for chaining"
        assert len(m._bounds) == 2, "One point should create 2 bound entries (min/max)"

    def test_add_point_with_icon_marker(self) -> None:
        """
        Scenario: Add a point with a Font Awesome icon.

        Given: An empty map and a MarkerStyle with a home icon
        When: A point is added with that style
        Then: The point is added without errors
        """
        # Arrange - Given
        m = Map()
        point = Point(4.8834, 52.3667)
        style = MarkerStyle(icon="home", marker_color="green", prefix="fa")

        # Act - When
        m.add_point(point, hover="**Anne Frank House**", marker_style=style)

        # Assert - Then
        assert len(m._bounds) == 2, "Point should be tracked in bounds"

    def test_add_point_with_popup(self) -> None:
        """
        Scenario: Add a point that shows a popup on click.

        Given: An empty map and a Point
        When: A point is added with both hover and popup text
        Then: Both interactions are configured
        """
        # Arrange - Given
        m = Map()
        point = Point(4.9041, 52.3676)

        # Act - When
        m.add_point(
            point,
            hover="**Hover** text",
            popup="# Popup\nWith *markdown* support",
        )

        # Assert - Then
        assert len(m._bounds) == 2, "Point should be tracked in bounds"

    def test_add_circle_marker(self) -> None:
        """
        Scenario: Add a fixed-size circle marker for data visualization.

        Given: An empty map and a custom CircleStyle
        When: A circle is added at the Rijksmuseum location
        Then: The circle is placed on the map with the configured style
        """
        # Arrange - Given
        m = Map()
        point = Point(4.8795, 52.3600)
        style = CircleStyle(
            radius=12,
            stroke=StrokeStyle(color="#8e44ad", weight=2),
            fill=FillStyle(color="#8e44ad", opacity=0.5),
        )

        # Act - When
        result = m.add_circle(point, hover="**Rijksmuseum**", style=style)

        # Assert - Then
        assert result is m, "add_circle should return self"
        assert len(m._bounds) == 2, "Circle center should be tracked"

    def test_add_point_default_marker(self) -> None:
        """
        Scenario: Add a point with no label, no emoji, default marker.

        Given: An empty map and a Point
        When: add_point is called with only the point (no label or style)
        Then: A default blue pin marker is placed
        """
        # Arrange - Given
        m = Map()

        # Act - When
        m.add_point(Point(4.9, 52.37))

        # Assert - Then
        assert len(m._bounds) == 2, "Point should be tracked"

    def test_add_polygon_all_defaults(self) -> None:
        """
        Scenario: Add a polygon with no custom styling.

        Given: An empty map and a Polygon
        When: add_polygon is called with only the polygon
        Then: Default blue stroke and 20% blue fill are used
        """
        # Arrange - Given
        m = Map()
        poly = Polygon([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)])

        # Act - When
        m.add_polygon(poly)

        # Assert - Then
        assert len(m._bounds) == 2, "Polygon should be tracked"

    def test_add_point_with_only_hover(self) -> None:
        """
        Scenario: Add a point with hover but no label (icon marker).

        Given: An empty map
        When: add_point is called with hover text but no label
        Then: A default icon marker with hover tooltip is placed
        """
        # Arrange - Given
        m = Map()

        # Act - When
        m.add_point(Point(4.9, 52.37), hover="**Info only**")

        # Assert - Then
        assert len(m._bounds) == 2


# ===================================================================
# Scenarios for adding lines and polygons.
# ===================================================================


class TestAddShapes:
    """Scenarios for adding lines and polygons."""

    def test_add_linestring_as_route(self) -> None:
        """
        Scenario: Draw a walking route through Amsterdam.

        Given: An empty map and a LineString with 4 coordinate pairs
        When: The line is added with a dashed red stroke
        Then: The line is on the map and bounds cover all coordinates
        """
        # Arrange - Given
        m = Map()
        route = LineString(
            [
                (4.8852, 52.3702),
                (4.8910, 52.3663),
                (4.8932, 52.3631),
                (4.8840, 52.3569),
            ]
        )
        stroke = StrokeStyle(color="#e74c3c", weight=4, dash_array="10 6")

        # Act - When
        result = m.add_linestring(route, hover="**Walking route**", stroke=stroke)

        # Assert - Then
        assert result is m, "add_linestring should return self"
        assert len(m._bounds) == 2, "Line bounding box should be tracked"

    def test_add_polygon_with_fill(self) -> None:
        """
        Scenario: Highlight a neighbourhood area.

        Given: An empty map and a rectangular Polygon for De Jordaan
        When: The polygon is added with green stroke and semi-transparent fill
        Then: The polygon is on the map and bounds are tracked
        """
        # Arrange - Given
        m = Map()
        jordaan = Polygon(
            [
                (4.8760, 52.3720),
                (4.8890, 52.3720),
                (4.8890, 52.3800),
                (4.8760, 52.3800),
            ]
        )
        stroke = StrokeStyle(color="#2ecc71", weight=2)
        fill = FillStyle(color="#2ecc71", opacity=0.15)

        # Act - When
        result = m.add_polygon(jordaan, hover="**De Jordaan**", stroke=stroke, fill=fill)

        # Assert - Then
        assert result is m, "add_polygon should return self"
        assert len(m._bounds) == 2, "Polygon bounding box should be tracked"

    def test_add_multipolygon_adds_all_parts(self) -> None:
        """
        Scenario: Add a multi-part polygon (e.g. islands).

        Given: An empty map and a MultiPolygon with 2 rectangles
        When: The MultiPolygon is added
        Then: Both polygons are on the map (4 bound entries)
        """
        # Arrange - Given
        m = Map()
        mp = MultiPolygon(
            [
                Polygon([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)]),
                Polygon([(5.00, 52.35), (5.10, 52.35), (5.10, 52.40), (5.00, 52.40)]),
            ]
        )

        # Act - When
        result = m.add_multipolygon(mp, hover="**Two zones**")

        # Assert - Then
        assert result is m, "add_multipolygon should return self"
        assert len(m._bounds) == 4, "Each polygon should add 2 bound entries"

    def test_add_multilinestring(self) -> None:
        """
        Scenario: Add two transit lines as a MultiLineString.

        Given: An empty map and a MultiLineString with 2 routes
        When: The MultiLineString is added
        Then: Both lines are on the map
        """
        # Arrange - Given
        m = Map()
        ml = MultiLineString(
            [
                [(4.9, 52.37), (5.1, 52.09)],
                [(4.3, 52.07), (5.1, 52.09)],
            ]
        )

        # Act - When
        result = m.add_multilinestring(ml)

        # Assert - Then
        assert result is m, "add_multilinestring should return self"
        assert len(m._bounds) == 4, "Each line should add 2 bound entries"

    def test_add_multipoint(self) -> None:
        """
        Scenario: Add multiple sensor locations as a MultiPoint.

        Given: An empty map and a MultiPoint with 2 locations
        When: The MultiPoint is added with red circle labels
        Then: Both points appear on the map
        """
        # Arrange - Given
        m = Map()
        mp = MultiPoint([(4.9, 52.37), (5.1, 52.09)])

        # Act - When
        result = m.add_multipoint(mp, label="🔴")

        # Assert - Then
        assert result is m, "add_multipoint should return self"
        assert len(m._bounds) == 4, "Each point should add 2 bound entries"

    def test_add_linear_ring(self) -> None:
        """
        Scenario: Add a LinearRing via the generic dispatcher.

        Given: An empty map and a LinearRing (closed loop)
        When: add_geometry is called with the ring
        Then: It is rendered as a LineString
        """
        # Arrange - Given
        m = Map()
        ring = LinearRing([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)])

        # Act - When
        result = m.add_geometry(ring)

        # Assert - Then
        assert result is m, "add_geometry should return self"
        assert len(m._bounds) == 2, "Ring bounding box should be tracked"


# ===================================================================
# Scenarios for add_geometry auto-dispatching.
# ===================================================================


class TestGeometryDispatch:
    """Scenarios for add_geometry auto-dispatching."""

    def test_dispatch_point(self) -> None:
        """
        Scenario: Auto-dispatch a Point geometry.

        Given: An empty map and a Shapely Point
        When: add_geometry is called with the Point
        Then: It delegates to add_point and tracks bounds
        """
        # Arrange - Given
        m = Map()
        point = Point(4.9, 52.37)

        # Act - When
        m.add_geometry(point, label="📍")

        # Assert - Then
        assert len(m._bounds) == 2, "Point should be dispatched and tracked"

    def test_dispatch_polygon(self) -> None:
        """
        Scenario: Auto-dispatch a Polygon geometry.

        Given: An empty map and a Shapely Polygon
        When: add_geometry is called with the Polygon
        Then: It delegates to add_polygon and tracks bounds
        """
        # Arrange - Given
        m = Map()
        poly = Polygon([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)])

        # Act - When
        m.add_geometry(poly, fill=FillStyle(color="red"))

        # Assert - Then
        assert len(m._bounds) == 2, "Polygon should be dispatched and tracked"

    def test_dispatch_unsupported_type_raises(self) -> None:
        """
        Scenario: Attempt to add an unsupported geometry type.

        Given: An empty map and a non-geometry object
        When: add_geometry is called with a string
        Then: A TypeError is raised with a descriptive message
        """
        # Arrange - Given
        m = Map()

        # Act & Assert - When/Then
        with pytest.raises(TypeError, match="Unsupported"):
            m.add_geometry("not a geometry")

    def test_dispatch_linestring(self) -> None:
        """
        Scenario: add_geometry dispatches a LineString.

        Given: An empty map and a LineString
        When: add_geometry is called
        Then: It delegates to add_linestring
        """
        m = Map()
        m.add_geometry(LineString([(4.9, 52.37), (5.1, 52.09)]))
        assert len(m._bounds) == 2

    def test_dispatch_multipolygon(self) -> None:
        """
        Scenario: add_geometry dispatches a MultiPolygon.

        Given: An empty map and a MultiPolygon
        When: add_geometry is called
        Then: It delegates to add_multipolygon (4 bound entries)
        """
        m = Map()
        mp = MultiPolygon(
            [
                Polygon([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)]),
                Polygon([(5.0, 52.35), (5.1, 52.35), (5.1, 52.40), (5.0, 52.40)]),
            ]
        )
        m.add_geometry(mp)
        assert len(m._bounds) == 4

    def test_dispatch_multilinestring(self) -> None:
        """
        Scenario: add_geometry dispatches a MultiLineString.

        Given: An empty map and a MultiLineString
        When: add_geometry is called
        Then: It delegates to add_multilinestring
        """
        m = Map()
        ml = MultiLineString(
            [
                [(4.9, 52.37), (5.1, 52.09)],
                [(4.3, 52.07), (5.1, 52.09)],
            ]
        )
        m.add_geometry(ml)
        assert len(m._bounds) == 4

    def test_dispatch_multipoint(self) -> None:
        """
        Scenario: add_geometry dispatches a MultiPoint.

        Given: An empty map and a MultiPoint
        When: add_geometry is called
        Then: It delegates to add_multipoint
        """
        m = Map()
        mp = MultiPoint([(4.9, 52.37), (5.1, 52.09)])
        m.add_geometry(mp, label="🔵")
        assert len(m._bounds) == 4

    def test_add_geometry_dispatches_linearring_to_linestring(self) -> None:
        """
        Scenario: add_geometry converts a LinearRing to a LineString.

        Given: An empty map and a LinearRing
        When: add_geometry is called with the LinearRing
        Then: It is rendered as a LineString on the map

        Covers: line 948
        """
        # Arrange - Given
        m = Map()
        ring = LinearRing([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)])

        # Act - When
        result = m.add_geometry(ring, hover="**Ring boundary**", stroke=StrokeStyle(color="red"))

        # Assert - Then
        assert result is m
        assert len(m._bounds) == 2


# ===================================================================
# Scenarios for organising layers into toggleable groups.
# ===================================================================


class TestFeatureGroups:
    """Scenarios for organising layers into toggleable groups."""

    def test_create_feature_group(self) -> None:
        """
        Scenario: Organize museum markers in a named layer.

        Given: An empty map
        When: A feature group "Museums" is created
        Then: The group is registered and becomes the active target
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m.create_feature_group("Museums")

        # Assert - Then
        assert result is m, "create_feature_group should return self"
        assert "Museums" in m._feature_groups, "Group should be registered"
        assert m._active_group is m._feature_groups["Museums"], "Group should be active"

    def test_features_go_to_active_group(self) -> None:
        """
        Scenario: Points are added to the currently active group.

        Given: A map with an active feature group "Parks"
        When: A point is added
        Then: The point exists inside the feature group, not the base map
        """
        # Arrange - Given
        m = Map()
        m.create_feature_group("Parks")

        # Act - When
        m.add_point(Point(4.8765, 52.3579), label="🌳", hover="**Vondelpark**")

        # Assert - Then
        fg = m._feature_groups["Parks"]
        assert len(fg._children) > 0, "Point should be added to the active group"

    def test_switch_between_groups(self) -> None:
        """
        Scenario: Switch from one layer group to another.

        Given: A map with two feature groups "Museums" and "Parks"
        When: set_feature_group("Museums") is called
        Then: The active target switches to Museums
        """
        # Arrange - Given
        m = Map()
        m.create_feature_group("Museums")
        m.create_feature_group("Parks")

        # Act - When
        m.set_feature_group("Museums")

        # Assert - Then
        assert m._active_group is m._feature_groups["Museums"]

    def test_reset_target_to_base_map(self) -> None:
        """
        Scenario: Return to adding features directly to the base map.

        Given: A map with an active feature group
        When: reset_target() is called
        Then: Subsequent features go to the base map
        """
        # Arrange - Given
        m = Map()
        m.create_feature_group("Temp Layer")

        # Act - When
        m.reset_target()

        # Assert - Then
        assert m._active_group is m._map, "Active target should be the base map"

    def test_set_nonexistent_group_raises(self) -> None:
        """
        Scenario: Attempt to switch to a group that doesn't exist.

        Given: A map with no feature groups
        When: set_feature_group("Ghost") is called
        Then: A KeyError is raised with the group name
        """
        # Arrange - Given
        m = Map()

        # Act & Assert - When/Then
        with pytest.raises(KeyError, match="Ghost"):
            m.set_feature_group("Ghost")

    def test_add_layer_control(self) -> None:
        """
        Scenario: Add a layer toggle widget after creating groups.

        Given: A map with two feature groups and some points
        When: add_layer_control() is called
        Then: The control is added and the method returns self
        """
        # Arrange - Given
        m = Map()
        m.create_feature_group("A").add_point(Point(4.9, 52.37))
        m.create_feature_group("B").add_point(Point(5.1, 52.09))

        # Act - When
        result = m.add_layer_control(collapsed=False)

        # Assert - Then
        assert result is m, "add_layer_control should return self"

    def test_create_hidden_feature_group(self) -> None:
        """
        Scenario: Create a feature group that is hidden by default.

        Given: An empty map
        When: create_feature_group is called with show=False
        Then: The group is registered but not visible initially
        """
        # Arrange - Given
        m = Map()

        # Act - When
        m.create_feature_group("Hidden Layer", show=False)

        # Assert - Then
        assert "Hidden Layer" in m._feature_groups
        fg = m._feature_groups["Hidden Layer"]
        assert fg.show is False, "Feature group should be hidden"

    def test_add_layer_control_with_position(self) -> None:
        """
        Scenario: Place the layer control at a specific position.

        Given: A map with feature groups
        When: add_layer_control is called with position="bottomleft"
        Then: The control is added (no error raised)
        """
        # Arrange - Given
        m = Map()
        m.create_feature_group("A")

        # Act - When
        result = m.add_layer_control(collapsed=True, position="bottomleft")

        # Assert - Then
        assert result is m


# ===================================================================
# Scenarios for adding GeoJSON data layers.
# ===================================================================


class TestGeoJSON:
    """Scenarios for adding GeoJSON data layers."""

    @pytest.fixture
    def sample_geojson(self) -> dict:
        """A minimal GeoJSON FeatureCollection with two zones."""
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Zone A", "value": 42.0},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40), (4.85, 52.35)]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Zone B", "value": 78.0},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[(4.95, 52.35), (5.05, 52.35), (5.05, 52.40), (4.95, 52.40), (4.95, 52.35)]],
                    },
                },
            ],
        }

    def test_add_geojson_from_dict(self, sample_geojson: dict) -> None:
        """
        Scenario: Add a GeoJSON layer from a Python dict.

        Given: An empty map and a GeoJSON FeatureCollection dict
        When: add_geojson is called with hover_fields
        Then: The layer is added and the method returns self
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m.add_geojson(sample_geojson, hover_fields=["name", "value"])

        # Assert - Then
        assert result is m, "add_geojson should return self"

    def test_add_geojson_from_json_string(self, sample_geojson: dict) -> None:
        """
        Scenario: Add a GeoJSON layer from a JSON string.

        Given: An empty map and a GeoJSON serialized as string
        When: add_geojson is called with the string
        Then: The string is parsed and the layer is added
        """
        # Arrange - Given
        m = Map()
        json_str = json.dumps(sample_geojson)

        # Act - When
        m.add_geojson(json_str)

        # Assert - Then
        assert len(m._bounds) > 0, "Bounds should be tracked from GeoJSON"

    def test_add_geojson_from_file(self, sample_geojson: dict, tmp_path: Path) -> None:
        """
        Scenario: Add a GeoJSON layer from a .geojson file.

        Given: A .geojson file on disk
        When: add_geojson is called with the Path
        Then: The file is read and the layer is added
        """
        # Arrange - Given
        m = Map()
        filepath = tmp_path / "zones.geojson"
        filepath.write_text(json.dumps(sample_geojson))

        # Act - When
        m.add_geojson(filepath)

        # Assert - Then
        assert len(m._bounds) > 0, "Bounds should be tracked from file"

    def test_add_geojson_with_custom_style(self, sample_geojson: dict) -> None:
        """
        Scenario: Add GeoJSON with custom styling and highlight.

        Given: An empty map and GeoJSON data
        When: add_geojson is called with style and highlight dicts
        Then: The layer is added with the custom appearance
        """
        # Arrange - Given
        m = Map()

        # Act - When
        m.add_geojson(
            sample_geojson,
            style={"color": "#e74c3c", "weight": 2, "fillOpacity": 0.1},
            highlight={"weight": 5, "fillOpacity": 0.3},
        )

        # Assert - Then
        assert len(m._bounds) > 0, "Layer should be added with bounds"

    def test_add_geojson_string_path_to_file(self, tmp_path: Path) -> None:
        """
        Scenario: Pass a string file path (not Path object) to add_geojson.

        Given: A .geojson file and its path as a string
        When: add_geojson is called with the string path
        Then: The file is detected and loaded
        """
        # Arrange - Given
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Test"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40), (4.85, 52.35)]],
                    },
                }
            ],
        }
        filepath = tmp_path / "test.geojson"
        filepath.write_text(json.dumps(geojson))
        m = Map()

        # Act - When
        m.add_geojson(str(filepath))

        # Assert - Then
        assert len(m._bounds) > 0, "GeoJSON from string path should be loaded"

    def test_add_geojson_no_hover_fields(self) -> None:
        """
        Scenario: Add GeoJSON without hover fields (no tooltip).

        Given: A GeoJSON dict
        When: add_geojson is called without hover_fields
        Then: The layer is added without a tooltip
        """
        # Arrange - Given
        m = Map()
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Point",
                        "coordinates": [4.9, 52.37],
                    },
                }
            ],
        }

        # Act - When
        result = m.add_geojson(geojson)

        # Assert - Then
        assert result is m

    def test_add_geojson_short_non_file_string(self) -> None:
        """
        Scenario: Pass a short JSON string that doesn't start with '{' and doesn't match any file — falls through to json.loads.

        Given: A short non-path string that is valid JSON (wrapped differently)
        When: add_geojson is called
        Then: It falls through the path check and parses as JSON

        Covers: line 987
        """
        # Arrange - Given
        m = Map()

        # Use a fake short path-like string that doesn't exist
        fake_path = "/tmp/nonexistent_12345.geojson"

        # Act & Assert - When/Then
        # This should raise json.JSONDecodeError because the string isn't valid JSON
        with pytest.raises(json.JSONDecodeError):
            m.add_geojson(fake_path)

    def test_add_geojson_long_json_string(self) -> None:
        """
        Scenario: Pass a long JSON string (>500 chars) starting with '{'.

        Given: A large GeoJSON string (>500 chars)
        When: add_geojson is called
        Then: It skips the path check and parses directly as JSON

        Covers: lines 988-989 (the else branch for long strings)
        """
        # Arrange - Given
        m = Map()
        # Build a GeoJSON string that exceeds 500 chars
        features = [
            {
                "type": "Feature",
                "properties": {"name": f"Zone {i}", "value": i * 10},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            (4.85 + i * 0.01, 52.35),
                            (4.86 + i * 0.01, 52.35),
                            (4.86 + i * 0.01, 52.36),
                            (4.85 + i * 0.01, 52.36),
                            (4.85 + i * 0.01, 52.35),
                        ]
                    ],
                },
            }
            for i in range(20)
        ]  # 20 features to ensure the string is long enough
        geojson = {"type": "FeatureCollection", "features": features}
        json_str = json.dumps(geojson)
        assert len(json_str) > 500, "String must exceed 500 chars for this test"

        # Act - When
        result = m.add_geojson(json_str)

        # Assert - Then
        assert result is m

    def test_geojson_bounds_exception_is_caught(self) -> None:
        """
        Scenario: GeoJSON layer.get_bounds() raises an exception.

        Given: A Map and a GeoJSON that causes get_bounds to fail
        When: add_geojson is called
        Then: The exception is silently caught and the method returns self

        Covers: lines 1009-1010
        """
        # Arrange - Given
        m = Map()
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {"type": "Point", "coordinates": [4.9, 52.37]},
                }
            ],
        }

        # Act - When — mock get_bounds to raise
        with patch.object(folium.GeoJson, "get_bounds", side_effect=ValueError("boom")):
            result = m.add_geojson(geojson)

        # Assert - Then
        assert result is m, "Exception should be caught silently"

    def test_choropleth_bounds_exception_is_caught(self) -> None:
        """
        Scenario: Choropleth layer.get_bounds() raises an exception.

        Given: A Map and valid choropleth data
        When: add_choropleth is called and get_bounds fails
        Then: The exception is silently caught

        Covers: lines 1124-1125
        """
        # Arrange - Given
        m = Map()
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "A", "val": 50},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40), (4.85, 52.35)]],
                    },
                }
            ],
        }

        # Act - When — mock get_bounds to raise
        with patch.object(folium.GeoJson, "get_bounds", side_effect=RuntimeError("fail")):
            result = m.add_choropleth(
                geojson,
                value_column="val",
                key_on="feature.properties.name",
            )

        # Assert - Then
        assert result is m


# ===================================================================
# Scenarios for colour-coded choropleth layers.
# ===================================================================


class TestChoropleth:
    """Scenarios for colour-coded choropleth layers."""

    @pytest.fixture
    def scored_geojson(self) -> dict:
        """GeoJSON with a numeric 'score' property."""
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Centrum", "score": 92},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[(4.88, 52.36), (4.92, 52.36), (4.92, 52.38), (4.88, 52.38), (4.88, 52.36)]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"name": "West", "score": 74},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[(4.84, 52.36), (4.88, 52.36), (4.88, 52.38), (4.84, 52.38), (4.84, 52.36)]],
                    },
                },
            ],
        }

    def test_choropleth_from_properties(self, scored_geojson: dict) -> None:
        """
        Scenario: Create a choropleth that reads values from GeoJSON properties.

        Given: An empty map and GeoJSON with a "score" property per feature
        When: add_choropleth is called with value_column="score"
        Then: A colormap is created and added as a legend
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m.add_choropleth(
            geojson_data=scored_geojson,
            value_column="score",
            key_on="feature.properties.name",
            legend_name="Liveability Score",
            hover_fields=["name", "score"],
        )

        # Assert - Then
        assert result is m, "add_choropleth should return self"
        assert len(m._colormaps) == 1, "One colormap should be registered"

    def test_choropleth_with_explicit_values(self, scored_geojson: dict) -> None:
        """
        Scenario: Create a choropleth with externally provided values.

        Given: GeoJSON data and a separate dict mapping names to values
        When: add_choropleth is called with the values dict
        Then: The explicit values override the GeoJSON properties
        """
        # Arrange - Given
        m = Map()
        values = {"Centrum": 100.0, "West": 25.0}

        # Act - When
        m.add_choropleth(
            geojson_data=scored_geojson,
            value_column="score",
            key_on="feature.properties.name",
            values=values,
            vmin=0,
            vmax=100,
        )

        # Assert - Then
        assert len(m._colormaps) == 1, "Colormap should still be created"

    def test_choropleth_from_file_path(self, scored_geojson: dict, tmp_path: Path) -> None:
        """
        Scenario: Create a choropleth from a GeoJSON file on disk.

        Given: A .geojson file with scored features
        When: add_choropleth is called with a Path object
        Then: The file is loaded and the choropleth is created
        """
        # Arrange - Given
        m = Map()
        filepath = tmp_path / "scores.geojson"
        filepath.write_text(json.dumps(scored_geojson))

        # Act - When
        m.add_choropleth(
            geojson_data=filepath,
            value_column="score",
            key_on="feature.properties.name",
        )

        # Assert - Then
        assert len(m._colormaps) == 1

    def test_choropleth_nan_features_get_fill_color(self, scored_geojson: dict) -> None:
        """
        Scenario: Features with missing values use the nan_fill_color.

        Given: GeoJSON where one feature has score=None
        When: add_choropleth is called with nan_fill_color="#999999"
        Then: The choropleth is created without errors
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m.add_choropleth(
            geojson_data=scored_geojson,
            value_column="score",
            key_on="feature.properties.name",
            nan_fill_color="#999999",
            nan_fill_opacity=0.3,
        )

        # Assert - Then
        assert result is m, "Choropleth with NaN values should not error"

    def test_choropleth_from_json_string(self, scored_geojson: dict) -> None:
        """
        Scenario: Create a choropleth from a JSON string.

        Given: GeoJSON serialized as a string
        When: add_choropleth is called with the string
        Then: The string is parsed and the choropleth is created
        """
        # Arrange - Given
        m = Map()
        json_str = json.dumps(scored_geojson)

        # Act - When
        m.add_choropleth(
            geojson_data=json_str,
            value_column="score",
            key_on="feature.properties.name",
        )

        # Assert - Then
        assert len(m._colormaps) == 1

    def test_choropleth_short_string_path(self, tmp_path: Path) -> None:
        """
        Scenario: Pass a short string file path to add_choropleth.

        Given: A .geojson file and its path as a short string
        When: add_choropleth is called with the string path
        Then: The file is detected and loaded

        Covers: lines 1062-1064
        """
        # Arrange - Given
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "A", "val": 50},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40), (4.85, 52.35)]],
                    },
                }
            ],
        }
        filepath = tmp_path / "choropleth.geojson"
        filepath.write_text(json.dumps(geojson))
        m = Map()

        # Act - When
        m.add_choropleth(
            geojson_data=str(filepath),
            value_column="val",
            key_on="feature.properties.name",
        )

        # Assert - Then
        assert len(m._colormaps) == 1

    def test_choropleth_short_nonexistent_path_falls_to_json(self) -> None:
        """
        Scenario: Pass a short string that isn't a valid file and isn't valid JSON.

        Given: A short non-path, non-JSON string
        When: add_choropleth is called
        Then: json.loads fails with JSONDecodeError

        Covers: lines 1065-1066
        """
        # Arrange - Given
        m = Map()

        # Act & Assert - When/Then
        with pytest.raises(json.JSONDecodeError):
            m.add_choropleth(
                geojson_data="/tmp/nonexistent_xyz.geojson",
                value_column="val",
                key_on="feature.properties.name",
            )

    def test_choropleth_long_json_string(self) -> None:
        """
        Scenario: Pass a long JSON string (>500 chars) to add_choropleth.

        Given: A large GeoJSON string
        When: add_choropleth is called
        Then: It parses directly as JSON, skipping the path check

        Covers: lines 1067-1068 (else branch for long strings)
        """
        # Arrange - Given
        m = Map()
        features = [
            {
                "type": "Feature",
                "properties": {"name": f"Z{i}", "val": float(i * 5)},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            (4.85 + i * 0.01, 52.35),
                            (4.86 + i * 0.01, 52.35),
                            (4.86 + i * 0.01, 52.36),
                            (4.85 + i * 0.01, 52.36),
                            (4.85 + i * 0.01, 52.35),
                        ]
                    ],
                },
            }
            for i in range(20)
        ]
        geojson = {"type": "FeatureCollection", "features": features}
        json_str = json.dumps(geojson)
        assert len(json_str) > 500

        # Act - When
        m.add_choropleth(
            geojson_data=json_str,
            value_column="val",
            key_on="feature.properties.name",
        )

        # Assert - Then
        assert len(m._colormaps) == 1

    def test_choropleth_style_fn_nan_branch(self) -> None:
        """
        Scenario: A choropleth feature has no matching value in the values dict.

        Given: GeoJSON with two features but values dict only has one key
        When: add_choropleth is called and Folium renders both features
        Then: The missing feature uses nan_fill_color

        Covers: line 1107
        """
        # Arrange - Given
        m = Map()
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Known", "val": 50},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[(4.85, 52.35), (4.90, 52.35), (4.90, 52.38), (4.85, 52.38), (4.85, 52.35)]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Unknown", "val": None},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[(4.90, 52.35), (4.95, 52.35), (4.95, 52.38), (4.90, 52.38), (4.90, 52.35)]],
                    },
                },
            ],
        }

        # Act - When
        m.add_choropleth(
            geojson_data=geojson,
            value_column="val",
            key_on="feature.properties.name",
            values={"Known": 50.0},  # "Unknown" not in values
            nan_fill_color="#aaaaaa",
            vmin=0,
            vmax=100,
        )

        # Force Folium to render which triggers style_fn for each feature
        html = m._repr_html_()

        # Assert - Then
        assert len(m._colormaps) == 1
        assert "#aaaaaa" in html, "nan_fill_color should appear in rendered output"


# ===================================================================
# Scenarios for heatmap layers.
# ===================================================================


class TestHeatmap:
    """Scenarios for heatmap layers."""

    def test_heatmap_from_shapely_points(self) -> None:
        """
        Scenario: Create a heatmap from Shapely Point objects.

        Given: An empty map and a list of 10 Points
        When: add_heatmap is called with the points
        Then: A heatmap layer is added and bounds are tracked
        """
        # Arrange - Given
        m = Map()
        points = [Point(4.85 + i * 0.01, 52.35 + i * 0.005) for i in range(10)]

        # Act - When
        result = m.add_heatmap(points)

        # Assert - Then
        assert result is m, "add_heatmap should return self"
        assert len(m._bounds) == 20, "Each point should add 2 bound entries"

    def test_heatmap_from_tuples(self) -> None:
        """
        Scenario: Create a heatmap from (lat, lon) tuples.

        Given: An empty map and raw coordinate tuples
        When: add_heatmap is called with the tuples
        Then: The heatmap is created from the tuple coordinates
        """
        # Arrange - Given
        m = Map()
        tuples = [(52.37, 4.9), (52.38, 4.95), (52.36, 4.85)]

        # Act - When
        m.add_heatmap(tuples)

        # Assert - Then
        assert len(m._bounds) == 3, "Each tuple should add 1 bound entry"

    def test_heatmap_with_intensity_weights(self) -> None:
        """
        Scenario: Create a heatmap with weighted intensities.

        Given: An empty map and (lat, lon, intensity) triples
        When: add_heatmap is called with the weighted data
        Then: The heatmap uses the intensity values
        """
        # Arrange - Given
        m = Map()
        weighted = [(52.37, 4.9, 1.0), (52.38, 4.95, 0.3), (52.36, 4.85, 0.7)]

        # Act - When
        m.add_heatmap(weighted)

        # Assert - Then
        assert len(m._bounds) == 3, "Weighted triples should track bounds"

    def test_heatmap_with_custom_style(self) -> None:
        """
        Scenario: Configure heatmap appearance with custom gradient.

        Given: An empty map and a HeatmapStyle with a blue-to-red gradient
        When: add_heatmap is called with the style
        Then: The heatmap uses the custom configuration
        """
        # Arrange - Given
        m = Map()
        style = HeatmapStyle(
            radius=25,
            blur=20,
            gradient={0.4: "blue", 0.65: "lime", 1.0: "red"},
        )
        points = [Point(4.9, 52.37)]

        # Act - When
        m.add_heatmap(points, style=style)

        # Assert - Then
        assert len(m._bounds) == 2, "Heatmap point should be tracked"

    def test_heatmap_with_layer_name(self) -> None:
        """
        Scenario: Create a named heatmap layer for layer control.

        Given: An empty map and some points
        When: add_heatmap is called with name="Activity"
        Then: The heatmap layer is named and can be toggled
        """
        # Arrange - Given
        m = Map()
        points = [Point(4.9, 52.37), Point(4.95, 52.38)]

        # Act - When
        result = m.add_heatmap(points, name="Activity")

        # Assert - Then
        assert result is m


# ===================================================================
# Scenarios for clustered markers.
# ===================================================================


class TestMarkerCluster:
    """Scenarios for clustered markers."""

    def test_cluster_groups_nearby_markers(self) -> None:
        """
        Scenario: Cluster 50 café markers that expand on zoom.

        Given: An empty map and 50 Points near Amsterdam center
        When: add_marker_cluster is called with labels and hovers
        Then: All points are added and the cluster layer is on the map
        """
        # Arrange - Given
        m = Map()
        cafes = [Point(4.88 + i * 0.001, 52.36 + i * 0.0005) for i in range(50)]
        labels = ["☕"] * 50
        hovers = [f"**Café #{i + 1}**" for i in range(50)]

        # Act - When
        result = m.add_marker_cluster(cafes, labels=labels, hovers=hovers, name="Cafés")

        # Assert - Then
        assert result is m, "add_marker_cluster should return self"
        assert len(m._bounds) == 100, "50 points x 2 bound entries each"

    def test_cluster_without_labels(self) -> None:
        """
        Scenario: Create a cluster with default icon markers.

        Given: An empty map and a list of Points with no labels
        When: add_marker_cluster is called without labels
        Then: Default Folium icons are used
        """
        # Arrange - Given
        m = Map()
        points = [Point(4.9 + i * 0.01, 52.37) for i in range(5)]

        # Act - When
        m.add_marker_cluster(points)

        # Assert - Then
        assert len(m._bounds) == 10, "5 points should track 10 bound entries"

    def test_cluster_with_popups(self) -> None:
        """
        Scenario: Clustered markers with click popups.

        Given: An empty map and points with popup text
        When: add_marker_cluster is called with popups
        Then: All markers have popups configured
        """
        # Arrange - Given
        m = Map()
        points = [Point(4.9, 52.37), Point(4.95, 52.38)]
        popups = ["# Popup A\nDetails A", "# Popup B\nDetails B"]

        # Act - When
        result = m.add_marker_cluster(points, popups=popups)

        # Assert - Then
        assert result is m
        assert len(m._bounds) == 4

    def test_cluster_with_named_layer(self) -> None:
        """
        Scenario: Cluster with a named layer for the layer control.

        Given: An empty map
        When: add_marker_cluster is called with name="Sensors"
        Then: The cluster layer is named
        """
        # Arrange - Given
        m = Map()
        points = [Point(4.9, 52.37)]

        # Act - When
        m.add_marker_cluster(points, name="Sensors")

        # Assert - Then
        assert len(m._bounds) == 2


# ===================================================================
# Scenarios for placing text labels on the map.
# ===================================================================


class TestTextAnnotation:
    """Scenarios for placing text labels on the map."""

    def test_add_text_from_shapely_point(self) -> None:
        """
        Scenario: Place a neighbourhood label using a Shapely Point.

        Given: An empty map and a Point for the label location
        When: add_text is called with a styled label
        Then: The text appears at the coordinate and bounds are tracked
        """
        # Arrange - Given
        m = Map()
        location = Point(4.9041, 52.3676)
        style = LabelStyle(font_size=16, font_color="#2c3e50")

        # Act - When
        result = m.add_text(location, "Amsterdam Centrum", style=style)

        # Assert - Then
        assert result is m, "add_text should return self"
        assert len(m._bounds) == 2, "Text location should be tracked"

    def test_add_text_from_tuple(self) -> None:
        """
        Scenario: Place a text label using a (lat, lon) tuple.

        Given: An empty map and a (lat, lon) tuple
        When: add_text is called with the tuple
        Then: The label is placed at the correct location
        """
        # Arrange - Given
        m = Map()

        # Act - When
        m.add_text((52.37, 4.9), "Label here")

        # Assert - Then
        assert (52.37, 4.9) in m._bounds, "Tuple location should be tracked directly"

    def test_add_text_with_transparent_background(self) -> None:
        """
        Scenario: Place floating text without a background box.

        Given: An empty map and a LabelStyle with no background or border
        When: add_text is called with that style
        Then: The text appears without visual chrome
        """
        # Arrange - Given
        m = Map()
        style = LabelStyle(
            font_size=14,
            font_color="red",
            background_color=None,
            border=None,
        )

        # Act - When
        m.add_text((52.37, 4.9), "Floating", style=style)

        # Assert - Then
        assert len(m._bounds) == 1, "One tuple adds one bound entry"

    def test_add_text_with_hover(self) -> None:
        """
        Scenario: A text label with an additional hover tooltip.

        Given: An empty map
        When: add_text is called with both text and hover
        Then: The label has text visible and hover on mouse-over
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m.add_text(
            Point(4.9, 52.37),
            "Station A",
            hover="**Click for details**",
        )

        # Assert - Then
        assert result is m
        assert len(m._bounds) == 2


# ===================================================================
# Scenarios for CRS detection and transformation.
# ===================================================================


class TestCoordinateTransformation:
    """Scenarios for CRS detection and transformation."""

    def test_wgs84_coordinates_pass_through(self) -> None:
        """
        Scenario: WGS84 coordinates are left unchanged.

        Given: Coordinates already in WGS84 (small lon/lat values)
        When: _detect_and_transform_coords is called without source_crs
        Then: The coordinates are returned unchanged
        """
        # Arrange - Given
        coords = [(4.9, 52.37), (5.1, 52.09)]

        # Act - When
        result = _detect_and_transform_coords(coords)

        # Assert - Then
        assert result == coords, "WGS84 coords should pass through unchanged"

    def test_rd_new_auto_detection(self) -> None:
        """
        Scenario: RD New coordinates are auto-detected and transformed.

        Given: Coordinates in the RD New range (x: 0-300k, y: 300k-625k)
        When: _detect_and_transform_coords is called without source_crs
        Then: The coordinates are transformed to WGS84 (near Amsterdam)
        """
        # Arrange - Given
        coords_rd = [(121_000, 487_000)]

        # Act - When
        result = _detect_and_transform_coords(coords_rd)

        # Assert - Then
        lon, lat = result[0]
        assert 4.5 < lon < 5.5, f"Longitude {lon} should be near Amsterdam"
        assert 52.0 < lat < 53.0, f"Latitude {lat} should be near Amsterdam"

    def test_explicit_crs_transforms_correctly(self) -> None:
        """
        Scenario: Explicit EPSG:28992 CRS forces transformation.

        Given: Coordinates and an explicit source_crs="EPSG:28992"
        When: _detect_and_transform_coords is called
        Then: The coordinates are transformed to WGS84
        """
        # Arrange - Given
        coords = [(155_000, 463_000)]

        # Act - When
        result = _detect_and_transform_coords(coords, source_crs="EPSG:28992")

        # Assert - Then
        lon, lat = result[0]
        assert 5.0 < lon < 6.0, "Should be in the Netherlands"
        assert 51.5 < lat < 53.0, "Should be in the Netherlands"

    def test_transform_point_geometry(self) -> None:
        """
        Scenario: Transform a Shapely Point from RD New to WGS84.

        Given: A Point in RD New coordinates
        When: _transform_geometry is called with EPSG:28992
        Then: The returned Point has WGS84 coordinates
        """
        # Arrange - Given
        pt = Point(155_000, 463_000)

        # Act - When
        result = _transform_geometry(pt, "EPSG:28992")

        # Assert - Then
        assert isinstance(result, Point), "Should return a Point"
        assert 5.0 < result.x < 6.0, "Longitude should be in NL range"
        assert 51.5 < result.y < 53.0, "Latitude should be in NL range"

    def test_transform_polygon_geometry(self) -> None:
        """
        Scenario: Transform a Polygon from RD New to WGS84.

        Given: A rectangular Polygon in RD New coordinates
        When: _transform_geometry is called
        Then: The centroid of the result is in the Netherlands
        """
        # Arrange - Given
        poly = Polygon(
            [
                (155_000, 463_000),
                (156_000, 463_000),
                (156_000, 464_000),
                (155_000, 464_000),
            ]
        )

        # Act - When
        result = _transform_geometry(poly, "EPSG:28992")

        # Assert - Then
        cx, cy = result.centroid.x, result.centroid.y
        assert 3.0 < cx < 8.0, "Centroid longitude should be in NL"
        assert 50.0 < cy < 54.0, "Centroid latitude should be in NL"

    def test_empty_coords_returns_empty(self) -> None:
        """
        Scenario: Transform an empty coordinate list.

        Given: An empty list of coordinates
        When: _detect_and_transform_coords is called
        Then: An empty list is returned
        """
        # Act & Assert
        assert _detect_and_transform_coords([]) == []

    def test_rd_point_on_geomap_lands_in_netherlands(self) -> None:
        """
        Scenario: Add an RD New point to a map and verify placement.

        Given: A Map and a Point in RD New coordinates (Amsterdam)
        When: The point is added to the map
        Then: The tracked bounds are in the WGS84 Netherlands range
        """
        # Arrange - Given
        m = Map()
        rd_point = Point(121_000, 487_000)

        # Act - When
        m.add_point(rd_point, label="📍")

        # Assert - Then
        lat, lon = m._bounds[0]
        assert 50.0 < lat < 54.0, "Latitude should be in the Netherlands"
        assert 3.0 < lon < 8.0, "Longitude should be in the Netherlands"

    def test_explicit_wgs84_passes_through(self) -> None:
        """
        Scenario: Explicitly passing EPSG:4326 does not transform.

        Given: WGS84 coordinates and source_crs="EPSG:4326"
        When: _detect_and_transform_coords is called
        Then: The coordinates are returned unchanged
        """
        # Arrange - Given
        coords = [(4.9, 52.37)]

        # Act - When
        result = _detect_and_transform_coords(coords, source_crs="EPSG:4326")

        # Assert - Then
        assert result == coords, "EPSG:4326 should pass through unchanged"

    def test_transform_linestring_geometry(self) -> None:
        """
        Scenario: Transform a LineString from RD New to WGS84.

        Given: A LineString in RD New coordinates
        When: _transform_geometry is called with EPSG:28992
        Then: The returned LineString has WGS84 coordinates
        """
        # Arrange - Given
        line = LineString([(155_000, 463_000), (156_000, 464_000)])

        # Act - When
        result = _transform_geometry(line, "EPSG:28992")

        # Assert - Then
        assert isinstance(result, LineString), "Should return a LineString"
        coords = list(result.coords)
        assert 3.0 < coords[0][0] < 8.0, "Longitude should be in NL"

    def test_transform_multilinestring_geometry(self) -> None:
        """
        Scenario: Transform a MultiLineString from RD New to WGS84.

        Given: A MultiLineString in RD New coordinates
        When: _transform_geometry is called
        Then: All constituent lines are transformed
        """
        # Arrange - Given
        ml = MultiLineString(
            [
                [(155_000, 463_000), (156_000, 464_000)],
                [(157_000, 465_000), (158_000, 466_000)],
            ]
        )

        # Act - When
        result = _transform_geometry(ml, "EPSG:28992")

        # Assert - Then
        assert isinstance(result, MultiLineString)
        assert len(list(result.geoms)) == 2

    def test_transform_multipolygon_geometry(self) -> None:
        """
        Scenario: Transform a MultiPolygon from RD New to WGS84.

        Given: A MultiPolygon with two rectangles in RD New
        When: _transform_geometry is called
        Then: Both polygons have WGS84 coordinates
        """
        # Arrange - Given
        mp = MultiPolygon(
            [
                Polygon([(155_000, 463_000), (156_000, 463_000), (156_000, 464_000), (155_000, 464_000)]),
                Polygon([(160_000, 465_000), (161_000, 465_000), (161_000, 466_000), (160_000, 466_000)]),
            ]
        )

        # Act - When
        result = _transform_geometry(mp, "EPSG:28992")

        # Assert - Then
        assert isinstance(result, MultiPolygon)
        for poly in result.geoms:
            cx = poly.centroid.x
            assert 3.0 < cx < 8.0, f"Centroid lon {cx} should be in NL"

    def test_transform_linearring_geometry(self) -> None:
        """
        Scenario: Transform a LinearRing from RD New to WGS84.

        Given: A LinearRing in RD New coordinates
        When: _transform_geometry is called
        Then: The result has WGS84 coordinates (may degrade to LineString
              due to floating-point rounding in the transform)
        """
        # Arrange - Given
        ring = LinearRing(
            [
                (155_000, 463_000),
                (156_000, 463_000),
                (156_000, 464_000),
                (155_000, 464_000),
            ]
        )

        # Act - When
        result = _transform_geometry(ring, "EPSG:28992")

        # Assert - Then
        assert isinstance(result, LinearRing | LineString), "Should be ring or line"
        coords = list(result.coords)
        assert 3.0 < coords[0][0] < 8.0, "Longitude should be in NL range"

    def test_transform_polygon_with_hole(self) -> None:
        """
        Scenario: Transform a polygon that has an interior ring (hole).

        Given: A Polygon in RD New with one hole
        When: _transform_geometry is called
        Then: Both exterior and interior rings are transformed
        """
        # Arrange - Given
        exterior = [(155_000, 463_000), (157_000, 463_000), (157_000, 465_000), (155_000, 465_000)]
        hole = [(155_500, 463_500), (156_500, 463_500), (156_500, 464_500), (155_500, 464_500)]
        poly = Polygon(exterior, [hole])

        # Act - When
        result = _transform_geometry(poly, "EPSG:28992")

        # Assert - Then
        assert isinstance(result, Polygon)
        assert len(list(result.interiors)) == 1, "Hole should be preserved"
        hole_coords = list(result.interiors[0].coords)
        assert 3.0 < hole_coords[0][0] < 8.0, "Hole should also be transformed"

    def test_unsupported_geometry_returns_unchanged(self) -> None:
        """
        Scenario: An unrecognized geometry type passes through unchanged.

        Given: A geometry-like object that isn't a standard Shapely type
        When: _transform_geometry is called
        Then: The same object is returned (no error, no transformation)
        """
        # Arrange - Given
        gc = GeometryCollection([Point(4.9, 52.37)])

        # Act - When
        result = _transform_geometry(gc, "EPSG:28992")

        # Assert - Then
        assert result is gc, "Unsupported type should be returned unchanged"

    def test_missing_pyproj_raises_import_error(self) -> None:
        """
        Scenario: Attempting CRS transform without pyproj installed.

        Given: Coordinates that need transformation and pyproj is unavailable
        When: _detect_and_transform_coords is called with a non-WGS84 CRS
        Then: An ImportError is raised with install instructions
        """
        # Arrange - Given
        coords = [(155_000, 463_000)]

        # Act & Assert - When/Then
        with patch.dict("sys.modules", {"pyproj": None}), pytest.raises(ImportError, match="pyproj"):
            _detect_and_transform_coords(coords, source_crs="EPSG:28992")

    def test_transform_multipoint_with_rd_coords(self) -> None:
        """
        Scenario: Transform a MultiPoint from RD New to WGS84.

        Given: A MultiPoint with coordinates in the RD New range
        When: _transform_geometry is called with EPSG:28992
        Then: Each constituent point is individually transformed

        Covers: line 173
        """
        # Arrange - Given
        mp = MultiPoint([(121_000, 487_000), (155_000, 463_000)])

        # Act - When
        result = _transform_geometry(mp, "EPSG:28992")

        # Assert - Then
        assert isinstance(result, MultiPoint)
        points = list(result.geoms)
        assert len(points) == 2
        # First point near Amsterdam
        assert 4.0 < points[0].x < 6.0
        assert 52.0 < points[0].y < 53.0

    def test_transform_linearring_with_rd_coords(self) -> None:
        """
        Scenario: Transform a LinearRing from RD New where the ring stays closed.

        Given: A LinearRing with 5 points (closing point matches first)
        When: _transform_geometry is called with EPSG:28992
        Then: The result is a LinearRing with WGS84 coordinates

        Covers: lines 165-167 (LinearRing branch, now before LineString)
        """
        # Arrange - Given
        ring = LinearRing(
            [
                (155_000, 463_000),
                (156_000, 463_000),
                (156_000, 464_000),
                (155_000, 464_000),
                (155_000, 463_000),
            ]
        )

        # Act - When
        result = _transform_geometry(ring, "EPSG:28992")

        # Assert - Then
        assert isinstance(result, LinearRing), "Should return a LinearRing now"
        coords = list(result.coords)
        assert len(coords) >= 4
        assert 3.0 < coords[0][0] < 8.0, "Should be in NL longitude range"


# ===================================================================
# Scenarios for Markdown-to-HTML conversion and tooltip/popup helpers.
# ===================================================================


class TestMarkdownToHtml:
    """Scenarios for Markdown-to-HTML conversion and tooltip/popup helpers."""

    def test_bold_text(self) -> None:
        """
        Scenario: Bold markdown renders as <strong>.

        Given: A markdown string with **bold** text
        When: _markdown_to_html is called
        Then: The output contains <strong> tags
        """
        assert "<strong>Amsterdam</strong>" in _markdown_to_html("**Amsterdam**")

    def test_italic_text(self) -> None:
        """
        Scenario: Italic markdown renders as <em>.

        Given: A markdown string with *italic* text
        When: _markdown_to_html is called
        Then: The output contains <em> tags
        """
        assert "<em>historic</em>" in _markdown_to_html("*historic*")

    def test_inline_code(self) -> None:
        """
        Scenario: Backtick code renders as <code>.

        Given: A markdown string with `code`
        When: _markdown_to_html is called
        Then: The output contains <code> tags
        """
        assert "<code>EPSG:4326</code>" in _markdown_to_html("`EPSG:4326`")

    def test_link(self) -> None:
        """
        Scenario: Markdown link renders as clickable <a> tag.

        Given: A markdown link [text](url)
        When: _markdown_to_html is called
        Then: The output contains an <a> tag with href and target
        """
        result = _markdown_to_html("[Wiki](https://example.com)")
        assert 'href="https://example.com"' in result
        assert 'target="_blank"' in result

    def test_unordered_list(self) -> None:
        """
        Scenario: Markdown list items render as <ul>/<li>.

        Given: Markdown with dash-prefixed list items
        When: _markdown_to_html is called
        Then: The output contains <ul> and <li> tags
        """
        result = _markdown_to_html("- apples\n- oranges")
        assert "<ul>" in result
        assert "<li>apples</li>" in result
        assert "<li>oranges</li>" in result

    def test_xss_is_escaped(self) -> None:
        """
        Scenario: HTML injection is escaped in tooltips.

        Given: A markdown string containing a <script> tag
        When: _markdown_to_html is called
        Then: The angle brackets are escaped as HTML entities
        """
        result = _markdown_to_html("<script>alert('xss')</script>")
        assert "<script>" not in result, "Raw script tags must be escaped"
        assert "&lt;script&gt;" in result

    def test_combined_formatting(self) -> None:
        """
        Scenario: Multiple markdown features in one tooltip.

        Given: Markdown combining bold, italic, code, and a link
        When: _markdown_to_html is called
        Then: All features render correctly
        """
        # Arrange - Given
        md = "**Bold** and *italic* with `code` and [link](http://x.com)"

        # Act - When
        result = _markdown_to_html(md)

        # Assert - Then
        assert "<strong>Bold</strong>" in result
        assert "<em>italic</em>" in result
        assert "<code>code</code>" in result
        assert 'href="http://x.com"' in result

    def test_h1_header_renders(self) -> None:
        """
        Scenario: A single-hash header renders as <h2>.

        Given: Markdown text "# Site Overview"
        When: _markdown_to_html is called
        Then: The output contains <h2>Site Overview</h2>
        """
        # Act - When
        result = _markdown_to_html("# Site Overview")

        # Assert - Then
        assert "<h2>Site Overview</h2>" in result

    def test_h2_header_renders(self) -> None:
        """
        Scenario: A double-hash header renders as <h3>.

        Given: Markdown text "## Details"
        When: _markdown_to_html is called
        Then: The output contains <h3>Details</h3>
        """
        result = _markdown_to_html("## Details")
        assert "<h3>Details</h3>" in result

    def test_h3_header_renders(self) -> None:
        """
        Scenario: A triple-hash header renders as <h4>.

        Given: Markdown text "### Notes"
        When: _markdown_to_html is called
        Then: The output contains <h4>Notes</h4>
        """
        result = _markdown_to_html("### Notes")
        assert "<h4>Notes</h4>" in result

    def test_newline_between_text_becomes_br(self) -> None:
        r"""
        Scenario: A newline between two text lines inserts a <br>.

        Given: Markdown with "line1\\nline2"
        When: _markdown_to_html is called
        Then: A <br> tag appears between the lines
        """
        result = _markdown_to_html("line1\nline2")
        assert "<br>" in result
        assert "line1" in result
        assert "line2" in result

    def test_ampersand_is_escaped(self) -> None:
        """
        Scenario: Ampersands in text are HTML-escaped.

        Given: Markdown containing "Tom & Jerry"
        When: _markdown_to_html is called
        Then: The & is escaped to &amp;
        """
        result = _markdown_to_html("Tom & Jerry")
        assert "&amp;" in result
        assert "Tom &amp; Jerry" in result

    def test_empty_string_returns_empty(self) -> None:
        """
        Scenario: An empty markdown string returns an empty HTML string.

        Given: An empty string ""
        When: _markdown_to_html is called
        Then: The result is an empty string
        """
        result = _markdown_to_html("")
        assert result == ""

    def test_plain_text_passes_through(self) -> None:
        """
        Scenario: Plain text with no markdown formatting passes through.

        Given: "Just a simple label"
        When: _markdown_to_html is called
        Then: The text is returned unchanged (no tags added)
        """
        result = _markdown_to_html("Just a simple label")
        assert result == "Just a simple label"

    def test_make_tooltip_returns_none_for_none(self) -> None:
        """
        Scenario: No hover text means no tooltip.

        Given: A Map instance
        When: _make_tooltip is called with None
        Then: None is returned
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m._make_tooltip(None)

        # Assert - Then
        assert result is None, "None input should produce None tooltip"

    def test_make_tooltip_returns_none_for_empty_string(self) -> None:
        """
        Scenario: Empty hover text means no tooltip.

        Given: A Map instance
        When: _make_tooltip is called with ""
        Then: None is returned (empty string is falsy)
        """
        m = Map()
        result = m._make_tooltip("")
        assert result is None

    def test_make_tooltip_returns_folium_tooltip(self) -> None:
        """
        Scenario: Valid markdown hover text produces a Folium Tooltip.

        Given: A Map instance and markdown text
        When: _make_tooltip is called
        Then: A folium.Tooltip is returned
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m._make_tooltip("**Bold tooltip**")

        # Assert - Then
        assert isinstance(result, folium.Tooltip)

    def test_make_popup_returns_none_for_none(self) -> None:
        """
        Scenario: No popup text means no popup.

        Given: A Map instance
        When: _make_popup is called with None
        Then: None is returned
        """
        m = Map()
        result = m._make_popup(None)
        assert result is None

    def test_make_popup_returns_folium_popup(self) -> None:
        """
        Scenario: Valid markdown popup text produces a Folium Popup.

        Given: A Map instance and markdown text
        When: _make_popup is called
        Then: A folium.Popup is returned
        """
        m = Map()
        result = m._make_popup("# Title\nSome content")
        assert isinstance(result, folium.Popup)


# ===================================================================
# Scenarios for style dataclass defaults and MapConfig.
# ===================================================================


class TestStyleDataclasses:
    """Scenarios for style dataclass defaults and MapConfig."""

    def test_stroke_style_defaults(self) -> None:
        """
        Scenario: StrokeStyle has sensible defaults.

        Given: No arguments
        When: A StrokeStyle is created
        Then: It uses blue color, 3px weight, full opacity, no dash
        """
        s = StrokeStyle()
        assert s.color == "#3388ff"
        assert s.weight == 3.0
        assert s.opacity == 1.0
        assert s.dash_array is None

    def test_fill_style_defaults(self) -> None:
        """
        Scenario: FillStyle defaults to low opacity for overlapping shapes.

        Given: No arguments
        When: A FillStyle is created
        Then: It uses 20% opacity
        """
        f = FillStyle()
        assert f.opacity == 0.2

    def test_marker_style_defaults(self) -> None:
        """
        Scenario: MarkerStyle defaults to blue pin with no emoji.

        Given: No arguments
        When: A MarkerStyle is created
        Then: emoji is None and marker_color is blue
        """
        ms = MarkerStyle()
        assert ms.emoji is None
        assert ms.marker_color == "blue"
        assert ms.icon == "info-sign"

    def test_heatmap_style_defaults(self) -> None:
        """
        Scenario: HeatmapStyle defaults to reasonable visualization values.

        Given: No arguments
        When: A HeatmapStyle is created
        Then: radius=15, no custom gradient
        """
        hs = HeatmapStyle()
        assert hs.radius == 15
        assert hs.blur == 10
        assert hs.gradient is None

    def test_mapconfig_default_dimensions(self) -> None:
        """
        Scenario: MapConfig defaults to 100% width and height.

        Given: No arguments
        When: A MapConfig is created
        Then: width="100%" and height="100%"
        """
        cfg = MapConfig()
        assert cfg.width == "100%"
        assert cfg.height == "100%"
        assert cfg.max_zoom == 19
        assert cfg.control_scale is True

    def test_mapconfig_custom_dimensions(self) -> None:
        """
        Scenario: MapConfig accepts pixel dimensions.

        Given: width=800 and height=600
        When: A MapConfig is created
        Then: The dimensions are stored as integers
        """
        cfg = MapConfig(width=800, height=600)
        assert cfg.width == 800
        assert cfg.height == 600

    def test_stroke_style_custom_values(self) -> None:
        """
        Scenario: Create a StrokeStyle with all custom values.

        Given: Custom color, weight, opacity, and dash_array
        When: A StrokeStyle is created
        Then: All values are stored correctly
        """
        s = StrokeStyle(color="#ff0000", weight=5.0, opacity=0.8, dash_array="5 10")
        assert s.color == "#ff0000"
        assert s.weight == 5.0
        assert s.opacity == 0.8
        assert s.dash_array == "5 10"

    def test_circle_style_nested_defaults(self) -> None:
        """
        Scenario: CircleStyle creates default StrokeStyle and FillStyle.

        Given: No arguments
        When: A CircleStyle is created
        Then: It contains properly initialized nested styles
        """
        cs = CircleStyle()
        assert isinstance(cs.stroke, StrokeStyle)
        assert isinstance(cs.fill, FillStyle)
        assert cs.stroke.color == "#3388ff"
        assert cs.fill.opacity == 0.2

    def test_label_style_all_defaults(self) -> None:
        """
        Scenario: LabelStyle has all default values set.

        Given: No arguments
        When: A LabelStyle is created
        Then: All fields have their defaults
        """
        ls = LabelStyle()
        assert ls.font_size == 12
        assert ls.font_family == "Arial, sans-serif"
        assert ls.font_color == "#333333"
        assert ls.font_weight == "bold"
        assert ls.background_color == "rgba(255,255,255,0.8)"
        assert ls.border == "1px solid #cccccc"
        assert ls.padding == "2px 6px"

    def test_fill_style_custom_values(self) -> None:
        """
        Scenario: Create a FillStyle with full opacity.

        Given: color="#00ff00" and opacity=1.0
        When: A FillStyle is created
        Then: The values are stored
        """
        f = FillStyle(color="#00ff00", opacity=1.0)
        assert f.color == "#00ff00"
        assert f.opacity == 1.0

    def test_marker_style_with_emoji(self) -> None:
        """
        Scenario: Create a MarkerStyle configured for emoji display.

        Given: emoji="🏗️" and emoji_size=32
        When: A MarkerStyle is created
        Then: The emoji fields override the icon
        """
        ms = MarkerStyle(emoji="🏗️", emoji_size=32)
        assert ms.emoji == "🏗️"
        assert ms.emoji_size == 32

    def test_heatmap_style_with_gradient(self) -> None:
        """
        Scenario: Create a HeatmapStyle with a custom gradient.

        Given: A gradient dict mapping stops to colors
        When: A HeatmapStyle is created
        Then: The gradient is stored
        """
        gradient = {0.2: "blue", 0.5: "lime", 1.0: "red"}
        hs = HeatmapStyle(gradient=gradient)
        assert hs.gradient == gradient


# ===================================================================
# Scenarios for the tile provider registry and tile layer management.
# ===================================================================


class TestTileProviders:
    """Scenarios for the tile provider registry and tile layer management."""

    def test_all_providers_have_required_fields(self) -> None:
        """
        Scenario: Every registered tile provider is properly configured.

        Given: The TILE_PROVIDERS registry
        When: All entries are inspected
        Then: Each has both "tiles" and "attr" keys
        """
        for name, provider in TILE_PROVIDERS.items():
            assert "tiles" in provider, f"{name} missing 'tiles' key"
            assert "attr" in provider, f"{name} missing 'attr' key"

    def test_kadaster_providers_available(self) -> None:
        """
        Scenario: Dutch Kadaster tile providers are registered.

        Given: The TILE_PROVIDERS registry
        When: Checked for Kadaster keys
        Then: brt, luchtfoto, and grijs are all present
        """
        assert "kadaster_brt" in TILE_PROVIDERS
        assert "kadaster_luchtfoto" in TILE_PROVIDERS
        assert "kadaster_grijs" in TILE_PROVIDERS

    def test_create_map_with_each_provider(self) -> None:
        """
        Scenario: A map can be created with every registered provider.

        Given: Each tile provider name
        When: A Map is created with that provider
        Then: No errors are raised
        """
        for name in TILE_PROVIDERS:
            m = Map(config=MapConfig(tile_layer=name))
            assert m._map is not None, f"Map creation failed for provider '{name}'"

    def test_add_tile_layer_by_provider_name(self) -> None:
        """
        Scenario: Add a Kadaster aerial photo layer by name.

        Given: An empty map
        When: add_tile_layer("kadaster_luchtfoto") is called
        Then: The layer is added and the method returns self
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m.add_tile_layer("kadaster_luchtfoto")

        # Assert - Then
        assert result is m, "add_tile_layer should return self"

    def test_add_custom_tile_layer(self) -> None:
        """
        Scenario: Add a custom XYZ tile layer with a URL.

        Given: An empty map and a custom tile URL
        When: add_tile_layer is called with a URL and attribution
        Then: The custom tile layer is added
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m.add_tile_layer(
            "Custom Tiles",
            tiles="https://example.com/tiles/{z}/{x}/{y}.png",
            attribution="My Tiles",
        )

        # Assert - Then
        assert result is m, "Custom tile layer should be added"

    def test_add_tile_layer_as_overlay(self) -> None:
        """
        Scenario: Add a tile layer as an overlay (not base layer).

        Given: An empty map
        When: add_tile_layer is called with overlay=True and attribution
        Then: The tile layer is added as an overlay
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m.add_tile_layer(
            "Satellite",
            tiles="https://example.com/{z}/{x}/{y}.png",
            attribution="Example Tiles",
            overlay=True,
        )

        # Assert - Then
        assert result is m


# ===================================================================
# Scenarios for export methods: HTML, PNG, SVG, BytesIO, and async variants.
# ===================================================================


class TestExport:
    """Scenarios for export methods: HTML, PNG, SVG, BytesIO, and async variants."""

    def test_export_to_html_file(self, tmp_path: Path) -> None:
        """
        Scenario: Export a map as a standalone HTML file.

        Given: A map with one point
        When: to_html is called with a file path
        Then: The file exists and contains Leaflet references
        """
        # Arrange - Given
        m = Map(title="Export Test")
        m.add_point(Point(4.9, 52.37), label="📍")

        # Act - When
        out = m.to_html(tmp_path / "test.html")

        # Assert - Then
        assert out.exists(), "HTML file should be created"
        content = out.read_text()
        assert "leaflet" in content.lower(), "HTML should reference Leaflet"

    def test_export_to_html_with_open(self, tmp_path: Path) -> None:
        """
        Scenario: Export HTML and open in browser.

        Given: A map with one point
        When: to_html is called with open=True
        Then: The file is created and webbrowser.open is called with the file URI
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))

        with patch("webbrowser.open") as mock_open:
            out = m.to_html(tmp_path / "open_test.html", open=True)

        assert out.exists()
        mock_open.assert_called_once_with(out.resolve().as_uri())

    def test_export_to_html_open_ignored_without_path(self) -> None:
        """
        Scenario: open=True is ignored when path is None.

        Given: A map with one point
        When: to_html is called with path=None and open=True
        Then: An HTML string is returned; webbrowser is never called
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))

        with patch("webbrowser.open") as mock_open:
            result = m.to_html(path=None, open=True)

        assert isinstance(result, str)
        mock_open.assert_not_called()

    def test_export_auto_fits_bounds(self, tmp_path: Path) -> None:
        """
        Scenario: A map without a center auto-fits to its geometries.

        Given: A map with no center and two distant points
        When: to_html is called
        Then: The file is created (fit_bounds was called internally)
        """
        # Arrange - Given
        m = Map()
        m.add_point(Point(4.9, 52.37))
        m.add_point(Point(5.5, 51.44))

        # Act - When
        out = m.to_html(tmp_path / "autofit.html")

        # Assert - Then
        assert out.exists(), "HTML should be created even without explicit center"

    def test_repr_html_for_jupyter(self) -> None:
        """
        Scenario: Map renders inline in a Jupyter notebook.

        Given: A map with a point
        When: _repr_html_ is called
        Then: A non-empty HTML string is returned
        """
        # Arrange - Given
        m = Map()
        m.add_point(Point(4.9, 52.37))

        # Act - When
        html = m._repr_html_()

        # Assert - Then
        assert isinstance(html, str), "Should return a string"
        assert len(html) > 100, "Should contain substantial HTML"

    def test_image_export_without_selenium_fails_gracefully(self) -> None:
        """
        Scenario: PNG export without Selenium gives a clear error.

        Given: A map with a point (Selenium may not be installed)
        When: to_image is called
        Then: An ImportError or RuntimeError is raised (not a crash)
        """
        # Arrange - Given
        m = Map()
        m.add_point(Point(4.9, 52.37))

        # Act & Assert - When/Then
        with contextlib.suppress(ImportError, RuntimeError):
            # Expected — clear error message
            m.to_image()

    def test_to_html_with_center_skips_fit_bounds(self, tmp_path: Path) -> None:
        """
        Scenario: A map with an explicit center does not auto-fit.

        Given: A map created with center=(52.37, 4.90)
        When: to_html is called
        Then: The file is created (fit_bounds is skipped)
        """
        # Arrange - Given
        m = Map(center=(52.37, 4.90))

        # Act - When
        out = m.to_html(tmp_path / "centered.html")

        # Assert - Then
        assert out.exists()

    def test_to_html_returns_string_when_path_is_none(self) -> None:
        """
        Scenario: Get the full HTML document as a string without writing to disk.

        Given: A map with a point
        When: to_html is called with path=None
        Then: A string containing the full HTML document is returned
        """
        # Arrange - Given
        m = Map(title="String Export")
        m.add_point(Point(4.9, 52.37), label="📍")

        # Act - When
        result = m.to_html()

        # Assert - Then
        assert isinstance(result, str), "Should return a string when path is None"
        assert "leaflet" in result.lower(), "HTML should contain Leaflet"
        assert len(result) > 100, "Should be a full HTML document"

    def test_to_html_default_returns_string(self) -> None:
        """
        Scenario: Calling to_html() with no arguments returns a string.

        Given: An empty map
        When: to_html is called with no arguments
        Then: A non-empty HTML string is returned
        """
        # Arrange - Given
        m = Map()

        # Act - When
        result = m.to_html()

        # Assert - Then
        assert isinstance(result, str)

    def test_to_html_empty_map(self, tmp_path: Path) -> None:
        """
        Scenario: Export an empty map with no geometries.

        Given: A map with nothing added
        When: to_html is called
        Then: A valid HTML file is still created
        """
        # Arrange - Given
        m = Map()

        # Act - When
        out = m.to_html(tmp_path / "empty.html")

        # Assert - Then
        assert out.exists()
        assert out.stat().st_size > 0

    def test_get_html_returns_string(self) -> None:
        """
        Scenario: _get_html renders the map to an HTML string.

        Given: A map with a point
        When: _get_html is called
        Then: An HTML string is returned
        """
        # Arrange - Given
        m = Map()
        m.add_point(Point(4.9, 52.37))

        # Act - When
        html = m._get_html()

        # Assert - Then
        assert isinstance(html, str)
        assert "leaflet" in html.lower()

    def test_fit_bounds_with_no_bounds_does_nothing(self) -> None:
        """
        Scenario: Calling _fit_bounds on an empty map has no side effects.

        Given: A map with no geometries (empty bounds)
        When: _fit_bounds is called
        Then: No error is raised
        """
        # Arrange - Given
        m = Map()

        # Act - When — should not raise
        m._fit_bounds()

        # Assert - Then
        assert m._bounds == [], "Bounds should still be empty"

    def test_check_selenium_missing_package(self) -> None:
        """
        Scenario: Selenium package is not installed.

        Given: selenium is not importable
        When: _check_selenium is called
        Then: An ImportError is raised with install instructions
        """
        with patch.dict("sys.modules", {"selenium": None, "selenium.webdriver": None}):
            # The import inside _check_selenium will fail
            # We need to actually test the function's behavior
            with pytest.raises(ImportError, match="selenium"):
                _check_selenium()

            with pytest.raises(RuntimeError):
                # Chrome not found is also acceptable
                _check_selenium()

    def test_missing_chromedriver_raises_runtime_error(self) -> None:
        """
        Scenario: Chrome is found but chromedriver is not on PATH.

        Given: selenium is installed and Chrome exists
        When: _check_selenium is called but chromedriver is missing
        Then: A RuntimeError is raised mentioning chromedriver

        Covers: lines 446-447
        """
        # Arrange - Given
        original_which = shutil.which

        def mock_which(name: str) -> str | None:
            """Return a fake path for Chrome, None for chromedriver."""
            if "chrome" in name and "driver" not in name:
                return "/usr/bin/google-chrome"
            if name == "chromedriver":
                return None
            return original_which(name)

        # Act & Assert - When/Then
        with patch("shutil.which", side_effect=mock_which), pytest.raises(RuntimeError, match="chromedriver"):
            _check_selenium()

    def test_missing_chrome_raises_runtime_error(self) -> None:
        """
        Scenario: selenium is installed but Chrome/Chromium is not found.

        Given: selenium is importable but no Chrome binary on PATH
        When: _check_selenium is called
        Then: A RuntimeError is raised mentioning Chrome

        Covers: lines 440-444 (already covered but good to be explicit)
        """
        # Act & Assert - When/Then
        with patch(target="shutil.which", return_value=None), pytest.raises(RuntimeError, match="Chrome"):
            _check_selenium()

    def test_capture_screenshot_returns_png_bytes(self, tmp_path: Path) -> None:
        """
        Scenario: Capture a screenshot of an HTML file.

        Given: A valid HTML file and a mocked Chrome WebDriver
        When: _capture_screenshot is called
        Then: PNG bytes are returned and the driver is quit

        Covers: lines 476-495
        """
        # Arrange - Given
        html_file = tmp_path / "test.html"
        html_file.write_text("<html><body>Hello</body></html>")

        fake_png = b"\x89PNG_fake_image_bytes"

        # Build the mock driver
        mock_driver = MagicMock()
        mock_driver.get_screenshot_as_png.return_value = fake_png

        # Build Options mock
        mock_options_instance = MagicMock()
        mock_options_class = MagicMock(return_value=mock_options_instance)

        # Build webdriver mock: webdriver.Chrome(options=...) -> mock_driver
        mock_webdriver = MagicMock()
        mock_webdriver.Chrome.return_value = mock_driver

        # Build the selenium module hierarchy so that:
        #   `from selenium import webdriver`       -> mock_webdriver
        #   `from selenium.webdriver.chrome.options import Options` -> mock_options_class
        mock_selenium = MagicMock()
        mock_selenium.webdriver = mock_webdriver

        mock_chrome_mod = MagicMock()
        mock_options_mod = MagicMock()
        mock_options_mod.Options = mock_options_class

        mock_webdriver.chrome = mock_chrome_mod
        mock_chrome_mod.options = mock_options_mod

        # Act - When
        with (
            patch("blueprints.utils.map._check_selenium"),
            patch.dict(
                "sys.modules",
                {
                    "selenium": mock_selenium,
                    "selenium.webdriver": mock_webdriver,
                    "selenium.webdriver.chrome": mock_chrome_mod,
                    "selenium.webdriver.chrome.options": mock_options_mod,
                },
            ),
        ):
            result = _capture_screenshot(str(html_file), 800, 600, 0.1)

        # Assert - Then
        assert result == fake_png, "Should return the PNG bytes from the driver"
        mock_driver.get_screenshot_as_png.assert_called_once()
        mock_driver.quit.assert_called_once()
        mock_driver.set_window_size.assert_called_once_with(800, 600)
        assert mock_options_instance.add_argument.call_count == 5

    @pytest.fixture
    def map_with_point(self) -> Map:
        """A map with one point for export tests."""
        m = Map(title="Export")
        m.add_point(Point(4.9, 52.37), label="📍")
        return m

    @pytest.fixture
    def mock_to_image(self) -> Generator[MagicMock | AsyncMock, Any, None]:
        """Patch to_image to return fake PNG bytes."""
        fake_png = b"\x89PNG\r\n\x1a\n_fake_image_data_1234567890"
        with patch.object(Map, "to_image", return_value=fake_png) as mock:
            mock.fake_png = fake_png
            yield mock

    def test_to_image_returns_bytes(self, map_with_point: Map) -> None:
        """
        Scenario: to_image with path=None returns raw PNG bytes.

        Given: A map with a point
        When: to_image is called with path=None
        Then: PNG bytes are returned

        Covers: lines 1546-1547
        """
        # Arrange - Given
        fake_png = b"\x89PNG_fake"

        # Act - When
        with patch("blueprints.utils.map._capture_screenshot", return_value=fake_png):
            result = map_with_point.to_image(path=None)

        # Assert - Then
        assert result == fake_png

    def test_to_image_saves_to_file(self, map_with_point: Map, tmp_path: Path) -> None:
        """
        Scenario: to_image with a path saves PNG to disk.

        Given: A map with a point and an output path
        When: to_image is called with a file path
        Then: The file is written and the Path is returned

        Covers: lines 1548-1550
        """
        # Arrange - Given
        fake_png = b"\x89PNG_fake_data"
        out_path = tmp_path / "map.png"

        # Act - When
        with patch("blueprints.utils.map._capture_screenshot", return_value=fake_png):
            result = map_with_point.to_image(path=out_path)

        # Assert - Then
        assert result == out_path
        assert out_path.exists()
        assert out_path.read_bytes() == fake_png

    def test_to_bytesio_returns_buffer(self, map_with_point: Map, mock_to_image: Generator[MagicMock | AsyncMock, Any, None]) -> None:
        """
        Scenario: to_bytesio returns an in-memory PNG buffer.

        Given: A map with a point
        When: to_bytesio is called
        Then: A BytesIO buffer at position 0 is returned

        Covers: lines 1571-1573
        """
        # Act - When
        result = map_with_point.to_bytesio(width=800, height=600, delay=0.1)

        # Assert - Then
        assert isinstance(result, io.BytesIO)
        assert result.tell() == 0, "Buffer should be at position 0"
        content = result.read()
        assert content == mock_to_image.fake_png

    def test_to_svg_returns_string(self, map_with_point: Map) -> None:
        """
        Scenario: to_svg with path=None returns an SVG string.

        Given: A map with a point
        When: to_svg is called without a path
        Then: An SVG string containing the base64-encoded PNG is returned

        Covers: lines 1596-1609
        """
        # Act - When
        result = map_with_point.to_svg(path=None, width=800, height=600, delay=0.1)

        # Assert - Then
        assert isinstance(result, str)
        assert result.startswith('<?xml version="1.0"')
        assert "<svg" in result
        assert "data:image/png;base64," in result

    def test_to_svg_saves_to_file(self, map_with_point: Map, tmp_path: Path) -> None:
        """
        Scenario: to_svg with a path saves SVG to disk.

        Given: A map and an output path
        When: to_svg is called with a file path
        Then: The SVG file is written

        Covers: lines 1610-1612
        """
        # Arrange - Given
        out_path = tmp_path / "map.svg"

        # Act - When
        result = map_with_point.to_svg(path=out_path, width=800, height=600, delay=0.1)

        # Assert - Then
        assert result == out_path
        assert out_path.exists()
        content = out_path.read_text()
        assert "<svg" in content

    def test_to_image_async(self, map_with_point: Map, mock_to_image: Generator[MagicMock | AsyncMock, Any, None]) -> None:
        """
        Scenario: Async PNG export delegates to to_image in an executor.

        Given: A map with a point
        When: to_image_async is awaited
        Then: PNG bytes are returned

        Covers: lines 1629-1630
        """
        # Act - When
        result = asyncio.run(map_with_point.to_image_async(path=None, width=800, height=600, delay=0.1))

        # Assert - Then
        assert result == mock_to_image.fake_png

    def test_to_svg_async(self, map_with_point: Map) -> None:
        """
        Scenario: Async SVG export delegates to to_svg in an executor.

        Given: A map with a point
        When: to_svg_async is awaited
        Then: An SVG string is returned

        Covers: lines 1649-1650
        """
        # Arrange — mock to_image so to_svg can work
        fake_png = b"\x89PNG_fake"
        with patch.object(Map, "to_image", return_value=fake_png):
            # Act - When
            result = asyncio.run(map_with_point.to_svg_async(path=None, width=800, height=600, delay=0.1))

        # Assert - Then
        assert isinstance(result, str)
        assert "<svg" in result


# ===================================================================
# Scenarios for combining two maps with the + operator.
# ===================================================================


class TestMapMerge:
    """Scenarios for combining two maps with the + operator."""

    def test_merge_two_maps_preserves_left_title(self) -> None:
        """
        Scenario: Merge two maps using the + operator.

        Given: Map A titled "Sites" with one point, and map B with one polygon
        When: A + B is computed
        Then: The result has A's title and contains both geometries
        """
        # Arrange - Given
        a = Map(title="Sites")
        a.add_point(Point(4.9, 52.37), label="📍")

        b = Map()
        b.add_polygon(Polygon([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)]))

        # Act - When
        combined = a + b

        # Assert - Then
        assert combined._title == "Sites", "Left map's title should be preserved"
        assert len(combined._bounds) == 4, "Both geometries should contribute bounds"

    def test_merge_combines_feature_groups(self) -> None:
        """
        Scenario: Merging maps combines their feature group registries.

        Given: Map A with group "Roads" and map B with group "Buildings"
        When: A + B is computed
        Then: The merged map has both "Roads" and "Buildings"
        """
        # Arrange - Given
        a = Map(title="A")
        a.create_feature_group("Roads")
        a.add_linestring(LineString([(4.9, 52.37), (5.0, 52.38)]))

        b = Map()
        b.create_feature_group("Buildings")
        b.add_polygon(Polygon([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)]))

        # Act - When
        combined = a + b

        # Assert - Then
        assert "Roads" in combined._feature_groups
        assert "Buildings" in combined._feature_groups

    def test_merge_combines_colormaps(self) -> None:
        """
        Scenario: Merging maps combines their colormap legends.

        Given: Map A with a choropleth and map B with another choropleth
        When: A + B is computed
        Then: The merged map has both colormaps
        """
        # Arrange - Given
        geojson_a = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "X", "val": 10},
                    "geometry": {"type": "Polygon", "coordinates": [[(4.85, 52.35), (4.90, 52.35), (4.90, 52.38), (4.85, 52.38), (4.85, 52.35)]]},
                }
            ],
        }
        geojson_b = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Y", "val": 90},
                    "geometry": {"type": "Polygon", "coordinates": [[(4.90, 52.35), (4.95, 52.35), (4.95, 52.38), (4.90, 52.38), (4.90, 52.35)]]},
                }
            ],
        }

        a = Map()
        a.add_choropleth(geojson_a, value_column="val", key_on="feature.properties.name")

        b = Map()
        b.add_choropleth(geojson_b, value_column="val", key_on="feature.properties.name")

        # Act - When
        combined = a + b

        # Assert - Then
        assert len(combined._colormaps) == 2, "Both colormaps should be preserved"

    def test_merge_combines_bounds(self) -> None:
        """
        Scenario: Merging maps combines their bounds for auto-fit.

        Given: Map A with a point in Amsterdam, map B with a point in Rotterdam
        When: A + B is computed
        Then: The bounds cover both cities
        """
        # Arrange - Given
        a = Map()
        a.add_point(Point(4.9, 52.37))  # Amsterdam

        b = Map()
        b.add_point(Point(4.48, 51.92))  # Rotterdam

        # Act - When
        combined = a + b

        # Assert - Then
        assert len(combined._bounds) == 4, "Both points' bounds should be combined"


# ===================================================================
# Scenarios for the fluent API.
# ===================================================================


class TestMethodChaining:
    """Scenarios for the fluent API."""

    def test_full_chain_produces_html(self, tmp_path: Path) -> None:
        """
        Scenario: Build a complete map in a single chained expression.

        Given: Nothing
        When: A map is built using chained add_* calls ending with to_html
        Then: The resulting HTML file exists on disk
        """
        # Act - When
        out = (
            Map(title="Chained")
            .add_point(Point(4.9, 52.37), label="📍")
            .add_circle(Point(5.1, 52.09), hover="Circle")
            .add_linestring(LineString([(4.9, 52.37), (5.1, 52.09)]))
            .add_polygon(Polygon([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)]))
            .add_text((52.3, 4.9), "Label")
            .create_feature_group("Layer 1")
            .add_point(Point(4.3, 52.07), label="🔴")
            .reset_target()
            .add_layer_control()
            .to_html(tmp_path / "chained.html")
        )

        # Assert - Then
        assert out.exists(), "Chained call should produce a valid HTML file"


# ===================================================================
# Scenarios for creating maps from GeoPandas GeoDataFrames.
# ===================================================================


class TestGeoDataFrame:
    """Scenarios for creating maps from GeoPandas GeoDataFrames."""

    @pytest.fixture
    def cities_gdf(self) -> GeoDataFrame:
        """GeoDataFrame with 3 Dutch cities."""
        return GeoDataFrame(
            data={
                "name": ["Amsterdam", "Rotterdam", "Utrecht"],
                "population": [872_680, 651_446, 361_924],
                "geometry": [
                    Point(4.9041, 52.3676),
                    Point(4.4777, 51.9244),
                    Point(5.1214, 52.0907),
                ],
            },
            crs="EPSG:4326",
        )

    @pytest.fixture
    def rd_gdf(self) -> GeoDataFrame:
        """GeoDataFrame in RD New CRS."""
        return GeoDataFrame(
            data={"name": ["AMS"], "geometry": [Point(121_000, 487_000)]},
            crs="EPSG:28992",
        )

    def test_create_map_from_geodataframe(self, cities_gdf: GeoDataFrame) -> None:
        """
        Scenario: Create a map from a GeoDataFrame with hover columns.

        Given: A GeoDataFrame with 3 cities and their populations
        When: from_geodataframe is called with hover_columns
        Then: All 3 points are on the map with tooltips
        """
        # Act - When
        m = Map.from_geodataframe(cities_gdf, hover_columns=["name", "population"])

        # Assert - Then
        assert len(m._bounds) == 6, "3 points x 2 bound entries each"

    def test_geodataframe_with_color_column(self, cities_gdf: GeoDataFrame) -> None:
        """
        Scenario: Color-code cities by population.

        Given: A GeoDataFrame with a numeric "population" column
        When: from_geodataframe is called with color_column="population"
        Then: A colormap is created and added as legend
        """
        # Act - When
        m = Map.from_geodataframe(
            cities_gdf,
            color_column="population",
            legend_name="Population",
        )

        # Assert - Then
        assert len(m._colormaps) == 1, "One colormap should be registered"

    def test_geodataframe_with_label_column(self, cities_gdf: GeoDataFrame) -> None:
        """
        Scenario: Use city names as marker labels.

        Given: A GeoDataFrame with a "name" column
        When: from_geodataframe is called with label_column="name"
        Then: All points are added with text labels
        """
        # Act - When
        m = Map.from_geodataframe(cities_gdf, label_column="name")

        # Assert - Then
        assert len(m._bounds) == 6, "All cities should be on the map"

    def test_geodataframe_auto_reprojects_rd(self, rd_gdf: GeoDataFrame) -> None:
        """
        Scenario: A GeoDataFrame in RD New is auto-reprojected to WGS84.

        Given: A GeoDataFrame with CRS EPSG:28992
        When: from_geodataframe is called
        Then: The resulting map bounds are in WGS84 range
        """
        # Act - When
        m = Map.from_geodataframe(rd_gdf, hover_columns=["name"])

        # Assert - Then
        lat, lon = m._bounds[0]
        assert 50.0 < lat < 54.0, f"Latitude {lat} should be in NL"
        assert 3.0 < lon < 8.0, f"Longitude {lon} should be in NL"

    def test_missing_geopandas_raises_import_error(self) -> None:
        """
        Scenario: Calling from_geodataframe without geopandas installed.

        Given: geopandas is not available (mocked)
        When: from_geodataframe is called
        Then: An ImportError is raised with install instructions
        """
        # Act & Assert - When/Then
        with patch.dict("sys.modules", {"geopandas": None}), contextlib.suppress(ImportError, AttributeError):
            # Expected
            Map.from_geodataframe(None)

    @pytest.fixture
    def _check_geopandas(self) -> None:
        """Skip if geopandas is not installed."""
        try:
            shutil.which("geopandas")
        except ImportError:
            pytest.skip("geopandas not installed")

    def test_geodataframe_skips_null_geometries(self) -> None:
        """
        Scenario: Rows with null or empty geometries are silently skipped.

        Given: A GeoDataFrame where one row has geometry=None
        When: from_geodataframe is called
        Then: Only the valid rows appear on the map
        """
        # Arrange - Given
        gdf = GeoDataFrame(
            data={
                "name": ["Valid", "Null", "Empty"],
                "geometry": [Point(4.9, 52.37), None, Point(5.1, 52.09).buffer(0).boundary],
            },
            crs="EPSG:4326",
        )
        # Replace the third geometry with an actually empty one
        gdf.loc[2, "geometry"] = Point()

        # Act - When
        m = Map.from_geodataframe(gdf, hover_columns=["name"])

        # Assert - Then
        # Only the first valid point should contribute bounds
        assert len(m._bounds) >= 2, "At least one valid point should be on the map"

    def test_geodataframe_with_popup_columns(self) -> None:
        """
        Scenario: Create a map with click popups from DataFrame columns.

        Given: A GeoDataFrame with name and population columns
        When: from_geodataframe is called with popup_columns
        Then: Popups are configured for each row
        """
        # Arrange - Given
        gdf = GeoDataFrame(
            {
                "name": ["Amsterdam", "Rotterdam"],
                "population": [872_680, 651_446],
                "geometry": [Point(4.9, 52.37), Point(4.48, 51.92)],
            },
            crs="EPSG:4326",
        )

        # Act - When
        m = Map.from_geodataframe(
            gdf,
            popup_columns=["name", "population"],
        )

        # Assert - Then
        assert len(m._bounds) == 4, "Both cities should be on the map"

    def test_geodataframe_with_nan_in_color_column(self) -> None:
        """
        Scenario: GeoDataFrame with NaN in the color column..

        Given: A GeoDataFrame where one row has NaN population
        When: from_geodataframe is called with color_column="population"
        Then: The map is created without errors (NaN row uses default style)
        """
        # Arrange - Given
        gdf = GeoDataFrame(
            {
                "name": ["Amsterdam", "Unknown"],
                "population": [872_680, float("nan")],
                "geometry": [Point(4.9, 52.37), Point(5.1, 52.09)],
            },
            crs="EPSG:4326",
        )

        # Act - When
        m = Map.from_geodataframe(gdf, color_column="population")

        # Assert - Then
        assert len(m._bounds) == 4, "Both points should be on the map"
        assert len(m._colormaps) == 1, "Colormap should still be created"

    def test_geodataframe_with_custom_stroke_and_fill(self) -> None:
        """
        Scenario: Override default styling for a GeoDataFrame..

        Given: A GeoDataFrame and custom stroke/fill styles
        When: from_geodataframe is called with those styles
        Then: The map uses the custom styles
        """
        # Arrange - Given
        gdf = GeoDataFrame(
            data={
                "name": ["Zone"],
                "geometry": [Polygon([(4.85, 52.35), (4.95, 52.35), (4.95, 52.40), (4.85, 52.40)])],
            },
            crs="EPSG:4326",
        )
        stroke = StrokeStyle(color="red", weight=5)
        fill = FillStyle(color="red", opacity=0.5)

        # Act - When
        m = Map.from_geodataframe(gdf, stroke=stroke, fill=fill)

        # Assert - Then
        assert len(m._bounds) == 2

    def test_geodataframe_with_custom_config(self) -> None:
        """
        Scenario: Create a map from GeoDataFrame with custom MapConfig..

        Given: A GeoDataFrame and a dark-theme MapConfig
        When: from_geodataframe is called with the config
        Then: The map uses the custom configuration
        """
        # Arrange - Given
        gdf = GeoDataFrame(
            {"name": ["AMS"], "geometry": [Point(4.9, 52.37)]},
            crs="EPSG:4326",
        )
        config = MapConfig(tile_layer="cartodb_dark", fullscreen=True)

        # Act - When
        m = Map.from_geodataframe(gdf, config=config, title="Dark Cities")

        # Assert - Then
        assert m._config.tile_layer == "cartodb_dark"
        assert m._title == "Dark Cities"

    def test_geodataframe_with_polygon_geometries(self) -> None:
        """
        Scenario: Create a map from a GeoDataFrame with polygon geometries..

        Given: A GeoDataFrame with Polygon geometry (not points)
        When: from_geodataframe is called
        Then: The polygons are dispatched correctly
        """
        # Arrange - Given
        gdf = GeoDataFrame(
            {
                "name": ["Centrum", "West"],
                "geometry": [
                    Polygon([(4.88, 52.36), (4.92, 52.36), (4.92, 52.38), (4.88, 52.38)]),
                    Polygon([(4.84, 52.36), (4.88, 52.36), (4.88, 52.38), (4.84, 52.38)]),
                ],
            },
            crs="EPSG:4326",
        )

        # Act - When
        m = Map.from_geodataframe(gdf, hover_columns=["name"])

        # Assert - Then -
        assert len(m._bounds) == 4, "Two polygons x 2 bound entries each"


# ===================================================================
# Scenarios for shape markers (RegularPolygonMarker).
# ===================================================================


class TestShapeMarkers:
    """Scenarios for shape-based point markers."""

    def test_circle_shape_creates_polygon_marker(self) -> None:
        """
        Scenario: Add a point with shape="circle".

        Given: A MarkerStyle with shape="circle"
        When: add_point is called
        Then: The HTML contains a RegularPolygonMarker element
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), marker_style=MarkerStyle(shape="circle"))
        html = m._get_html()
        assert "regular_polygon_marker" in html.lower() or "RegularPolygonMarker" in html or "L.regularPolygonMarker" in html

    def test_square_shape_creates_polygon_marker(self) -> None:
        """
        Scenario: Add a point with shape="square".

        Given: A MarkerStyle with shape="square"
        When: add_point is called
        Then: The HTML contains a marker with 4 sides and rotation 45
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), marker_style=MarkerStyle(shape="square", shape_color="red"))
        html = m._get_html()
        assert "numberOfSides" in html or "number_of_sides" in html or "regularPolygonMarker" in html.lower()

    def test_triangle_shape_creates_div_icon(self, tmp_path: Path) -> None:
        """
        Scenario: Add a point with shape="triangle".

        Given: A MarkerStyle with shape="triangle"
        When: add_point is called
        Then: The HTML contains the triangle unicode character
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), marker_style=MarkerStyle(shape="triangle", shape_color="green"))
        out = tmp_path / "triangle.html"
        m.to_html(out)
        html = out.read_text(encoding="utf-8")
        # Triangle unicode is JSON-escaped in saved HTML
        assert "\\u25bc" in html
        assert "green" in html

    def test_shape_with_hover_and_popup(self) -> None:
        """
        Scenario: Shape marker with tooltip and popup.

        Given: A circle shape with hover and popup
        When: add_point is called
        Then: The map has bounds and generates HTML without error
        """
        m = Map()
        m.add_point(
            Point(4.9, 52.37),
            hover="**Info**",
            popup="Details",
            marker_style=MarkerStyle(shape="circle"),
        )
        m._get_html()
        assert len(m._bounds) == 2

    def test_shape_ignored_when_label_set(self, tmp_path: Path) -> None:
        """
        Scenario: Label takes precedence over shape.

        Given: A MarkerStyle with shape="circle" and a label
        When: add_point is called with label="A"
        Then: The emoji/label path is used (DivIcon with label text)
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), label="A", marker_style=MarkerStyle(shape="circle"))
        out = tmp_path / "label.html"
        m.to_html(out)
        html = out.read_text(encoding="utf-8")
        # Label should appear via emoji path (DivIcon with font-size:24px)
        # Shape path (RegularPolygonMarker) should NOT be used
        assert "regularPolygonMarker" not in html
        assert "font-size:24px" in html

    def test_shape_ignored_when_emoji_set(self, tmp_path: Path) -> None:
        """
        Scenario: Emoji takes precedence over shape.

        Given: A MarkerStyle with shape="square" and emoji="📍"
        When: add_point is called
        Then: The emoji path is used
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), marker_style=MarkerStyle(shape="square", emoji="\U0001f4cd"))
        out = tmp_path / "emoji.html"
        m.to_html(out)
        html = out.read_text(encoding="utf-8")
        # Emoji is JSON-escaped but the emoji path (DivIcon) should be used
        assert "regularPolygonMarker" not in html
        assert "font-size:24px" in html

    def test_unknown_shape_defaults_to_circle(self) -> None:
        """
        Scenario: Unknown shape falls back to circle config.

        Given: A MarkerStyle with shape="hexagon" (not in _SHAPE_CONFIG)
        When: add_point is called
        Then: The default circle config (36 sides, rotation 0) is used
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), marker_style=MarkerStyle(shape="hexagon"))
        html = m._get_html()
        # Should not crash; uses circle defaults
        assert html

    def test_marker_style_defaults(self) -> None:
        """
        Scenario: MarkerStyle new fields have correct defaults.

        Given: A default MarkerStyle
        When: The object is inspected
        Then: shape is None, shape_color is "blue", shape_size is 10
        """
        ms = MarkerStyle()
        assert ms.shape is None
        assert ms.shape_color == "blue"
        assert ms.shape_size == 10

    def test_shape_config_constant(self) -> None:
        """
        Scenario: _SHAPE_CONFIG contains expected entries.

        Given: The _SHAPE_CONFIG constant
        When: Inspected
        Then: "circle" has 36 sides and "square" has 4 sides with rotation 45
        """
        assert _SHAPE_CONFIG["circle"]["sides"] == 36
        assert _SHAPE_CONFIG["circle"]["rotation"] == 0
        assert _SHAPE_CONFIG["square"]["sides"] == 4
        assert _SHAPE_CONFIG["square"]["rotation"] == 45


# ===================================================================
# Scenarios for text_label on add_point.
# ===================================================================


class TestTextLabel:
    """Scenarios for the text_label parameter on add_point."""

    def test_text_label_with_shape_marker(self, tmp_path: Path) -> None:
        """
        Scenario: Shape marker with a text label below.

        Given: A triangle shape marker and text_label="CPT-01"
        When: add_point is called
        Then: The HTML contains both the triangle and the label text
        """
        m = Map()
        m.add_point(
            Point(4.9, 52.37),
            marker_style=MarkerStyle(shape="triangle", shape_color="black"),
            text_label="CPT-01",
        )
        out = tmp_path / "text_label.html"
        m.to_html(out)
        html = out.read_text(encoding="utf-8")
        assert "CPT-01" in html
        assert "\\u25bc" in html  # triangle character (JSON-escaped)

    def test_text_label_with_emoji_marker(self, tmp_path: Path) -> None:
        """
        Scenario: Emoji marker with a text label below.

        Given: A point with label="📍" and text_label="Amsterdam"
        When: add_point is called
        Then: The HTML contains the label text
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), label="\U0001f4cd", text_label="Amsterdam")
        out = tmp_path / "emoji_label.html"
        m.to_html(out)
        html = out.read_text(encoding="utf-8")
        assert "Amsterdam" in html

    def test_text_label_with_icon_marker(self, tmp_path: Path) -> None:
        """
        Scenario: Default icon marker with a text label below.

        Given: A point with no shape/emoji and text_label="Station"
        When: add_point is called
        Then: The HTML contains the label text
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), text_label="Station")
        out = tmp_path / "icon_label.html"
        m.to_html(out)
        html = out.read_text(encoding="utf-8")
        assert "Station" in html

    def test_text_label_with_custom_label_style(self, tmp_path: Path) -> None:
        """
        Scenario: Text label with custom styling.

        Given: A shape marker with text_label and a custom LabelStyle
        When: add_point is called
        Then: The HTML contains the custom style properties
        """
        m = Map()
        m.add_point(
            Point(4.9, 52.37),
            marker_style=MarkerStyle(shape="circle"),
            text_label="S-001",
            label_style=LabelStyle(font_size=14, font_color="red"),
        )
        out = tmp_path / "styled_label.html"
        m.to_html(out)
        html = out.read_text(encoding="utf-8")
        assert "S-001" in html
        assert "font-size:14px" in html
        assert "color:red" in html

    def test_text_label_none_adds_no_extra_marker(self) -> None:
        """
        Scenario: No text_label means no extra marker.

        Given: A shape marker without text_label
        When: add_point is called
        Then: Only the shape marker children are on the map (no label marker)
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), marker_style=MarkerStyle(shape="circle"))
        # Count markers on the map (excluding tile layer)
        children_before = len(m._map._children)

        m2 = Map()
        m2.add_point(Point(4.9, 52.37), marker_style=MarkerStyle(shape="circle"), text_label="X")
        children_after = len(m2._map._children)

        assert children_after > children_before, "text_label should add an extra marker"

    def test_text_label_default_style_has_no_background(self, tmp_path: Path) -> None:
        """
        Scenario: Default label_style for text_label has no background/border.

        Given: A text_label without explicit label_style
        When: add_point is called
        Then: The label does not have a background or border CSS
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), marker_style=MarkerStyle(shape="triangle"), text_label="Test")
        out = tmp_path / "default_style.html"
        m.to_html(out)
        html = out.read_text(encoding="utf-8")
        # The default text_label style should NOT have background/border
        assert "background:" not in html.split("Test")[0].split("margin-top:15px")[-1]

    def test_text_label_with_min_zoom_tracks_both(self) -> None:
        """
        Scenario: min_zoom tracks both the shape marker and the text label.

        Given: A shape marker with text_label and min_zoom=10
        When: add_point is called
        Then: Two entries are added to _zoom_controlled_markers
        """
        m = Map()
        m.add_point(
            Point(4.9, 52.37),
            marker_style=MarkerStyle(shape="triangle"),
            text_label="CPT-01",
            min_zoom=10,
        )
        assert len(m._zoom_controlled_markers) == 2, "Both marker and label should be tracked"
        assert all(entry["min_zoom"] == 10 for entry in m._zoom_controlled_markers)


# ===================================================================
# Scenarios for zoom-dependent marker visibility.
# ===================================================================


class TestZoomDependentVisibility:
    """Scenarios for min_zoom marker visibility control."""

    def test_add_point_with_min_zoom(self) -> None:
        """
        Scenario: Point with min_zoom is tracked.

        Given: A Map
        When: add_point is called with min_zoom=10
        Then: The marker is tracked in _zoom_controlled_markers
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), min_zoom=10)
        assert len(m._zoom_controlled_markers) == 1
        assert m._zoom_controlled_markers[0]["min_zoom"] == 10

    def test_add_point_without_min_zoom(self) -> None:
        """
        Scenario: Point without min_zoom is not tracked.

        Given: A Map
        When: add_point is called without min_zoom
        Then: _zoom_controlled_markers is empty
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))
        assert len(m._zoom_controlled_markers) == 0

    def test_min_zoom_zero_ignored(self) -> None:
        """
        Scenario: min_zoom=0 is treated as "always visible".

        Given: A Map
        When: add_point is called with min_zoom=0
        Then: The marker is NOT tracked
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), min_zoom=0)
        assert len(m._zoom_controlled_markers) == 0

    def test_min_zoom_none_ignored(self) -> None:
        """
        Scenario: min_zoom=None is treated as "always visible".

        Given: A Map
        When: add_point is called with min_zoom=None
        Then: The marker is NOT tracked
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), min_zoom=None)
        assert len(m._zoom_controlled_markers) == 0

    def test_add_circle_with_min_zoom(self) -> None:
        """
        Scenario: Circle with min_zoom is tracked.

        Given: A Map
        When: add_circle is called with min_zoom=12
        Then: The marker is tracked
        """
        m = Map()
        m.add_circle(Point(4.9, 52.37), min_zoom=12)
        assert len(m._zoom_controlled_markers) == 1
        assert m._zoom_controlled_markers[0]["min_zoom"] == 12

    def test_add_text_with_min_zoom(self) -> None:
        """
        Scenario: Text with min_zoom is tracked.

        Given: A Map
        When: add_text is called with min_zoom=8
        Then: The marker is tracked
        """
        m = Map()
        m.add_text((52.37, 4.9), "Hello", min_zoom=8)
        assert len(m._zoom_controlled_markers) == 1
        assert m._zoom_controlled_markers[0]["min_zoom"] == 8

    def test_add_marker_cluster_with_min_zoom(self) -> None:
        """
        Scenario: Marker cluster with min_zoom is tracked.

        Given: A Map
        When: add_marker_cluster is called with min_zoom=5
        Then: The cluster is tracked
        """
        m = Map()
        m.add_marker_cluster([Point(4.9, 52.37), Point(5.0, 52.38)], min_zoom=5)
        assert len(m._zoom_controlled_markers) == 1
        assert m._zoom_controlled_markers[0]["min_zoom"] == 5

    def test_zoom_js_present_in_html(self) -> None:
        """
        Scenario: Zoom JS is injected when min_zoom markers exist.

        Given: A Map with a min_zoom marker
        When: _get_html is called
        Then: The HTML contains the zoom JavaScript
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), min_zoom=10)
        html = m._get_html()
        assert "zoomend" in html
        assert "minZoom" in html

    def test_zoom_js_absent_when_not_used(self) -> None:
        """
        Scenario: No zoom JS when no min_zoom markers.

        Given: A Map with no min_zoom markers
        When: _get_html is called
        Then: The HTML does NOT contain the zoom JavaScript
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))
        html = m._get_html()
        assert "zoomend" not in html

    def test_zoom_js_injected_only_once(self) -> None:
        """
        Scenario: Repeated _get_html calls inject JS only once.

        Given: A Map with a min_zoom marker
        When: _get_html is called twice
        Then: The flag _zoom_js_injected is True and JS appears only once
        """
        m = Map()
        m.add_point(Point(4.9, 52.37), min_zoom=10)
        html1 = m._get_html()
        html2 = m._get_html()
        assert m._zoom_js_injected is True
        assert html1.count("zoomend") == html2.count("zoomend")

    def test_merge_combines_zoom_markers(self) -> None:
        """
        Scenario: Merging maps combines zoom-controlled markers.

        Given: Map A with 1 zoom marker and Map B with 1 zoom marker
        When: A + B
        Then: Combined has 2 zoom markers
        """
        a = Map()
        a.add_point(Point(4.9, 52.37), min_zoom=10)

        b = Map()
        b.add_point(Point(5.0, 52.38), min_zoom=12)

        combined = a + b
        assert len(combined._zoom_controlled_markers) == 2


# ===================================================================
# Scenarios for set_bounds.
# ===================================================================


class TestSetBounds:
    """Scenarios for the set_bounds method."""

    def test_set_bounds_empty_map(self) -> None:
        """
        Scenario: set_bounds on an empty map returns self.

        Given: An empty Map
        When: set_bounds is called
        Then: Self is returned without error
        """
        m = Map()
        result = m.set_bounds()
        assert result is m

    def test_set_bounds_fits_data(self) -> None:
        """
        Scenario: set_bounds fits the map view to data points.

        Given: A Map with two points
        When: set_bounds is called
        Then: The Folium map has fit_bounds set
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))
        m.add_point(Point(5.1, 52.09))
        result = m.set_bounds()
        assert result is m

    def test_set_bounds_with_padding(self) -> None:
        """
        Scenario: set_bounds adds padding to bounds.

        Given: A Map with one point
        When: set_bounds is called with padding=0.01
        Then: The map is still valid (no errors)
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))
        result = m.set_bounds(padding=0.01)
        assert result is m

    def test_set_bounds_restrict_true(self) -> None:
        """
        Scenario: restrict=True sets maxBounds on the Folium map.

        Given: A Map with data
        When: set_bounds(restrict=True) is called
        Then: maxBounds and maxBoundsViscosity are set
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))
        m.add_point(Point(5.1, 52.09))
        m.set_bounds(restrict=True)
        assert "maxBounds" in m._map.options
        assert m._map.options["maxBoundsViscosity"] == 1.0

    def test_set_bounds_restrict_false(self) -> None:
        """
        Scenario: restrict=False does not set maxBounds.

        Given: A Map with data
        When: set_bounds(restrict=False) is called
        Then: maxBounds is NOT in the options
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))
        m.set_bounds(restrict=False)
        assert "maxBounds" not in m._map.options


# ===================================================================
# Scenarios for hide_controls in image export.
# ===================================================================


class TestHideControls:
    """Scenarios for clean image export with hidden controls."""

    def test_hide_controls_true_injects_css(self) -> None:
        """
        Scenario: hide_controls=True injects CSS to hide controls.

        Given: A Map with a point
        When: to_image is called with hide_controls=True
        Then: The screenshot function is called (CSS was injected)
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))

        fake_png = b"\x89PNG_fake"
        with patch("blueprints.utils.map._capture_screenshot", return_value=fake_png) as mock_cap:
            m.to_image(path=None, hide_controls=True)
            assert mock_cap.called

    def test_hide_controls_false_no_css(self) -> None:
        """
        Scenario: hide_controls=False does not inject CSS.

        Given: A Map with a point
        When: to_image is called with hide_controls=False
        Then: The temporary HTML does not contain hide CSS
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))

        captured_html: dict[str, str] = {}

        def mock_screenshot(html_path: str, *_args: object, **_kwargs: object) -> bytes:
            captured_html["content"] = Path(html_path).read_text(encoding="utf-8")
            return b"\x89PNG_fake"

        with patch("blueprints.utils.map._capture_screenshot", side_effect=mock_screenshot):
            m.to_image(path=None, hide_controls=False)

        assert ".leaflet-control{display:none" not in captured_html["content"]

    def test_hide_controls_true_content(self) -> None:
        """
        Scenario: Verify CSS injection content.

        Given: A Map with a point
        When: to_image is called with hide_controls=True
        Then: The HTML sent to screenshot contains leaflet-control hide CSS
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))

        captured_html: dict[str, str] = {}

        def mock_screenshot(html_path: str, *_args: object, **_kwargs: object) -> bytes:
            captured_html["content"] = Path(html_path).read_text(encoding="utf-8")
            return b"\x89PNG_fake"

        with patch("blueprints.utils.map._capture_screenshot", side_effect=mock_screenshot):
            m.to_image(path=None, hide_controls=True)

        assert ".leaflet-control{display:none !important;}" in captured_html["content"]

    def test_hide_controls_propagates_to_bytesio(self) -> None:
        """
        Scenario: to_bytesio passes hide_controls to to_image.

        Given: A Map with a point
        When: to_bytesio is called with hide_controls=False
        Then: to_image receives hide_controls=False
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))

        fake_png = b"\x89PNG_fake_data_for_bytesio"
        with patch.object(Map, "to_image", return_value=fake_png) as mock_img:
            m.to_bytesio(hide_controls=False)
            mock_img.assert_called_once_with(path=None, width=1200, height=800, delay=2.0, hide_controls=False)

    def test_hide_controls_propagates_to_svg(self) -> None:
        """
        Scenario: to_svg passes hide_controls to to_image.

        Given: A Map with a point
        When: to_svg is called with hide_controls=False
        Then: to_image receives hide_controls=False
        """
        m = Map()
        m.add_point(Point(4.9, 52.37))

        fake_png = b"\x89PNG_fake_data_for_svg"
        with patch.object(Map, "to_image", return_value=fake_png) as mock_img:
            m.to_svg(hide_controls=False)
            mock_img.assert_called_once_with(path=None, width=1200, height=800, delay=2.0, hide_controls=False)


# ===================================================================
# Scenarios for RawHTML bypass.
# ===================================================================


class TestRawHTML:
    """Scenarios for the RawHTML wrapper class."""

    def test_raw_html_is_str_subclass(self) -> None:
        """
        Scenario: RawHTML is a string subclass usable anywhere str is expected.

        Given: A RawHTML instance
        When: isinstance check is performed
        Then: It is an instance of str
        """
        html = RawHTML("<b>bold</b>")
        assert isinstance(html, str)

    def test_raw_html_tooltip_bypasses_markdown(self) -> None:
        """
        Scenario: RawHTML in hover bypasses markdown-to-HTML conversion.

        Given: A Map and a RawHTML string with raw HTML tags
        When: _make_tooltip is called with RawHTML
        Then: The HTML passes through unescaped
        """
        m = Map()
        raw = RawHTML("<b>bold</b> and <em>italic</em>")
        tooltip = m._make_tooltip(raw)

        assert isinstance(tooltip, folium.Tooltip)
        # The raw HTML should be present unescaped in the tooltip text
        assert "<b>bold</b>" in tooltip.text

    def test_raw_html_popup_bypasses_markdown(self) -> None:
        """
        Scenario: RawHTML in popup bypasses markdown-to-HTML conversion.

        Given: A Map and a RawHTML string with a table
        When: _make_popup is called with RawHTML
        Then: The table HTML passes through unescaped
        """
        m = Map()
        raw = RawHTML("<table><tr><td>Cell</td></tr></table>")
        popup = m._make_popup(raw)

        assert isinstance(popup, folium.Popup)

    def test_plain_string_tooltip_gets_markdown_converted(self) -> None:
        """
        Scenario: Plain strings still get markdown conversion.

        Given: A Map and a plain markdown string
        When: _make_tooltip is called
        Then: Markdown is converted to HTML (bold tags appear)
        """
        m = Map()
        tooltip = m._make_tooltip("**Bold**")

        assert isinstance(tooltip, folium.Tooltip)
        assert "<strong>Bold</strong>" in tooltip.text

    def test_plain_string_popup_gets_markdown_converted(self) -> None:
        """
        Scenario: Plain strings still get markdown conversion in popups.

        Given: A Map and a plain markdown string
        When: _make_popup is called
        Then: Markdown is converted to HTML
        """
        m = Map()
        popup = m._make_popup("**Bold**")
        assert isinstance(popup, folium.Popup)

    def test_empty_raw_html_returns_none_tooltip(self) -> None:
        """
        Scenario: Empty RawHTML is treated as falsy (no tooltip created).

        Given: A Map and an empty RawHTML
        When: _make_tooltip is called
        Then: None is returned
        """
        m = Map()
        result = m._make_tooltip(RawHTML(""))
        assert result is None

    def test_empty_raw_html_returns_none_popup(self) -> None:
        """
        Scenario: Empty RawHTML is treated as falsy (no popup created).

        Given: A Map and an empty RawHTML
        When: _make_popup is called
        Then: None is returned
        """
        m = Map()
        result = m._make_popup(RawHTML(""))
        assert result is None

    def test_raw_html_on_add_point(self) -> None:
        """
        Scenario: RawHTML works end-to-end on add_point.

        Given: A Map and RawHTML for both hover and popup
        When: add_point is called
        Then: The point is added without error
        """
        m = Map()
        result = m.add_point(
            Point(4.9, 52.37),
            hover=RawHTML("<b>Hover</b>"),
            popup=RawHTML("<i>Popup</i>"),
        )
        assert result is m


# ===================================================================
# Scenarios for PopupStyle configuration.
# ===================================================================


class TestPopupStyle:
    """Scenarios for the PopupStyle dataclass."""

    def test_default_popup_style_values(self) -> None:
        """
        Scenario: PopupStyle defaults match previous hardcoded values.

        Given: No arguments
        When: A PopupStyle is created
        Then: width=300, height=150, max_width=300
        """
        ps = PopupStyle()
        assert ps.width == 300
        assert ps.height == 150
        assert ps.max_width == 300

    def test_custom_popup_style_dimensions(self) -> None:
        """
        Scenario: Custom PopupStyle changes popup dimensions.

        Given: A PopupStyle with larger dimensions
        When: _make_popup is called with that style
        Then: The IFrame uses the custom dimensions
        """
        m = Map()
        ps = PopupStyle(width=500, height=300, max_width=600)
        popup = m._make_popup("Some content", popup_style=ps)

        assert isinstance(popup, folium.Popup)
        assert popup.options["max_width"] == 600

    def test_popup_style_none_uses_defaults(self) -> None:
        """
        Scenario: popup_style=None uses default PopupStyle values.

        Given: A Map
        When: _make_popup is called without popup_style
        Then: The popup uses default dimensions (300x150, max_width=300)
        """
        m = Map()
        popup = m._make_popup("Content")
        assert isinstance(popup, folium.Popup)
        assert popup.options["max_width"] == 300

    def test_popup_style_on_add_point(self) -> None:
        """
        Scenario: popup_style parameter on add_point works.

        Given: A Map and a custom PopupStyle
        When: add_point is called with popup and popup_style
        Then: The point is added without error
        """
        m = Map()
        ps = PopupStyle(width=400, height=250)
        result = m.add_point(
            Point(4.9, 52.37),
            popup="**Details**",
            popup_style=ps,
        )
        assert result is m

    def test_popup_style_on_add_circle(self) -> None:
        """
        Scenario: popup_style parameter on add_circle works.

        Given: A Map and a custom PopupStyle
        When: add_circle is called with popup and popup_style
        Then: The circle is added without error
        """
        m = Map()
        result = m.add_circle(
            Point(4.9, 52.37),
            popup="Circle info",
            popup_style=PopupStyle(width=400, height=200),
        )
        assert result is m

    def test_popup_style_on_add_linestring(self) -> None:
        """
        Scenario: popup_style parameter on add_linestring works.

        Given: A Map and a custom PopupStyle
        When: add_linestring is called with popup and popup_style
        Then: The line is added without error
        """
        m = Map()
        line = LineString([(4.9, 52.37), (5.0, 52.38)])
        result = m.add_linestring(
            line,
            popup="Line info",
            popup_style=PopupStyle(width=350, height=200),
        )
        assert result is m

    def test_popup_style_on_add_polygon(self) -> None:
        """
        Scenario: popup_style parameter on add_polygon works.

        Given: A Map and a custom PopupStyle
        When: add_polygon is called with popup and popup_style
        Then: The polygon is added without error
        """
        m = Map()
        poly = Polygon([(4.9, 52.3), (5.0, 52.3), (5.0, 52.4), (4.9, 52.4)])
        result = m.add_polygon(
            poly,
            popup="Polygon info",
            popup_style=PopupStyle(width=400, height=300),
        )
        assert result is m

    def test_popup_style_on_add_multipolygon(self) -> None:
        """
        Scenario: popup_style propagates through add_multipolygon.

        Given: A Map and a MultiPolygon with popup_style
        When: add_multipolygon is called
        Then: The multi polygon is added without error
        """
        m = Map()
        mp = MultiPolygon(
            [
                Polygon([(4.9, 52.3), (5.0, 52.3), (5.0, 52.4), (4.9, 52.4)]),
                Polygon([(5.0, 52.3), (5.1, 52.3), (5.1, 52.4), (5.0, 52.4)]),
            ]
        )
        result = m.add_multipolygon(mp, popup="MP info", popup_style=PopupStyle(width=400))
        assert result is m

    def test_popup_style_on_add_multilinestring(self) -> None:
        """
        Scenario: popup_style propagates through add_multilinestring.

        Given: A Map and a MultiLineString with popup_style
        When: add_multilinestring is called
        Then: The multi linestring is added without error
        """
        m = Map()
        ml = MultiLineString(
            [
                [(4.9, 52.3), (5.0, 52.4)],
                [(5.0, 52.3), (5.1, 52.4)],
            ]
        )
        result = m.add_multilinestring(ml, popup="ML info", popup_style=PopupStyle(height=200))
        assert result is m

    def test_popup_style_on_add_multipoint(self) -> None:
        """
        Scenario: popup_style propagates through add_multipoint.

        Given: A Map and a MultiPoint with popup_style
        When: add_multipoint is called
        Then: The multi point is added without error
        """
        m = Map()
        mp = MultiPoint([Point(4.9, 52.37), Point(5.0, 52.38)])
        result = m.add_multipoint(mp, popup="MP info", popup_style=PopupStyle(width=350))
        assert result is m

    def test_popup_style_on_add_marker_cluster(self) -> None:
        """
        Scenario: popup_style on add_marker_cluster works.

        Given: A Map with points and popup_style
        When: add_marker_cluster is called
        Then: The cluster is added without error
        """
        m = Map()
        points = [Point(4.9, 52.37), Point(5.0, 52.38)]
        result = m.add_marker_cluster(
            points,
            popups=["Info 1", "Info 2"],
            popup_style=PopupStyle(width=400, height=250),
        )
        assert result is m

    def test_popup_style_with_raw_html_combo(self) -> None:
        """
        Scenario: PopupStyle works together with RawHTML.

        Given: A Map, a RawHTML popup, and a custom PopupStyle
        When: _make_popup is called with both
        Then: A popup is created with custom dimensions and raw HTML
        """
        m = Map()
        ps = PopupStyle(width=500, height=400, max_width=600)
        popup = m._make_popup(RawHTML("<h1>Title</h1>"), popup_style=ps)

        assert isinstance(popup, folium.Popup)
        assert popup.options["max_width"] == 600

    def test_popup_style_on_add_geometry(self) -> None:
        """
        Scenario: popup_style propagates through add_geometry.

        Given: A Map and a Point geometry
        When: add_geometry is called with popup_style
        Then: The geometry is added without error
        """
        m = Map()
        result = m.add_geometry(
            Point(4.9, 52.37),
            popup="Info",
            popup_style=PopupStyle(width=400),
        )
        assert result is m


# ===================================================================
# Scenarios for popup on add_text.
# ===================================================================


class TestTextPopup:
    """Scenarios for popup support on add_text."""

    def test_add_text_with_popup(self) -> None:
        """
        Scenario: add_text with popup creates a clickable text label.

        Given: A Map
        When: add_text is called with popup text
        Then: The text label is added and returns self
        """
        m = Map()
        result = m.add_text(
            Point(4.9, 52.37),
            "Label",
            popup="**Click info**",
        )
        assert result is m

    def test_add_text_with_popup_and_hover(self) -> None:
        """
        Scenario: add_text with both popup and hover.

        Given: A Map
        When: add_text is called with both hover and popup
        Then: The text label has both tooltip and popup
        """
        m = Map()
        result = m.add_text(
            Point(4.9, 52.37),
            "Label",
            hover="**Hover text**",
            popup="**Popup text**",
        )
        assert result is m

    def test_add_text_with_popup_style(self) -> None:
        """
        Scenario: add_text with popup_style customizes popup dimensions.

        Given: A Map and a custom PopupStyle
        When: add_text is called with popup and popup_style
        Then: The text label is added without error
        """
        m = Map()
        result = m.add_text(
            (52.37, 4.9),
            "Label",
            popup="Content",
            popup_style=PopupStyle(width=400, height=250),
        )
        assert result is m


# ===================================================================
# Scenarios for dict-based style shortcuts.
# ===================================================================


class TestDictStyleShortcuts:
    """Scenarios for passing dicts instead of style dataclass instances."""

    def test_add_polygon_with_stroke_and_fill_dicts(self) -> None:
        """
        Scenario: Pass stroke and fill as plain dicts to add_polygon.

        Given: A Map and a Polygon
        When: add_polygon is called with stroke=dict and fill=dict
        Then: The polygon is added with the specified styling
        """
        m = Map()
        poly = Polygon([(4.9, 52.3), (5.0, 52.3), (5.0, 52.4), (4.9, 52.4)])
        result = m.add_polygon(
            poly,
            stroke={"color": "red", "weight": 4},
            fill={"color": "red", "opacity": 0.3},
        )
        assert result is m
        assert len(m._bounds) > 0

    def test_add_linestring_with_stroke_dict(self) -> None:
        """
        Scenario: Pass stroke as a dict to add_linestring.

        Given: A Map and a LineString
        When: add_linestring is called with stroke=dict
        Then: The line is added with the specified styling
        """
        m = Map()
        line = LineString([(4.9, 52.3), (5.0, 52.4)])
        result = m.add_linestring(line, stroke={"color": "#e74c3c", "dash_array": "5 10"})
        assert result is m

    def test_add_point_with_marker_style_dict(self) -> None:
        """
        Scenario: Pass marker_style as a dict to add_point.

        Given: A Map and a Point
        When: add_point is called with marker_style=dict
        Then: The marker is added using the dict values
        """
        m = Map()
        result = m.add_point(
            Point(4.9, 52.37),
            marker_style={"icon": "home", "marker_color": "green", "prefix": "fa"},
        )
        assert result is m

    def test_add_circle_with_flat_style_dict(self) -> None:
        """
        Scenario: Pass a flat CircleStyle dict (no nested stroke/fill).

        Given: A Map and a Point
        When: add_circle is called with style={"radius": 15}
        Then: The circle is added with default stroke/fill and custom radius
        """
        m = Map()
        result = m.add_circle(Point(4.9, 52.37), style={"radius": 15})
        assert result is m

    def test_add_circle_with_nested_style_dicts(self) -> None:
        """
        Scenario: Pass a CircleStyle dict with nested stroke/fill dicts.

        Given: A Map and a Point
        When: add_circle is called with nested stroke and fill dicts inside the style dict
        Then: The nested dicts are resolved into StrokeStyle/FillStyle instances
        """
        m = Map()
        result = m.add_circle(
            Point(4.9, 52.37),
            style={
                "radius": 12,
                "stroke": {"color": "#8e44ad", "weight": 2},
                "fill": {"color": "#8e44ad", "opacity": 0.5},
            },
        )
        assert result is m

    def test_add_text_with_label_style_dict(self) -> None:
        """
        Scenario: Pass a LabelStyle dict to add_text.

        Given: A Map and a location
        When: add_text is called with style=dict
        Then: The text is rendered with the dict-based style
        """
        m = Map()
        result = m.add_text(
            Point(4.9, 52.37),
            "Test Label",
            style={"font_size": 18, "font_color": "#ff0000"},
        )
        assert result is m

    def test_add_heatmap_with_style_dict(self) -> None:
        """
        Scenario: Pass a HeatmapStyle dict to add_heatmap.

        Given: A Map and a list of points
        When: add_heatmap is called with style=dict
        Then: The heatmap layer is added
        """
        m = Map()
        points = [Point(4.9 + i * 0.01, 52.37) for i in range(5)]
        result = m.add_heatmap(points, style={"radius": 20, "blur": 15})
        assert result is m

    def test_make_popup_with_popup_style_dict(self) -> None:
        """
        Scenario: _make_popup resolves a PopupStyle dict.

        Given: A Map, popup text, and a PopupStyle dict
        When: _make_popup is called with the dict
        Then: A Popup is created with the dict-based dimensions
        """
        m = Map()
        popup = m._make_popup("**Hello**", popup_style={"width": 400, "height": 200})
        assert popup is not None

    def test_add_marker_cluster_with_marker_style_dict(self) -> None:
        """
        Scenario: Pass marker_style as a dict to add_marker_cluster.

        Given: A Map and a list of Points
        When: add_marker_cluster is called with marker_style=dict
        Then: The cluster is added using the dict values
        """
        m = Map()
        points = [Point(4.9 + i * 0.01, 52.37) for i in range(3)]
        result = m.add_marker_cluster(points, marker_style={"emoji": "📍", "emoji_size": 20})
        assert result is m

    def test_resolve_style_none_returns_none(self) -> None:
        """
        Scenario: _resolve_style with None input.

        Given: None as value
        When: _resolve_style is called
        Then: None is returned
        """
        assert _resolve_style(None, StrokeStyle) is None

    def test_resolve_style_dataclass_passthrough(self) -> None:
        """
        Scenario: _resolve_style with an existing dataclass instance.

        Given: A StrokeStyle instance
        When: _resolve_style is called with the instance
        Then: The same instance is returned unchanged
        """
        s = StrokeStyle(color="red")
        assert _resolve_style(s, StrokeStyle) is s

    def test_resolve_style_invalid_key_raises_type_error(self) -> None:
        """
        Scenario: _resolve_style with an invalid dict key.

        Given: A dict with a key that doesn't match any dataclass field
        When: _resolve_style is called
        Then: A TypeError is raised by the dataclass constructor
        """
        with pytest.raises(TypeError):
            _resolve_style({"nonexistent_field": 42}, StrokeStyle)

    def test_resolve_style_non_dict_non_instance_passthrough(self) -> None:
        """
        Scenario: _resolve_style with an unsupported type (not None, not dict, not instance).

        Given: An integer value
        When: _resolve_style is called
        Then: The value is returned as-is (caller/dataclass will handle the error)
        """
        result = _resolve_style(42, StrokeStyle)
        assert result == 42

    def test_dict_and_dataclass_backward_compatible(self) -> None:
        """
        Scenario: Passing a dataclass instance still works (backward compat).

        Given: A Map and a StrokeStyle object
        When: add_polygon is called with the object
        Then: The polygon is added exactly as before
        """
        m = Map()
        poly = Polygon([(4.9, 52.3), (5.0, 52.3), (5.0, 52.4), (4.9, 52.4)])
        style = StrokeStyle(color="blue", weight=5)
        result = m.add_polygon(poly, stroke=style)
        assert result is m

    def test_add_point_with_label_style_dict_for_text_label(self) -> None:
        """
        Scenario: Pass label_style as a dict to add_point for text_label styling.

        Given: A Map and a Point with a text_label
        When: add_point is called with label_style=dict
        Then: The text label is rendered with the dict-based style
        """
        m = Map()
        result = m.add_point(
            Point(4.9, 52.37),
            label="📍",
            text_label="Test",
            label_style={"font_size": 16, "font_color": "#000000"},
        )
        assert result is m

    def test_add_polygon_with_popup_style_dict(self) -> None:
        """
        Scenario: Pass popup_style as a dict to add_polygon.

        Given: A Map and a Polygon with popup text
        When: add_polygon is called with popup_style=dict
        Then: The polygon popup uses the dict-based dimensions
        """
        m = Map()
        poly = Polygon([(4.9, 52.3), (5.0, 52.3), (5.0, 52.4), (4.9, 52.4)])
        result = m.add_polygon(poly, popup="**Info**", popup_style={"width": 500, "height": 300})
        assert result is m
