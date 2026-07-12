# Cross-section Analysis

**Analyse a reinforced-concrete cross-section straight from its internal forces.** Give `CrossSectionAnalysis` a section (rectangular, circular or custom) and a set of `SectionForces`, and it returns the serviceability stresses and strains, the ultimate capacities, the interaction diagrams and the unity check — all in one consistent, plottable API.

!!! tip "Where should you start?"

    - **New to this?** Read the short [mental model](#the-mental-model) and [conventions](#coordinate-system-signs-and-units) below, run the [60-second quick start](#the-60-second-quick-start), then work through the [SLS](sls.md) and [ULS](uls.md) pages in order.
    - **Know what you need?** Jump straight to the [task → method map](#task-method-map) and pick the one call you're after.

## The mental model

There is one object to learn: the **analyzer**. You build it once from a cross-section, then ask it questions by passing section forces.

```text
ReinforcedCrossSection  ──►  CrossSectionAnalysis  ──►  result objects
(geometry + materials +      (the analyzer)             (stresses, capacities,
 longitudinal rebars)                                    diagrams, unity checks)
```

Every question falls into one of two limit states:

- **SLS** (serviceability) — *"what are the stresses and strains under this everyday load?"* Linear-elastic, with an automatic cracked/uncracked decision. This is the [SLS page](sls.md).
- **ULS** (ultimate) — *"how much can the section carry, and does my design action fit?"* Design materials (`f_cd`, `f_yd`), capacities, interaction diagrams and the unity check. This is the [ULS page](uls.md).

Every result object is a plain, immutable dataclass you can read fields off, and most carry a `.plot()` for a figure.

## Coordinate system, signs and units

Forces are supplied as a `SectionForces` object. The one convention to internalise: **tension is positive, compression is negative** — for the axial force, the concrete stress and the steel stress alike.

```python exec="on" result="html" html="true"
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

fig, ax = plt.subplots(figsize=(6.6, 5.4))
w, h = 300, 600
ax.add_patch(plt.Rectangle((-w / 2, -h / 2), w, h, facecolor="#efefef", edgecolor="black", lw=1.5))
xs = np.linspace(-w / 2 + 45, w / 2 - 45, 4)
ax.scatter(xs, [-h / 2 + 50] * 4, s=85, color="saddlebrown", zorder=5)
ax.annotate("", xy=(-w / 2, -h / 2 - 42), xytext=(w / 2, -h / 2 - 42), arrowprops=dict(arrowstyle="<->", color="dimgray"))
ax.text(0, -h / 2 - 60, "width 300 mm", ha="center", va="top", fontsize=9, color="dimgray")
ax.annotate("", xy=(-w / 2 - 48, -h / 2), xytext=(-w / 2 - 48, h / 2), arrowprops=dict(arrowstyle="<->", color="dimgray"))
ax.text(-w / 2 - 56, 0, "height 600 mm", ha="right", va="center", rotation=90, fontsize=9, color="dimgray")
ax.add_patch(Arc((0, h / 2 + 55), 210, 120, angle=0, theta1=210, theta2=330, color="tab:purple", lw=2.0))
ax.annotate("", xy=(103, h / 2 + 40), xytext=(96, h / 2 + 28), arrowprops=dict(arrowstyle="-|>", color="tab:purple", lw=2.0))
ax.text(0, h / 2 + 70, "+M_y : sagging", ha="center", color="tab:purple", fontsize=10)
ax.text(0, h / 2 - 35, "compression side", ha="center", color="navy", fontsize=9)
ax.text(0, -h / 2 + 95, "tension side", ha="center", color="crimson", fontsize=9)
ax.annotate("", xy=(0, -h / 2 + 58), xytext=(0, -h / 2 + 88), arrowprops=dict(arrowstyle="-|>", color="crimson", lw=1.4))
ax.text(0, -h / 2 + 20, "lower bars", ha="center", color="saddlebrown", fontsize=8.5)
ax.text(
    w / 2 + 55, h / 2,
    "sign convention\n tension  +\n compression  -\n\n+N : axial tension\n+M_y : sagging\n  (tension at bottom)\n+M_z : bends about\n  the vertical axis",
    fontsize=8.8, va="top", ha="left", family="monospace",
    bbox=dict(boxstyle="round", facecolor="white", edgecolor="lightgray"),
)
ax.set_xlim(-w / 2 - 160, w / 2 + 300)
ax.set_ylim(-h / 2 - 100, h / 2 + 110)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("The reference beam and how the section forces act", fontsize=11)
fig.tight_layout()

from io import StringIO
buffer = StringIO()
plt.savefig(buffer, format="svg")
print(buffer.getvalue())
```

The reference beam above — a 300 × 600 mm C30/37 section with four ⌀25 bars on the lower edge — is used throughout this guide, so its numbers stay comparable from page to page.

| Symbol (code field) | Meaning | Sign / unit |
|---|---|---|
| N (`n`) | axial force | tension **+**, compression **−** · kN |
| M_y (`m_y`) | bending about the y-axis — **sagging** for `+m_y` (tension at the lower edge) | kNm |
| M_z (`m_z`) | bending about the z-axis — for this beam, bending about the vertical axis (tension on one side face) | kNm |
| θ (`theta`) | neutral-axis angle in the capacity methods (see the note below) | `0` sagging · `90` about z · `180` hogging · ° |
| ε | strain | compression **−** · ‰ (per mille) |
| σ | stress (concrete and steel) | compression **−** · MPa |
| κ | curvature | 1/mm |
| φ (`creep_coefficient`) | creep coefficient (a user input) | — |
| M_Rd / M_Ed | design capacity / design action | kNm |

The display symbols above map straight to the lowercase code fields in brackets: the figure's `N`, `M_y`, `M_z` are the `n`, `m_y`, `m_z` arguments of `SectionForces`.

!!! note "What `theta` means"

    `theta` (in the capacity methods) is the **neutral-axis angle** in degrees — the orientation of the zero-strain line — not the direction of the moment vector. `theta=0` bends about the y-axis with a horizontal neutral axis: **sagging**, tension at the bottom. `theta=180` keeps that axis but flips the compression side to the top: **hogging**. `theta=90` bends about the z-axis. So you select sagging vs hogging with `0` vs `180`, not with a positive vs negative angle.

??? info "The formal axis definition (SAF member axes)"

    `SectionForces` follows the SAF member-axis system: `m_y` is the moment about the y-axis (rotation from x to z) and `m_z` the moment about the z-axis (rotation from x to y), with `n` positive in tension. For a beam drawn with its height vertical, `+m_y` puts the section into sagging (tension at the lower edge) — which is why the reference beam carries its bars on the `edge="lower"`. You never have to translate axes by hand: pass the SAF components straight to `SectionForces` and read the results back in the same convention.

## The 60-second quick start

Build the beam, then ask the analyzer three questions — an SLS stress state, a ULS bending capacity, and a unity check of a design action:

```python exec="on" source="material-block" result="ansi" session="rc_index"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

# build the section once ...
cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", material=ReinforcementSteelMaterial(ReinforcementSteelQuality.B500B))
analysis = CrossSectionAnalysis(cs)

# ... then ask it questions
forces = SectionForces(n=-100, m_y=150)  # 100 kN compression, 150 kNm sagging

sls = analysis.stress(forces)  # serviceability stress/strain (auto cracked/uncracked)
check = analysis.verify(forces)  # ultimate unity check of the same action

print(f"SLS regime:            {sls.regime.value}")
print(f"Concrete stress:       {sls.concrete_stress_min:6.2f} MPa")
print(f"Bending capacity M_Rd: {check.m_rd:6.1f} kNm")
print(f"Unity check:           {check.utilization:.2f}  ({'OK' if check.is_ok else 'NOT OK'})")
```

That is the whole loop: **build once, ask many times.** The rest of the guide is a tour of the questions you can ask.

## Task → method map

Every method below is called on the `analysis` object. The result column links the return type; most results carry a `.plot()`.

| I want to… | Call | Returns | Page |
|---|---|---|---|
| the SLS stress/strain state | `stress(forces)` | `StressStrainResult` — `.plot()`, `.plot_mesh_stress()` | [SLS](sls.md) |
| to force the cracked or uncracked regime | `stress(forces, regime=...)` | `StressStrainResult` | [SLS](sls.md#force-a-specific-regime) |
| long-term (creep) stresses | `stress(forces, creep_coefficient=...)` | `StressStrainResult` | [SLS](sls.md#long-term-effects-creep) |
| the **ULS** stress/strain state at a design action | `stress(forces, regime=Regime.ULS)` | `StressStrainResult` | [ULS](uls.md#uls-stressstrain-at-a-design-action) |
| the bending capacity `M_Rd` | `bending_capacity(n=..., theta=...)` | `UltimateCapacityResult` | [ULS](uls.md#bending-capacity) |
| the N-M diagram (one moment sense) | `interaction(theta=...)` | `MomentInteractionResult` — `.plot()` | [ULS](uls.md#n-m-interaction-diagram) |
| the **closed** N-M loop (both senses) | `interaction_envelope(axis=...)` | `MomentInteractionEnvelope` — `.plot()` | [ULS](uls.md#closed-n-m-resultant-envelope) |
| the biaxial `M_y`-`M_z` envelope at a fixed N | `biaxial_interaction(n=...)` | `BiaxialInteractionResult` — `.plot()` | [ULS](uls.md#biaxial-interaction) |
| the full 3-D surface, and any planar section of it | `interaction_surface()` → `.ring()`, `.section_*()`, `.plot_3d()` | `InteractionSurface` | [ULS](uls.md#interaction-surface-and-sections) |
| the moment-curvature response | `moment_curvature(...)` | `MomentCurvatureResult` — `.plot()` | [ULS](uls.md#moment-curvature) |
| a unity check as a **number** | `verify(forces_ed)` | `UtilizationResult` | [ULS](uls.md#unity-check) |
| a unity check as a **drawing** | `verification_diagram(forces_ed)` | `VerificationDiagram` — `.plot()` | [ULS](uls.md#verification-diagram) |

!!! tip "Rebuilding is cheap, re-asking is cheaper"

    The analyzer lazily builds and caches a backend section per configuration, so calling many methods on one `analysis` reuses that work. If you mutate the underlying cross-section, call `analysis.invalidate_cache()` to force a rebuild.

## Scope, assumptions and limitations

Read this once to know when the analyzer fits your problem:

- **SLS is linear-elastic.** Concrete is linear up to cracking at the secant modulus `E_cm`; reinforcement is elastic at `f_yk / E_s` (no partial factor). Tension stiffening is not included in the stress state (it *is* available for moment-curvature deflections).
- **ULS uses design materials.** Concrete at `f_cd` (bilinear or parabola-rectangle per the material's `diagram_type`); reinforcement at `f_yd` with the simplified horizontal branch by default (the inclined branch is opt-in). All ULS analyses are fully biaxial.
- **Creep is the effective modulus only** — `E_c,eff = E_cm / (1 + φ)`, with φ a user input. Shrinkage and the age-adjusted effective modulus are out of scope.
- **Cracked analysis is uniaxial.** Uncracked biaxial bending is exact (linear superposition); cracked *biaxial* bending raises a `NotImplementedError`. Bend about a single axis for cracked SLS.
- **Interaction-surface sections are interpolated** — a visualization tool. For a governing check, use the exact `bending_capacity` / `biaxial_interaction` routines (which is what `verify` does).
- **Shear and torsion are out of scope** of the stress analysis; they are handled as truss-model resistance checks (EN 1992-1-1 art. 6.2/6.3).
- **Backend.** Analyses run on the `concreteproperties` backend, a core Blueprints dependency.

## The pages of this guide

- **[SLS Stress/Strain Analysis](sls.md)** — uncracked/cracked concrete and reinforcement stresses and strains, automatic regime detection, creep, sagging vs hogging, biaxial and other section shapes, and the strain/stress-over-height figures.
- **[ULS Capacity & Checks](uls.md)** — bending capacity, the N-M and closed-envelope and biaxial interaction diagrams, the 3-D interaction surface and its planar sections, moment-curvature, and the unity check (as a number and as a diagram).
- **[Validation](validation.md)** — how the results are pinned down: closed-form hand calculations you can follow on paper, and a comparison against established section-analysis software on precisely defined reference cases.

## Complete example

Everything from the quick start in one copy-paste-ready script:

```python
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

# 300 x 600 mm beam, C30/37, 4 diameter-25 B500B bars on the lower (tension) edge
concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)
cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=concrete)
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", material=steel)

analysis = CrossSectionAnalysis(cs)
forces = SectionForces(n=-100, m_y=150)  # kN / kNm, tension positive

# SLS: stress/strain state (automatic uncracked/cracked decision)
sls = analysis.stress(forces)
print(f"SLS regime:            {sls.regime.value}")
print(f"Concrete stress:       {sls.concrete_stress_min:.2f} MPa")
print(f"Reinforcement stress:  {sls.rebar_results[0].stress:.1f} MPa")

# ULS: bending capacity and unity check
capacity = analysis.bending_capacity(n=forces.n)
check = analysis.verify(forces)
print(f"Bending capacity M_Rd: {capacity.m_rd:.1f} kNm")
print(f"Unity check:           {check.utilization:.2f} ({'OK' if check.is_ok else 'NOT OK'})")

# visualise the SLS strain/stress state
sls.plot().show()
```

**Ready?** Start with the [SLS analysis](sls.md), or jump to the [ULS toolbox](uls.md).
