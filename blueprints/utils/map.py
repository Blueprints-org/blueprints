"""Blueprints Map generator.

Provides a high-level API for creating interactive OpenStreetMap visualizations
with support for Shapely geometries, GeoPandas DataFrames, emoji/icon markers,
text annotations, markdown tooltip text, choropleth coloring, heatmaps,
and export to HTML, PNG, and SVG formats.

Examples
--------
>>> from shapely.geometry import Point, Polygon
>>> from blueprints.utils import Map
>>> m = Map(title="My Map")
>>> m.add_point(Point(4.9, 52.37), marker="\U0001f4cd", tooltip="**Amsterdam**")
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
from typing import Any, Literal, Self, cast

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
    "openstreetmap": {"tiles": "OpenStreetMap", "attr": "OpenStreetMap", "name": "OpenStreetMap"},
    "cartodb_positron": {"tiles": "CartoDB positron", "attr": "CartoDB", "name": "CartoDB Positron"},
    "cartodb_dark": {"tiles": "CartoDB dark_matter", "attr": "CartoDB", "name": "CartoDB Dark"},
    "esri_satellite": {
        "tiles": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "attr": "Esri World Imagery",
        "name": "Esri Satellite",
    },
    "esri_topo": {
        "tiles": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        "attr": "Esri World Topo Map",
        "name": "Esri Topo",
    },
    "stamen_terrain": {
        "tiles": "https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}{r}.png",
        "attr": "Stadia/Stamen Terrain",
        "name": "Stamen Terrain",
    },
    "stamen_toner": {
        "tiles": "https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}{r}.png",
        "attr": "Stadia/Stamen Toner",
        "name": "Stamen Toner",
    },
    "kadaster_brt": {
        "tiles": "https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/standaard/EPSG:3857/{z}/{x}/{y}.png",
        "attr": "Kadaster BRT Achtergrondkaart",
        "name": "Kadaster BRT",
    },
    "kadaster_luchtfoto": {
        "tiles": "https://service.pdok.nl/hwh/luchtfotorgb/wmts/v1_0/Actueel_orthoHR/EPSG:3857/{z}/{x}/{y}.png",
        "attr": "Kadaster Luchtfoto",
        "name": "Kadaster Luchtfoto",
    },
    "kadaster_grijs": {
        "tiles": "https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/grijs/EPSG:3857/{z}/{x}/{y}.png",
        "attr": "Kadaster BRT Grijs",
        "name": "Kadaster Grijs",
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


# ---------------------------------------------------------------------------
# Default CSS for marker styles (replaces IconStyle / TextStyle / CaptionStyle)
# ---------------------------------------------------------------------------

_DEFAULT_ICON_CSS: dict[str, str] = {
    "font-size": "20px",
    "color": "#002855",
}

_DEFAULT_TEXT_CSS: dict[str, str] = {
    "font-size": "16px",
    "color": "black",
}

_DEFAULT_CAPTION_CSS: dict[str, str] = {
    "font-size": "12px",
    "font-family": "Arial, sans-serif",
    "color": "#333333",
    "font-weight": "bold",
    "background-color": "rgba(255,255,255,0.8)",
    "border": "1px solid #cccccc",
    "padding": "2px 6px",
    "white-space": "nowrap",
    "text-align": "center",
}

# Caption style when used under a marker (transparent background, no border)
_DEFAULT_MARKER_CAPTION_CSS: dict[str, str] = {
    **_DEFAULT_CAPTION_CSS,
    "background-color": "transparent",
    "border": "none",
}


def _css_to_style(css: dict[str, str]) -> str:
    """Convert a CSS property dict to an inline style string."""
    return ";".join(f"{k}:{v}" for k, v in css.items())


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
class TooltipStyle:
    """Tooltip appearance configuration.

    Parameters
    ----------
    sticky : bool
        Whether the tooltip follows the mouse cursor.
    style : str | None
        Inline CSS style string for the tooltip container.
        Example: ``"font-size:14px; background-color:#fff;"``
    """

    sticky: bool = True
    style: str | None = None


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
        Radius of each location in pixels.
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
    tile_layer : str | list[str]
        Key from ``TILE_PROVIDERS`` or Folium built-in name.
        Pass a list to add multiple base layers (use
        :meth:`Map.add_layer_control` to toggle between them).
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

    tile_layer: str | list[str] = "cartodb_positron"
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
# Markdown tooltip helper
# ---------------------------------------------------------------------------


def _sanitize_href(url: str) -> str:
    """Allow only safe URL schemes (http, https, mailto). Returns ``#`` otherwise."""
    stripped = url.strip()
    if re.match(r"^https?://", stripped, re.IGNORECASE) or re.match(r"^mailto:", stripped, re.IGNORECASE):
        return stripped
    return "#"


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
    text = re.sub(r"\[(.+?)\]\((.+?)\)", lambda m: f'<a href="{_sanitize_href(m.group(2))}" target="_blank">{m.group(1)}</a>', text)

    # Lists
    text = re.sub(r"^- (.+)$", r"<li>\1</li>", text, flags=re.MULTILINE)
    if "<li>" in text:
        text = re.sub(r"((?:<li>.*?</li>\s*)+)", r"<ul>\1</ul>", text, flags=re.DOTALL)

    # Newlines (not after block elements)
    return re.sub(r"(?<!>)\n(?!<)", "<br>", text)


class RawHTML(str):
    """String subclass that bypasses markdown-to-HTML conversion.

    Use this to pass pre-formatted HTML directly to ``tooltip`` or ``popup``
    parameters on any ``add_*`` method.

    Examples
    --------
    >>> from blueprints.utils.map import RawHTML
    >>> html = RawHTML("<b>Bold</b> and <em>italic</em>")
    >>> m.add_point(Point(4.9, 52.37), tooltip=html)
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


def _classify_marker(s: str) -> Literal["emoji", "icon_class", "icon_name"]:
    """Classify a marker string.

    Returns
    -------
    "emoji"
        Non-ASCII content (emojis, unicode symbols) → render as text.
    "icon_class"
        Full CSS class string containing a space (e.g. ``"fa fa-home"``) → use as-is.
    "icon_name"
        Bare icon name (e.g. ``"home"``, ``"fa-arrow-right"``) → auto-prefix.
    """
    if not s or not all(c.isascii() for c in s):
        return "emoji"
    if " " in s:
        return "icon_class"
    return "icon_name"


def _caption_html(text: str, css: dict[str, str]) -> str:
    """Build an HTML snippet for a caption below a marker icon.

    Parameters
    ----------
    text : str
        Caption text.
    css : dict[str, str]
        CSS property dict merged with appropriate defaults by the caller.

    Returns
    -------
    str
        HTML ``<div>`` string.
    """
    merged = {**_DEFAULT_CAPTION_CSS, **css}
    return f'<div style="{_css_to_style(merged)}">{text}</div>'


def _build_icon_marker(
    icon: str,
    css: dict[str, str],
    caption: str | None,
    caption_css: dict[str, str],
) -> folium.DivIcon:
    """Build an icon-based DivIcon marker with optional caption.

    Parameters
    ----------
    icon : str
        Icon name or full CSS class string.  Strings containing a space
        (e.g. ``"fa-solid fa-house"``) are used verbatim.  Bare names
        starting with ``"fa-"`` get an ``"fa-solid"`` prefix; other bare
        names (e.g. ``"home"``) get a ``"glyphicon"`` prefix.
    css : dict[str, str]
        CSS property overrides for the icon element.
    caption : str | None
        Optional caption text below the icon.
    caption_css : dict[str, str]
        CSS property overrides for the caption.

    Returns
    -------
    folium.DivIcon
    """
    merged = {**_DEFAULT_ICON_CSS, **css}
    style_str = _css_to_style(merged)
    caption_suffix = _caption_html(caption, caption_css) if caption else ""
    # Full CSS class string (contains a space) → use as-is
    # Bare name starting with "fa-" → FontAwesome 6 (fa-solid prefix)
    # Other bare name → Glyphicon
    if " " in icon:
        icon_class = icon
    elif icon.startswith("fa-"):
        icon_class = f"fa-solid {icon}"
    else:
        icon_class = f"glyphicon glyphicon-{icon}"
    icon_html = f'<div style="text-align:center;"><i class="{icon_class}" style="{style_str}"></i></div>{caption_suffix}'
    return folium.DivIcon(
        html=icon_html,
        icon_size=(100, 50),
        icon_anchor=(50, 15),
    )


def _build_text_marker(
    text: str,
    css: dict[str, str],
    caption: str | None,
    caption_css: dict[str, str],
) -> folium.DivIcon:
    """Build a text/emoji DivIcon marker with optional caption.

    Parameters
    ----------
    text : str
        The actual text/emoji to render.
    css : dict[str, str]
        CSS property overrides for the text element.
    caption : str | None
        Optional caption text below the text.
    caption_css : dict[str, str]
        CSS property overrides for the caption.

    Returns
    -------
    folium.DivIcon
        A DivIcon rendering the text and optional caption.
    """
    merged = {**_DEFAULT_TEXT_CSS, **css}
    style_str = _css_to_style(merged) + ";text-align:center"
    caption_suffix = _caption_html(caption, caption_css) if caption else ""
    inner = f'<div style="{style_str}">{text}</div>'
    html = f'<div style="text-align:center;">{inner}{caption_suffix}</div>'
    # size estimation for icon_size/anchor from font-size
    fs = int(merged.get("font-size", "16px").replace("px", ""))
    w = max(fs + 10, 100 if caption else 0)
    h = fs + 10 + (20 if caption else 0)
    return folium.DivIcon(
        html=html,
        icon_size=(w, h),
        icon_anchor=(w // 2, (fs + 10) // 2),
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
    >>> m.add_point(Point(5.0, 52.0), tooltip="**Hello**")
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

    def _create_base_map(self) -> folium.Map:  # noqa: PLR0912, C901
        """Create the base Folium Map object.

        Returns
        -------
        folium.Map
        """
        cfg = self._config

        # Normalise tile_layer to a list
        layers = cfg.tile_layer if isinstance(cfg.tile_layer, list) else [cfg.tile_layer]
        multiple = len(layers) > 1

        if multiple:
            # Multiple layers: create map without tiles, add all as TileLayer
            kwargs: dict[str, Any] = {
                "tiles": None,
                "zoom_start": cfg.zoom_start,
                "min_zoom": cfg.min_zoom,
                "max_zoom": cfg.max_zoom,
                "width": cfg.width,
                "height": cfg.height,
                "control_scale": cfg.control_scale,
            }
            if self._center:
                kwargs["location"] = list(self._center)
            fmap = folium.Map(**kwargs)

            for i, layer_key in enumerate(layers):
                p = TILE_PROVIDERS.get(layer_key.lower())
                if p:
                    folium.TileLayer(
                        tiles=p["tiles"],
                        name=p.get("name", layer_key),
                        attr=p.get("attr"),
                        show=i == 0,
                    ).add_to(fmap)
                else:
                    folium.TileLayer(
                        tiles=layer_key,
                        name=layer_key,
                        attr=cfg.attribution,
                        show=i == 0,
                    ).add_to(fmap)
        else:
            # Single layer: pass directly to folium.Map (original behaviour)
            provider = TILE_PROVIDERS.get(layers[0].lower())
            if provider:
                tiles = provider["tiles"]
                attr = provider.get("attr")
            else:
                tiles = layers[0]
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
                "border-radius:6px;font-family:Arial,sans-serif;font-size:16px;"
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

    def _make_tooltip(
        self,
        hover: str | RawHTML | None,
        tooltip_style: TooltipStyle | dict[str, Any] | None = None,
    ) -> folium.Tooltip | None:
        """Create Tooltip from markdown or raw HTML."""
        if not hover:
            return None
        ts = _resolve_style(tooltip_style, TooltipStyle) or TooltipStyle()
        html = hover if isinstance(hover, RawHTML) else _markdown_to_html(hover)
        return folium.Tooltip(html, sticky=ts.sticky, style=ts.style)

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
        marker: str | None = None,
        caption: str | None = None,
        tooltip: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        marker_style: dict[str, str] | None = None,
        caption_style: dict[str, str] | None = None,
        tooltip_style: TooltipStyle | dict[str, Any] | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
        min_zoom: int | None = None,
    ) -> Self:
        """Add a location marker.

        Parameters
        ----------
        point : Point
            Shapely Point ``(x, y)`` in source CRS.
        marker : str | None
            Desired marker symbol.  Rendering path is auto-detected:

            - Bare icon name (e.g. ``"home"``) → Glyphicon prefix.
            - Bare FA name (e.g. ``"fa-arrow-right"``) → ``fa-solid`` prefix.
            - Full CSS class (e.g. ``"fa-solid fa-house"``) → used as-is.
            - Emoji / unicode text → rendered as text DivIcon.
            - ``None`` → default ``"arrow-down"`` icon.
        caption : str | None
            Text annotation placed below the marker.  Works with any marker
            type (emoji, icon).  Can be styled via ``caption_style``.
        tooltip : str | RawHTML | None
            Information shown on mouse tooltip.  Markdown supported for
            strings, or use ``RawHTML`` for pre-formatted HTML.
        popup : str | RawHTML | None
            Information shown on click.  Markdown supported for strings,
            or use ``RawHTML`` for pre-formatted HTML.
        marker_style : dict[str, str] | None
            CSS property overrides for the marker element.  Merged with
            ``_DEFAULT_ICON_CSS`` or ``_DEFAULT_TEXT_CSS`` depending on the
            detected marker type.
        caption_style : dict[str, str] | None
            CSS property overrides for the caption.  Merged with
            ``_DEFAULT_MARKER_CAPTION_CSS``.
        tooltip_style : TooltipStyle | dict[str, Any] | None
            Tooltip appearance.  Defaults to Folium's default tooltip style.
            Pass a ``dict`` as shortcut for ``TooltipStyle(**dict)``.
        popup_style : PopupStyle | dict[str, Any] | None
            Popup dimensions.  Defaults to ``PopupStyle()``.
            Pass a ``dict`` as shortcut for ``PopupStyle(**dict)``.
        min_zoom : int | None
            Minimum zoom level at which the marker is visible.
            ``None`` or ``0`` means always visible.

        Returns
        -------
        Map
        """
        point = cast(Point, self._transform(point))
        self._extend_bounds(point)
        lat, lon = point.y, point.x

        css = marker_style or {}
        cap_css = {**_DEFAULT_MARKER_CAPTION_CSS, **(caption_style or {})}

        kind = _classify_marker(marker) if marker else "icon_name"
        if kind == "emoji":
            assert marker is not None  # guarded by _classify_marker above
            icon = _build_text_marker(marker, css, caption, cap_css)
        else:
            icon_name = marker or "arrow-down"
            icon = _build_icon_marker(icon_name, css, caption, cap_css)

        m = folium.Marker(
            location=[lat, lon],
            icon=icon,
            tooltip=self._make_tooltip(tooltip, tooltip_style),
            popup=self._make_popup(popup, popup_style),
        )
        m.add_to(self._target())

        if min_zoom is not None and min_zoom > 0:
            self._zoom_controlled_markers.append(
                {
                    "var_name": m.get_name(),
                    "min_zoom": min_zoom,
                }
            )

        return self

    def add_circle(
        self,
        point: Point,
        tooltip: str | RawHTML | None = None,
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
        tooltip : str | RawHTML | None
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
            tooltip=self._make_tooltip(tooltip),
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
        tooltip: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        stroke: StrokeStyle | dict[str, Any] | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
    ) -> Self:
        """Add a LineString.

        Parameters
        ----------
        line : LineString
            Shapely LineString.
        tooltip : str | RawHTML | None
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
            tooltip=self._make_tooltip(tooltip),
            popup=self._make_popup(popup, popup_style),
        ).add_to(self._target())
        return self

    def add_polygon(
        self,
        polygon: Polygon,
        tooltip: str | RawHTML | None = None,
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
        tooltip : str | RawHTML | None
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
        locations: list[list[tuple[float, float]]] = [exterior] + [[(c[1], c[0]) for c in interior.coords] for interior in polygon.interiors]
        folium.Polygon(
            locations=locations,
            color=s.color,
            weight=s.weight,
            opacity=s.opacity,
            dash_array=s.dash_array,
            fill=True,
            fill_color=f.color,
            fill_opacity=f.opacity,
            tooltip=self._make_tooltip(tooltip),
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
            self.add_polygon(poly, tooltip=hover, popup=popup, stroke=stroke, fill=fill, popup_style=popup_style)
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
            self.add_linestring(line, tooltip=hover, popup=popup, stroke=stroke, popup_style=popup_style)
        return self

    def add_multipoint(
        self,
        mp: MultiPoint,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        label: str | None = None,
        marker_style: dict[str, str] | None = None,
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
            self.add_point(pt, tooltip=hover, popup=popup, marker=label, marker_style=marker_style, popup_style=popup_style)
        return self

    def add_geometry(
        self,
        geom: BaseGeometry,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        label: str | None = None,
        stroke: StrokeStyle | dict[str, Any] | None = None,
        fill: FillStyle | dict[str, Any] | None = None,
        marker_style: dict[str, str] | None = None,
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
            self.add_point(geom, tooltip=hover, popup=popup, marker=label, marker_style=marker_style, popup_style=popup_style)
        elif isinstance(geom, LinearRing):
            # LinearRing is a subclass of LineString — check first
            self.add_linestring(LineString(geom.coords), tooltip=hover, popup=popup, stroke=stroke, popup_style=popup_style)
        elif isinstance(geom, LineString):
            self.add_linestring(geom, tooltip=hover, popup=popup, stroke=stroke, popup_style=popup_style)
        elif isinstance(geom, Polygon):
            self.add_polygon(geom, tooltip=hover, popup=popup, stroke=stroke, fill=fill, popup_style=popup_style)
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
            Legend marker.
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
        marker_style: dict[str, str] | None = None,
        name: str | None = None,
        min_zoom: int | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
        captions: list[str] | None = None,
        caption_style: dict[str, str] | None = None,
    ) -> Self:
        """Add clustered markers that group at low zoom.

        Parameters
        ----------
        points : list[Point]
            Shapely Points.
        labels : list[str] | None
            Per-location marker content (icon names or emoji/text).
        hovers : list[str] | None
            Per-location markdown tooltips.
        popups : list[str] | None
            Per-location markdown popups.
        marker_style : dict[str, str] | None
            CSS property overrides for each marker.  Merged with
            ``_DEFAULT_ICON_CSS`` or ``_DEFAULT_TEXT_CSS`` depending on
            the detected marker type.
        name : str | None
            Layer name.
        min_zoom : int | None
            Minimum zoom level at which the cluster is visible.
            ``None`` or ``0`` means always visible.
        popup_style : PopupStyle | dict[str, Any] | None
            Popup dimensions.  Defaults to ``PopupStyle()``.
        captions : list[str] | None
            Per-location text annotations placed below each marker.
            Styled via ``caption_style``.
        caption_style : dict[str, str] | None
            CSS property overrides for ``captions``.  Merged with
            ``_DEFAULT_MARKER_CAPTION_CSS``.

        Returns
        -------
        Map
        """
        css = marker_style or {}
        cap_css = {**_DEFAULT_MARKER_CAPTION_CSS, **(caption_style or {})}
        cluster = folium.plugins.MarkerCluster(name=name)

        for i, point in enumerate(points):
            pt = cast(Point, self._transform(point))
            self._extend_bounds(pt)
            lat, lon = pt.y, pt.x

            label = labels[i] if labels and i < len(labels) else None
            hover = hovers[i] if hovers and i < len(hovers) else None
            popup = popups[i] if popups and i < len(popups) else None
            txt = captions[i] if captions and i < len(captions) else None

            kind = _classify_marker(label) if label else "icon_name"
            if kind == "emoji":
                assert label is not None  # guarded by _classify_marker above
                icon = _build_text_marker(label, css, txt, cap_css)
            else:
                icon_name = label or "arrow-down"
                icon = _build_icon_marker(icon_name, css, txt, cap_css)

            folium.Marker(
                location=[lat, lon],
                icon=icon,
                tooltip=self._make_tooltip(hover),
                popup=self._make_popup(popup, popup_style),
            ).add_to(cluster)

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
        point: tuple[float, float] | Point,
        text: str,
        style: dict[str, str] | None = None,
        hover: str | RawHTML | None = None,
        popup: str | RawHTML | None = None,
        popup_style: PopupStyle | dict[str, Any] | None = None,
        min_zoom: int | None = None,
    ) -> Self:
        """Add a text marker at a location.

        Parameters
        ----------
        point : tuple[float, float] | Point
            ``(lat, lon)`` tuple or Shapely Point ``(lon, lat)``.
        text : str
            Label text.
        style : dict[str, str] | None
            CSS property overrides.  Merged with ``_DEFAULT_CAPTION_CSS``.
        hover : str | RawHTML | None
            Markdown tooltip, or ``RawHTML`` for pre-formatted HTML.
        popup : str | RawHTML | None
            Markdown popup, or ``RawHTML`` for pre-formatted HTML.
        popup_style : PopupStyle | dict[str, Any] | None
            Popup dimensions.  Defaults to ``PopupStyle()``.
        min_zoom : int | None
            Minimum zoom level at which the text is visible.
            ``None`` or ``0`` means always visible.

        Returns
        -------
        Map
        """
        merged = {**_DEFAULT_CAPTION_CSS, "border-radius": "3px", "overflow-wrap": "break-word", **(style or {})}
        if isinstance(point, Point):
            loc = cast(Point, self._transform(point))
            lat, lon = loc.y, loc.x
            self._extend_bounds(loc)
        else:
            lat, lon = point
            self._bounds.append((lat, lon))

        css_str = _css_to_style(merged)
        # Estimate icon size from text length and font size so the anchor
        # centers the marker on the coordinate and Leaflet doesn't render a
        # phantom shadow from a zero-sized container.
        fs = int(merged.get("font-size", "12px").replace("px", ""))
        est_w = max(len(text) * fs * 0.65 + 16, 20)
        est_h = fs + 12
        icon = folium.DivIcon(
            html=f'<div style="{css_str}">{text}</div>',
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
        marker_style: dict[str, str] | None = None,
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
            Columns for tooltip tooltip.
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
        marker_style : dict[str, str] | None
            CSS property overrides for location markers.
        title : str | None
            Map title.
        config : MapConfig | None
            Map configuration.
        legend_name : str | None
            Color scale marker.

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

            # Build tooltip/popup text
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
        display_name = name
        if provider and tiles is None:
            tiles = provider["tiles"]
            attribution = attribution or provider.get("attr")
            display_name = provider.get("name", name)
        folium.TileLayer(
            tiles=tiles or name,
            name=display_name,
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
