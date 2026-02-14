"""Blueprints Map generator.

Provides a high-level API for creating interactive OpenStreetMap visualizations
with support for Shapely geometries, GeoPandas DataFrames, emoji/icon markers,
text annotations, markdown hover text, choropleth coloring, heatmaps,
and export to HTML, PNG, and SVG formats.

Examples
--------
>>> from shapely.geometry import Point, Polygon
>>> from blueprints.utils import Map
>>> m = Map(title="My Map")
>>> m.add_point(Point(4.9, 52.37), label="\U0001f4cd", hover="**Amsterdam**")
>>> m.add_polygon(Polygon([(4.9, 52.3), (5.0, 52.3), (5.0, 52.4), (4.9, 52.4)]))
>>> m.to_html("map.html")
"""

import asyncio
import base64
import io
import json
import re
import shutil
import tempfile
import time
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Self, cast

import branca.colormap as cm
import folium
import folium.features
import folium.plugins
from pyproj import Transformer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shapely.geometry import (
    LinearRing,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from shapely.geometry.base import BaseGeometry

# ---------------------------------------------------------------------------
# Constants - tile providers
# ---------------------------------------------------------------------------

TILE_PROVIDERS: dict[str, dict[str, str]] = {
    "openstreetmap": {"tiles": "OpenStreetMap", "attr": "OpenStreetMap"},
    "cartodb_positron": {"tiles": "CartoDB positron", "attr": "CartoDB"},
    "cartodb_dark": {"tiles": "CartoDB dark_matter", "attr": "CartoDB"},
    "esri_satellite": {
        "tiles": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "attr": "Esri World Imagery",
    },
    "esri_topo": {
        "tiles": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        "attr": "Esri World Topo Map",
    },
    "stamen_terrain": {
        "tiles": "https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}{r}.png",
        "attr": "Stadia/Stamen Terrain",
    },
    "stamen_toner": {
        "tiles": "https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}{r}.png",
        "attr": "Stadia/Stamen Toner",
    },
    "kadaster_brt": {
        "tiles": "https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/standaard/EPSG:3857/{z}/{x}/{y}.png",
        "attr": "Kadaster BRT Achtergrondkaart",
    },
    "kadaster_luchtfoto": {
        "tiles": "https://service.pdok.nl/hwh/luchtfotorgb/wmts/v1_0/Actueel_orthoHR/EPSG:3857/{z}/{x}/{y}.png",
        "attr": "Kadaster Luchtfoto",
    },
    "kadaster_grijs": {
        "tiles": "https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/grijs/EPSG:3857/{z}/{x}/{y}.png",
        "attr": "Kadaster BRT Grijs",
    },
}


# ---------------------------------------------------------------------------
# Coordinate system helpers
# ---------------------------------------------------------------------------


def _detect_and_transform_coords(
    coords: list[tuple[float, ...]],
    source_crs: str | None = None,
) -> list[tuple[float, float]]:
    """Detect coordinate system and transform to WGS84 if necessary.

    Auto-detects RD New (EPSG:28992) based on coordinate ranges.

    Parameters
    ----------
    coords : list[tuple[float, ...]]
        Input coordinate tuples as ``(x, y)``.
    source_crs : str | None
        Explicit source CRS (e.g. ``"EPSG:28992"``). Auto-detects if ``None``.

    Returns
    -------
    list[tuple[float, float]]
        Coordinates in WGS84 ``(longitude, latitude)``.
    """
    if not coords:
        return []

    sample_x, sample_y = coords[0][0], coords[0][1]

    if source_crs is None:
        # Auto-detect RD New: x ~ 0-300k, y ~ 300k-625k
        if 0 < sample_x < 300_000 and 300_000 < sample_y < 625_000:
            source_crs = "EPSG:28992"
        else:
            return [(c[0], c[1]) for c in coords]

    if source_crs and source_crs != "EPSG:4326":
        transformer = Transformer.from_crs(source_crs, "EPSG:4326", always_xy=True)
        return [transformer.transform(c[0], c[1]) for c in coords]

    return [(c[0], c[1]) for c in coords]


def _transform_geometry(geom: BaseGeometry, source_crs: str | None = None) -> BaseGeometry:  # noqa: PLR0911
    """Transform a Shapely geometry to WGS84.

    Parameters
    ----------
    geom : BaseGeometry
        Input geometry in any supported CRS.
    source_crs : str | None
        Source CRS. If ``None``, auto-detection is attempted.

    Returns
    -------
    BaseGeometry
        Geometry in WGS84 coordinates.
    """
    if isinstance(geom, Point):
        coords = _detect_and_transform_coords([(geom.x, geom.y)], source_crs)
        return Point(coords[0])
    if isinstance(geom, LinearRing):
        # LinearRing is a subclass of LineString — check first
        coords = _detect_and_transform_coords(list(geom.coords), source_crs)
        return LinearRing(coords)
    if isinstance(geom, LineString):
        coords = _detect_and_transform_coords(list(geom.coords), source_crs)
        return LineString(coords)
    if isinstance(geom, Polygon):
        ext = _detect_and_transform_coords(list(geom.exterior.coords), source_crs)
        holes = [_detect_and_transform_coords(list(r.coords), source_crs) for r in geom.interiors]
        return Polygon(ext, holes)
    if isinstance(geom, MultiPoint):
        return MultiPoint([cast(Point, _transform_geometry(g, source_crs)) for g in geom.geoms])
    if isinstance(geom, MultiPolygon):
        return MultiPolygon([cast(Polygon, _transform_geometry(g, source_crs)) for g in geom.geoms])
    if isinstance(geom, MultiLineString):
        return MultiLineString([cast(LineString, _transform_geometry(g, source_crs)) for g in geom.geoms])
    return geom


# ---------------------------------------------------------------------------
# Configuration data classes
# ---------------------------------------------------------------------------


@dataclass
class StrokeStyle:
    """Style for lines and polygon borders.

    Parameters
    ----------
    color : str
        CSS color string.
    weight : float
        Stroke width in pixels.
    opacity : float
        Stroke opacity, 0.0 - 1.0.
    dash_array : str | None
        SVG dash-array, e.g. ``"5 10"``.
    """

    color: str = "#3388ff"
    weight: float = 3.0
    opacity: float = 1.0
    dash_array: str | None = None


@dataclass
class FillStyle:
    """Style for polygon fills.

    Parameters
    ----------
    color : str
        Fill CSS color.
    opacity : float
        Fill opacity, 0.0 - 1.0.
    """

    color: str = "#3388ff"
    opacity: float = 0.2


@dataclass
class MarkerStyle:
    """Style for point markers.

    Parameters
    ----------
    icon : str | None
        Folium icon name. Ignored when ``emoji`` is set.
    icon_color : str
        Icon glyph color.
    marker_color : str
        Marker background color.
    prefix : str
        Icon set: ``"glyphicon"`` or ``"fa"``.
    emoji : str | None
        Emoji/text rendered as DivIcon.
    emoji_size : int
        Font size in px for the DivIcon.
    shape : str | None
        Shape type: ``"circle"``, ``"square"``, or ``"triangle"``.
        Ignored when ``emoji`` or ``label`` is set.
    shape_color : str
        Fill/stroke color for shape markers.
    shape_size : int
        Radius in pixels for shape markers.
    """

    icon: str | None = "info-sign"
    icon_color: str = "white"
    marker_color: str = "blue"
    prefix: str = "glyphicon"
    emoji: str | None = None
    emoji_size: int = 24
    shape: str | None = None
    shape_color: str = "blue"
    shape_size: int = 10


_SHAPE_CONFIG: dict[str, dict[str, int]] = {
    "circle": {"sides": 36, "rotation": 0},
    "square": {"sides": 4, "rotation": 45},
}


@dataclass
class LabelStyle:
    """Style for text annotation labels.

    Parameters
    ----------
    font_size : int
        Font size in px.
    font_family : str
        CSS font-family.
    font_color : str
        Text color.
    font_weight : str
        CSS font-weight.
    background_color : str | None
        Background color. ``None`` = transparent.
    border : str | None
        CSS border string.
    padding : str
        CSS padding.
    min_width : int | None
        Minimum label width in pixels. Useful for short labels to prevent excessive wrapping.
    max_width : int | None
        Maximum label width in pixels. Text will wrap if exceeded.
    min_height : int | None
        Minimum label height in pixels. Useful for short labels to prevent excessive wrapping.
    max_height : int | None
        Maximum label height in pixels. Text will be truncated if exceeded.
    """

    font_size: int = 12
    font_family: str = "Arial, sans-serif"
    font_color: str = "#333333"
    font_weight: str = "bold"
    background_color: str | None = "rgba(255,255,255,0.8)"
    border: str | None = "1px solid #cccccc"
    padding: str = "2px 6px"
    min_width: int | None = None
    max_width: int | None = None
    min_height: int | None = None
    max_height: int | None = None


@dataclass
class PopupStyle:
    """Popup appearance configuration.

    Parameters
    ----------
    width : int
        IFrame width in pixels.
    height : int
        IFrame height in pixels.
    max_width : int
        Maximum popup width in pixels.
    """

    width: int = 300
    height: int = 150
    max_width: int = 300


@dataclass
class CircleStyle:
    """Style for circle markers (fixed pixel size).

    Parameters
    ----------
    radius : float
        Circle radius in pixels.
    stroke : StrokeStyle
        Border stroke style.
    fill : FillStyle
        Fill style.
    """

    radius: float = 8.0
    stroke: StrokeStyle = field(default_factory=StrokeStyle)
    fill: FillStyle = field(default_factory=FillStyle)


@dataclass
class HeatmapStyle:
    """Configuration for heatmap layers.

    Parameters
    ----------
    radius : int
        Radius of each point in pixels.
    blur : int
        Blur radius in pixels.
    min_opacity : float
        Minimum heatmap opacity.
    max_zoom : int
        Zoom at which points reach full intensity.
    gradient : dict[float, str] | None
        Custom gradient ``{stop: color}``.
    """

    radius: int = 15
    blur: int = 10
    min_opacity: float = 0.3
    max_zoom: int = 18
    gradient: dict[float, str] | None = None


@dataclass
class MapConfig:
    """Global map configuration.

    Parameters
    ----------
    tile_layer : str
        Key from ``TILE_PROVIDERS`` or Folium built-in name.
    zoom_start : int
        Initial zoom level.
    min_zoom : int
        Minimum zoom level, preventing users from zooming out beyond this
        level.  Lower values allow viewing larger areas like continents.
        Useful for bounding maps to specific regions.
    max_zoom : int
        Maximum zoom level, limiting how far users can zoom in.  Higher
        values enable more detailed views, but effectiveness depends on
        the tile provider (e.g. OpenStreetMap maxes at 19).  Exceeding
        the provider's limit may show blank tiles.
    attribution : str | None
        Custom tile attribution.
    width : str | int
        Map width.
    height : str | int
        Map height.
    control_scale : bool
        Show scale bar.
    fullscreen : bool
        Add fullscreen button.
    minimap : bool
        Add minimap inset.
    measure_control : bool
        Add measure tool.
    mouse_position : bool
        Show cursor coordinates.
    """

    tile_layer: str = "cartodb_positron"
    zoom_start: int = 12
    min_zoom: int = 0
    max_zoom: int = 19
    attribution: str | None = None
    width: str | int = "100%"
    height: str | int = "100%"
    control_scale: bool = True
    fullscreen: bool = False
    minimap: bool = False
    measure_control: bool = False
    mouse_position: bool = True


# ---------------------------------------------------------------------------
# Markdown hover helper
# ---------------------------------------------------------------------------


def _markdown_to_html(md_text: str) -> str:
    """Convert a subset of Markdown to HTML for popups/tooltips.

    Supports ``**bold**``, ``*italic*``, backtick code, ``[links](url)``,
    headers (``#`` - ``###``), and unordered lists (``- item``).

    Parameters
    ----------
    md_text : str
        Markdown-formatted string.

    Returns
    -------
    str
        HTML string.
    """
    text = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Headers
    text = re.sub(r"^### (.+)$", r"<h4>\1</h4>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.+)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"^# (.+)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)

    # Bold, italic, code
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)

    # Links
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank">\1</a>', text)

    # Lists
    text = re.sub(r"^- (.+)$", r"<li>\1</li>", text, flags=re.MULTILINE)
    if "<li>" in text:
        text = re.sub(r"((?:<li>.*?</li>\s*)+)", r"<ul>\1</ul>", text, flags=re.DOTALL)

    # Newlines (not after block elements)
    return re.sub(r"(?<!>)\n(?!<)", "<br>", text)


class RawHTML(str):
    """String subclass that bypasses markdown-to-HTML conversion.

    Use this to pass pre-formatted HTML directly to ``hover`` or ``popup``
    parameters on any ``add_*`` method.

    Examples
    --------
    >>> from blueprints.utils.map import RawHTML
    >>> html = RawHTML("<b>Bold</b> and <em>italic</em>")
    >>> m.add_point(Point(4.9, 52.37), hover=html)
    """

    __slots__ = ()


# ---------------------------------------------------------------------------
# Style resolution helper
# ---------------------------------------------------------------------------


def _resolve_style(value: Any, cls: type) -> Any:  # noqa: ANN401
    """Convert a dict to a style dataclass instance, or return as-is.

    Supports nested dicts for composite styles like ``CircleStyle``.

    Parameters
    ----------
    value : Any
        ``None``, a style dataclass instance, or a ``dict`` of keyword arguments.
    cls : type
        The target style dataclass (e.g. ``StrokeStyle``, ``CircleStyle``).

    Returns
    -------
    Any
        ``None`` if *value* is ``None``, the original instance if already the
        correct type, or a newly constructed ``cls(**value)`` from a dict.
    """
    if value is None or isinstance(value, cls):
        return value
    if isinstance(value, dict):
        kwargs = dict(value)
        if cls is CircleStyle:
            if isinstance(kwargs.get("stroke"), dict):
                kwargs["stroke"] = StrokeStyle(**kwargs["stroke"])
            if isinstance(kwargs.get("fill"), dict):
                kwargs["fill"] = FillStyle(**kwargs["fill"])
        return cls(**kwargs)
    return value


# ---------------------------------------------------------------------------
# Selenium helper with proper error handling
# ---------------------------------------------------------------------------


def _check_selenium() -> None:
    """Verify Selenium and Chrome driver availability.

    Raises
    ------
    ImportError
        If selenium is not installed.
    RuntimeError
        If Chrome/chromedriver is not found.
    """
    chrome_paths = [
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("chrome"),
        shutil.which("googlechrome"),
        shutil.which("chromium.exe"),
        shutil.which("chrome_proxy.exe"),
        shutil.which("chromedriver"),
    ]
    if not any(chrome_paths):
        try:
            import chromedriver_autoinstaller  # noqa: PLC0415

            chromedriver_autoinstaller.install()
        except (ImportError, ModuleNotFoundError):
            pass  # Will be caught by the chromedriver check below

    if not shutil.which("chromedriver"):
        raise RuntimeError(
            "Chrome or Chromium not found. Image export requires Chrome.\n"
            "  Ubuntu/Debian: sudo apt install chromium-browser\n"
            "  macOS:         brew install --cask google-chrome\n"
            "  Windows:       Download from https://www.google.com/chrome/\n"
            "chromedriver not found on PATH.\n"
            "  pip install chromedriver-autoinstaller\n"
            "  Or download: https://googlechromelabs.github.io/chrome-for-testing/"
        )


def _capture_screenshot(
    html_path: str,
    width: int = 1200,
    height: int = 800,
    delay: float = 2.0,
) -> bytes:
    """Capture a screenshot of an HTML file using headless Chrome.

    Parameters
    ----------
    html_path : str
        Path to the HTML file.
    width : int
        Viewport width in pixels.
    height : int
        Viewport height in pixels.
    delay : float
        Seconds to wait for tile loading.

    Returns
    -------
    bytes
        PNG image bytes.
    """
    _check_selenium()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={width},{height}")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(width, height)
        driver.get(f"file://{html_path}")
        time.sleep(delay)
        return driver.get_screenshot_as_png()
    finally:
        if driver:
            driver.quit()


def _text_label_html(text: str, ls: LabelStyle) -> str:
    """Build an HTML snippet for a text label below a marker icon.

    Parameters
    ----------
    text : str
        Label text.
    ls : LabelStyle
        Label appearance.

    Returns
    -------
    str
        HTML ``<div>`` string.
    """
    return (
        f'<div style="font-size:{ls.font_size}px;font-family:{ls.font_family};'
        f"color:{ls.font_color};font-weight:{ls.font_weight};"
        f'white-space:nowrap;text-align:center;">{text}</div>'
    )


# ---------------------------------------------------------------------------
# Main Map class
# ---------------------------------------------------------------------------


class Map:
    """Interactive map builder backed by Folium and OpenStreetMap tiles.

    Parameters
    ----------
    center : tuple[float, float] | None
        Map center ``(latitude, longitude)``. Auto-fits if ``None``.
    title : str | None
        Title rendered at the top of the map.
    config : MapConfig | None
        Global map configuration.
    source_crs : str | None
        Default source CRS (e.g. ``"EPSG:28992"``). Auto-detects if ``None``.

    Examples
    --------
    >>> m = Map(title="Demo")
    >>> m.add_point(Point(5.0, 52.0), hover="**Hello**")
    >>> m.to_html("demo.html")
    """

    def __init__(
        self,
        center: tuple[float, float] | None = None,
        title: str | None = None,
        config: MapConfig | None = None,
        source_crs: str | None = None,
    ) -> None:
        self._config = config or MapConfig()
        self._center = center
        self._title = title
        self._source_crs = source_crs
        self._map = self._create_base_map()
        self._bounds: list[tuple[float, float]] = []
        self._feature_groups: dict[str, folium.FeatureGroup] = {}
        self._active_group: folium.FeatureGroup | folium.Map = self._map
        self._colormaps: list[cm.LinearColormap] = []
        self._zoom_controlled_markers: list[dict[str, Any]] = []
        self._zoom_js_injected: bool = False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _create_base_map(self) -> folium.Map:
        """Create the base Folium Map object.

        Returns
        -------
        folium.Map
        """
        cfg = self._config

        # Resolve tile provider
        provider = TILE_PROVIDERS.get(cfg.tile_layer.lower())
        if provider:
            tiles = provider["tiles"]
            attr = provider.get("attr")
        else:
            tiles = cfg.tile_layer
            attr = cfg.attribution

        kwargs: dict[str, Any] = {
            "tiles": tiles,
            "zoom_start": cfg.zoom_start,
            "min_zoom": cfg.min_zoom,
            "max_zoom": cfg.max_zoom,
            "width": cfg.width,
            "height": cfg.height,
            "control_scale": cfg.control_scale,
        }
        if self._center:
            kwargs["location"] = list(self._center)
        if attr:
            kwargs["attr"] = attr

        fmap = folium.Map(**kwargs)

        # Title overlay
        if self._title:
            title_html = (
                '<div style="position:fixed;top:10px;left:50%;transform:translateX(-50%);'
                "z-index:1000;background:rgba(255,255,255,0.9);padding:8px 20px;"
                "border-radius:6px;font-family:Arial,sans-serif;font-size:18px;"
                f'font-weight:bold;box-shadow:0 2px 6px rgba(0,0,0,0.3);pointer-events:none;">'
                f"{self._title}</div>"
            )
            fmap.get_root().html.add_child(folium.Element(title_html))  # type: ignore[union-attr]

        # Optional plugins
        if cfg.fullscreen:
            folium.plugins.Fullscreen().add_to(fmap)
        if cfg.minimap:
            folium.plugins.MiniMap(toggle_display=True).add_to(fmap)
        if cfg.measure_control:
            folium.plugins.MeasureControl(primary_length_unit="meters", primary_area_unit="sqmeters").add_to(fmap)
        if cfg.mouse_position:
            folium.plugins.MousePosition(position="bottomleft", separator=" | ", num_digits=6).add_to(fmap)

        return fmap

    def _transform(self, geom: BaseGeometry) -> BaseGeometry:
        """Transform geometry to WGS84."""
        return _transform_geometry(geom, self._source_crs)

    def _extend_bounds(self, geom: BaseGeometry) -> None:
        """Track geometry bounds for auto-fit."""
        b = geom.bounds  # (minx, miny, maxx, maxy) = (lon, lat, lon, lat)
        self._bounds.append((b[1], b[0]))
        self._bounds.append((b[3], b[2]))

    def _make_tooltip(self, hover: str | RawHTML | None) -> folium.Tooltip | None:
        """Create Tooltip from markdown or raw HTML."""
        if not hover:
            return None
        html = hover if isinstance(hover, RawHTML) else _markdown_to_html(hover)
        return folium.Tooltip(html)

    def _make_popup(self, popup: str | RawHTML | None, popup_style: PopupStyle | dict[str, Any] | None = None) -> folium.Popup | None:
        """Create Popup from markdown or raw HTML."""
        if not popup:
            return None
        ps = _resolve_style(popup_style, PopupStyle) or PopupStyle()
        html = popup if isinstance(popup, RawHTML) else _markdown_to_html(popup)
        iframe = folium.IFrame(html, width=ps.width, height=ps.height)  # type: ignore[arg-type]
        return folium.Popup(iframe, max_width=ps.max_width)

    def _target(self) -> folium.FeatureGroup | folium.Map:
        """Current target layer."""
        return self._active_group

    def _fit_bounds(self) -> None:
        """Fit map view to tracked bounds."""
        if self._bounds:
            self._map.fit_bounds(self._bounds)

    def set_bounds(self, padding: float = 0.0, restrict: bool = False) -> Self:
        """Fit map view to tracked bounds with optional padding and restriction.

        Parameters
        ----------
        padding : float
            Padding in degrees around the data bounds.
        restrict : bool
            If ``True``, prevent the user from panning/zooming beyond the
            data bounds (sets ``maxBounds`` and ``maxBoundsViscosity``).

        Returns
        -------
        Map
            Self, for chaining.
        """
        if not self._bounds:
            return self

        lats = [b[0] for b in self._bounds]
        lons = [b[1] for b in self._bounds]
        bounds = [
            [min(lats) - padding, min(lons) - padding],
            [max(lats) + padding, max(lons) + padding],
        ]
        self._map.fit_bounds(bounds)

        if restrict:
            self._map.options["maxBounds"] = bounds
            self._map.options["maxBoundsViscosity"] = 1.0

        return self

    # ------------------------------------------------------------------
    # Feature groups / layers
    # ------------------------------------------------------------------

    def create_feature_group(self, name: str, show: bool = True) -> Self:
        """Create a named feature group for layer toggling.

        Subsequent ``add_*`` calls target this group until changed.

        To stop targeting a group and return to the base map, call ``reset_target()``.

        Parameters
        ----------
        name : str
            Display name for layer control.
        show : bool
            Visible by default.

        Returns
        -------
        Map
            Self, for chaining.
        """
        fg = folium.FeatureGroup(name=name, show=show)
        fg.add_to(self._map)
        self._feature_groups[name] = fg
        self._active_group = fg
        return self

    def set_feature_group(self, name: str) -> Self:
        """Activate an existing feature group.

        Parameters
        ----------
        name : str
            Feature group name.

        Returns
        -------
        Map

        Raises
        ------
        KeyError
            If group does not exist.
        """
        if name not in self._feature_groups:
            raise KeyError(f"Feature group '{name}' not found. Available: {list(self._feature_groups.keys())}")
        self._active_group = self._feature_groups[name]
        return self

    def reset_target(self) -> Self:
        """Reset target to base map (no feature group).

        Returns
        -------
        Map
        """
        self._active_group = self._map
        return self

    # ------------------------------------------------------------------
    # Adding geometries
    # ------------------------------------------------------------------

    def add_point(
        self,
        point: Point,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        label: str | None = None,
        marker_style: MarkerStyle | dict[str, Any] | None = None,
        label_style: LabelStyle | dict[str, Any] | None = None,
        min_zoom: int | None = None,
        text_label: str | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add a point marker.

        Parameters
        ----------
        point : Point
            Shapely Point ``(x, y)`` in source CRS.
        hover : str | RawHTML | None
            Markdown tooltip text, or ``RawHTML`` for pre-formatted HTML.
        popup : str | RawHTML | None
            Markdown popup text, or ``RawHTML`` for pre-formatted HTML.
        label : str | None
            Emoji / short text for the marker.
        marker_style : MarkerStyle | dict[str, Any] | None
            Marker appearance. Pass a ``dict`` as shortcut for
            ``MarkerStyle(**dict)``.
        label_style : LabelStyle | dict[str, Any] | None
            Style for the ``text_label``.  Defaults to a borderless,
            transparent-background ``LabelStyle`` when not provided.
            Pass a ``dict`` as shortcut for ``LabelStyle(**dict)``.
        min_zoom : int | None
            Minimum zoom level at which the marker is visible.
            ``None`` or ``0`` means always visible.
        text_label : str | None
            Text annotation placed below the marker.  Works with any
            marker type (shape, emoji, icon).  Styled via ``label_style``.
        popup_style : PopupStyle | dict[str, Any] | None
            Popup dimensions. Defaults to ``PopupStyle()``.
            Pass a ``dict`` as shortcut for ``PopupStyle(**dict)``.

        Returns
        -------
        Map
        """
        point = cast(Point, self._transform(point))
        self._extend_bounds(point)
        ms = _resolve_style(marker_style, MarkerStyle) or MarkerStyle()
        lat, lon = point.y, point.x

        emoji = label or ms.emoji
        ls = _resolve_style(label_style, LabelStyle) or LabelStyle(background_color=None, border=None)
        label_suffix = _text_label_html(text_label, ls) if text_label else ""

        if ms.shape and not emoji:
            # Shape marker path
            shape = ms.shape
            if shape == "triangle":
                inner = f'<div style="font-size:20px;color:{ms.shape_color};text-align:center;">\u25bc</div>'
                html = f'<div style="text-align:center;">{inner}{label_suffix}</div>'
                h = 40 + (20 if text_label else 0)
                icon = folium.DivIcon(html=html, icon_size=(100, h), icon_anchor=(50, 10))
                marker = folium.Marker(
                    location=[lat, lon],
                    icon=icon,
                    tooltip=self._make_tooltip(hover),
                    popup=self._make_popup(popup, popup_style),
                )
            else:
                cfg = _SHAPE_CONFIG.get(shape, _SHAPE_CONFIG["circle"])
                marker = folium.RegularPolygonMarker(
                    location=[lat, lon],
                    number_of_sides=cfg["sides"],
                    radius=ms.shape_size,
                    color=ms.shape_color,
                    fill=True,
                    fill_color=ms.shape_color,
                    fill_opacity=0.7,
                    tooltip=self._make_tooltip(hover),
                    popup=self._make_popup(popup, popup_style),
                    rotation=cfg["rotation"],
                )
                # RegularPolygonMarker can't embed HTML; add separate label
                if text_label:
                    label_icon = folium.DivIcon(
                        html=f'<div style="text-align:center;margin-top:10px;">{label_suffix}</div>',
                        icon_size=(100, 30),
                        icon_anchor=(50, 0),
                    )
                    folium.Marker(location=[lat, lon], icon=label_icon).add_to(self._target())
            marker.add_to(self._target())
        elif emoji:
            inner = f'<div style="font-size:{ms.emoji_size}px;text-align:center;">{emoji}</div>'
            html = f'<div style="text-align:center;">{inner}{label_suffix}</div>'
            w = max(ms.emoji_size + 10, 100 if text_label else 0)
            h = ms.emoji_size + 10 + (20 if text_label else 0)
            icon = folium.DivIcon(html=html, icon_size=(w, h), icon_anchor=(w // 2, (ms.emoji_size + 10) // 2))
            marker = folium.Marker(
                location=[lat, lon],
                icon=icon,
                tooltip=self._make_tooltip(hover),
                popup=self._make_popup(popup, popup_style),
            )
            marker.add_to(self._target())
        else:
            icon = folium.Icon(
                icon=ms.icon or "info-sign",
                color=ms.marker_color,
                icon_color=ms.icon_color,
                prefix=ms.prefix,
            )
            marker = folium.Marker(
                location=[lat, lon],
                icon=icon,
                tooltip=self._make_tooltip(hover),
                popup=self._make_popup(popup, popup_style),
            )
            marker.add_to(self._target())
            # folium.Icon can't embed HTML; add separate label
            if text_label:
                label_icon = folium.DivIcon(
                    html=f'<div style="text-align:center;margin-top:10px;">{label_suffix}</div>',
                    icon_size=(100, 30),
                    icon_anchor=(50, 0),
                )
                folium.Marker(location=[lat, lon], icon=label_icon).add_to(self._target())

        if min_zoom is not None and min_zoom > 0:
            self._zoom_controlled_markers.append(
                {
                    "var_name": marker.get_name(),
                    "min_zoom": min_zoom,
                }
            )

        return self

    def add_circle(
        self,
        point: Point,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        style: CircleStyle | dict[str, Any] | None = None,
        min_zoom: int | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add a circle marker (fixed pixel size).

        Parameters
        ----------
        point : Point
            Shapely Point.
        hover : str | RawHTML | None
            Markdown tooltip, or ``RawHTML`` for pre-formatted HTML.
        popup : str | RawHTML | None
            Markdown popup, or ``RawHTML`` for pre-formatted HTML.
        style : CircleStyle | dict[str, Any] | None
            Circle appearance. Pass a ``dict`` as shortcut for
            ``CircleStyle(**dict)``.  Nested ``stroke`` and ``fill``
            dicts are resolved automatically.
        min_zoom : int | None
            Minimum zoom level at which the marker is visible.
            ``None`` or ``0`` means always visible.
        popup_style : PopupStyle | dict[str, Any] | None
            Popup dimensions. Defaults to ``PopupStyle()``.

        Returns
        -------
        Map
        """
        point = cast(Point, self._transform(point))
        self._extend_bounds(point)
        cs = _resolve_style(style, CircleStyle) or CircleStyle()
        marker = folium.CircleMarker(
            location=[point.y, point.x],
            radius=cs.radius,
            color=cs.stroke.color,
            weight=cs.stroke.weight,
            opacity=cs.stroke.opacity,
            fill=True,
            fill_color=cs.fill.color,
            fill_opacity=cs.fill.opacity,
            tooltip=self._make_tooltip(hover),
            popup=self._make_popup(popup, popup_style),
            dash_array=cs.stroke.dash_array,
        )
        marker.add_to(self._target())
        if min_zoom is not None and min_zoom > 0:
            self._zoom_controlled_markers.append(
                {
                    "var_name": marker.get_name(),
                    "min_zoom": min_zoom,
                }
            )
        return self

    def add_linestring(
        self,
        line: LineString,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        stroke: StrokeStyle | dict[str, Any] | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add a LineString.

        Parameters
        ----------
        line : LineString
            Shapely LineString.
        hover : str | RawHTML | None
            Markdown tooltip, or ``RawHTML`` for pre-formatted HTML.
        popup : str | RawHTML | None
            Markdown popup, or ``RawHTML`` for pre-formatted HTML.
        stroke : StrokeStyle | dict[str, Any] | None
            Line style. Pass a ``dict`` as shortcut for
            ``StrokeStyle(**dict)``.
        popup_style : PopupStyle | dict[str, Any] | None
            Popup dimensions. Defaults to ``PopupStyle()``.

        Returns
        -------
        Map
        """
        line = cast(LineString, self._transform(line))
        self._extend_bounds(line)
        s = _resolve_style(stroke, StrokeStyle) or StrokeStyle()
        locations = [(c[1], c[0]) for c in line.coords]
        folium.PolyLine(
            locations=locations,
            color=s.color,
            weight=s.weight,
            opacity=s.opacity,
            dash_array=s.dash_array,
            tooltip=self._make_tooltip(hover),
            popup=self._make_popup(popup, popup_style),
        ).add_to(self._target())
        return self

    def add_polygon(
        self,
        polygon: Polygon,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        stroke: StrokeStyle | dict[str, Any] | None = None,
        fill: FillStyle | dict[str, Any] | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add a Polygon.

        Parameters
        ----------
        polygon : Polygon
            Shapely Polygon.
        hover : str | RawHTML | None
            Markdown tooltip, or ``RawHTML`` for pre-formatted HTML.
        popup : str | RawHTML | None
            Markdown popup, or ``RawHTML`` for pre-formatted HTML.
        stroke : StrokeStyle | dict[str, Any] | None
            Border style. Pass a ``dict`` as shortcut for
            ``StrokeStyle(**dict)``.
        fill : FillStyle | dict[str, Any] | None
            Fill style. Pass a ``dict`` as shortcut for
            ``FillStyle(**dict)``.
        popup_style : PopupStyle | dict[str, Any] | None
            Popup dimensions. Defaults to ``PopupStyle()``.

        Returns
        -------
        Map
        """
        polygon = cast(Polygon, self._transform(polygon))
        self._extend_bounds(polygon)
        s = _resolve_style(stroke, StrokeStyle) or StrokeStyle()
        f = _resolve_style(fill, FillStyle) or FillStyle()
        exterior = [(c[1], c[0]) for c in polygon.exterior.coords]
        folium.Polygon(
            locations=exterior,
            color=s.color,
            weight=s.weight,
            opacity=s.opacity,
            dash_array=s.dash_array,
            fill=True,
            fill_color=f.color,
            fill_opacity=f.opacity,
            tooltip=self._make_tooltip(hover),
            popup=self._make_popup(popup, popup_style),
        ).add_to(self._target())
        return self

    def add_multipolygon(
        self,
        mp: MultiPolygon,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        stroke: StrokeStyle | dict[str, Any] | None = None,
        fill: FillStyle | dict[str, Any] | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add a MultiPolygon.

        Parameters
        ----------
        mp : MultiPolygon
            Shapely MultiPolygon.
        hover, popup, stroke, fill, popup_style
            See ``add_polygon``.

        Returns
        -------
        Map
        """
        for poly in mp.geoms:
            self.add_polygon(poly, hover=hover, popup=popup, stroke=stroke, fill=fill, popup_style=popup_style)
        return self

    def add_multilinestring(
        self,
        ml: MultiLineString,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        stroke: StrokeStyle | dict[str, Any] | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add a MultiLineString.

        Parameters
        ----------
        ml : MultiLineString
            Shapely MultiLineString.
        hover, popup, stroke, popup_style
            See ``add_linestring``.

        Returns
        -------
        Map
        """
        for line in ml.geoms:
            self.add_linestring(line, hover=hover, popup=popup, stroke=stroke, popup_style=popup_style)
        return self

    def add_multipoint(
        self,
        mp: MultiPoint,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        label: str | None = None,
        marker_style: MarkerStyle | dict[str, Any] | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add a MultiPoint.

        Parameters
        ----------
        mp : MultiPoint
            Shapely MultiPoint.
        hover, popup, label, marker_style, popup_style
            See ``add_point``.

        Returns
        -------
        Map
        """
        for pt in mp.geoms:
            self.add_point(pt, hover=hover, popup=popup, label=label, marker_style=marker_style, popup_style=popup_style)
        return self

    def add_geometry(
        self,
        geom: BaseGeometry,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        label: str | None = None,
        stroke: StrokeStyle | dict[str, Any] | None = None,
        fill: FillStyle | dict[str, Any] | None = None,
        marker_style: MarkerStyle | dict[str, Any] | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add any Shapely geometry (auto-dispatches by type).

        Parameters
        ----------
        geom : BaseGeometry
            Any supported Shapely geometry.
        hover, popup, label, stroke, fill, marker_style, popup_style
            Style and interaction parameters.

        Returns
        -------
        Map

        Raises
        ------
        TypeError
            If geometry type is unsupported.
        """
        if isinstance(geom, Point):
            self.add_point(geom, hover=hover, popup=popup, label=label, marker_style=marker_style, popup_style=popup_style)
        elif isinstance(geom, LinearRing):
            # LinearRing is a subclass of LineString — check first
            self.add_linestring(LineString(geom.coords), hover=hover, popup=popup, stroke=stroke, popup_style=popup_style)
        elif isinstance(geom, LineString):
            self.add_linestring(geom, hover=hover, popup=popup, stroke=stroke, popup_style=popup_style)
        elif isinstance(geom, Polygon):
            self.add_polygon(geom, hover=hover, popup=popup, stroke=stroke, fill=fill, popup_style=popup_style)
        elif isinstance(geom, MultiPolygon):
            self.add_multipolygon(geom, hover=hover, popup=popup, stroke=stroke, fill=fill, popup_style=popup_style)
        elif isinstance(geom, MultiLineString):
            self.add_multilinestring(geom, hover=hover, popup=popup, stroke=stroke, popup_style=popup_style)
        elif isinstance(geom, MultiPoint):
            self.add_multipoint(geom, hover=hover, popup=popup, label=label, marker_style=marker_style, popup_style=popup_style)
        else:
            raise TypeError(f"Unsupported geometry type: {type(geom).__name__}")
        return self

    # ------------------------------------------------------------------
    # GeoJSON
    # ------------------------------------------------------------------

    def add_geojson(
        self,
        data: dict | str | Path,
        hover_fields: list[str] | None = None,
        style: dict[str, Any] | None = None,
        highlight: dict[str, Any] | None = None,
    ) -> Self:
        """Add a GeoJSON layer.

        Parameters
        ----------
        data : dict | str | Path
            GeoJSON as dict, JSON string, or file path.
        hover_fields : list[str] | None
            Property fields for the tooltip.
        style : dict[str, Any] | None
            Style kwargs.
        highlight : dict[str, Any] | None
            Highlight kwargs for mouse-over.

        Returns
        -------
        Map
        """
        if isinstance(data, Path):
            data = json.loads(data.read_text("utf-8"))
        elif isinstance(data, str):
            # Try as file path first (only short strings), otherwise parse as JSON
            if len(data) < 500 and not data.lstrip().startswith("{"):
                path = Path(data)
                data = json.loads(path.read_text("utf-8")) if path.exists() else json.loads(data)
            else:
                data = json.loads(data)

        ds = {"color": "#3388ff", "weight": 2, "fillOpacity": 0.2}
        if style:
            ds.update(style)
        dh = {"weight": 5, "fillOpacity": 0.4}
        if highlight:
            dh.update(highlight)

        tooltip = folium.GeoJsonTooltip(fields=hover_fields, localize=True) if hover_fields else None

        layer = folium.GeoJson(
            data,
            style_function=lambda _: ds,
            highlight_function=lambda _: dh,
            tooltip=tooltip,
        )
        layer.add_to(self._target())
        try:
            layer_bounds = layer.get_bounds()
            if layer_bounds:
                self._bounds.extend(cast(list[tuple[float, float]], layer_bounds))
        except Exception:
            pass
        return self

    # ------------------------------------------------------------------
    # Choropleth / colormap
    # ------------------------------------------------------------------

    def add_choropleth(  # noqa: C901, PLR0913
        self,
        geojson_data: dict | str | Path,
        value_column: str,
        key_on: str,
        values: dict[str, float] | None = None,
        vmin: float | None = None,
        vmax: float | None = None,
        legend_name: str | None = None,
        nan_fill_color: str = "#cccccc",
        nan_fill_opacity: float = 0.4,
        line_weight: float = 1.0,
        line_opacity: float = 0.5,
        fill_opacity: float = 0.7,
        hover_fields: list[str] | None = None,
    ) -> Self:
        """Add a choropleth (color-coded) layer.

        Parameters
        ----------
        geojson_data : dict | str | Path
            GeoJSON FeatureCollection.
        value_column : str
            Property name with numeric values.
        key_on : str
            Join key, e.g. ``"feature.properties.id"``.
        values : dict[str, float] | None
            Key -> value mapping. Reads from properties if ``None``.
        colors : str
            Colormap name (e.g. ``"YlOrRd"``, ``"Blues"``).
        vmin, vmax : float | None
            Color scale range. Auto-calculated if ``None``.
        legend_name : str | None
            Legend label.
        nan_fill_color : str
            Color for missing values.
        nan_fill_opacity : float
            Opacity for missing values.
        line_weight, line_opacity, fill_opacity : float
            Styling parameters.
        hover_fields : list[str] | None
            Tooltip property fields.

        Returns
        -------
        Map
        """
        # Parse data
        if isinstance(geojson_data, Path):
            geojson_data = json.loads(geojson_data.read_text("utf-8"))
        elif isinstance(geojson_data, str):
            if len(geojson_data) < 500 and not geojson_data.lstrip().startswith("{"):
                p = Path(geojson_data)
                geojson_data = json.loads(p.read_text("utf-8")) if p.exists() else json.loads(geojson_data)
            else:
                geojson_data = json.loads(geojson_data)

        # Extract values if not provided
        if values is None:
            values = {}
            key_parts = key_on.split(".")
            for feat in geojson_data.get("features", []):
                obj = feat
                for part in key_parts[1:]:
                    obj = obj.get(part, {})
                key = obj if isinstance(obj, str) else str(obj)
                val = feat.get("properties", {}).get(value_column)
                if val is not None:
                    values[key] = float(val)

        # Min/max
        vals = list(values.values())
        if vals:
            vmin = vmin if vmin is not None else min(vals)
            vmax = vmax if vmax is not None else max(vals)

        # Build colormap
        colormap = cm.LinearColormap(
            colors=["#ffffb2", "#fecc5c", "#fd8d3c", "#f03b20", "#bd0026"],
            vmin=vmin or 0,
            vmax=vmax or 1,
            caption=legend_name or value_column,
        )

        # Capture in closure
        _vals, _cmap = values, colormap

        def style_fn(feature: dict) -> dict:
            obj = feature
            for part in key_on.split(".")[1:]:
                obj = obj.get(part, {})
            key = obj if isinstance(obj, str) else str(obj)
            val = _vals.get(key)
            if val is not None:
                return {"fillColor": _cmap(val), "color": "#333", "weight": line_weight, "fillOpacity": fill_opacity, "opacity": line_opacity}
            return {"fillColor": nan_fill_color, "color": "#333", "weight": line_weight, "fillOpacity": nan_fill_opacity, "opacity": line_opacity}

        tooltip = folium.GeoJsonTooltip(fields=hover_fields, localize=True) if hover_fields else None
        layer = folium.GeoJson(
            geojson_data,
            style_function=style_fn,
            highlight_function=lambda _: {"weight": 3, "fillOpacity": min(fill_opacity + 0.15, 1.0)},
            tooltip=tooltip,
        )
        layer.add_to(self._target())
        colormap.add_to(self._map)
        self._colormaps.append(colormap)

        try:
            layer_bounds = layer.get_bounds()
            if layer_bounds:
                self._bounds.extend(cast(list[tuple[float, float]], layer_bounds))
        except Exception:
            pass
        return self

    # ------------------------------------------------------------------
    # Heatmap
    # ------------------------------------------------------------------

    def add_heatmap(
        self,
        points: list[Point] | list[tuple[float, float]] | list[tuple[float, float, float]],
        style: HeatmapStyle | dict[str, Any] | None = None,
        name: str | None = None,
    ) -> Self:
        """Add a heatmap layer.

        Parameters
        ----------
        points : list[Point] | list[tuple]
            Shapely Points ``(lon, lat)`` or tuples ``(lat, lon[, intensity])``.
        style : HeatmapStyle | dict[str, Any] | None
            Heatmap appearance. Pass a ``dict`` as shortcut for
            ``HeatmapStyle(**dict)``.
        name : str | None
            Layer name.

        Returns
        -------
        Map
        """
        hs = _resolve_style(style, HeatmapStyle) or HeatmapStyle()
        heat_data: list[list[float]] = []
        for p in points:
            if isinstance(p, Point):
                pt = cast(Point, self._transform(p))
                heat_data.append([pt.y, pt.x])
                self._extend_bounds(pt)
            elif len(p) == 2:
                heat_data.append([p[0], p[1]])
                self._bounds.append((p[0], p[1]))
            else:
                heat_data.append(list(p[:3]))
                self._bounds.append((p[0], p[1]))

        kwargs: dict[str, Any] = {
            "radius": hs.radius,
            "blur": hs.blur,
            "min_opacity": hs.min_opacity,
            "max_zoom": hs.max_zoom,
        }
        if hs.gradient:
            kwargs["gradient"] = hs.gradient

        folium.plugins.HeatMap(heat_data, name=name, **kwargs).add_to(self._target())
        return self

    # ------------------------------------------------------------------
    # Marker cluster
    # ------------------------------------------------------------------

    def add_marker_cluster(
        self,
        points: list[Point],
        labels: list[str] | None = None,
        hovers: list[str] | None = None,
        popups: list[str] | None = None,
        marker_style: MarkerStyle | dict[str, Any] | None = None,
        name: str | None = None,
        min_zoom: int | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
        text_labels: list[str] | None = None,
        label_style: LabelStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add clustered markers that group at low zoom.

        Parameters
        ----------
        points : list[Point]
            Shapely Points.
        labels : list[str] | None
            Per-point emoji/text labels.
        hovers : list[str] | None
            Per-point markdown tooltips.
        popups : list[str] | None
            Per-point markdown popups.
        marker_style : MarkerStyle | dict[str, Any] | None
            Default marker appearance. Pass a ``dict`` as shortcut for
            ``MarkerStyle(**dict)``.
        name : str | None
            Layer name.
        min_zoom : int | None
            Minimum zoom level at which the cluster is visible.
            ``None`` or ``0`` means always visible.
        popup_style : PopupStyle | dict[str, Any] | None
            Popup dimensions. Defaults to ``PopupStyle()``.
        text_labels : list[str] | None
            Per-point text annotations placed below each marker.
            Styled via ``label_style``.
        label_style : LabelStyle | dict[str, Any] | None
            Style for ``text_labels``.  Defaults to a borderless,
            transparent-background ``LabelStyle``.  Pass a ``dict``
            as shortcut for ``LabelStyle(**dict)``.

        Returns
        -------
        Map
        """
        ms = _resolve_style(marker_style, MarkerStyle) or MarkerStyle()
        cluster = folium.plugins.MarkerCluster(name=name)

        for i, point in enumerate(points):
            pt = cast(Point, self._transform(point))
            self._extend_bounds(pt)
            lat, lon = pt.y, pt.x

            label = labels[i] if labels and i < len(labels) else None
            hover = hovers[i] if hovers and i < len(hovers) else None
            popup = popups[i] if popups and i < len(popups) else None

            emoji = label or ms.emoji
            ls = _resolve_style(label_style, LabelStyle) or LabelStyle(background_color=None, border=None)
            txt = text_labels[i] if text_labels and i < len(text_labels) else None
            label_suffix = _text_label_html(txt, ls) if txt else ""

            if emoji:
                inner = f'<div style="font-size:{ms.emoji_size}px;text-align:center;">{emoji}</div>'
                html = f'<div style="text-align:center;">{inner}{label_suffix}</div>'
                width = max(ms.emoji_size + 10, 100 if txt else 0)
                height = ms.emoji_size + 10 + (20 if txt else 0)
                icon = folium.DivIcon(
                    html=html,
                    icon_size=(width, height),
                    icon_anchor=(width // 2, (ms.emoji_size + 10) // 2),
                )
            else:
                icon = folium.Icon(
                    icon=ms.icon or "info-sign",
                    color=ms.marker_color,
                    icon_color=ms.icon_color,
                    prefix=ms.prefix,
                )

            folium.Marker(
                location=[lat, lon],
                icon=icon,
                tooltip=self._make_tooltip(hover),
                popup=self._make_popup(popup, popup_style),
            ).add_to(cluster)

            # folium.Icon can't embed HTML; add separate label to cluster
            if txt and not emoji:
                label_icon = folium.DivIcon(
                    html=f'<div style="text-align:center;margin-top:10px;">{label_suffix}</div>',
                    icon_size=(100, 30),
                    icon_anchor=(50, 0),
                )
                folium.Marker(location=[lat, lon], icon=label_icon).add_to(cluster)

        cluster.add_to(self._target())
        if min_zoom is not None and min_zoom > 0:
            self._zoom_controlled_markers.append(
                {
                    "var_name": cluster.get_name(),
                    "min_zoom": min_zoom,
                }
            )
        return self

    # ------------------------------------------------------------------
    # Text annotations
    # ------------------------------------------------------------------

    def add_text(
        self,
        location: tuple[float, float] | Point,
        text: str,
        style: LabelStyle | dict[str, Any] | None = None,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
        min_zoom: int | None = None,
    ) -> Self:
        """Add a text label at a location.

        Parameters
        ----------
        location : tuple[float, float] | Point
            ``(lat, lon)`` tuple or Shapely Point ``(lon, lat)``.
        text : str
            Label text.
        style : LabelStyle | dict[str, Any] | None
            Text appearance. Pass a ``dict`` as shortcut for
            ``LabelStyle(**dict)``.
        hover : str | RawHTML | None
            Markdown tooltip, or ``RawHTML`` for pre-formatted HTML.
        popup : str | RawHTML | None
            Markdown popup, or ``RawHTML`` for pre-formatted HTML.
        popup_style : PopupStyle | dict[str, Any] | None
            Popup dimensions. Defaults to ``PopupStyle()``.
        min_zoom : int | None
            Minimum zoom level at which the text is visible.
            ``None`` or ``0`` means always visible.

        Returns
        -------
        Map
        """
        ls = _resolve_style(style, LabelStyle) or LabelStyle()
        if isinstance(location, Point):
            loc = cast(Point, self._transform(location))
            lat, lon = loc.y, loc.x
            self._extend_bounds(loc)
        else:
            lat, lon = location
            self._bounds.append((lat, lon))

        bg = f"background:{ls.background_color};" if ls.background_color else ""
        border = f"border:{ls.border};" if ls.border else ""
        min_height = f"min-height:{ls.min_height}px;" if ls.min_height else ""
        max_height = f"max-height:{ls.max_height}px;" if ls.max_height else ""
        min_width = f"min-width:{ls.min_width}px;" if ls.min_width else ""
        max_width = f"max-width:{ls.max_width}px;" if ls.max_width else ""
        css = (
            f"font-size:{ls.font_size}px;font-family:{ls.font_family};"
            f"color:{ls.font_color};font-weight:{ls.font_weight};"
            f"padding:{ls.padding};"
            f"border-radius:3px;"
            "overflow-wrap:break-word;"
            f"{bg}{border}{max_height}{min_height}{max_width}{min_width}"
        )
        # Estimate icon size from text length and font size so the anchor
        # centers the label on the coordinate and Leaflet doesn't render a
        # phantom shadow from a zero-sized container.
        est_w = max(len(text) * ls.font_size * 0.65 + 16, 20)
        est_h = ls.font_size + 12
        icon = folium.DivIcon(
            html=f'<div style="{css}">{text}</div>',
            icon_size="100%",  # type: ignore[arg-type]  # Let CSS control sizing
            icon_anchor=(int(est_w // 2), int(est_h // 2)),
            class_name="",
        )
        marker = folium.Marker(
            location=[lat, lon],
            icon=icon,
            tooltip=self._make_tooltip(hover),
            popup=self._make_popup(popup, popup_style),
        )
        marker.add_to(self._target())
        if min_zoom is not None and min_zoom > 0:
            self._zoom_controlled_markers.append(
                {
                    "var_name": marker.get_name(),
                    "min_zoom": min_zoom,
                }
            )
        return self

    # ------------------------------------------------------------------
    # GeoDataFrame integration
    # ------------------------------------------------------------------

    @classmethod
    def from_geodataframe(  # noqa: PLR0913, C901
        cls,
        gdf: Any,  # noqa: ANN401
        hover_columns: list[str] | None = None,
        popup_columns: list[str] | None = None,
        label_column: str | None = None,
        color_column: str | None = None,
        stroke: StrokeStyle | None = None,
        fill: FillStyle | None = None,
        marker_style: MarkerStyle | None = None,
        title: str | None = None,
        config: MapConfig | None = None,
        legend_name: str | None = None,
    ) -> Self:
        """Create a GeoMap from a GeoPandas GeoDataFrame.

        Parameters
        ----------
        gdf : geopandas.GeoDataFrame
            GeoDataFrame with a geometry column.
        hover_columns : list[str] | None
            Columns for hover tooltip.
        popup_columns : list[str] | None
            Columns for click popup.
        label_column : str | None
            Column with emoji/text labels for points.
        color_column : str | None
            Numeric column for choropleth coloring.
        stroke : StrokeStyle | None
            Default border style.
        fill : FillStyle | None
            Default fill style.
        marker_style : MarkerStyle | None
            Default marker style.
        title : str | None
            Map title.
        config : MapConfig | None
            Map configuration.
        legend_name : str | None
            Color scale label.

        Returns
        -------
        Map

        Raises
        ------
        ImportError
            If geopandas is not installed.
        """
        # Reproject to WGS84 if needed
        if gdf.crs and str(gdf.crs) != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")

        m = cls(title=title, config=config)

        # Build colormap
        colormap = None
        if color_column and color_column in gdf.columns:
            vals = gdf[color_column].dropna()
            if len(vals) > 0:
                vmin, vmax = float(vals.min()), float(vals.max())
                colormap = cm.LinearColormap(
                    colors=["#ffffb2", "#fecc5c", "#fd8d3c", "#f03b20", "#bd0026"],
                    vmin=vmin,
                    vmax=vmax,
                    caption=legend_name or color_column,
                )
                colormap.add_to(m._map)
                m._colormaps.append(colormap)

        # Iterate rows
        for idx, row in gdf.iterrows():
            geom = row.geometry

            if not isinstance(geom, BaseGeometry):
                continue

            if geom is None or geom.is_empty:
                continue

            # Build hover/popup text
            hover = None
            if hover_columns:
                parts = [f"**{c}**: {row[c]}" for c in hover_columns if c in row.index]
                hover = "\n".join(parts) if parts else None

            popup = None
            if popup_columns:
                parts = [f"**{c}**: {row[c]}" for c in popup_columns if c in row.index]
                popup = "\n".join(parts) if parts else None

            lbl = str(row[label_column]) if label_column and label_column in row.index else None

            # Resolve color
            cur_fill, cur_stroke = fill, stroke
            if colormap and color_column and color_column in row.index:
                val = row[color_column]
                if val is not None and not isinstance(val, float):
                    c = colormap(float(val))
                    cur_fill = FillStyle(color=c, opacity=(fill or FillStyle()).opacity)
                    cur_stroke = StrokeStyle(
                        color=c,
                        weight=(stroke or StrokeStyle()).weight,
                        opacity=(stroke or StrokeStyle()).opacity,
                    )

            m.add_geometry(
                geom=geom,
                hover=hover,
                popup=popup,
                label=lbl,
                stroke=cur_stroke,
                fill=cur_fill,
                marker_style=marker_style,
            )

        return m

    # ------------------------------------------------------------------
    # Layer management
    # ------------------------------------------------------------------

    def add_layer_control(self, collapsed: bool = True, position: str = "topright") -> Self:
        """Add a layer control toggle.

        Parameters
        ----------
        collapsed : bool
            Start collapsed.
        position : str
            Control position.

        Returns
        -------
        Map
        """
        folium.LayerControl(collapsed=collapsed, position=position).add_to(self._map)
        return self

    def add_tile_layer(
        self,
        name: str,
        tiles: str | None = None,
        attribution: str | None = None,
        overlay: bool = False,
    ) -> Self:
        """Add an additional tile layer.

        Parameters
        ----------
        name : str
            Display name or ``TILE_PROVIDERS`` key.
        tiles : str | None
            Tile URL. Looks up ``name`` in providers if ``None``.
        attribution : str | None
            Tile attribution.
        overlay : bool
            Add as overlay vs base layer.

        Returns
        -------
        Map
        """
        provider = TILE_PROVIDERS.get(name.lower())
        if provider and tiles is None:
            tiles = provider["tiles"]
            attribution = attribution or provider.get("attr")
        folium.TileLayer(
            tiles=tiles or name,
            name=name,
            attr=attribution,
            overlay=overlay,
        ).add_to(self._map)
        return self

    # ------------------------------------------------------------------
    # Map combination
    # ------------------------------------------------------------------

    def __add__(self, other: Self) -> Self:
        """Merge two GeoMaps. Left map config/title is preserved.

        Parameters
        ----------
        other : Map
            Another map instance.

        Returns
        -------
        Map
            Combined map (self with other's features).
        """
        for child in other._map._children.values():
            child.add_to(self._map)
        self._bounds.extend(other._bounds)
        self._feature_groups.update(other._feature_groups)
        self._colormaps.extend(other._colormaps)
        self._zoom_controlled_markers.extend(other._zoom_controlled_markers)
        return self

    # ------------------------------------------------------------------
    # Export methods
    # ------------------------------------------------------------------

    @property
    def folium_map(self) -> folium.Map:
        """Access the underlying Folium Map for advanced customization."""
        return self._map

    def _generate_zoom_javascript(self) -> str:
        """Generate JavaScript for zoom-dependent marker visibility.

        Returns
        -------
        str
            A ``<script>`` block that toggles marker visibility based on zoom.
        """
        marker_config = ", ".join(f'{{id: "{m["var_name"]}", minZoom: {m["min_zoom"]}}}' for m in self._zoom_controlled_markers)
        return (
            "<script>\n"
            "document.addEventListener('DOMContentLoaded', function() {\n"
            "    var checkInterval = setInterval(function() {\n"
            "        var mapContainer = document.querySelector('.folium-map');\n"
            "        if (mapContainer && mapContainer._leaflet_map) {\n"
            "            clearInterval(checkInterval);\n"
            "            var map = mapContainer._leaflet_map;\n"
            "            var configs = [" + marker_config + "];\n"
            "            function update() {\n"
            "                var z = map.getZoom();\n"
            "                configs.forEach(function(c) {\n"
            "                    var el = eval(c.id);\n"
            "                    if (z >= c.minZoom) { el.addTo(map); }\n"
            "                    else { map.removeLayer(el); }\n"
            "                });\n"
            "            }\n"
            "            map.on('zoomend', update);\n"
            "            update();\n"
            "        }\n"
            "    }, 100);\n"
            "});\n"
            "</script>"
        )

    def _get_html(self) -> str:
        """Render map to HTML string (auto-fits bounds)."""
        if not self._center:
            self._fit_bounds()
        if self._zoom_controlled_markers and not self._zoom_js_injected:
            self._map.get_root().html.add_child(folium.Element(self._generate_zoom_javascript()))  # type: ignore[union-attr]
            self._zoom_js_injected = True
        return self._map._repr_html_()

    def to_html(self, path: str | Path | None = None, open_in_browser: bool = False) -> str | Path:
        """Export as standalone HTML.

        Parameters
        ----------
        path : str | Path | None
            Output file path.  When ``None``, the full HTML document is
            returned as a string instead of being written to disk.
        open_in_browser : bool
            If ``True`` and *path* is given, open the file in the default
            browser after saving.  Ignored when *path* is ``None``.

        Returns
        -------
        str | Path
            HTML string when *path* is ``None``, otherwise the resolved
            output :class:`~pathlib.Path`.
        """
        if not self._center:
            self._fit_bounds()
        if path is None:
            return self._get_html()
        out = Path(path)
        self._map.save(str(out))
        if open_in_browser:
            webbrowser.open(out.resolve().as_uri())
        return out

    def to_image(
        self,
        path: str | Path | None = None,
        width: int = 1200,
        height: int = 800,
        delay: float = 0.50,
        hide_controls: bool = True,
    ) -> bytes | Path:
        """Save the map as a PNG image.

        Parameters
        ----------
        path : str | Path | None
            Output path. Returns bytes if ``None``.
        width : int
            Viewport width in px.
        height : int
            Viewport height in px.
        delay : float
            Seconds to wait for tiles.
        hide_controls : bool
            If ``True``, inject CSS to hide Leaflet UI controls in the
            exported image.

        Returns
        -------
        bytes | Path

        Raises
        ------
        ImportError
            If selenium not installed.
        RuntimeError
            If Chrome/chromedriver not found.
        """
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
            self.to_html(tmp.name)
            tmp_path = tmp.name
        try:
            if hide_controls:
                content = Path(tmp_path).read_text(encoding="utf-8")
                hide_css = "<style>.leaflet-control{display:none !important;}</style>"
                content = content.replace("</head>", f"{hide_css}\n</head>", 1)
                Path(tmp_path).write_text(content, encoding="utf-8")
            png_bytes = _capture_screenshot(
                html_path=tmp_path,
                width=width,
                height=height,
                delay=delay,
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        if path is None:
            return png_bytes
        out = Path(path)
        out.write_bytes(png_bytes)
        return out

    def to_bytesio(
        self,
        width: int = 1200,
        height: int = 800,
        delay: float = 2.0,
        hide_controls: bool = True,
    ) -> io.BytesIO:
        """Export as PNG in a BytesIO buffer.

        Parameters
        ----------
        width : int
            Viewport width.
        height : int
            Viewport height.
        delay : float
            Tile loading wait time.
        hide_controls : bool
            If ``True``, hide Leaflet UI controls.

        Returns
        -------
        io.BytesIO
            Buffer at position 0.
        """
        png = cast(bytes, self.to_image(path=None, width=width, height=height, delay=delay, hide_controls=hide_controls))
        buf = io.BytesIO(png)
        buf.seek(0)
        return buf

    def to_svg(
        self,
        path: str | Path | None = None,
        width: int = 1200,
        height: int = 800,
        delay: float = 2.0,
        hide_controls: bool = True,
    ) -> str | Path:
        """Export as SVG (raster-wrapped).

        Captures PNG then wraps in an SVG container.

        Parameters
        ----------
        path : str | Path | None
            Output path. Returns SVG string if ``None``.
        width, height : int
            Viewport dimensions.
        delay : float
            Tile loading wait time.
        hide_controls : bool
            If ``True``, hide Leaflet UI controls.

        Returns
        -------
        str | Path
        """
        png_bytes = cast(bytes, self.to_image(path=None, width=width, height=height, delay=delay, hide_controls=hide_controls))
        b64 = base64.b64encode(png_bytes).decode("ascii")
        svg = (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
            f'  <image width="{width}" height="{height}" '
            f'xlink:href="data:image/png;base64,{b64}"/>\n'
            f"</svg>"
        )
        if path is None:
            return svg
        out = Path(path)
        out.write_text(svg, encoding="utf-8")
        return out

    async def to_image_async(
        self,
        path: str | Path | None = None,
        width: int = 1200,
        height: int = 800,
        delay: float = 2.0,
        hide_controls: bool = True,
    ) -> bytes | Path:
        """Async PNG export (runs Selenium in executor).

        Parameters
        ----------
        path, width, height, delay
            See ``to_image``.
        hide_controls : bool
            If ``True``, hide Leaflet UI controls.

        Returns
        -------
        bytes | Path
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.to_image(path=path, width=width, height=height, delay=delay, hide_controls=hide_controls)
        )

    async def to_svg_async(
        self,
        path: str | Path | None = None,
        width: int = 1200,
        height: int = 800,
        delay: float = 2.0,
        hide_controls: bool = True,
    ) -> str | Path:
        """Async SVG export.

        Parameters
        ----------
        path, width, height, delay
            See ``to_svg``.
        hide_controls : bool
            If ``True``, hide Leaflet UI controls.

        Returns
        -------
        str | Path
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.to_svg(path=path, width=width, height=height, delay=delay, hide_controls=hide_controls))

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """String representation."""
        n = len(self._bounds) // 2
        groups = list(self._feature_groups.keys())
        return f"Map(title={self._title!r}, geometries~{n}, feature_groups={groups})"

    def _repr_html_(self) -> str:
        """Jupyter notebook display."""
        return self._get_html()
