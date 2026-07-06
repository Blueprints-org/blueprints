# Cross-section Analysis

`CrossSectionAnalysis` computes the structural response of any `ReinforcedCrossSection` (rectangular, circular, custom) directly from `SectionForces`: serviceability stresses and strains, ultimate capacities and unity checks.

The guide is split over three pages:

- **[SLS Stress/Strain Analysis](sls.md)** — uncracked/cracked concrete and reinforcement stresses and strains, with automatic regime detection, creep via the effective modulus, and IDEA-RCS-style strain/stress figures
- **[ULS Capacity & Checks](uls.md)** — bending capacity, N-M and biaxial interaction diagrams, moment-curvature, and the unity check of design actions
- **[Validation](validation.md)** — how the results are pinned down: closed-form hand-calculation anchors and the IDEA StatiCa RCS reference case

!!! note "Optional backend required"

    The analyzer needs the optional `concreteproperties` backend. Install it with `pip install blue-prints[rc-analysis]`.

## Quick Start

A complete, copy-paste-ready example: build a beam, compute the SLS stress state, the ULS bending capacity and the unity check of a design action.

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

# Visualize the SLS strain/stress state
figure = sls.plot()
figure.show()
```

Continue with the [SLS analysis](sls.md) for the full serviceability workflow, or jump to the [ULS toolbox](uls.md) for capacities and interaction diagrams. Each page ends with its own complete, copy-paste-ready example.
