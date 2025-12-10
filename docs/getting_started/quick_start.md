# Quick Start

This guide will help you get started with Blueprints quickly by walking through common use cases.

!!! tip "Before You Begin"
    Make sure you have Blueprints installed. If not, see the [Installation Guide](installation.md).

## Your First Calculation

Let's start with a simple concrete material calculation:

```python exec="on" source="material-block" result="ansi" session="quickstart"
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass

# Create a C30/37 concrete material
concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)

# Access material properties
print(f"Concrete: {concrete.name}")
print(f"Characteristic strength (fck): {concrete.f_ck} MPa")
print(f"Design strength (fcd): {concrete.f_cd} MPa")
print(f"Mean tensile strength (fctm): {concrete.f_ctm:.2f} MPa")
```

That's it! You've just calculated key concrete properties according to Eurocode standards.

## Working with Reinforcement Steel

Now let's add reinforcement steel to the mix:

```python exec="on" source="material-block" result="ansi" session="quickstart"
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality

# Create B500B reinforcement steel
rebar = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

print(f"Steel quality: {rebar.name}")
print(f"Characteristic yield strength (fyk): {rebar.f_yk} MPa")
print(f"Design yield strength (fyd): {rebar.f_yd:.2f} MPa")
print(f"Modulus of elasticity (Es): {rebar.e_s} MPa")
```

## Working with Formulas

Blueprints organizes formulas by engineering standard. Here's how to use them:

```python exec="on" source="material-block" session="quickstart" result="ansi"
# Create a Formula instance using Eurocode formula 4.1: c_nom = c_min + Δc_dev
c_min = 25.0  # mm
delta_c_dev = 10.0  # mm
concrete_cover = Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

print(f"Formula result: {concrete_cover} mm")
print(f"Formula label: {concrete_cover.label}")
print(f"Source document: {concrete_cover.source_document}")
print(f"Stored parameters: c_min={concrete_cover.c_min}, delta_c_dev={concrete_cover.delta_c_dev}")
```

## Combining all elements in a Rectangular Reinforced cross section

```python exec="on" source="above" session="quickstart" result="html" html="true"
from blueprints.structural_sections.concrete.covers import CoversRectangular
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection

applied_cover = 5 + concrete_cover

# Define a rectangular reinforced cross-section
cs = RectangularReinforcedCrossSection(
    width=1000,
    height=800,
    covers=CoversRectangular(upper=applied_cover, right=applied_cover, lower=applied_cover, left=applied_cover),
    concrete_material=concrete,
)

# Add reinforcement to the upper edge
cs.add_longitudinal_reinforcement_by_quantity(
    n=10,
    diameter=16,
    edge="lower",
    material=rebar,
)

# Plot the cross-section
fig = cs.plot(show=False) #change show to True in your local example to show the plot directly 

from io import StringIO   # markdown-exec: hide
import matplotlib.pyplot as plt   # markdown-exec: hide
buffer = StringIO()   # markdown-exec: hide
plt.savefig(buffer, format="svg")   # markdown-exec: hide
print(buffer.getvalue())   # markdown-exec: hide
```
## Next Steps

Now that you've seen the basics, you can:

- **Explore the [API Reference](../API reference/)** - Detailed documentation of all available functionality
- **Check out [Examples](../guides/examples/)** - More complex, real-world scenarios
- **Read about [Library Organization](../guides/concepts/library_organization.md)** - Understand why Blueprints is structured the way it is
- **Join the [Discord community](https://discord.gg/hBZBqegEzA)** - Ask questions and connect with other engineers

Happy engineering! 🚀