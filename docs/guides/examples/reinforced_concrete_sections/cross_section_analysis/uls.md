# ULS Capacity & Checks

This example shows the ultimate limit state (ULS) toolbox of the `CrossSectionAnalysis` analyzer: the bending capacity, the N-M and biaxial interaction diagrams, the moment-curvature response and the unity check of a design action.

All ULS analyses use the design materials — concrete at `f_cd` and reinforcement at `f_yd` — and are fully biaxial.

This page is part of the [cross-section analysis guide](index.md), together with the [SLS stress/strain analysis](sls.md) and [validation](validation.md) pages.

## Build the Reinforced Cross-section

We reuse the reference beam of the SLS page: 300 × 600 mm in C30/37 with 4⌀25 B500B bars on the lower (tension) edge:

```python exec="on" source="material-block" session="rc_uls"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", material=ReinforcementSteelMaterial())
analysis = CrossSectionAnalysis(cs)
```

## Bending Capacity

`bending_capacity` computes the ultimate (ULS) bending capacity with the design materials: concrete at `f_cd` (bilinear or parabola-rectangle, per the material's `diagram_type`) and reinforcement at `f_yd`. The strain plane pivots on the concrete crushing strain `ε_cu3` and the neutral axis is iterated until the internal axial force balances `n`:

```python exec="on" source="material-block" result="ansi" session="rc_uls"
sagging = analysis.bending_capacity()  # theta=0: tension at the bottom
hogging = analysis.bending_capacity(theta=180)  # tension at the top
with_compression = analysis.bending_capacity(n=-500)  # capacity at N_Ed = -500 kN

print(f"Sagging capacity M_Rd:          {sagging.m_rd:6.1f} kNm  (neutral axis at {sagging.neutral_axis_depth:.0f} mm)")
print(f"Hogging capacity M_Rd:          {hogging.m_rd:6.1f} kNm")
print(f"Capacity at N = -500 kN:        {with_compression.m_rd:6.1f} kNm")
```

The hogging capacity is smaller because this beam only has bottom reinforcement. A moderate compression raises the capacity of an under-reinforced section (N-M interaction).

The reinforcement design diagram defaults to the simplified **horizontal branch** at `f_yd` (EN 1992-1-1 art. 3.2.7(2)(b), no strain limit). The **inclined branch** — rising towards `k·f_yd` with the strain limit `ε_ud = 0.9·ε_uk` — is available on the analyzer:

```python exec="on" source="material-block" result="ansi" session="rc_uls"
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import SteelBranch

inclined = CrossSectionAnalysis(cs, steel_branch=SteelBranch.INCLINED).bending_capacity()
print(f"Inclined-branch capacity M_Rd:  {inclined.m_rd:6.1f} kNm  (+{(inclined.m_rd / sagging.m_rd - 1) * 100:.1f}%)")
```

## N-M Interaction Diagram

`interaction` traces the uniaxial N-M interaction diagram from the pure-compression (squash) point to the zero-curvature tension point, including the balanced and pure-bending control points:

```python exec="on" source="material-block" result="ansi" session="rc_uls"
diagram = analysis.interaction()

forces = [point.n for point in diagram.points]
print(f"Squash load N_Rd:    {min(forces):7.0f} kN")
print(f"Tension capacity:    {max(forces):7.0f} kN")
print(f"Number of points:    {len(diagram.points)}")
```

```python exec="on" source="above" result="html" html="true" session="rc_uls"
diagram.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## Biaxial Interaction

For a column under bending about both axes, `biaxial_interaction` traverses the neutral-axis angle over a full revolution and returns the M_y-M_z capacity envelope at a fixed axial force:

```python exec="on" source="material-block" result="ansi" session="rc_biaxial_uls"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

column = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
for x in (-150, 150):
    for y in (-150, 150):
        column.add_longitudinal_rebar(Rebar(diameter=25, x=x, y=y, material=ReinforcementSteelMaterial()))
column_analysis = CrossSectionAnalysis(column)

envelope = column_analysis.biaxial_interaction(n=-800, n_points=16)
print(f"Max M_y capacity at N = -800 kN: {max(point.m_y for point in envelope.points):6.1f} kNm")
print(f"Diagonal capacity (m_y = m_z):   {envelope.capacity_along(1, 1):6.1f} kNm")
```

```python exec="on" source="above" result="html" html="true" session="rc_biaxial_uls"
envelope.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

The envelope cost grows linearly with `n_points`; `capacity_along` intersects the envelope along any load direction.

## Moment-Curvature

`moment_curvature` traces the full M-κ response with the design material set: concrete bilinear-horizontal at `f_cd` with a tension branch up to `f_ctm,fl` (producing the cracking kink), reinforcement at `f_yd`. The trace ends at material failure, so the peak reproduces the ultimate capacity. The `creep_coefficient` follows the same mental model as `stress`: `0.0` is short-term (`E_cm`), a positive φ softens the elastic branch to `E_c,eff`:

```python exec="on" source="material-block" result="ansi" session="rc_uls"
short_term = analysis.moment_curvature()
long_term = analysis.moment_curvature(creep_coefficient=2.0)

print(f"Ultimate moment (short-term): {short_term.m_ultimate:6.1f} kNm")
print(f"Ultimate moment (phi = 2):    {long_term.m_ultimate:6.1f} kNm")
print(f"Bending capacity M_Rd:        {sagging.m_rd:6.1f} kNm  (the M-K peak matches)")
```

```python exec="on" source="above" result="html" html="true" session="rc_uls"
short_term.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

Creep barely changes the ultimate moment (strength is material-driven) but visibly softens the pre-yield branches — the long-term curve reaches the same moment at a larger curvature.

By default the curve is the bare section response. Passing `tension_stiffening=True` returns the **mean** curvature of EN 1992-1-1 art. 7.4.3 instead — the concrete between cracks keeps carrying tension, stiffening the cracked branch (the curve used for deflections). The distribution factor β is chosen automatically (1.0 short-term, 0.5 when creep marks a sustained load), and the result's `tension_stiffening` flag records that the interpolation was applied. See the [validation page](validation.md#moment-curvature-m-n-) for the comparison against IDEA StatiCa RCS.

```python exec="on" source="material-block" result="ansi" session="rc_uls"
mean = analysis.moment_curvature(tension_stiffening=True)
index = min(range(len(short_term.m)), key=lambda i: abs(short_term.m[i] - 150))
print(f"at M = {short_term.m[index]:.0f} kNm  ->  bare {short_term.kappa[index] * 1000:.5f} 1/m, mean {mean.kappa[index] * 1000:.5f} 1/m")
```

## ULS Stress/Strain at a Design Action

`stress` with `regime=Regime.ULS` returns the ultimate stress/strain state belonging to a design action: the bending direction follows from the moment vector, the strain plane pivots on the concrete crushing strain, and the reported stresses are the design stress blocks of that failure state (at `M_Rd`):

```python exec="on" source="material-block" result="ansi" session="rc_uls"
uls_state = analysis.stress(SectionForces(n=-100, m_y=150), regime=Regime.ULS)

print(f"Regime:                   {uls_state.regime.value}")
print(f"Concrete stress at pivot: {uls_state.concrete_stress_min:.1f} MPa  (= -f_cd)")
print(f"Steel stress:             {uls_state.rebar_results[0].stress:.1f} MPa  (= f_yd)")
print(f"Strain at top fibre:      {uls_state.strain_plane.strain_at(0, 300):.2f} per mille  (= -eps_cu3)")
```

```python exec="on" source="above" result="html" html="true" session="rc_uls"
uls_state.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## Unity Check

`verify` runs the ULS unity check of a design action against the design capacity. It picks its route automatically: pure axial actions are checked against the squash or tensile capacity, uniaxial moments against the bending capacity at the design axial force, and biaxial moment pairs against the biaxial envelope along the load direction:

```python exec="on" source="material-block" result="ansi" session="rc_uls"
check = analysis.verify(SectionForces(n=-200, m_y=150))

print(f"Governing check: {check.governing}")
print(f"M_Ed = {check.m_ed:.0f} kNm, M_Rd = {check.m_rd:.0f} kNm")
print(f"Utilization:     {check.utilization:.2f}  ({'OK' if check.is_ok else 'NOT OK'})")
```

A biaxial design action on the column automatically routes through the biaxial envelope:

```python exec="on" source="material-block" result="ansi" session="rc_biaxial_uls"
biaxial_check = column_analysis.verify(SectionForces(n=-800, m_y=120, m_z=90), n_points=16)

print(f"Governing check: {biaxial_check.governing}")
print(f"M_Ed = {biaxial_check.m_ed:.0f} kNm, M_Rd = {biaxial_check.m_rd:.0f} kNm")
print(f"Utilization:     {biaxial_check.utilization:.2f}  ({'OK' if biaxial_check.is_ok else 'NOT OK'})")
```

!!! info "Modelling assumptions (ULS and creep)"

    - **Reinforcement at ULS**: the simplified horizontal branch at `f_yd` without a strain limit is the default (EN 1992-1-1 art. 3.2.7(2)(b)); the inclined branch with `ε_ud = 0.9·ε_uk` is available via `steel_branch=SteelBranch.INCLINED`.
    - **Concrete at ULS**: the design diagram follows the material's `diagram_type` (bilinear default, parabola-rectangle via `DiagramType.PARABOLIC`), always at `f_cd`.
    - **Moment-curvature** uses a bilinear-horizontal concrete curve at `f_cd` (the diagram IDEA StatiCa RCS uses for its N-M-κ stiffness points) with a near-brittle tension branch up to `f_ctm,fl`.
    - **Creep** is modelled through the effective modulus `E_c,eff = E_cm / (1 + φ)` only, with φ as user input: shrinkage, the age-adjusted effective modulus (AAEM) and tension stiffening are out of scope.
    - **Cracked biaxial SLS** analysis remains unsupported (see the SLS page); the ULS analyses are fully biaxial.

## Complete Example

Everything above in one copy-paste-ready script:

```python
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime, SteelBranch
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

# 300 x 600 mm beam, C30/37, 4 diameter-25 B500B bars on the lower (tension) edge
concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)
steel = ReinforcementSteelMaterial()
cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=concrete)
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", material=steel)
analysis = CrossSectionAnalysis(cs)  # steel_branch=SteelBranch.INCLINED for the inclined design diagram

# bending capacity: sagging, hogging and at a design axial force
sagging = analysis.bending_capacity()
hogging = analysis.bending_capacity(theta=180)
print(f"Sagging M_Rd: {sagging.m_rd:.1f} kNm (neutral axis at {sagging.neutral_axis_depth:.0f} mm)")
print(f"Hogging M_Rd: {hogging.m_rd:.1f} kNm")

# uniaxial N-M interaction diagram
diagram = analysis.interaction()
print(f"Squash load: {min(point.n for point in diagram.points):.0f} kN")
diagram.plot().show()

# moment-curvature, short-term and long-term
curve = analysis.moment_curvature()
long_term = analysis.moment_curvature(creep_coefficient=2.0)
print(f"Ultimate moment M_u: {curve.m_ultimate:.1f} kNm")
curve.plot().show()

# ULS stress/strain state of a design action
uls_state = analysis.stress(SectionForces(n=-100, m_y=150), regime=Regime.ULS)
print(f"Concrete stress at pivot: {uls_state.concrete_stress_min:.1f} MPa (= -f_cd)")
uls_state.plot().show()

# unity check of a design action (automatic axial / uniaxial / biaxial routing)
check = analysis.verify(SectionForces(n=-200, m_y=150))
print(f"Unity check: {check.utilization:.2f} ({'OK' if check.is_ok else 'NOT OK'}), governing: {check.governing}")

# biaxial: a 400 x 400 mm column with a corner bar layout
column = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=concrete)
for x in (-150, 150):
    for y in (-150, 150):
        column.add_longitudinal_rebar(Rebar(diameter=25, x=x, y=y, material=steel))
column_analysis = CrossSectionAnalysis(column)

envelope = column_analysis.biaxial_interaction(n=-800, n_points=16)
envelope.plot().show()
biaxial_check = column_analysis.verify(SectionForces(n=-800, m_y=120, m_z=90), n_points=16)
print(f"Biaxial unity check: {biaxial_check.utilization:.2f} ({'OK' if biaxial_check.is_ok else 'NOT OK'})")
```

## Summary

This page demonstrated the ULS toolbox of `CrossSectionAnalysis`:

1. **Compute** the bending capacity with `bending_capacity` — sagging, hogging, about either axis, at any axial force
2. **Trace** the uniaxial N-M `interaction` diagram and the `biaxial_interaction` M_y-M_z envelope
3. **Follow** the full `moment_curvature` response, short-term or long-term via the creep coefficient
4. **Inspect** the ultimate stress/strain state of a design action with `stress(..., regime=Regime.ULS)`
5. **Check** a design action with `verify` (automatic axial / uniaxial / biaxial routing)

**Next:** see how these results are pinned to hand calculations and reference software on the [validation](validation.md) page.
