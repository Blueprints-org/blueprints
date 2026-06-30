# Analyze a Reinforced Cross-section (SLS strains and stresses)

This example shows how to compute the serviceability (SLS) strains and stresses of a reinforced concrete cross-section from its section forces, using the `CrossSectionAnalysis` analyzer.

Given a `ReinforcedCrossSection` and a set of `SectionForces`, Blueprints decides whether the section is uncracked or cracked and returns the matching concrete and reinforcement results.

!!! note "Optional backend required"

    The analyzer needs the optional `concreteproperties` backend. Install it with `pip install blue-prints[rc-analysis]`.

## Build the Reinforced Cross-section

We create a 300 × 500 mm beam in C30/37 with 4⌀20 B500B bars on the lower (tension) edge:

```python exec="on" source="material-block" session="rc_analysis"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=concrete)
cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, edge="lower", material=steel)
```

## Run the Analysis

We create the analyzer and call `calculate_stress`. Blueprints runs the cheap uncracked analysis first and, if the concrete tensile stress exceeds the flexural tensile strength, returns the cracked result instead.

Here we apply a small compression and a bending moment about the y-axis:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
analysis = CrossSectionAnalysis(cs)

forces = SectionForces(n=-100, m_y=150)  # 100 kN compression, 150 kNm about the y-axis
result = analysis.calculate_stress(forces)

print(f"Cracked regime: {result.is_cracked}")
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

## Force a Specific Regime

Besides the automatic decision, you can request a specific regime explicitly, for example to compare the cracked and uncracked states of the same section:

```python exec="on" source="material-block" result="ansi" session="rc_analysis"
uncracked = analysis.uncracked_stress(forces)
cracked = analysis.cracked_stress(forces)

print(f"Uncracked max concrete tensile stress: {uncracked.concrete_stress_max:.2f} MPa")
print(f"Cracked max reinforcement stress:      {max(bar.stress for bar in cracked.rebar_results):.1f} MPa")
```

## Visualize the Stress State

Finally, plot the stress state. The plot is delegated to the `concreteproperties` backend:

```python exec="on" source="above" result="html" html="true" session="rc_analysis"
result.plot()

from io import StringIO  # markdown-exec: hide
import matplotlib.pyplot as plt  # markdown-exec: hide
buffer = StringIO()  # markdown-exec: hide
plt.savefig(buffer, format="svg")  # markdown-exec: hide
print(buffer.getvalue())  # markdown-exec: hide
```

## Summary

This example demonstrated the SLS stress/strain analysis of a reinforced concrete cross-section:

1. **Build** a `ReinforcedCrossSection` with materials and reinforcement
2. **Create** a `CrossSectionAnalysis` and call `calculate_stress` with `SectionForces`
3. **Let Blueprints decide** between the uncracked and cracked regime
4. **Inspect** concrete stresses, per-bar stresses/strains/forces and cracked-section properties
5. **Force a regime** explicitly with `uncracked_stress` / `cracked_stress` when needed
6. **Visualize** the stress state

Key points:

- All results use the Blueprints convention: **compression negative, tension positive**, in MPa, per mille and kN.
- The regime decision handles combined N + M naturally: compression raises the cracking threshold, tension lowers the margin.
- Shear and torsion are deliberately out of scope of the stress analysis; they are handled as truss-model resistance checks (EN 1992-1-1 art. 6.2/6.3).
