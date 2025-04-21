"""Fixtures for testing reinforced concrete sections."""

import pytest

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.circular import CircularReinforcedCrossSection


@pytest.fixture
def circular_reinforced_cross_section() -> CircularReinforcedCrossSection:
    """Return a circular reinforced cross-section."""
    # Define a concrete material
    concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C35_45)

    # Define the reinforcement steel material
    reinforcement_steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

    # Define the cross-section
    cs = CircularReinforcedCrossSection(diameter=400, concrete_material=concrete, cover=25)

    # Add longitudinal reinforcement
    cs.add_longitudinal_reinforcement_by_quantity(n=3, diameter=25, material=reinforcement_steel)

    # Add longitudinal reinforcement
    cs.add_longitudinal_reinforcement_by_quantity(n=3, diameter=10, material=reinforcement_steel, start_angle=45)

    # Add stirrups
    cs.add_stirrup_along_perimeter(diameter=25, distance=200, material=reinforcement_steel)

    # Add stirrups
    cs.add_stirrup_along_perimeter(diameter=10, distance=200, material=reinforcement_steel)

    # Add longitudinal rebar in center
    cs.add_longitudinal_rebar(rebar=Rebar(diameter=16, x=0, y=0, material=reinforcement_steel))

    return cs
