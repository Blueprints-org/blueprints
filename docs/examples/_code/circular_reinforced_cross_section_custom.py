"""Reinforced concrete cross-section example."""

from shapely import LineString

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.circular import CircularReinforcedCrossSection, ReinforcementByQuantity

# Define a concrete material
concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C35_45)

# Define a reinforcement steel material
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

# Define a circular reinforced cross-section
cs = CircularReinforcedCrossSection(
    diameter=400,
    cover=35,
    concrete_material=concrete,
)

# Add longitudinal reinforcement to the cross-section
cs.add_longitudinal_reinforcement_by_quantity(
    n=5,
    diameter=25,
    material=steel,
)

# Add longitudinal reinforcement to the cross-section
cs.add_longitudinal_reinforcement_by_quantity(
    n=5,
    diameter=16,
    material=steel,
    start_angle=45,
)

# Add stirrups to the cross-section
cs.add_stirrup_along_perimeter(
    diameter=10,
    distance=150,
    material=steel,
)

# Add reinforcement configuration to the cross-section in a diagonal line
linestring = LineString([(-100, 100), (100, 0)])
cs.add_reinforcement_configuration(
    line=linestring,
    configuration=ReinforcementByQuantity(
        diameter=12,
        n=7,
        material=steel,
    ),
)

# Add longitudinal rebar in center
cs.add_longitudinal_rebar(rebar=Rebar(diameter=16, x=0, y=0, material=steel))

# Plot the cross-section
cs.plot(show=True)
