# Steel U-Shaped Sheet Pile Profile

This page demonstrates how to create and visualize U-shaped sheet pile profiles using the Blueprints library. U-shaped sheet piles are interlocking structural elements used in retaining walls and cofferdams. The `PU`, `PAU`, `PAL`, `AU` and `GU` series are standardized families of U-shaped sheet piles available in Blueprints.

We will:

- Create, plot and inspect the section properties of a standard PU profile
- Combine several interlocking sheets into a wall
- Apply a corrosion allowance
- Use a standard GU sheet pile
- Define a fully custom U-shaped sheet pile from raw coordinates

## 1. Create a Standard PU Profile

The standard `PU` sheet pile profiles are available from the `standard_profiles` module. Access one of the predefined profiles as a class attribute, for example `PU18`. This returns a `SheetpileUProfile` instance representing a single sheet.

```python exec="on" source="material-block" result="ansi" session="sheetpile"
from blueprints.structural_sections.steel.standard_profiles import PU

pu_profile = PU.PU18
print(f"Profile name: {pu_profile.name}")
print(f"Web thickness: {pu_profile.web_thickness} mm")
print(f"Flange thickness: {pu_profile.flange_thickness} mm")
print(f"Interlocking distance (center-to-center): {pu_profile.interlocking_ctc} mm")
```

## 2. Plot the Single Sheet

Generate a plot of the profile using the `plot()` method to verify its geometry.

```python exec="on" source="material-block" session="sheetpile" result="html" html="true"
fig = pu_profile.plot(show=False)  # use show=True locally to open the plot directly

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## 3. Access the Section Properties

Retrieve the section properties (area, perimeter, moments of inertia, section moduli, etc.) of the single sheet using the `section_properties()` method.

```python exec="on" source="material-block" result="ansi" session="sheetpile"
properties = pu_profile.section_properties()
print(f"Area: {properties.area:.1f} mm²")
print(f"Perimeter: {properties.perimeter:.1f} mm")
print(f"Second moment of area about x-axis (ixx_c): {properties.ixx_c:.0f} mm⁴")
print(f"Section modulus (zxx_plus): {properties.zxx_plus:.0f} mm³")
```

## 4. Build a Wall from Multiple Interlocking Sheets

Sheet piles are installed side by side to form a continuous wall. Use the `multiple_sheets()` method to create a new profile made up of several interlocking sheets. Every second sheet is automatically mirrored and connected at the interlock, matching how the sheets snap together on site. At each interlock a small connector element is drawn between adjacent sheets to represent the clutch where the two sheets lock together, alternating between the top and bottom of the wall.

```python exec="on" source="material-block" session="sheetpile" result="html" html="true"
pu_wall = pu_profile.multiple_sheets(number_of_sheets=4)
fig = pu_wall.plot(show=False)

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## 5. Apply a Corrosion Allowance (optional)

Sheet piles in aggressive environments lose material over their design life. Use `with_corrosion()` to reduce the wall thickness on both faces by the given amount. The web and flange thicknesses are each reduced by twice the corrosion value (corrosion acts on both sides).

```python exec="on" source="material-block" session="sheetpile" result="html" html="true"
pu_corroded = pu_profile.with_corrosion(corrosion=1.0)
fig = pu_corroded.plot(show=False)

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## 6. Use a Standard GU Sheet Pile (optional)

The `GU` series is another standardized family of U-shaped sheet piles. Access them just like the PU profiles from the `standard_profiles` module. Each `GU` profile is a `SheetpileUProfile` and supports the same `plot()`, `section_properties()`, `multiple_sheets()` and `with_corrosion()` methods shown above.

```python exec="on" source="material-block" result="ansi" session="sheetpile"
from blueprints.structural_sections.steel.standard_profiles import GU

gu_profile = GU.GU18N
print(f"Profile name: {gu_profile.name}")
print(f"Interlocking distance (center-to-center): {gu_profile.interlocking_ctc} mm")
```

```python exec="on" source="material-block" session="sheetpile" result="html" html="true"
fig = gu_profile.plot(show=False)

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## 7. Define a Custom U-Shaped Sheet Pile (optional)

When a profile is not part of the standard database, you can build one directly from its outline coordinates using `SheetpileUProfile`. Provide the `(x, y)` coordinates of the single-sheet outline together with the web thickness, flange thickness and the center-to-center interlocking distance. The custom profile supports the same `plot()`, `section_properties()`, `multiple_sheets()` and `with_corrosion()` methods as the standard profiles.

```python exec="on" source="material-block" session="sheetpile" result="html" html="true"
from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile

custom_u_profile = SheetpileUProfile(
    coordinates=list(PU.PU18.coordinates),  # replace with your own outline
    web_thickness=9.5,  # mm
    flange_thickness=9.5,  # mm
    interlocking_ctc=630,  # mm (center-to-center distance between sheets)
    name="Custom U-Profile",
)
fig = custom_u_profile.plot(show=False)

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```
