# Cross-section Analysis

`CrossSectionAnalysis` computes the serviceability (SLS) stresses and strains of any `ReinforcedCrossSection` — rectangular, circular or custom — directly from its section forces.

![Blueprints CrossSectionAnalysis](../_images/cross_section_analysis.png)

This guide has three pages:

- **This page** — a quick start, the axes and sign conventions, and what a result contains.
- **[SLS Stress/Strain Analysis](sls.md)** — the cracked/uncracked decision, creep, sagging and hogging, biaxial bending and other section shapes.
- **[Validation](validation.md)** — hand calculations and a comparison with IDEA StatiCa RCS.

## Quick start

Build the section once, create the analyzer, and pass it a set of `SectionForces`. The example is a 300 × 600 mm C30/37 beam with 4⌀25 B500B bars on the lower edge; the same beam is used throughout this guide.

```python exec="on" source="material-block" result="ansi" session="rc_index"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)
cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=concrete)
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", cover=50, material=steel)

analysis = CrossSectionAnalysis(cs)
result = analysis.stress(SectionForces(n=-100, m_y=150))  # 100 kN compression, 150 kNm sagging

print(f"Regime:                    {result.regime.value}")
print(f"Max concrete compression:  {result.concrete_stress_min:.2f} MPa")
print(f"Max reinforcement stress:  {max(bar.stress for bar in result.rebar_results):.1f} MPa")
print(f"Neutral-axis depth:        {result.strain_plane.neutral_axis_depth:.1f} mm")
```

Blueprints decided that the section cracks under these forces and returned the cracked stress state. `result.plot()` draws it over the section height:

```python exec="on" source="above" result="html" html="true" session="rc_index"
result.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide

buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

Use `plt.show()` in a script to open the figure in a window.

The analyzer caches the meshed section, so asking it about many load cases is cheap: create it once and call `stress` for every set of forces. If you change the cross-section afterwards (for example by adding bars), call `analysis.invalidate_cache()` so the next analysis rebuilds it.

## Axes, signs and units

**Tension is positive, compression is negative** — for the axial force, the strains and the stresses alike. Forces are in kN and kNm, lengths in mm, stresses in MPa and strains in ‰ (per mille).

```python exec="on" result="html" html="true"
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5.2, 5.6))
w, h = 300, 600
ax.add_patch(plt.Rectangle((-w / 2, -h / 2), w, h, facecolor="#efefef", edgecolor="black", lw=1.5))
for x in (-105, -35, 35, 105):
    ax.add_patch(plt.Circle((x, -h / 2 + 62.5), 12.5, color="saddlebrown", zorder=5))

# member axes at the centroid: y to the right, z upwards, x out of the page
arrow = dict(arrowstyle="-|>", color="black", lw=1.6, mutation_scale=16)
ax.annotate("", xy=(110, 0), xytext=(0, 0), arrowprops=arrow)
ax.annotate("", xy=(0, 110), xytext=(0, 0), arrowprops=arrow)
ax.add_patch(plt.Circle((0, 0), 9, facecolor="white", edgecolor="black", lw=1.4, zorder=6))
ax.add_patch(plt.Circle((0, 0), 2.5, color="black", zorder=7))
ax.text(118, 0, "y", va="center", fontsize=11)
ax.text(0, 122, "z", ha="center", fontsize=11)
ax.text(-14, -14, "x", ha="right", va="top", fontsize=11)

# faces in tension under positive moments
ax.plot([-w / 2, w / 2], [-h / 2 - 6, -h / 2 - 6], color="crimson", lw=4)
ax.text(0, -h / 2 - 22, "tension face under +M_y (sagging)", ha="center", va="top", color="crimson", fontsize=9.5)
ax.plot([w / 2 + 6, w / 2 + 6], [-h / 2, h / 2], color="tab:purple", lw=4)
ax.text(w / 2 + 18, h / 4, "tension face\nunder +M_z", va="center", color="tab:purple", fontsize=9.5)

ax.set_xlim(-w / 2 - 40, w / 2 + 130)
ax.set_ylim(-h / 2 - 70, h / 2 + 30)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()

from io import StringIO

buffer = StringIO()
plt.savefig(buffer, format="svg")
print(buffer.getvalue())
```

The forces follow the member axes of the SAF format: `x` along the member, `y` horizontal and `z` vertical in the cross-section. The axial force acts at the centroid of the concrete outline (mid-height for a rectangle), and the moments are taken about that point. Results that describe a *position* in the cross-section — `Rebar.x` / `Rebar.y`, the bar positions in the results and `strain_plane.strain_at(x, y)` — use the coordinates of the section drawing instead, which lie along the same lines:

| Member axis (forces) | Section coordinate (positions) | In the figure |
|---|---|---|
| `y` | `x` | horizontal, positive to the right |
| `z` | `y` | vertical, positive upwards |

| Quantity | Code | Unit | Positive means |
|---|---|---|---|
| Axial force N | `SectionForces.n` | kN | tension |
| Bending moment M_y | `SectionForces.m_y` | kNm | sagging: tension at the lower face |
| Bending moment M_z | `SectionForces.m_z` | kNm | tension at the right face (positive section `x`) |
| Strain ε | `strain`, `strain_at(x, y)` | ‰ | elongation (tension) |
| Stress σ | `stress`, `concrete_stress_min/max` | MPa | tension |
| Curvature κ | `strain_plane.kappa_y`, `kappa_z` | 1/mm | — |
| Neutral-axis angle | `neutral_axis_angle` | ° | counter-clockwise from the horizontal; `0` for bending about `y` |
| Creep coefficient φ | `creep_coefficient` (input) | — | — |

`SectionForces` also accepts the shear forces `v_y`, `v_z` and the torsional moment `t`, so a complete SAF result can be passed in one go — for example with `SectionForces.from_saf_result(...)`. The stress analysis uses `n`, `m_y` and `m_z` only.

## What a result contains

`stress()` returns a [`StressStrainResult`][structural_sections.concrete.reinforced_concrete_sections.analysis.results.StressStrainResult], a frozen dataclass:

| Field | Contents |
|---|---|
| `regime`, `is_cracked` | Which regime produced the result: `Regime.SLS_UNCRACKED` or `Regime.SLS_CRACKED`. |
| `concrete_stress_min` | The largest concrete **compression** (the most negative stress) [MPa]. |
| `concrete_stress_max` | The largest concrete **tension** [MPa]; `0` in the cracked regime, where concrete carries no tension. |
| `rebar_results` | One [`RebarStressResult`][structural_sections.concrete.reinforced_concrete_sections.analysis.results.RebarStressResult] per bar: position `x`, `y`, `diameter`, `stress` [MPa], `strain` [‰] and `force` [kN]. |
| `strain_plane` | The linear strain field: a [`StrainPlane`][structural_sections.concrete.reinforced_concrete_sections.analysis.results.StrainPlane] with the strain at the origin, the curvatures, the **actual** neutral-axis depth and angle, and `strain_at(x, y)`. |
| `cracked_properties` | For a cracked result, [`CrackedProperties`][structural_sections.concrete.reinforced_concrete_sections.analysis.results.CrackedProperties]: cracking moment `m_cr`, cracked second moment of area `i_cracked`, and the pure-bending neutral-axis depth and angle. `None` for an uncracked result. |
| `elastic_modulus` | The concrete modulus used: `E_cm`, or `E_c,eff` with creep [MPa]. |
| `forces` | The `SectionForces` that were analysed. |
| `raw` | The backend's own result object, for advanced use (in the backend's sign convention). |

Two methods draw it: `plot()` gives the strain and stress over the section height, and `plot_mesh_stress()` the stress as a colour map over the meshed section.

## Scope and assumptions

- **Linear-elastic.** Concrete is linear with the secant modulus `E_cm` (EN 1992-1-1 table 3.1); reinforcement is elastic with `E_s` up to `f_yk`. There are no partial factors.
- **Cracked or uncracked.** The section counts as cracked when the uncracked concrete tensile stress exceeds the flexural tensile strength `f_ctm,fl` (EN 1992-1-1 formula 3.23). A cracked section carries no concrete tension. See [the cracking criterion](sls.md#2-cracked-or-uncracked).
- **Creep** through the effective modulus `E_c,eff = E_cm / (1 + φ)` (EN 1992-1-1 formula 7.20), with the creep coefficient φ as an input. Shrinkage, the age-adjusted effective modulus and tension stiffening are not included.
- **Biaxial bending** is supported in the uncracked regime. A cracked analysis under biaxial bending raises a `NotImplementedError`.
- **Shear and torsion** are not part of a strain-plane analysis; `v_y`, `v_z` and `t` are ignored.
- **Backend.** The section is meshed and analysed by [`concreteproperties`](https://robbievanleeuwen.github.io/concrete-properties/), a core Blueprints dependency. Every input and result is converted to the Blueprints conventions above.
