"""Reinforced concrete cross-section example."""

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.covers import CoversRectangular
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection

# Define a concrete material
concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C35_45)

# Define a reinforcement steel material
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

# Define a rectangular reinforced cross-section
cs = RectangularReinforcedCrossSection(
    width=1000,
    height=800,
    covers=CoversRectangular(upper=45, right=30, lower=35, left=50),
    concrete_material=concrete,
)

# Add reinforcement to the cross-section
cs.add_longitudinal_reinforcement_by_quantity(
    n=5,
    diameter=14,
    edge="upper",
    material=steel,
)
cs.add_longitudinal_reinforcement_by_quantity(
    n=4,
    diameter=40,
    edge="lower",
    material=steel,
)
cs.add_longitudinal_reinforcement_by_quantity(
    n=5,
    diameter=14,
    edge="right",
    material=steel,
)
cs.add_longitudinal_reinforcement_by_quantity(
    n=5,
    diameter=14,
    edge="left",
    material=steel,
)

# Add stirrups to the cross-section
cs.add_stirrup_along_edges(
    diameter=8,
    distance=150,
    material=steel,
)
# Add stirrups to the cross-section
cs.add_stirrup_along_edges(
    diameter=12,
    distance=300,
    material=steel,
)

cs.plot(show=True)
