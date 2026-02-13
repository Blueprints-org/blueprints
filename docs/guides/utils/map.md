# Map

**Interactive maps from Shapely geometries.** One import, a few method calls, and you've got a full OpenStreetMap
visualization — with hover tooltips, choropleths, heatmaps, and export to HTML, PNG, or SVG.

---

**Key features:**

- 🗺️ **Shapely-native** — pass `Point`, `Polygon`, `LineString` directly, including multi-geometries
- 📝 **Markdown hover text** — bold, italic, links, lists, and code in tooltips
- 🎨 **Choropleth & heatmaps** — color-coded maps from numeric data
- 📊 **GeoPandas integration** — `Map.from_geodataframe()` one-liner
- 🌐 **Auto CRS detection** — RD New (EPSG:28992) coordinates transform automatically
- 📤 **Export anywhere** — HTML, PNG, SVG, async variants, and `BytesIO` buffers
- 🧩 **Feature groups** — toggleable layers with a built-in layer control
- 🔌 **10 tile providers** — OpenStreetMap, CartoDB, Esri, Stamen, and Kadaster

??? example "TL;DR — full example for power users"

    Points, lines, polygons, popups, feature groups, layer control, style dicts, and HTML export in one block.
    Everything below this fold explains each piece step by step.

    ```python exec="true" html="true" source="tabbed-right"
    from shapely.geometry import Point, LineString, Polygon
    from blueprints.utils import Map, MapConfig

    m = Map(
        title="Amsterdam Overview",
        config=MapConfig(
            tile_layer="cartodb_positron",
            fullscreen=True,
            minimap=True,
            measure_control=True,
            mouse_position=True,
        ),
    )

    # — Feature group: landmarks (emoji markers with hover + popups) —
    m.create_feature_group("Landmarks")
    m.add_point(
        Point(4.9041, 52.3676),
        label="🏛️",
        hover="**Royal Palace**",
        popup="**Royal Palace**\nDam Square, Amsterdam\nBuilt: 1665",
        popup_style={"width": 280, "height": 120},
    )
    m.add_point(
        Point(4.8834, 52.3667),
        label="📖",
        hover="**Anne Frank House**",
        popup="**Anne Frank House**\nPrinsengracht 263\nVisitors/year: ~1.3 million",
        popup_style={"width": 300, "height": 120},
    )
    m.add_point(
        Point(4.8795, 52.3600),
        hover="**Rijksmuseum**",
        popup="**Rijksmuseum**\nDutch art and history since 1800",
        marker_style={"icon": "home", "marker_color": "green", "prefix": "fa"},
    )

    # — Feature group: areas (polygon + line, styled with dicts) —
    m.create_feature_group("Areas")
    m.add_polygon(
        Polygon([(4.876, 52.372), (4.889, 52.372), (4.889, 52.380), (4.876, 52.380)]),
        hover="**De Jordaan**\nHistoric neighbourhood",
        popup="**De Jordaan**\n\nOne of Amsterdam's most famous neighbourhoods.\n- Narrow streets\n- Independent galleries\n- Brown cafés",
        stroke={"color": "#2ecc71", "weight": 2},
        fill={"color": "#2ecc71", "opacity": 0.15},
        popup_style={"width": 300, "height": 180},
    )
    m.add_linestring(
        LineString([(4.8852, 52.3702), (4.8910, 52.3663), (4.8932, 52.3631), (4.884, 52.3569)]),
        hover="**Walking route**\n*Centraal → Leidseplein*",
        stroke={"color": "#e74c3c", "weight": 4, "dash_array": "10 6"},
    )

    # — Circle marker with nested style dict —
    m.reset_target()
    m.add_circle(
        Point(4.8812, 52.3584),
        hover="**Van Gogh Museum**",
        popup="**Van Gogh Museum**\nOver 200 paintings, 500 drawings",
        style={"radius": 12, "stroke": {"color": "#8e44ad", "weight": 2}, "fill": {"color": "#8e44ad", "opacity": 0.5}},
    )

    # — Text annotation —
    m.add_text(Point(4.89, 52.37), "Centrum", style={"font_size": 14, "font_color": "#2c3e50"})

    m.add_layer_control(collapsed=False)
    m.set_bounds(padding=0.005)
    m.to_html("amsterdam_overview.html")

    print(m.to_html())  # markdown-exec: hide
    ```

## Your first map

Let's start with the absolute minimum, a single point on a map, exported to HTML.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils import Map

# Create a map and add a point
m = Map(title="Hello Amsterdam")
m.add_point(Point(4.9041, 52.3676), label="📍", hover="**Amsterdam**")

# Save to an HTML file you can open in any browser
m.to_html("hello.html")
print(m.to_html())  # markdown-exec: hide

```

That's it. Open `hello.html` and you'll see an interactive OpenStreetMap with a 📍 emoji marker on Amsterdam. Hover over
it, and you get a bold "Amsterdam" tooltip.

Let's walk through what happened:

**`Map(title="Hello Amsterdam")`** creates a new map. The `title` shows as a floating label at the top. You didn't
pass a `center` — that's fine. Map auto-fits the viewport to whatever geometries you add.

**`add_point()`** takes a Shapely `Point(longitude, latitude)`. The `label` parameter turns the marker into an emoji (or
any short text). The `hover` parameter accepts Markdown — `**Amsterdam**` renders as bold in the tooltip.

**`to_html()`** writes a standalone HTML file. No server needed — just open it in a browser.

!!! tip

    Every `add_*` method returns `self`, so you can chain calls:
    
    ```python exec="true" html="true" source="tabbed-left"
    from shapely.geometry import Point
    from blueprints.utils import Map

    m = Map(title="Chained Calls")

    m.add_point(Point(4.9, 52.37), label="📍").add_point(Point(5.1, 52.09), label="🏠").to_html("chained.html")

    print(m.to_html()) # markdown-exec: hide
    ```

---

## Add lines and polygons

Points are useful, but maps really come alive with shapes. Let's draw a walking route and highlight an area.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point, LineString, Polygon
from blueprints.utils.map import Map, StrokeStyle, FillStyle

m = Map(title="Amsterdam Walk")

# A walking route through the city center
route = LineString([
    (4.8852, 52.3702),  # Centraal Station
    (4.8910, 52.3663),  # Damrak
    (4.8932, 52.3631),  # Dam Square
    (4.8840, 52.3569),  # Leidseplein
])
m.add_linestring(
    route,
    hover="**Walking route**\n*Centraal → Leidseplein*",
    stroke=StrokeStyle(color="#e74c3c", weight=4, dash_array="10 6"),
)

# Highlight the Jordaan neighbourhood
jordaan = Polygon([
    (4.8760, 52.3720), (4.8890, 52.3720),
    (4.8890, 52.3800), (4.8760, 52.3800),
])
m.add_polygon(
    jordaan,
    hover="**De Jordaan**\nHistoric neighbourhood",
    stroke=StrokeStyle(color="#2ecc71", weight=2),
    fill=FillStyle(color="#2ecc71", opacity=0.15),
)

m.to_html("amsterdam_walk.html")

print(m.to_html())  # markdown-exec: hide
```

A few things to notice here:

**Coordinates are always `(longitude, latitude)`** — that's the Shapely convention (x, y). Map handles the flip to
Leaflet's `(lat, lon)` internally.

**`StrokeStyle`** controls borders and lines. You've got `color`, `weight` (pixels), `opacity`, and `dash_array` (an SVG
dash pattern like `"10 6"` for dashed lines).

**`FillStyle`** controls polygon fills with `color` and `opacity`. If you skip it, you get the default blue at 20%
opacity.

**Markdown in tooltips** supports `**bold**`, `*italic*`, `` `code` ``, `[links](url)`, `# headers`, and `- list items`.
Line breaks with `\n` work too.

!!! info "All the geometry types"

    Map handles every Shapely geometry: `Point`, `LineString`, `Polygon`, `MultiPoint`, `MultiLineString`,
    `MultiPolygon`, and `LinearRing`. You can use the specific `add_point()`, `add_linestring()`, etc. — or just use *
    *`add_geometry()`** which auto-dispatches by type:
    
        ```python
        m.add_geometry(some_shapely_object, hover="Works for any type")
        ```

---

## Style with dicts or objects

Every `add_*` method that accepts a style object (`StrokeStyle`, `FillStyle`, `MarkerStyle`, etc.) also accepts a
plain `dict` with the same keyword arguments. This means you can skip the extra imports for quick one-off styling:

```python
from shapely.geometry import Polygon
from blueprints.utils import Map  # one import

m = Map(title="Quick styling")
poly = Polygon([(4.9, 52.3), (5.0, 52.3), (5.0, 52.4), (4.9, 52.4)])

# Quick — pass dicts (no extra imports needed)
m.add_polygon(
    poly,
    stroke={"color": "red", "weight": 4},
    fill={"color": "red", "opacity": 0.15},
)
```

When you need **reusable** style configs or want IDE autocomplete, use the style dataclass objects instead:

```python
from blueprints.utils import Map, StrokeStyle, FillStyle

my_stroke = StrokeStyle(color="red", weight=4)
m.add_polygon(poly1, stroke=my_stroke)
m.add_polygon(poly2, stroke=my_stroke)  # reuse the same style
```

Both approaches work on all style parameters across the API: `stroke`, `fill`, `style`, `marker_style`,
`label_style`, and `popup_style`.

---

## Style your markers

The default marker is a blue pin, but you can swap it for emojis, Font Awesome icons, or fixed-size circles.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map, MarkerStyle, CircleStyle, StrokeStyle, FillStyle

m = Map(title="Marker Styles")

# Emoji marker (any text works as label)
m.add_point(
    Point(4.9041, 52.3676),
    label="🏛️",
    hover="**Royal Palace**",
)

# Icon marker (Folium/Font Awesome icons)
m.add_point(
    Point(4.8834, 52.3667),
    hover="**Anne Frank House**",
    marker_style=MarkerStyle(icon="home", marker_color="green", prefix="fa"),
)

# Circle marker (fixed pixel size, doesn't scale with zoom)
m.add_circle(
    Point(4.8795, 52.3600),
    hover="**Rijksmuseum**",
    style=CircleStyle(
        radius=12,
        stroke=StrokeStyle(color="#8e44ad", weight=2),
        fill=FillStyle(color="#8e44ad", opacity=0.5),
    ),
)

m.to_html("markers.html")

print(m.to_html())  # markdown-exec: hide
```

**`label`** on `add_point()` renders the marker as a `DivIcon` — essentially any HTML/emoji text. The `emoji_size` field
on `MarkerStyle` controls the font size (default 24px).

**`MarkerStyle`** gives you Folium's built-in icon system. Set `prefix="fa"`
for [Font Awesome](https://fontawesome.com/v4/icons/) icons or keep the default `"glyphicon"` for Bootstrap icons.

**`add_circle()`** draws a `CircleMarker` — a circle that stays the same pixel size at every zoom level. Great for data
visualization where you don't want markers overlapping at low zoom.

---

## Feature groups and layer control

When your map has multiple categories of data, you want the user to toggle them on and off. That's what "feature groups"
are for — think of them as named folders. Everything you add while a group is active goes into that folder.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils import Map

m = Map(title="Amsterdam POI")

# Group 1: Museums
m.create_feature_group("🏛️ Museums")
m.add_point(Point(4.8795, 52.3600), label="🖼️", hover="**Rijksmuseum**")
m.add_point(Point(4.8812, 52.3584), label="🌻", hover="**Van Gogh Museum**")

# Group 2: Parks
m.create_feature_group("🌳 Parks")
m.add_point(Point(4.8765, 52.3579), label="🌳", hover="**Vondelpark**")
m.add_point(Point(4.9125, 52.3597), label="🌿", hover="**Oosterpark**")

# Add layer control so the user can toggle groups
m.add_layer_control(collapsed=False)

m.to_html("poi_layers.html")

print(m.to_html())  # markdown-exec: hide
```

**`create_feature_group("name")`** creates a new group and immediately activates it. All subsequent `add_*` calls go
into this group until you call `create_feature_group()` again, `set_feature_group()` to switch, or `reset_target()` to
go back to the base map.

**`add_layer_control()`** adds the checkbox widget in the corner. Set `collapsed=False` to show it expanded by default.

---

## Choropleth maps

A "choropleth" is a map where areas are shaded by a numeric value — think population density, election results, or
temperature. Map builds one from a GeoJSON FeatureCollection and a value column.

```python exec="true" html="true" source="tabbed-right"
import json
from blueprints.utils import Map

# Example: three neighbourhoods with a "score" property
geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Centrum", "score": 92},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[4.88, 52.36], [4.92, 52.36], [4.92, 52.38], [4.88, 52.38], [4.88, 52.36]]],
            },
        },
        {
            "type": "Feature",
            "properties": {"name": "West", "score": 74},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[4.84, 52.36], [4.88, 52.36], [4.88, 52.38], [4.84, 52.38], [4.84, 52.36]]],
            },
        },
        {
            "type": "Feature",
            "properties": {"name": "Oost", "score": 85},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[4.92, 52.36], [4.96, 52.36], [4.96, 52.38], [4.92, 52.38], [4.92, 52.36]]],
            },
        },
    ],
}

m = Map(title="Neighbourhood Scores")
m.add_choropleth(
    geojson_data=geojson,
    value_column="score",
    key_on="feature.properties.name",
    legend_name="Liveability Score",
    hover_fields=["name", "score"],
    fill_opacity=0.7,
)

m.to_html("choropleth.html")

print(m.to_html())  # markdown-exec: hide
```

**`value_column`** tells Map which property holds the numeric value. **`key_on`** is the dot-path to the join key
inside each feature (Folium convention).

If you don't pass `values` explicitly, Map reads them straight from the GeoJSON properties — which is usually what
you want.

**`hover_fields`** turns property keys into a tooltip table on mouse-over.

!!! tip

    You can pass `geojson_data` as a dict, a JSON string, or a `Path` to a `.geojson` file — Map handles all three.

---

## Heatmaps

For dense point data (sensor readings, incidents, GPS traces), a heatmap shows intensity patterns better than individual
markers.

```python exec="true" html="true" source="tabbed-right"
import random
from shapely.geometry import Point
from blueprints.utils.map import Map, HeatmapStyle

# Generate 200 random points around Amsterdam
random.seed(42)
points = [
    Point(4.85 + random.gauss(0, 0.03), 52.35 + random.gauss(0, 0.015))
    for _ in range(200)
]

m = Map(title="Activity Heatmap")
m.add_heatmap(
    points,
    style=HeatmapStyle(radius=20, blur=15, min_opacity=0.4),
)

m.to_html("heatmap.html")

print(m.to_html())  # markdown-exec: hide
```

`add_heatmap()` accepts Shapely `Point` objects or raw `(lat, lon)` tuples. You can also pass `(lat, lon, intensity)`
tuples to weight certain points more heavily.

**`HeatmapStyle`** gives you control over `radius` (spread per point), `blur` (smoothing), `min_opacity`, and
`gradient` (a dict mapping `{0.4: "blue", 0.6: "lime", 1.0: "red"}`).

---

## Marker clusters

When you have hundreds of markers, the map becomes unreadable. Marker clusters group nearby points into numbered bubbles
that expand as you zoom in.

```python exec="true" html="true" source="tabbed-right"
import random
from shapely.geometry import Point
from blueprints.utils import Map

random.seed(42)
cafes = [Point(4.88 + random.uniform(-0.02, 0.02), 52.36 + random.uniform(-0.01, 0.01)) for _ in range(50)]
labels = ["☕"] * 50
hovers = [f"**Café #{i + 1}**" for i in range(50)]

m = Map(title="Amsterdam Cafés")
m.add_marker_cluster(cafes, labels=labels, hovers=hovers, name="Cafés")

m.to_html("clusters.html")

print(m.to_html())  # markdown-exec: hide
```

At low zoom you'll see cluster bubbles with counts. Zoom in and they split into individual ☕ markers.

---

## GeoPandas integration

If you're working with a `GeoDataFrame`, you don't need to loop through rows yourself. The `from_geodataframe()`
classmethod handles everything — CRS reprojection, per-row coloring, tooltips, and labels.

```python exec="true" html="true" source="tabbed-right"
import geopandas as gpd
from shapely.geometry import Point
from blueprints.utils import Map

# Build a simple GeoDataFrame
gdf = gpd.GeoDataFrame(
    {
        "name": ["Amsterdam", "Rotterdam", "Utrecht"],
        "population": [872_680, 651_446, 361_924],
        "geometry": [Point(4.9041, 52.3676), Point(4.4777, 51.9244), Point(5.1214, 52.0907)],
    },
    crs="EPSG:4326",
)

m = Map.from_geodataframe(
    gdf,
    hover_columns=["name", "population"],
    color_column="population",
    legend_name="Population",
    title="Dutch Cities",
)

m.to_html("cities.html")

print(m.to_html())  # markdown-exec: hide
```

**`color_column`** activates choropleth coloring — each geometry gets a color from a linear colormap based on its
numeric value. A legend is added automatically.

**`hover_columns`** builds a Markdown tooltip from the specified columns. Each column shows as `**column**: value`.

!!! warning

    If your GeoDataFrame uses a CRS other than WGS84 (EPSG:4326), Map reprojects it automatically using `gdf.to_crs()`.
    This requires `pyproj`.

---

## Coordinate auto-detection

Working with Dutch RD New coordinates (EPSG:28992)? Just pass them in. Map detects the coordinate range and
transforms to WGS84 automatically.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils import Map

# These are RD New coordinates (x: 0-300k, y: 300k-625k)
m = Map(title="RD New Auto-Detection")
m.add_point(Point(121_000, 487_000), label="📍", hover="**Amsterdam** (from RD)")

m.to_html("rd_new.html")

print(m.to_html())  # markdown-exec: hide
```

Map checks whether the x-coordinate is between 0–300,000 and y is between 300,000–625,000. If so, it assumes RD New
and transforms via pyproj.

You can also set the CRS explicitly on the constructor if auto-detection doesn't fit your case:

```python
m = Map(title="Explicit CRS", source_crs="EPSG:28992")
```

!!! info "How auto-detection works"

    The detection runs on the first coordinate of each geometry you add. If it falls within the RD New bounding box,
    transformation kicks in. For coordinates outside that range, nothing happens — they're assumed to be WGS84 already.
    
    This means you can't mix RD New and WGS84 geometries on the same map without setting `source_crs` explicitly on the constructor.

---

## Map configuration

The `MapConfig` dataclass controls the global look and feel of the map: tile provider, zoom, dimensions, and optional
plugins.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map, MapConfig

config = MapConfig(
    tile_layer="cartodb_dark",  # Dark theme
    zoom_start=14,  # Closer initial zoom
    fullscreen=True,  # Fullscreen button
    minimap=True,  # Inset minimap
    measure_control=True,  # Distance/area measurement tool
    mouse_position=True,  # Show coordinates at cursor
)

m = Map(title="Dark Mode", config=config)
m.add_point(Point(4.9041, 52.3676), label="🌃", hover="**Night Amsterdam**")

m.to_html("dark_mode.html")

print(m.to_html())  # markdown-exec: hide
```

### Available tile providers

| Key                  | Description                     |
|----------------------|---------------------------------|
| `openstreetmap`      | Default OpenStreetMap           |
| `cartodb_positron`   | Light, minimal CartoDB          |
| `cartodb_dark`       | Dark CartoDB                    |
| `esri_satellite`     | Esri satellite imagery          |
| `esri_topo`          | Esri topographic                |
| `stamen_terrain`     | Stamen terrain with hillshading |
| `stamen_toner`       | Stamen high-contrast B&W        |
| `kadaster_brt`       | Dutch Kadaster topographic      |
| `kadaster_luchtfoto` | Dutch Kadaster aerial photos    |
| `kadaster_grijs`     | Dutch Kadaster greyscale        |

You can also add extra tile layers after construction with `add_tile_layer()`, and combine them with
`add_layer_control()` to let users switch between base maps.

---

## Text annotations

Sometimes you need a floating label on the map — not tied to a marker, just text at a location.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map, LabelStyle

m = Map(title="Annotations")

m.add_text(
    Point(4.9041, 52.3676),
    "Amsterdam Centrum",
    style=LabelStyle(font_size=16, font_color="#2c3e50", background_color="rgba(255,255,255,0.85)"),
)

m.to_html("annotations.html")

print(m.to_html())  # markdown-exec: hide
```

**`add_text()`** accepts either a Shapely `Point(lon, lat)` or a plain `(lat, lon)` tuple. The `LabelStyle` dataclass
controls font size, family, color, weight, background, border, and padding.

---

## Site plans with shape markers

For geotechnical or infrastructure projects you often need a site plan with survey markers, borehole locations, or
measurement points. Shape markers (triangle, circle, square) combined with text labels and restricted bounds produce
clean site overview maps.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map, MapConfig, MarkerStyle

# Survey data — CPT and borehole locations near Hoofddorp
surveys = [
    {"lon": 4.6820, "lat": 52.3680, "label": "1123-25N-S13", "x_rd": 107650, "y_rd": 411350},
    {"lon": 4.6835, "lat": 52.3655, "label": "1123-25N-S12", "x_rd": 107680, "y_rd": 411280},
    {"lon": 4.6850, "lat": 52.3630, "label": "1123-25N-S11", "x_rd": 107710, "y_rd": 411240},
    {"lon": 4.6880, "lat": 52.3628, "label": "1123-25N-S14", "x_rd": 107750, "y_rd": 411235},
    {"lon": 4.6837, "lat": 52.3570, "label": "1123-25N-S01", "x_rd": 107737, "y_rd": 411210},
    {"lon": 4.6950, "lat": 52.3690, "label": "23248_S013", "x_rd": 107850, "y_rd": 411380},
    {"lon": 4.6990, "lat": 52.3685, "label": "23248_S019", "x_rd": 107890, "y_rd": 411370},
    {"lon": 4.6980, "lat": 52.3640, "label": "23248_S005", "x_rd": 107880, "y_rd": 411260},
    {"lon": 4.6960, "lat": 52.3600, "label": "23248_S011", "x_rd": 107860, "y_rd": 411180},
    {"lon": 4.6830, "lat": 52.3550, "label": "23248_S001", "x_rd": 107730, "y_rd": 411080},
    {"lon": 4.6980, "lat": 52.3580, "label": "23248_S018", "x_rd": 107880, "y_rd": 411140},
]

m = Map(
    title="CPT Survey Locations",
    config=MapConfig(tile_layer="openstreetmap", zoom_start=15),
)

# Add triangle markers with hover info and text labels
triangle = MarkerStyle(shape="triangle", shape_color="black")

for s in surveys:
    m.add_point(
        point=Point(s["lon"], s["lat"]),
        hover=f'**Naam:** {s["label"]}\n\nx [m RD] = {s["x_rd"]}\n\ny [m RD] = {s["y_rd"]}',
        marker_style=triangle,
        text_label=s["label"],
    )

# Fit bounds with padding and lock the view
m.set_bounds(padding=0.002, restrict=True)

m.to_html("site_plan.html")

print(m.to_html())  # markdown-exec: hide

```

A few things to highlight:

**`MarkerStyle(shape="triangle")`** renders a downward-pointing triangle (▼) instead of a pin. Available shapes are
`"triangle"`, `"circle"`, and `"square"`. Set `shape_color` and `shape_size` to customize them. Circles and squares
use Folium's `RegularPolygonMarker` (36-sided and 4-sided polygons respectively).

**`text_label`** places a text annotation just below the marker. It works with any marker type — shapes, emojis, and
icons. By default the label has no background and no border; pass a custom `label_style=LabelStyle(...)` to change
the font size, color, or add a background.

**`set_bounds(padding=0.002, restrict=True)`** fits the map to the data with a small margin, then locks the
viewport so the user can't accidentally pan away from the survey area.

!!! tip

    When `label` or `emoji` is set, it takes precedence over `shape`. This means you can mix shape markers
    (for data points) and emoji markers (for landmarks) on the same map without conflict:

    ```python
    # Shape marker with a text label below
    m.add_point(pt, marker_style=MarkerStyle(shape="circle", shape_color="red"), text_label="CPT-01")

    # Emoji marker — shape is ignored because label is set
    m.add_point(pt, label="🏗️", text_label="Site office")
    ```

---

## Export

### HTML (always works)

```python
m.to_html("map.html")
```

Writes a standalone HTML file. No dependencies needed to view it — just open in any browser.

### PNG image

```python
# Save to file
m.to_image("map.png", width=1600, height=1000, delay=3.0)

# Or get raw bytes
png_bytes = m.to_image()

# Or get a BytesIO buffer (useful for Django/Flask responses)
buf = m.to_bytesio(width=1200, height=800)
```

!!! warning

    PNG/SVG export requires **Selenium** and **Chrome/Chromium** with **chromedriver**. The `delay` parameter (seconds)
    controls how long Map waits for tiles to load before taking the screenshot. Increase it on slow connections.

### SVG

```python
# Raster-wrapped SVG (PNG embedded in SVG container)
m.to_svg("map.svg")
```

### Async variants

For web frameworks like FastAPI that run an async event loop:

```python
png_bytes = await m.to_image_async()
svg_string = await m.to_svg_async()
```

These run the Selenium capture in a thread executor so they don't block the event loop.

---

## Merge maps

You can combine two `Map` instances with `+`. The left map's title and config are preserved; the right map's
geometries and layers are added on top.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point, Polygon
from blueprints.utils import Map

museums = Map(title="Combined")
museums.add_point(Point(4.8795, 52.3600), label="🖼️", hover="**Rijksmuseum**")

parks = Map()
parks.add_polygon(
    Polygon([(4.8580, 52.3530), (4.8830, 52.3530), (4.8830, 52.3620), (4.8580, 52.3620)]),
    hover="**Vondelpark**",
)

combined = museums + parks
combined.to_html("merged.html")

print(combined.to_html())  # markdown-exec: hide
```

---

## GeoJSON layers

You can add raw GeoJSON as a styled layer with hover tooltips — useful when you already have GeoJSON files and don't
need choropleth coloring.

```python exec="true" html="true" source="tabbed-right"
from blueprints.utils import Map

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Zone A", "type": "residential"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[4.88, 52.36], [4.90, 52.36], [4.90, 52.37], [4.88, 52.37], [4.88, 52.36]]],
            },
        },
    ],
}

m = Map(title="GeoJSON Layer")
m.add_geojson(
    geojson,
    hover_fields=["name", "type"],
    style={"color": "#e74c3c", "weight": 2, "fillOpacity": 0.1},
    highlight={"weight": 5, "fillOpacity": 0.3},
)

m.to_html("geojson_layer.html")

print(m.to_html())  # markdown-exec: hide
```

**`hover_fields`** picks properties to show on mouse-over. **`highlight`** defines the style change on hover. You can
pass `data` as a dict, a JSON string, or a file `Path`.

---

## Rich popup content

By default, popups use fixed dimensions (300×150 px). For content-heavy popups — tables, images, or long text — use
`PopupStyle` to control the popup size.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map, PopupStyle

m = Map(title="Custom Popups")

m.add_point(
    Point(4.9041, 52.3676),
    label="📋",
    popup="**Amsterdam**\n\nPopulation: 872,680\nProvince: North Holland\nFounded: 1275",
    popup_style=PopupStyle(width=400, height=250),
)

m.to_html("custom.html")

print(m.to_html())  # markdown-exec: hide
```

**`PopupStyle`** has three fields: `width` (IFrame width in px), `height` (IFrame height in px), and `max_width`
(maximum popup width). All default to values matching the previous hardcoded behavior (300, 150, 300), so existing
code is unaffected.

---

## Raw HTML in popups

Markdown tooltips and popups are convenient, but sometimes you need full control — a styled table, an embedded image,
or colored text. Wrap your HTML string in `RawHTML` to bypass markdown conversion entirely.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map, RawHTML, PopupStyle

m = Map(title="Raw HTML")

table_html = RawHTML("""
<table style="border-collapse:collapse;width:100%;">
  <tr style="background:#3498db;color:white;">
    <th style="padding:6px;">Property</th>
    <th style="padding:6px;">Value</th>
  </tr>
  <tr><td style="padding:4px;">Name</td><td style="padding:4px;">Amsterdam</td></tr>
  <tr style="background:#f0f0f0;"><td style="padding:4px;">Population</td><td style="padding:4px;">872,680</td></tr>
  <tr><td style="padding:4px;">Province</td><td style="padding:4px;">North Holland</td></tr>
</table>
""")

m.add_point(
    Point(4.9041, 52.3676),
    label="📊",
    hover=RawHTML("<b>Amsterdam</b> — click for details"),
    popup=table_html,
    popup_style=PopupStyle(width=350, height=200),
)

m.to_html("custom.html")

print(m.to_html())  # markdown-exec: hide
```

**`RawHTML`** is a `str` subclass — it works anywhere a regular string does. The difference is that `Map` skips the
markdown-to-HTML conversion step, so your `<table>`, `<img>`, and `<style>` tags pass through untouched.

!!! tip

    `RawHTML` works on both `hover` (tooltip) and `popup` (click) parameters across all `add_*` methods.

---

## Escape hatch

Need something Map doesn't wrap? The underlying Folium `Map` object is always accessible:

```python exec="true" html="true" source="tabbed-right"
from blueprints.utils import Map

m = Map(title="Custom")

# Access the raw Folium Map
folium_map = m.folium_map

# Add anything Folium supports
import folium

folium.CircleMarker([52.37, 4.90], radius=50, color="red").add_to(folium_map)

m.to_html("custom.html")

print(m.to_html())  # markdown-exec: hide
```

---

## Quick reference

| What you want        | Method                                               |
|----------------------|------------------------------------------------------|
| Point marker         | `add_point(Point, label=, hover=)`                   |
| Shape marker         | `add_point(Point, marker_style=MarkerStyle(shape=))` |
| Marker + label below | `add_point(Point, ..., text_label="CPT-01")`         |
| Circle marker        | `add_circle(Point, style=CircleStyle)`               |
| Line                 | `add_linestring(LineString, stroke=StrokeStyle)`     |
| Polygon              | `add_polygon(Polygon, stroke=, fill=)`               |
| Any geometry         | `add_geometry(geom)` (auto-dispatches)               |
| GeoJSON layer        | `add_geojson(data, hover_fields=)`                   |
| Choropleth           | `add_choropleth(geojson, value_column=, key_on=)`    |
| Heatmap              | `add_heatmap(points, style=HeatmapStyle)`            |
| Marker cluster       | `add_marker_cluster(points, labels=, hovers=)`       |
| Text label           | `add_text(location, text, style=LabelStyle)`         |
| Custom popup size    | `add_point(..., popup_style=PopupStyle(width=400))`  |
| Raw HTML content     | `add_point(..., hover=RawHTML("<b>html</b>"))`       |
| Feature group        | `create_feature_group(name)` → `add_layer_control()` |
| Fit & lock bounds    | `set_bounds(padding=, restrict=True)`                |
| Zoom-dependent       | `add_point(..., min_zoom=12)`                        |
| From GeoDataFrame    | `Map.from_geodataframe(gdf, hover_columns=)`         |
| Export HTML          | `to_html("map.html")`                                |
| Export PNG           | `to_image("map.png")` / `to_bytesio()`               |
| Export SVG           | `to_svg("map.svg")`                                  |
| Clean export (no UI) | `to_image("map.png", hide_controls=True)`            |
| Merge maps           | `map_a + map_b`                                      |

### Style dataclasses

| Class          | Key fields                                                             |
|----------------|------------------------------------------------------------------------|
| `StrokeStyle`  | `color`, `weight`, `opacity`, `dash_array`                             |
| `FillStyle`    | `color`, `opacity`                                                     |
| `MarkerStyle`  | `icon`, `marker_color`, `prefix`, `emoji`, `shape`, `shape_color`      |
| `CircleStyle`  | `radius`, `stroke`, `fill`                                             |
| `LabelStyle`   | `font_size`, `font_family`, `font_color`, `background_color`           |
| `PopupStyle`   | `width`, `height`, `max_width`                                         |
| `HeatmapStyle` | `radius`, `blur`, `min_opacity`, `gradient`                            |
| `MapConfig`    | `tile_layer`, `zoom_start`, `fullscreen`, `minimap`, `measure_control` |