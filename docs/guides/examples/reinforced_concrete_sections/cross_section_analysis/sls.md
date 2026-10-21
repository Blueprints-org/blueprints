# SLS Stress/Strain Analysis

This page shows how to compute the serviceability (SLS) stresses and strains of a reinforced concrete cross-section from its section forces with `CrossSectionAnalysis`. Blueprints decides whether the section is cracked and returns the matching concrete and reinforcement results.

The section forces and their signs are explained on the [guide overview](index.md#axes-signs-and-units): **tension positive, compression negative**, in kN, kNm, mm, MPa and ‰.

We will:

- Build a reinforced cross-section and analyse it
- See how Blueprints decides between the cracked and uncracked state
- Read the concrete, reinforcement and neutral-axis results
- Draw the strain and stress state
- Include creep through the effective modulus
- Compare sagging and hogging, and analyse biaxial bending and a circular section

## Assumptions

- **Linear-elastic.** Concrete is linear with the secant modulus `E_cm` (EN 1992-1-1 table 3.1); reinforcement is elastic with `E_s` up to `f_yk`. There are no partial factors.
- **Cracked or uncracked.** The section counts as cracked when the uncracked concrete tensile stress exceeds the flexural tensile strength `f_ctm,fl` (EN 1992-1-1 formula 3.23). A cracked section carries no concrete tension. See [section 2](#2-cracked-or-uncracked).
- **Creep** through the effective modulus `E_c,eff = E_cm / (1 + φ)` (EN 1992-1-1 formula 7.20), with the creep coefficient φ as an input. Shrinkage, the age-adjusted effective modulus and tension stiffening are not included.
- **Biaxial bending** is supported in the uncracked regime. A cracked analysis under biaxial bending raises a `NotImplementedError`.

## 1. Build the Cross-section

A 300 × 600 mm beam in C30/37 with 4⌀25 B500B bars on the lower edge, 50 mm cover:

```python exec="on" source="material-block" session="rc_analysis"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=concrete)
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", cover=50, material=steel)
```

```python exec="on" source="above" result="html" html="true" session="rc_analysis"
cs.plot(show=False)

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide

buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## 2. Cracked or Uncracked

`stress()` first analyses the uncracked section. If the largest concrete tensile stress exceeds the flexural tensile strength `f_ctm,fl` (EN 1992-1-1 formula 3.23), the section is cracked and the cracked analysis is returned instead.

For this beam under 100 kN compression and 150 kNm sagging:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_23 import Form3Dot23FlexuralTensileStrength

analysis = CrossSectionAnalysis(cs)
forces = SectionForces(n=-100, m_y=150)

f_ctm_fl = Form3Dot23FlexuralTensileStrength(h=600, f_ctm=concrete.f_ctm)
uncracked = analysis.stress(forces, regime=Regime.SLS_UNCRACKED)

print(f"f_ctm:                           {concrete.f_ctm:.2f} MPa")
print(f"f_ctm,fl:                        {f_ctm_fl:.2f} MPa")
print(f"Uncracked concrete tension:      {uncracked.concrete_stress_max:.2f} MPa")

result = analysis.stress(forces)  # the default, Regime.AUTO
print(f"Regime chosen by Blueprints:     {result.regime.value}")
```

The uncracked tension of 6.74 MPa is well above `f_ctm,fl`, so the result is cracked. A compressive axial force lowers the tensile stress and therefore delays cracking; a tensile one does the opposite.

`f_ctm,fl = max((1.6 − h/1000)·f_ctm, f_ctm)` depends on the section height: for this 600 mm beam it equals `f_ctm`, while thinner members get a higher threshold.

As shown above, the `regime` argument forces a specific regime: `Regime.SLS_UNCRACKED` or `Regime.SLS_CRACKED`. That is useful to compare the two states, or to apply your own cracking criterion.

!!! note "`f_ctm` or `f_ctm,fl`?"

    EN 1992-1-1 art. 7.1(2) allows the tensile strength for an uncracked-section check to be taken as `f_ctm` or `f_ctm,fl`, provided the minimum tension reinforcement is calculated with the same value; crack widths are calculated with `f_ctm`. Blueprints uses `f_ctm,fl`. To work with `f_ctm` instead, compare `uncracked.concrete_stress_max` with `concrete.f_ctm` yourself and force the regime accordingly.

## 3. Concrete and Reinforcement Results

`stress()` returns a [`StressStrainResult`][structural_sections.concrete.reinforced_concrete_sections.analysis.results.StressStrainResult], a frozen dataclass:

| Field | Contents |
|---|---|
| `regime`, `is_cracked` | Which regime produced the result: `Regime.SLS_UNCRACKED` or `Regime.SLS_CRACKED`. |
| `concrete_stress_min` | The largest concrete **compression** (the most negative stress) [MPa]. |
| `concrete_stress_max` | The largest concrete **tension** [MPa]; `0` in the cracked regime, where concrete carries no tension. |
| `rebar_results` | One [`RebarStressResult`][structural_sections.concrete.reinforced_concrete_sections.analysis.results.RebarStressResult] per bar: position `x`, `y` [mm], `diameter` [mm], `stress` [MPa], `strain` [‰] and `force` [kN]. |
| `strain_plane` | The linear strain field: a [`StrainPlane`][structural_sections.concrete.reinforced_concrete_sections.analysis.results.StrainPlane] with the strain at the origin [‰], the curvatures `kappa_y` and `kappa_z` [1/mm], the **actual** neutral-axis depth [mm] and angle [°], and `strain_at(x, y)`. |
| `cracked_properties` | For a cracked result, [`CrackedProperties`][structural_sections.concrete.reinforced_concrete_sections.analysis.results.CrackedProperties]: cracking moment `m_cr` [kNm], cracked second moment of area `i_cracked` [mm⁴], and the pure-bending neutral-axis depth [mm] and angle [°]. `None` for an uncracked result. |
| `elastic_modulus` | The concrete modulus used: `E_cm`, or `E_c,eff` with creep [MPa]. |
| `forces` | The `SectionForces` that were analysed. |
| `raw` | The backend's own result object, for advanced use (in the backend's sign convention). |

Stresses and strains are positive in tension. Positions — the bar `x` and `y` and the arguments of `strain_at(x, y)` — are coordinates of the section drawing (`cs.plot()`): section `x` runs along the member `y` axis and section `y` along the member `z` axis. Neutral-axis angles are measured counter-clockwise from the horizontal; `0` means bending about `y`.

The cracked result carries the largest concrete compression and, per bar, the stress, strain and force:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
print(f"Max concrete compression: {result.concrete_stress_min:.2f} MPa")
for bar in result.rebar_results:
    print(f"bar at (x={bar.x:6.1f}, y={bar.y:6.1f}) mm: stress {bar.stress:6.1f} MPa, strain {bar.strain:.3f} per mille, force {bar.force:5.1f} kN")
```

Behind these values sits the **strain plane**: the linear strain field over the section (plane sections remain plane). It gives the strain at any point:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
plane = result.strain_plane
print(f"strain at the top fibre:    {plane.strain_at(0, 300):6.3f} per mille")
print(f"strain at the bottom fibre: {plane.strain_at(0, -300):6.3f} per mille")
```

## 4. Neutral Axis and Cracked-section Properties

A cracked result has two neutral-axis depths, and under combined N + M they differ:

- `result.strain_plane.neutral_axis_depth` — the **actual** neutral axis under the applied forces. This is the depth of the compression zone in the stress state above.
- `result.cracked_properties.neutral_axis_depth` — the neutral axis of the cracked section under **pure bending**. Together with the cracking moment `m_cr` and the cracked second moment of area `i_cracked`, it is a property of the section and does not depend on the forces.

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
cracked = result.cracked_properties
print(f"Actual neutral-axis depth (N + M):      {result.strain_plane.neutral_axis_depth:.1f} mm")
print(f"Pure-bending neutral-axis depth:        {cracked.neutral_axis_depth:.1f} mm")
print(f"Cracking moment m_cr:                   {cracked.m_cr:.1f} kNm")
print(f"Cracked second moment of area i_cracked: {cracked.i_cracked:.3e} mm4")
```

The 100 kN compression pushes the neutral axis down from 170.8 to 193.9 mm. Under pure bending the two depths are equal. For an uncracked result `cracked_properties` is `None`.

## 5. Visualize the Strain and Stress State

`result.plot()` draws the state over the section height in three panels:

- **section** — the outline with the reinforcement; the concrete in compression is hatched and, for bending about a single axis, the depth `x` of the compression zone is dimensioned.
- **ε [‰]** — the linear strain profile, with the strain at each bar.
- **σ [MPa]** — the concrete stress (zero in the cracked tension zone), with the reinforcement stresses on a separate axis because they are an order of magnitude larger.

The dashed line is the neutral axis.

```python exec="on" source="above" result="html" html="true" session="rc_analysis"
result.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide

buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

`result.plot_mesh_stress()` shows the stress as a colour map over the meshed cross-section, in the same sign convention (compression negative). Red marks tension, in the concrete and in the reinforcement:

```python exec="on" source="above" result="html" html="true" session="rc_analysis"
result.plot_mesh_stress()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide

buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## 6. Long-term Effects: Creep

Creep enters through the effective modulus of EN 1992-1-1 formula 7.20, `E_c,eff = E_cm / (1 + φ)`. The creep coefficient φ is an input, for example from EN 1992-1-1 figure 3.1 or annex B. The softer concrete deepens the neutral axis and sheds load to the reinforcement:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
short_term = analysis.stress(forces)
long_term = analysis.stress(forces, creep_coefficient=2.0)

for label, state in [("short-term (phi = 0)", short_term), ("long-term  (phi = 2)", long_term)]:
    print(
        f"{label}: E = {state.elastic_modulus:7.0f} MPa, neutral axis {state.strain_plane.neutral_axis_depth:5.1f} mm, "
        f"steel stress {max(bar.stress for bar in state.rebar_results):5.1f} MPa"
    )
```

The default `creep_coefficient=0.0` is the short-term analysis with `E_cm`. The cracking threshold `f_ctm,fl` is not affected by creep.

## 7. Sagging versus Hogging

The direction of bending decides which side cracks: a positive `m_y` (sagging) cracks the bottom and engages the bottom bars, a negative `m_y` (hogging) cracks the top and engages the top bars. We add three ⌀16 bars at the top and compare:

```python exec="on" source="material-block" result="ansi" session="rc_bending"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

steel = ReinforcementSteelMaterial()  # B500B
cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", cover=50, material=steel)
cs.add_longitudinal_reinforcement_by_quantity(n=3, diameter=16, edge="upper", cover=50, material=steel)
analysis = CrossSectionAnalysis(cs)

sagging = analysis.stress(SectionForces(m_y=150), regime=Regime.SLS_CRACKED)
hogging = analysis.stress(SectionForces(m_y=-150), regime=Regime.SLS_CRACKED)

for label, result in [("sagging (+M)", sagging), ("hogging (-M)", hogging)]:
    properties = result.cracked_properties
    print(
        f"{label}: neutral-axis depth {properties.neutral_axis_depth:5.1f} mm, "
        f"m_cr {properties.m_cr:4.1f} kNm, i_cracked {properties.i_cracked:.3e} mm4"
    )
```

The top reinforcement is lighter than the bottom reinforcement, so the hogging state has a shallower neutral axis and a smaller cracked second moment of area. The hatched compression zone moves from the top (sagging, first figure) to the bottom (hogging, second figure):

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

## 8. Biaxial Bending

`m_y` and `m_z` can act together. A 400 × 400 mm column with a ⌀25 bar in each corner, under moments small enough to stay uncracked:

```python exec="on" source="material-block" result="ansi" session="rc_biaxial"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

steel = ReinforcementSteelMaterial()
cs = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
for x in (-150, 150):
    for y in (-150, 150):
        cs.add_longitudinal_rebar(Rebar(diameter=25, x=x, y=y, material=steel))

result = CrossSectionAnalysis(cs).stress(SectionForces(m_y=20, m_z=15))

print(f"Regime: {result.regime.value}")
print(f"Concrete stress (min / max): {result.concrete_stress_min:.2f} / {result.concrete_stress_max:.2f} MPa")
print(f"Neutral-axis angle: {result.strain_plane.neutral_axis_angle:.1f} deg")
for bar in result.rebar_results:
    print(f"corner ({bar.x:+.0f}, {bar.y:+.0f}) mm: stress {bar.stress:+5.1f} MPa")
```

The two moments tilt the neutral axis: the bottom-left corner (tension from both `+m_y` and `+m_z`) carries the largest tension, the top-right corner the largest compression. `result.plot()` projects the state onto the direction perpendicular to the neutral axis, so the section is drawn rotated:

```python exec="on" source="above" result="html" html="true" session="rc_biaxial"
result.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide

buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

The mesh colour map shows the tilted stress field in the section's own orientation:

```python exec="on" source="above" result="html" html="true" session="rc_biaxial"
result.plot_mesh_stress()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide

buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

!!! warning "Cracked biaxial bending is not supported"

    Under biaxial bending the cracked neutral axis is generally not perpendicular to the moment vector; finding it requires an iterative biaxial solution that is not implemented. A cracked analysis under biaxial bending — forced with `Regime.SLS_CRACKED`, or reached with the default `Regime.AUTO` because the section cracks — therefore raises a `NotImplementedError` instead of returning an unreliable result. Larger moments on this column, such as `m_y=80, m_z=60`, crack it and raise this error.

## 9. Circular Section

The analyzer works on any `ReinforcedCrossSection`. A 500 mm diameter column with 8⌀20 bars under a normal force and bending:

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
print(f"Max concrete compression: {result.concrete_stress_min:.2f} MPa")
print(f"Max reinforcement stress: {max(bar.stress for bar in result.rebar_results):.1f} MPa")
```

```python exec="on" source="above" result="html" html="true" session="rc_circular"
result.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide

buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

On a curved section the mesh colour map shows the shape of the compression zone, which the height plot cannot:

```python exec="on" source="above" result="html" html="true" session="rc_circular"
result.plot_mesh_stress()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide

buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

The results on this page are checked against hand calculations and IDEA StatiCa RCS on the [validation](validation.md) page.
