"""Custom rectangular reinforced cross-section example."""

from shapely import LineString, Polygon

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.covers import CoversRectangular
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import (
    ReinforcementByDistance,
    ReinforcementByQuantity,
)
from blueprints.structural_sections.concrete.stirrups import StirrupConfiguration

# Define a concrete material
concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)

# Define a reinforcement steel material
steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

# Define a rectangular reinforced cross-section
cs = RectangularReinforcedCrossSection(
    width=600,
    height=500,
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

# add a second layer of reinforcement to the cross-section
cs.add_longitudinal_reinforcement_by_quantity(
    n=3,
    diameter=16,
    edge="upper",
    material=steel,
    cover=100,
)

# add reinforcement configurations to the cross-section in any position
cs.add_reinforcement_configuration(
    line=LineString([(50, -100), (150, 50)]),
    configuration=ReinforcementByQuantity(diameter=20, n=3, material=steel),
)

cs.add_reinforcement_configuration(
    line=LineString([(0, -180), (-250, 0)]),
    configuration=ReinforcementByDistance(diameter=12, center_to_center=40, material=steel),
)

# Add stirrups to the cross-section
cs.add_stirrup_configuration(
    stirrup=StirrupConfiguration(
        geometry=Polygon([(-200, -200), (-200, 200), (200, 200), (200, -200)]),
        diameter=8,
        distance=150,
        material=steel,
    ),
)

# Add a longitudinal rebar to the cross-section
cs.add_longitudinal_rebar(
    rebar=Rebar(
        diameter=12,
        x=0,
        y=0,
        material=steel,
    )
)

cs.plot(show=True)
