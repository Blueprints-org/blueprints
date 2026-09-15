# SLS Stress/Strain Analysis

This example shows how to compute the serviceability (SLS) strains and stresses of a reinforced concrete cross-section from its section forces, using the `CrossSectionAnalysis` analyzer — including long-term effects through the creep coefficient.

Given a `ReinforcedCrossSection` and a set of `SectionForces`, Blueprints decides whether the section is uncracked or cracked and returns the matching concrete and reinforcement results. The analyzer is shape-agnostic: it works on any `ReinforcedCrossSection` (rectangular, circular, custom).

New to the axes, signs and units? See the [conventions on the guide overview](index.md#coordinate-system-signs-and-units) — in short: **tension positive, compression negative**, in kN / kNm / mm / MPa / ‰.

This page is part of the [cross-section analysis guide](index.md), together with the [ULS capacity & checks](uls.md) and [validation](validation.md) pages.

## Build the Reinforced Cross-section

We create a 300 × 600 mm beam in C30/37 with 4⌀25 B500B bars on the lower (tension) edge:

```python exec="on" source="material-block" session="rc_analysis"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=concrete)
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", material=steel)
```

Let's visualize the cross-section and its reinforcement:

```python exec="on" source="above" result="html" html="true" session="rc_analysis"
cs.plot(show=False)

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## Run the Analysis

We create the analyzer and call `stress`. Blueprints runs the cheap uncracked analysis first and, if the concrete tensile stress exceeds the flexural tensile strength, returns the cracked result instead.

Here we apply a small compression and a bending moment about the y-axis:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
analysis = CrossSectionAnalysis(cs)

forces = SectionForces(n=-100, m_y=150)  # 100 kN compression, 150 kNm about the y-axis
result = analysis.stress(forces)

print(f"Regime: {result.regime.value}")
print(f"Concrete stress (min / max): {result.concrete_stress_min:.2f} / {result.concrete_stress_max:.2f} MPa")
```

Stresses and strains follow the Blueprints convention: **compression negative, tension positive**, consistent with a positive normal force being tension.

## Inspect the Reinforcement Results

Each longitudinal bar carries its own stress, strain and force:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
for bar in result.rebar_results:
    print(
        f"bar at (x={bar.x:6.1f}, y={bar.y:6.1f}) mm  ->  "
        f"stress {bar.stress:7.1f} MPa, strain {bar.strain:6.3f} per mille, force {bar.force:6.1f} kN"
    )
```

## Cracked Section Properties

When the section cracks, the result also carries the cracked-section properties: the cracking moment, the neutral-axis depth and the cracked second moment of area.

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
if result.cracked_properties is not None:
    cracked = result.cracked_properties
    print(f"Cracking moment m_cr:    {cracked.m_cr:.1f} kNm")
    print(f"Neutral-axis depth:      {cracked.neutral_axis_depth:.1f} mm")
    print(f"Cracked second moment I: {cracked.i_cracked:.3e} mm4")
```

!!! note "Two neutral-axis depths under combined N + M"

    `cracked_properties` describes the **pure-bending** cracked section: `m_cr`, `i_cracked` and its `neutral_axis_depth` are load-independent section constants. Under a combined N + M action the **actual** neutral axis is deeper (compression) or shallower (tension) than this pure-bending value — read it from `result.strain_plane.neutral_axis_depth` (the strain plane is introduced in [The strain plane](#the-strain-plane) below). The stresses above already reflect that actual, correctly solved state. See the [validation page](validation.md#neutral-axis-actual-state-versus-pure-bending-constant) for the worked comparison.

## Force a Specific Regime

Besides the automatic decision, you can request a specific regime explicitly with the `regime` argument, for example to compare the cracked and uncracked states of the same section:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import Regime

uncracked = analysis.stress(forces, regime=Regime.SLS_UNCRACKED)
cracked = analysis.stress(forces, regime=Regime.SLS_CRACKED)

print(f"Uncracked max concrete tensile stress: {uncracked.concrete_stress_max:.2f} MPa")
print(f"Cracked max reinforcement stress:      {max(bar.stress for bar in cracked.rebar_results):.1f} MPa")
```

## Long-term Effects: Creep

Creep enters through the effective modulus `E_c,eff = E_cm / (1 + φ)`, with the creep coefficient φ as a user input. A positive φ softens the concrete, which deepens the neutral axis and sheds load to the reinforcement:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
short_term = analysis.stress(forces, regime=Regime.SLS_CRACKED)
long_term = analysis.stress(forces, regime=Regime.SLS_CRACKED, creep_coefficient=2.0)

print(f"Short-term (phi=0): steel stress {short_term.rebar_results[0].stress:6.1f} MPa")
print(f"Long-term (phi=2):  steel stress {long_term.rebar_results[0].stress:6.1f} MPa")
```

Only the effective modulus is modelled: shrinkage, the age-adjusted effective modulus (AAEM) and tension stiffening are out of scope. With the default `creep_coefficient=0.0` the analysis is short-term (secant modulus `E_cm`).

## Visualize the Strain and Stress State

`result.plot()` draws the strain (ε) and stress (σ) diagrams over the section height, in the style used by section-analysis software. It has three panels that share the height axis:

- **section** — the outline with the reinforcement; the concrete in compression (strain < 0) is hatched.
- **ε [‰]** — the linear strain profile, with the strain value at each reinforcement bar.
- **σ [MPa]** — the concrete stress block (zero in the cracked tension zone), and the reinforcement stresses on a **separate axis** (steel stresses are an order of magnitude larger than the concrete stress, so they get their own scale to stay legible).

The green dashed line marks the neutral axis. Everything is projected onto the axis perpendicular to the neutral axis, so uniaxial and biaxial-uncracked states both render upright.

```python exec="on" source="above" result="html" html="true" session="rc_analysis"
result.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

### The strain plane

Behind the figure sits the reconstructed **strain plane** — the linear strain field over the section (plane sections remain plane). It is available directly on the result and lets you query the strain anywhere:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
plane = result.strain_plane
print(f"strain at the origin:   {plane.eps_0:6.3f} per mille")
print(f"neutral-axis angle:     {plane.neutral_axis_angle:6.1f} deg")
print(f"strain at top fibre:    {plane.strain_at(0, 300):6.3f} per mille")
print(f"strain at bottom fibre: {plane.strain_at(0, -300):6.3f} per mille")
```

### Backend mesh contour

Where `result.plot()` gives the strain/stress-over-height figure, the `concreteproperties` backend can also draw a 2D **mesh stress contour** — the stress colour-mapped across the meshed cross-section. It stays available under its own name, `result.plot_mesh_stress()`, which forwards any arguments to the backend plotter:

```python exec="on" source="above" result="html" html="true" session="rc_analysis"
result.plot_mesh_stress()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## Sagging versus Hogging

The cracked behaviour depends on the direction of bending: a positive `m_y` (sagging) cracks the bottom and engages the bottom reinforcement, while a negative `m_y` (hogging) cracks the top and engages the top reinforcement. The two regimes have a different neutral-axis depth and cracked stiffness.

We build a beam with both top and bottom reinforcement and compare the two:

```python exec="on" source="material-block" result="ansi" session="rc_bending"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

steel = ReinforcementSteelMaterial()
cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", material=steel)  # bottom
cs.add_longitudinal_reinforcement_by_quantity(n=3, diameter=16, edge="upper", material=steel)  # top
analysis = CrossSectionAnalysis(cs)

sagging = analysis.stress(SectionForces(m_y=150), regime=Regime.SLS_CRACKED)
hogging = analysis.stress(SectionForces(m_y=-150), regime=Regime.SLS_CRACKED)

for label, result in [("sagging (+M)", sagging), ("hogging (-M)", hogging)]:
    properties = result.cracked_properties
    print(
        f"{label}: neutral-axis depth {properties.neutral_axis_depth:6.1f} mm, "
        f"cracking moment {properties.m_cr:5.1f} kNm, cracked I {properties.i_cracked:.3e} mm4"
    )
```

The hogging case has a shallower neutral axis and a smaller cracked second moment of area, because the top reinforcement ratio is lower than the bottom. This is visible in the two cracked strain/stress figures below — sagging first, hogging below. Note how the hatched compression zone flips from the top (sagging) to the bottom (hogging):

```python exec="on" source="above" result="html" html="true" session="rc_bending"
sagging.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

```python exec="on" source="above" result="html" html="true" session="rc_bending"
hogging.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## Biaxial Bending

Under **biaxial bending** (a moment about both axes at once) the analyzer accepts `m_y` and `m_z` together. We analyze a 400 × 400 mm column with a bar in each corner:

```python exec="on" source="material-block" result="ansi" session="rc_biaxial"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

steel = ReinforcementSteelMaterial()
cs = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
for x in (-150, 150):
    for y in (-150, 150):
        cs.add_longitudinal_rebar(Rebar(diameter=25, x=x, y=y, material=steel))

result = CrossSectionAnalysis(cs).stress(SectionForces(m_y=80, m_z=60), regime=Regime.SLS_UNCRACKED)

print(f"Concrete stress (min / max): {result.concrete_stress_min:.2f} / {result.concrete_stress_max:.2f} MPa")
for bar in result.rebar_results:
    print(f"corner ({bar.x:+.0f}, {bar.y:+.0f}) mm  ->  stress {bar.stress:+6.1f} MPa")
```

The biaxial moment tilts the stress plane diagonally: one corner reaches the largest tension and the opposite corner the largest compression. The strain/stress-over-height figure projects onto the axis perpendicular to the neutral axis, so it renders upright:

```python exec="on" source="above" result="html" html="true" session="rc_biaxial"
result.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

The tilted plane is easiest to read on the backend's 2D mesh stress contour, where the diagonal stress bands and the four corner bars are visible at once:

```python exec="on" source="above" result="html" html="true" session="rc_biaxial"
result.plot_mesh_stress()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

!!! warning "Cracked biaxial bending is not supported"

    The **uncracked** biaxial analysis above is exact (linear superposition of `m_y` and `m_z`). The **cracked** analysis, however, is uniaxial: under biaxial bending the cracked neutral axis is not perpendicular to the moment vector, which requires an iterative biaxial solution that is out of scope here. `stress` with `regime=Regime.SLS_CRACKED` — or with the default `Regime.AUTO` when the section would crack — therefore raises a `NotImplementedError` for biaxial input rather than return an unreliable result. Apply bending about a single axis for cracked analyses.

## Other Section Shapes: Circular

The same analyzer works on a circular column. Here we analyze a 500 mm diameter section with 8⌀20 bars under a normal force and bending:

```python exec="on" source="material-block" result="ansi" session="rc_circular"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.circular import CircularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

cs = CircularReinforcedCrossSection(diameter=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
cs.add_longitudinal_reinforcement_by_quantity(n=8, diameter=20, material=ReinforcementSteelMaterial())

result = CrossSectionAnalysis(cs).stress(SectionForces(n=-200, m_y=120))

print(f"Regime: {result.regime.value}")
print(f"Concrete stress (min / max): {result.concrete_stress_min:.2f} / {result.concrete_stress_max:.2f} MPa")
print(f"Max reinforcement stress:    {max(bar.stress for bar in result.rebar_results):.1f} MPa")
```

The circular section with its 8 bars, and the resulting stress state:

```python exec="on" source="above" result="html" html="true" session="rc_circular"
cs.plot(show=False)

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

```python exec="on" source="above" result="html" html="true" session="rc_circular"
result.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

On a non-rectangular shape the backend's 2D mesh stress contour is particularly telling, since it follows the curved compression zone that a height plot cannot show directly:

```python exec="on" source="above" result="html" html="true" session="rc_circular"
result.plot_mesh_stress()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```


## Complete Example

Everything above in one copy-paste-ready script:

```python
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

# 300 x 600 mm beam, C30/37, 4 diameter-25 B500B bars on the lower (tension) edge
concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)
cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=concrete)
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", material=steel)

analysis = CrossSectionAnalysis(cs)
forces = SectionForces(n=-100, m_y=150)  # 100 kN compression, 150 kNm about the y-axis

# automatic uncracked/cracked decision
result = analysis.stress(forces)
print(f"Regime: {result.regime.value}")
print(f"Concrete stress (min / max): {result.concrete_stress_min:.2f} / {result.concrete_stress_max:.2f} MPa")
for bar in result.rebar_results:
    print(f"bar at (x={bar.x:6.1f}, y={bar.y:6.1f}) mm -> stress {bar.stress:7.1f} MPa, strain {bar.strain:6.3f} per mille")

# cracked-section properties (populated when the section cracks)
if result.cracked_properties is not None:
    print(f"Cracking moment m_cr: {result.cracked_properties.m_cr:.1f} kNm")
    print(f"Neutral-axis depth:   {result.cracked_properties.neutral_axis_depth:.1f} mm")

# force a specific regime, with and without creep
uncracked = analysis.stress(forces, regime=Regime.SLS_UNCRACKED)
long_term = analysis.stress(forces, regime=Regime.SLS_CRACKED, creep_coefficient=2.0)
print(f"Uncracked max concrete tension: {uncracked.concrete_stress_max:.2f} MPa")
print(f"Long-term (phi=2) steel stress: {long_term.rebar_results[0].stress:.1f} MPa")

# query the strain plane anywhere and draw the strain/stress figure
print(f"Strain at top fibre: {result.strain_plane.strain_at(0, 300):.3f} per mille")
figure = result.plot()
figure.show()
```

## Summary

This page demonstrated the SLS stress/strain analysis of reinforced concrete cross-sections:

1. **Build** a `ReinforcedCrossSection` (rectangular, circular or custom) with materials and reinforcement
2. **Create** a `CrossSectionAnalysis` and call `stress` with `SectionForces`
3. **Let Blueprints decide** between the uncracked and cracked regime (or force one with `regime`), optionally with a creep coefficient
4. **Inspect** concrete stresses, per-bar stresses/strains/forces and cracked-section properties
5. **Visualize** the strain (ε) and stress (σ) diagrams over the section height with `result.plot()`, and query the strain field anywhere with `result.strain_plane`
6. **Compare** sagging and hogging, and analyze different section shapes with the same API

Key points:

- All results use the Blueprints convention: **compression negative, tension positive**, in MPa, per mille and kN.
- The regime decision handles combined N + M naturally: compression raises the cracking threshold, tension lowers the margin.
- Creep uses one mental model: `creep_coefficient=0.0` is short-term, a positive φ softens the concrete to `E_c,eff = E_cm / (1 + φ)`.
- Biaxial bending (`m_y` + `m_z`) is supported for the uncracked analysis; cracked biaxial bending is not supported and raises a `NotImplementedError`.
- Shear and torsion are deliberately out of scope of the stress analysis; they are handled as truss-model resistance checks (EN 1992-1-1 art. 6.2/6.3).

**Next:** compute design capacities and run unity checks on the [ULS capacity & checks](uls.md) page, or see how the results are validated on the [validation](validation.md) page.
