"""Reinforced concrete cross-section example."""

from shapely import LineString

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.covers import CoversRectangular
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import ReinforcementByQuantity

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

# add a second layer of reinforcement to the cross-section
cs.add_longitudinal_reinforcement_by_quantity(
    n=3,
    diameter=16,
    edge="upper",
    material=steel,
    cover=100,
)

# add a free reinforcement configuration to the cross-section
cs.add_reinforcement_configuration(
    line=LineString([(50, -50), (200, 200)]),
    configuration=ReinforcementByQuantity(diameter=20, n=4, material=steel),
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

# Add a longitudinal rebar to the cross-section
cs.add_longitudinal_rebar(
    rebar=Rebar(
        diameter=12,
        x=-250,
        y=-100,
        material=steel,
    )
)

cs.plot(show=True)
