# Make beautiful maps with Blueprints

One import, a few method calls, and you've got a full OpenStreetMap visualization with hover tooltips, 
choropleths, heatmaps, and export to HTML, PNG, or SVG.

Perfect for geotechnical site plans, infrastructure overviews, or any spatial data visualization where you want more 
control than static images but don't need the full power of a GIS.

**Key features:**

- 🗺️ **Shapely-native**  pass `Point`, `Polygon`, `LineString` directly, including multi-geometries
- 📝 **Markdown/HTML hover and popup text** bold, italic, links, lists, and code in tooltips
- 📌 **Emoji & icon markers** any text or Font Awesome icons as markers
- 🎨 **Choropleth & heatmaps** color-coded maps from numeric data
- 📊 **GeoPandas integration** `Map.from_geodataframe()` one-liner
- 🌐 **Auto CRS detection** RD New (EPSG:28992) coordinates transform automatically
- 📤 **Export anywhere** HTML, PNG, SVG, async variants, and `BytesIO` buffers
- 🧩 **Feature groups** toggleable layers with a built-in layer control
- 🔌 **10 tile providers** OpenStreetMap, CartoDB, Esri, Stamen, and Kadaster

??? example "📝 TL;DR full example for power users"

    Are you in a hurry? Here's a complete map example with points, lines, polygons, popups, feature groups, layer control, style dicts, and HTML export in one block.
    Everything below this fold explains each piece step by step.

    ```python exec="true" html="true" source="tabbed-right"
    from shapely.geometry import Point, LineString, Polygon
    from blueprints.utils import Map, MapConfig

    m = Map(
        title="Amsterdam Overview",
        config=MapConfig(
            tile_layer=["cartodb_positron", "cartodb_dark", "kadaster_brt", "kadaster_luchtfoto"],
            fullscreen=True,
            minimap=True,
            measure_control=True,
            mouse_position=True,
        ),
    )

    # Feature group: landmarks (emoji markers with hover + popups)
    m.create_feature_group("🏛️ Landmarks")
    m.add_point(
        point=Point(4.9041, 52.3676),
        marker="🏛️",
        tooltip="**Royal Palace**",
        popup="**Royal Palace**\nDam Square, Amsterdam\nBuilt: 1665",
        popup_style={"width": 5000, "height": 120},
    )
    m.add_point(
        point=Point(4.8834, 52.3667),
        marker="📖",
        tooltip="**Anne Frank House**",
        popup="**Anne Frank House**\nPrinsengracht 263\nVisitors/year: ~1.3 million",
        popup_style={"width": 300, "height": 120},
    )
    m.add_point(
        point=Point(4.8795, 52.3600),
        marker="fa-landmark",
        tooltip="**Rijksmuseum**",
        popup="**Rijksmuseum**\nDutch art and history since 1800",
        marker_style={"font-size": "24px", "color": "green"},
    )

    # Feature group: areas (polygon + line, styled with dicts)
    m.create_feature_group("📍 Areas of Interest")
    m.add_polygon(
        polygon=Polygon([(4.876, 52.372), (4.889, 52.372), (4.889, 52.380), (4.876, 52.380)]),
        tooltip="**De Jordaan**\nHistoric neighbourhood",
        popup="**De Jordaan**\n\nOne of Amsterdam's most famous neighbourhoods.\n- Narrow streets\n- Independent galleries\n- Brown cafés",
        stroke={"color": "green", "weight": 2},
        fill={"color": "blue", "opacity": 0.15},
        popup_style={"width": 300, "height": 180},
    )
    # Polygon with an interior hole (the hole renders as a cutout)
    vondelpark = Polygon(
        [(4.858, 52.353), (4.883, 52.353), (4.883, 52.362), (4.858, 52.362)],  # outer boundary
        [[(4.865, 52.356), (4.875, 52.356), (4.875, 52.360), (4.865, 52.360)]],  # pond cutout
    )
    m.add_polygon(
        polygon=vondelpark,
        tooltip="**Vondelpark**\nThe hole is the pond!",
        stroke={"color": "#2ecc71", "weight": 2},
        fill={"color": "#2ecc71", "opacity": 0.25},
    )
    m.add_linestring(
        line=LineString([(4.8852, 52.3702), (4.8910, 52.3663), (4.8932, 52.3631), (4.884, 52.3569)]),
        tooltip="**Walking route**\n*Centraal → Leidseplein*",
        stroke={"color": "red", "weight": 4, "dash_array": "10 6"},
    )

    # Circle marker with nested style dict
    m.reset_target()
    m.add_circle(
        point=Point(4.8812, 52.3584),
        tooltip="**Van Gogh Museum**",
        popup="**Van Gogh Museum**\nOver 200 paintings, 500 drawings",
        style={"radius": 12, "stroke": {"color": "green", "weight": 2}, "fill": {"color": "orange", "opacity": 0.5}},
    )

    # Text annotation
    m.add_text(point=Point(4.89, 52.37), text="Centrum", style={"font-size": "14px", "color": "#2c3e50"})

    # Add layer control and fit bounds with padding
    m.add_layer_control(collapsed=False)
    m.set_bounds(padding=0.005)
    
    m.to_html("amsterdam_overview.html")

    print(m.to_html())  # markdown-exec: hide
    ```

??? example "📝 TL;DR geotechnical site investigation with marker clusters"

    For all those geotechnical engineers out there, here's a quick example of a site investigation map with 
    GeoPandas data, marker clusters with text labels, RawHTML table popups, feature groups, and layer control.

    Just imagine connecting this to your database of CPTs and boreholes, and you've got a dynamic site plan that 
    updates with new data, no GIS software needed, **just some Blueprints magic.**

    ```python exec="true" html="true" source="tabbed-right"
    import geopandas as gpd
    from shapely.geometry import Point
    from blueprints.utils.map import Map, MapConfig, RawHTML

    # CPT locations (Utrecht area)
    cpts = gpd.GeoDataFrame(
        {
            "id": ["CPT-01", "CPT-02", "CPT-03", "CPT-04", "CPT-05", "CPT-06"],
            "depth_m": [25, 30, 20, 28, 22, 35],
            "date": ["2024-03-15", "2024-03-16", "2024-03-18", "2024-03-20", "2024-03-21", "2024-03-22"],
            "qc_max_mpa": [18.2, 22.5, 15.0, 20.1, 16.8, 25.3],
        },
        geometry=[
            Point(5.1180, 52.0900), Point(5.1050, 52.0950), Point(5.1250, 52.0870),
            Point(5.0980, 52.1010), Point(5.1120, 52.0830), Point(5.1350, 52.0960),
        ],
        crs="EPSG:4326",
    )

    # Borehole locations
    boreholes = gpd.GeoDataFrame(
        {
            "id": ["BH-01", "BH-02", "BH-03", "BH-04", "BH-05"],
            "depth_m": [15, 20, 12, 18, 25],
            "date": ["2024-04-01", "2024-04-02", "2024-04-03", "2024-04-05", "2024-04-06"],
            "soil_type": ["Clay", "Peat / Clay", "Sand", "Clay / Sand", "Peat"],
        },
        geometry=[
            Point(5.1100, 52.0920), Point(5.1200, 52.0980), Point(5.1020, 52.0860),
            Point(5.1300, 52.0910), Point(5.0950, 52.0970),
        ],
        crs="EPSG:4326",
    )

    # RawHTML popup builders
    def cpt_popup(row: gpd.GeoDataFrame) -> RawHTML:
        """Build an HTML table popup for a CPT row."""
        return RawHTML(
            '<table style="border-collapse:collapse;width:100%;font-family:Arial,sans-serif;font-size:13px;">'
            f'<tr><th colspan="2" style="background:#2c3e50;color:white;padding:6px;text-align:center;">{row.id}</th></tr>'
            f'<tr><td style="padding:4px;border:1px solid #ddd;">Depth</td><td style="padding:4px;border:1px solid #ddd;">{row.depth_m} m</td></tr>'
            f'<tr><td style="padding:4px;border:1px solid #ddd;">Date</td><td style="padding:4px;border:1px solid #ddd;">{row.date}</td></tr>'
            f'<tr><td style="padding:4px;border:1px solid #ddd;">q<sub>c</sub> max</td>'
            f'<td style="padding:4px;border:1px solid #ddd;">{row.qc_max_mpa} MPa</td></tr>'
            "</table><br><p>This popup is built with <code>RawHTML</code> to allow for custom styling and layout. You can include any HTML content here, such as tables, images, or links.</p>"
        )

    def bh_popup(row: gpd.GeoDataFrame) -> RawHTML:
        """Build an HTML table popup for a borehole row."""
        return RawHTML(
            '<table style="border-collapse:collapse;width:100%;font-family:Arial,sans-serif;font-size:13px;">'
            f'<tr><th colspan="2" style="background:#2c3e50;color:white;padding:6px;text-align:center;">{row.id}</th></tr>'
            f'<tr><td style="padding:4px;border:1px solid #ddd;">Depth</td><td style="padding:4px;border:1px solid #ddd;">{row.depth_m} m</td></tr>'
            f'<tr><td style="padding:4px;border:1px solid #ddd;">Date</td><td style="padding:4px;border:1px solid #ddd;">{row.date}</td></tr>'
            f'<tr><td style="padding:4px;border:1px solid #ddd;">Soil type</td>'
            f'<td style="padding:4px;border:1px solid #ddd;">{row.soil_type}</td></tr>'
            "</table><br><p>This popup is built with <code>RawHTML</code> to allow for custom styling and layout. You can include any HTML content here, such as tables, images, or links.</p>"
        )

    # Build the map
    m = Map(
        title="Site Investigation - Utrecht",
        config=MapConfig(
            tile_layer="cartodb_positron",
            zoom_start=14,
            mouse_position=True,
            fullscreen=True,
            measure_control=True,
        ),
    )

    # CPT cluster layer (🔺 emoji markers with text labels)
    m.create_feature_group("🔺 CPTs")
    m.add_marker_cluster(
        points=list(cpts.geometry),
        labels=["🔺"] * len(cpts),
        hovers=[f"**{r.id}**\nDepth: {r.depth_m} m\nDate: {r.date}" for _, r in cpts.iterrows()],
        popups=[cpt_popup(r) for _, r in cpts.iterrows()],
        captions=list(cpts["id"]),
        name="🔺 CPTs",
        popup_style={"width": 280, "height": 160},
    )

    # Borehole cluster layer (🔵 emoji markers with text labels)
    m.create_feature_group("🔵 Boreholes")
    m.add_marker_cluster(
        points=list(boreholes.geometry),
        labels=["🔵"] * len(boreholes),
        hovers=[f"**{r.id}**\nDepth: {r.depth_m} m\nDate: {r.date}" for _, r in boreholes.iterrows()],
        popups=[bh_popup(r) for _, r in boreholes.iterrows()],
        captions=list(boreholes["id"]),
        name="🔵 Boreholes",
        popup_style={"width": 280, "height": 160},
    )

    m.add_layer_control(collapsed=False)
    m.set_bounds(padding=0.003)
    m.to_html("geotechnical_site_map.html")

    print(m.to_html())  # markdown-exec: hide
    ```

## Your first map

Let's start with the absolute minimum, a single point on a map, exported to HTML.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils import Map

# Create a map and add a location (tooltip, popup, and caption all support Markdown and are optional)
m = Map(title="Hello Amsterdam")
m.add_point(
    point=Point(4.9041, 52.3676),
    tooltip="**Amsterdam**",
    popup="**Amsterdam** is the capital city of the Netherlands, known for its canals, museums, and vibrant culture.",
    caption="AMS",
)

# Save to an HTML file you can open in any browser
m.to_html("hello.html")  # or just m.to_html() to get the HTML string that you can use in a web app or Marimo notebook
print(m.to_html())  # markdown-exec: hide
```

That's it. Open `hello.html` and you'll see an interactive OpenStreetMap centered in Amsterdam. Hover over
it, and you get a bold "Amsterdam" tooltip.

Let's walk through what happened:

**`Map(title="Hello Amsterdam")`** creates a new map. The `title` shows as a floating label at the top. You didn't
pass a `center` that's fine. Map auto-fits the viewport to whatever geometries you add.

**`add_point()`** takes a Shapely `Point(longitude, latitude)`. The `tooltip` parameter accepts Markdown so `**Amsterdam**` renders as bold in the tooltip.

**`to_html()`** writes a standalone HTML file. No server needed, just open it in a browser.

!!! tip "Chain calls for fluent API"

    Every `add_*` method returns `self`, so you can chain calls:
    
    ```python exec="true" html="true" source="tabbed-left"
    from shapely.geometry import Point
    from blueprints.utils import Map

    m = Map(title="Chained Calls")

    m.add_point(Point(5.1218, 52.09334), marker="📍").add_point(Point(5.1, 52.09), marker="🏠").to_html("chained.html")

    print(m.to_html()) # markdown-exec: hide
    ```

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
    line=route,
    tooltip="**Walking route**\n*Centraal → Leidseplein*",
    stroke=StrokeStyle(color="#e74c3c", weight=4, dash_array="10 6"),
)

# Highlight the Jordaan neighbourhood
jordaan = Polygon([
    (4.8760, 52.3720), (4.8890, 52.3720),
    (4.8890, 52.3800), (4.8760, 52.3800),
])
m.add_polygon(
    polygon=jordaan,
    tooltip="**De Jordaan**\nHistoric neighbourhood",
    stroke=StrokeStyle(color="#2ecc71", weight=2),
    fill=FillStyle(color="#2ecc71", opacity=0.15),
)

m.to_html("amsterdam_walk.html")

print(m.to_html())  # markdown-exec: hide
```

A few things to notice here:

**Coordinates are always `(longitude, latitude)`** that's the Shapely convention (x, y). Map handles the flip to
Leaflet's `(lat, lon)` internally.

**`StrokeStyle`** controls borders and lines. You've got `color`, `weight` (pixels), `opacity`, and `dash_array` (an SVG
dash pattern like `"10 6"` for dashed lines).

**`FillStyle`** controls polygon fills with `color` and `opacity`. If you skip it, you get the default blue at 20%
opacity.

**Markdown in tooltips** supports `**bold**`, `*italic*`, `` `code` ``, `[links](url)`, `# headers`, and `- list items`.
Line breaks with `\n` work too.

!!! info "All the geometry types"

    Map handles every Shapely geometry: `Point`, `LineString`, `Polygon`, `MultiPoint`, `MultiLineString`,
    `MultiPolygon`, and `LinearRing`. You can use the specific `add_point()`, `add_linestring()`, etc. or just use *
    *`add_geometry()`** which auto-dispatches by type:
    
    ```python
    m.add_geometry(some_shapely_object, tooltip="Works for any type")
    ```

!!! info "Style with dicts or objects"

    Leaflet/Folium configuration styles (`StrokeStyle`, `FillStyle`, `CircleStyle`, etc.) accept either a dataclass
    instance or a plain `dict` with the same keyword arguments.  **Marker and caption styles** use CSS dicts directly —
    no special import needed.

    ```python exec="true" html="true" source="tabbed-left"
    from shapely.geometry import Polygon
    from blueprints.utils import Map  # one import

    m = Map(title="Quick styling")
    poly = Polygon([(4.9, 52.3), (5.0, 52.3), (5.0, 52.4), (4.9, 52.4)])

    # Quick,  pass dicts (no extra imports needed)
    m.add_polygon(
        poly,
        stroke={"color": "red", "weight": 4},
        fill={"color": "red", "opacity": 0.15},
    )

    m.to_html("quick_style.html")

    print(m.to_html())  # markdown-exec: hide
    ```

    When you need **reusable** style configs or want IDE autocomplete, use the style dataclass objects for lines/polygons/circles:

    ```python exec="true" html="true" source="tabbed-left"
    from shapely.geometry import Polygon
    from blueprints.utils import Map, StrokeStyle, FillStyle

    m = Map(title="Reusable styles")

    poly1 = Polygon([(4.9, 52.3), (5.0, 52.3), (5.0, 52.4), (4.9, 52.4)])
    poly2 = Polygon([(4.85, 52.35), (4.95, 52.35), (4.95, 52.45), (4.85, 52.45)])

    my_stroke = StrokeStyle(color="red", weight=4)
    m.add_polygon(poly1, stroke=my_stroke)
    m.add_polygon(poly2, stroke=my_stroke)  # reuse the same style

    m.to_html("reusable_style.html")

    print(m.to_html())  # markdown-exec: hide
    ```

    For **marker and caption styling**, pass a plain CSS dict, any CSS property is valid:

    ```python
    m.add_point(pt, marker="fa-house", marker_style={"font-size": "30px", "color": "red"})
    m.add_point(pt, marker="📍", caption="AMS", caption_style={"font-size": "14px", "color": "blue"})
    m.add_text(pt, "Label", style={"font-size": "14px", "color": "#2c3e50"})
    ```

## Style your markers

The default marker is a down-arrow icon, but you can swap it for emojis, Font Awesome icons, or fixed-size circles.
Marker styling uses plain CSS dicts, no special imports needed.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map, CircleStyle, StrokeStyle, FillStyle

m = Map(title="Marker Styles")

# Emoji marker (any text works as marker)
m.add_point(
    point=Point(4.9041, 52.3676),
    marker="🏛️",
    tooltip="**Royal Palace**",
)

# Icon marker with custom CSS (Font Awesome icons)
m.add_point(
    point=Point(4.8834, 52.3667),
    marker="fa-house",
    tooltip="**Anne Frank House**",
    marker_style={"font-size": "24px", "color": "green"},
)

# Circle marker (fixed pixel size, doesn't scale with zoom)
m.add_circle(
    point=Point(4.8795, 52.3600),
    tooltip="**Rijksmuseum**",
    style=CircleStyle(
        radius=12,
        stroke=StrokeStyle(color="#8e44ad", weight=2),
        fill=FillStyle(color="#8e44ad", opacity=0.5),
    ),
)

m.to_html("markers.html")

print(m.to_html())  # markdown-exec: hide
```

**`marker`** on `add_point()` controls what's displayed.  Bare names like `"home"` get a Glyphicon prefix,
names starting with `"fa-"` get an `"fa-solid"` prefix, full CSS classes like `"fa-solid fa-house"` are used as-is,
and non-ASCII text (emojis) renders as a text DivIcon.

**`marker_style`** is a CSS dict, any valid CSS property works (`font-size`, `color`, `text-shadow`, etc.).

**`add_circle()`** draws a `CircleMarker` a circle that stays the same pixel size at every zoom level. Great for data
visualization where you don't want markers overlapping at low zoom.


## Feature groups and layer control

When your map has multiple categories of data, you want the user to toggle them on and off. That's what "feature groups"
are for, think of them as named folders. Everything you add while a group is active goes into that folder. 
Easy for turn on/off control with the layer control widget.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils import Map

m = Map(title="Amsterdam POI")

# Group 1: Museums
m.create_feature_group("🏛️ Museums")
m.add_point(point=Point(4.8795, 52.3600), marker="🖼️", tooltip="**Rijksmuseum**")
m.add_point(point=Point(4.8812, 52.3584), marker="🌻", tooltip="**Van Gogh Museum**")

# Group 2: Parks
m.create_feature_group("🌳 Parks")
m.add_point(point=Point(4.8765, 52.3579), marker="🌳", tooltip="**Vondelpark**")
m.add_point(point=Point(4.9125, 52.3597), marker="🌿", tooltip="**Oosterpark**")

# Add layer control so the user can toggle groups
m.add_layer_control(collapsed=False)

m.to_html("poi_layers.html")

print(m.to_html())  # markdown-exec: hide
```

**`create_feature_group("name")`** creates a new group and immediately activates it. All subsequent `add_*` calls go
into this group until you call `create_feature_group()` again, `set_feature_group()` to switch, or `reset_target()` to
go back to the base map.

**`add_layer_control()`** adds the checkbox widget in the corner. Set `collapsed=False` to show it expanded by default.


## Choropleth maps

A "choropleth" is a map where areas are shaded by a numeric value, think population density, election results, or
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

If you don't pass `values` explicitly, Map reads them straight from the GeoJSON properties, which is usually what
you want.

**`hover_fields`** turns property keys into a tooltip table on mouse-over.

!!! tip "Multiple ways to pass GeoJSON"

    You can pass `geojson_data` as a dict, a JSON string, or a `Path` to a `.geojson` file, Map handles all three.

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
    points=points,
    style=HeatmapStyle(radius=20, blur=15, min_opacity=0.4),
)

m.to_html("heatmap.html")

print(m.to_html())  # markdown-exec: hide
```

`add_heatmap()` accepts Shapely `Point` objects or raw `(lat, lon)` tuples. You can also pass `(lat, lon, intensity)`
tuples to weight certain points more heavily.

**`HeatmapStyle`** gives you control over `radius` (spread per point), `blur` (smoothing), `min_opacity`, and
`gradient` (a dict mapping `{0.4: "blue", 0.6: "lime", 1.0: "red"}`).

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
m.add_marker_cluster(points=cafes, labels=labels, hovers=hovers, name="Cafés")

m.to_html("clusters.html")

print(m.to_html())  # markdown-exec: hide
```

At low zoom you'll see cluster bubbles with counts. Zoom in and they split into individual ☕ markers.

## GeoPandas integration

If you're working with a `GeoDataFrame`, you don't need to loop through rows yourself. The `from_geodataframe()`
classmethod handles everything. CRS reprojection, per-row coloring, tooltips, and labels.

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
    gdf=gdf,
    hover_columns=["name", "population"],
    color_column="population",
    legend_name="Population",
    title="Dutch Cities",
)

m.to_html("cities.html")

print(m.to_html())  # markdown-exec: hide
```

**`color_column`** activates choropleth coloring, each geometry gets a color from a linear colormap based on its
numeric value. A legend is added automatically.

**`hover_columns`** builds a Markdown tooltip from the specified columns. Each column shows as `**column**: value`.

## Coordinate auto-detection

Working with Dutch RD New coordinates (EPSG:28992)? Just pass them in. Map detects the coordinate range and
transforms to WGS84 automatically.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils import Map

# These are RD New coordinates (x: 0-300k, y: 300k-625k)
m = Map(title="RD New Auto-Detection")
m.add_point(point=Point(121_000, 487_000), marker="📍", tooltip="**Amsterdam** (from RD)")

m.to_html("rd_new.html")

print(m.to_html())  # markdown-exec: hide
```

Map checks whether the x-coordinate is between 0–300,000 and y is between 300,000–625,000. If so, it assumes RD New
and transforms via `pyproj`.

You can also set the CRS explicitly on the constructor if auto-detection doesn't fit your case:

```python
m = Map(title="Explicit CRS", source_crs="EPSG:28992")
```

!!! info "How auto-detection works"

    The detection runs on the first coordinate of each geometry you add. If it falls within the RD New bounding box,
    transformation kicks in. For coordinates outside that range, nothing happens, they're assumed to be WGS84 already.
    
    This means you can't mix RD New and WGS84 geometries on the same map without setting `source_crs` explicitly on the constructor.


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
m.add_point(Point(4.9041, 52.3676), marker="🌃", tooltip="**Night Amsterdam**")

m.to_html("dark_mode.html")

print(m.to_html())  # markdown-exec: hide
```

!!! info "Available tile providers"

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

    **Multiple tile layers** pass a list to `tile_layer` and add a layer control so users can switch between
    base maps:

    ```python exec="true" html="true" source="tabbed-left"
    from shapely.geometry import Point
    from blueprints.utils import Map, MapConfig

    m = Map(
        title="Multiple Tile Layers",
        config=MapConfig(
            tile_layer=["kadaster_luchtfoto", "cartodb_positron", "kadaster_brt"],
        ),
    )
    m.add_point(Point(4.9041, 52.3676), marker="📍", tooltip="**Amsterdam**")
    m.add_layer_control(collapsed=False)

    m.to_html("multiple_tiles.html")

    print(m.to_html())  # markdown-exec: hide
    ```

    The first layer in the list is shown by default. You can also add layers after construction with
    `add_tile_layer()`:

    ```python
    m = Map(title="Multiple Tile Layers")
    m.add_tile_layer(name="esri_satellite")
    m.add_tile_layer(name="cartodb_dark")
    m.add_layer_control(collapsed=False)
    ```

## Text annotations

Sometimes you need a floating label on the map, not tied to a marker, just text at a location.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map

m = Map(title="Annotations")

m.add_text(
    point=Point(4.9041, 52.3676),
    text="Amsterdam Centrum",
    style={
        "font-size": "16px",
        "color": "black",
        "background-color": "white",
        "padding": "2px 4px",
        "border-radius": "4px",
        "border": "1px solid black",
        },
)

m.to_html("annotations.html")

print(m.to_html())  # markdown-exec: hide
```

**`add_text()`** accepts either a Shapely `Point(lon, lat)` or a plain `(lat, lon)` tuple. The `style` parameter
is a CSS dict, any CSS property is valid (`font-size`, `color`, `background-color`, `border`, `padding`, etc.).

## Site plans with icon markers

For geotechnical or infrastructure projects you often need a site plan with survey markers, borehole locations, or
measurement points.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map, MapConfig

# Example Survey data, CPT and borehole locations near Hoofddorp
surveys = [
    {"lon": 4.6820, "lat": 52.3680, "marker": "1123-25N-S13", "x_rd": 107650, "y_rd": 411350},
    {"lon": 4.6835, "lat": 52.3655, "marker": "1123-25N-S12", "x_rd": 107680, "y_rd": 411280},
    {"lon": 4.6850, "lat": 52.3630, "marker": "1123-25N-S11", "x_rd": 107710, "y_rd": 411240},
    {"lon": 4.6880, "lat": 52.3628, "marker": "1123-25N-S14", "x_rd": 107750, "y_rd": 411235},
    {"lon": 4.6837, "lat": 52.3570, "marker": "1123-25N-S01", "x_rd": 107737, "y_rd": 411210},
    {"lon": 4.6950, "lat": 52.3690, "marker": "23248_S013", "x_rd": 107850, "y_rd": 411380},
    {"lon": 4.6990, "lat": 52.3685, "marker": "23248_S019", "x_rd": 107890, "y_rd": 411370},
    {"lon": 4.6980, "lat": 52.3640, "marker": "23248_S005", "x_rd": 107880, "y_rd": 411260},
    {"lon": 4.6960, "lat": 52.3600, "marker": "23248_S011", "x_rd": 107860, "y_rd": 411180},
    {"lon": 4.6830, "lat": 52.3550, "marker": "23248_S001", "x_rd": 107730, "y_rd": 411080},
    {"lon": 4.6980, "lat": 52.3580, "marker": "23248_S018", "x_rd": 107880, "y_rd": 411140},
]

m = Map(
    title="CPT Survey Locations",
    config=MapConfig(tile_layer="openstreetmap", zoom_start=15),
)

# Add icon markers with tooltip info and text captions
for s in surveys:
    m.add_point(
        point=Point(s["lon"], s["lat"]),
        marker="fa-location-dot",
        tooltip=f'**Naam:** {s["marker"]}\n\nx [m RD] = {s["x_rd"]}\n\ny [m RD] = {s["y_rd"]}',
        marker_style={"color": "black"},
        caption=s["marker"],
    )

m.to_html("site_plan.html")

print(m.to_html())  # markdown-exec: hide

```

A few things to highlight:

**`marker`** sets the icon name, bare FontAwesome names like `"fa-location-dot"` get an `"fa-solid"` prefix
automatically.  You can also use full CSS class strings like `"fa-solid fa-location-dot"` or emoji like `"📍"`.

**`marker_style`** is a plain CSS dict.  Any CSS property works: `font-size`, `color`, `text-shadow`, etc.

**`caption`** places a text annotation just below the marker.  It works with any marker type, emojis and
icons.  By default the caption has a transparent background and no border; pass a custom `caption_style` CSS dict to
change the font size, color, or add a background.

!!! tip "Mix and match marker types"

    You can mix icon markers (for data points) and emoji markers (for landmarks) on the same map:

    ```python
    # Icon marker with a caption below
    m.add_point(pt, marker="fa-location-dot", marker_style={"color": "red"}, caption="CPT-01")

    # Emoji marker
    m.add_point(pt, marker="🏗️", caption="Site office")
    ```

## Export

### HTML (always works)

```python
m.to_html("map.html")
```

Writes a standalone HTML file. No dependencies needed to view it, just open in any browser.

Get the raw HTML string:

```python
html_string = m.to_html()
```

Open the file immediately after saving:

```python
m.to_html("map.html", open_in_browser=True)
```

### PNG image

```python
# Save to file
m.to_image("map.png", width=1600, height=1000, delay=3.0) # delay is seconds to wait for tiles to load before capture

# Or get raw bytes
png_bytes = m.to_image()

# Or get a BytesIO buffer (useful for Django/Flask/FastAPI responses)
buf = m.to_bytesio(width=1200, height=800)
```

!!! warning "External dependencies for image export"

    PNG/SVG export requires **Selenium** and **Chrome/Chromium** with **chromedriver**. The `delay` parameter (seconds)
    controls how long Map waits for tiles to load before taking the screenshot. Increase it on slow connections.

    If the delay isn't long enough, you might get a blank or partially rendered image. 
    If it's too long, it adds unnecessary wait time. Adjust based on your needs.

### SVG

Get a vector image of the map. Note that Leaflet's SVG export is actually a raster capture embedded in an SVG wrapper, 
so the output is a PNG image inside an SVG container. This means it won't scale infinitely like a true vector graphic, 
but it can be useful for certain applications.

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


## Merge maps

You can combine two `Map` instances with `+`. The left map's title and config are preserved; the right map's
geometries and layers are added on top.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point, Polygon
from blueprints.utils import Map

museums = Map(title="Combined")
museums.add_point(point=Point(4.8795, 52.3600), marker="🖼️", tooltip="**Rijksmuseum**")

parks = Map()
parks.add_polygon(
    polygon=Polygon([(4.8580, 52.3530), (4.8830, 52.3530), (4.8830, 52.3620), (4.8580, 52.3620)]),
    tooltip="**Vondelpark**",
)

# The `+` operator merges the two maps into a new one
# you can add as many maps together as you like, and the geometries/layers will all combine.
combined = museums + parks
combined.to_html("merged.html")

print(combined.to_html())  # markdown-exec: hide
```

## GeoJSON layers

You can add raw GeoJSON as a styled layer with hover tooltips, useful when you already have GeoJSON files and don't
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


## Rich popup content

By default, popups use fixed dimensions (300×150 px). For content-heavy popups like tables, images, or long text, use
`PopupStyle` to control the popup size.

```python exec="true" html="true" source="tabbed-right"
from shapely.geometry import Point
from blueprints.utils.map import Map, PopupStyle

m = Map(title="Custom Popups")

m.add_point(
    point=Point(4.9041, 52.3676),
    marker="📋",
    popup="**Amsterdam**\n\nPopulation: 872,680\nProvince: North Holland\nFounded: 1275",
    popup_style=PopupStyle(width=400, height=150),
)

m.to_html("custom.html")

print(m.to_html())  # markdown-exec: hide
```

**`PopupStyle`** has three fields: `width` (IFrame width in px), `height` (IFrame height in px), and `max_width`
(maximum popup width). All default to values matching the previous hardcoded behavior (300, 150, 300), so existing
code is unaffected.

## Raw HTML in popups

Markdown tooltips and popups are convenient, but sometimes you need full control, a styled table, an embedded image,
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
    marker="📊",
    tooltip=RawHTML("<b>Amsterdam</b><br> click for details"),
    popup=table_html,
    popup_style=PopupStyle(width=300, height=150),
)

m.to_html("custom.html")

print(m.to_html())  # markdown-exec: hide
```

**`RawHTML`** is a `str` subclass, it works anywhere a regular string does. The difference is that `Map` skips the
markdown-to-HTML conversion step, so your `<table>`, `<img>`, and `<style>` tags pass through untouched.

!!! tip

    `RawHTML` works on both `hover` (tooltip) and `popup` (click) parameters across all `add_*` methods.


## Escape hatch

Need something our Map doesn't wrap? The underlying Folium `Map` object is always accessible:

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
