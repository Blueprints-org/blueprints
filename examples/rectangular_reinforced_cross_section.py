"""Reinforced concrete cross-section example."""

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.covers import CoversRectangular
from blueprints.structural_sections.concrete.reinforced_concrete_sections.cross_sections_shapes import Edges
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular_rcs import RectangularReinforcedCrossSection

# Define a concrete material
concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C35_45)

# Define a reinforcement steel material
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

# Define a rectangular reinforced cross-section
cs = RectangularReinforcedCrossSection(
    width=1000,
    height=800,
    covers=CoversRectangular(upper=30, lower=30, left=30, right=30),
    concrete_material=concrete,
    steel_material=steel,
)

# Change the covers of the cross-section ( if necessary )
cs.set_covers(upper=60, lower=45)

# Add reinforcement to the cross-section
cs.add_longitudinal_reinforcement_by_quantity_on_edge(
    n=5,
    diameter=14,
    edge=Edges.UPPER_SIDE,
    material=steel,
)
cs.add_longitudinal_reinforcement_by_quantity_on_edge(
    n=4,
    diameter=20,
    edge=Edges.LOWER_SIDE,
    material=steel,
)


# Add stirrups to the cross-section
cs.add_stirrup_along_edges(
    diameter=8,
    distance=150,
    material=steel,
)

# Add a longitudinal rebar to the cross-section
cs.add_longitudinal_rebar(
    diameter=12,
    x=-250,
    y=-100,
    material=steel,
)

cs.plot(show=True)
