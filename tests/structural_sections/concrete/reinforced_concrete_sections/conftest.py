"""Fixtures for testing reinforced concrete sections."""

import pytest

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.covers import CoversRectangular
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.circular import CircularReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import (
    ReinforcementByDistance,
    ReinforcementByQuantity,
)


@pytest.fixture
def rectangular_reinforced_cross_section() -> RectangularReinforcedCrossSection:
    """Return a rectangular reinforced cross-section."""
    # Define a concrete material
    concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C35_45)

    # Define a reinforcement steel material
    steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

    # Define a rectangular reinforced cross-section
    cs = RectangularReinforcedCrossSection(
        name="Rectangular",
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

    return cs


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


@pytest.fixture
def reinforcement_by_distance() -> ReinforcementByDistance:
    """Creates a reinforcement by distance configuration."""
    return ReinforcementByDistance(
        diameter=12,
        center_to_center=100,
        material=ReinforcementSteelMaterial(),
    )


@pytest.fixture
def reinforcement_by_quantity() -> ReinforcementByQuantity:
    """Creates a reinforcement by quantity configuration."""
    return ReinforcementByQuantity(
        diameter=12,
        material=ReinforcementSteelMaterial(),
        n=10,
    )


@pytest.fixture
def rectangular_cross_section_no_reinforcement() -> RectangularReinforcedCrossSection:
    """Return a rectangular cross-section without longitudinal reinforcement."""
    # Define a concrete material
    concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C35_45)

    # Define a rectangular cross-section without reinforcement
    return RectangularReinforcedCrossSection(
        name="Rectangular No Reinforcement",
        width=1000,
        height=800,
        covers=CoversRectangular(upper=45, right=30, lower=35, left=50),
        concrete_material=concrete,
    )


@pytest.fixture
def circular_cross_section_no_reinforcement() -> CircularReinforcedCrossSection:
    """Return a circular cross-section without longitudinal reinforcement."""
    # Define a concrete material
    concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C35_45)

    # Define a circular cross-section without reinforcement
    return CircularReinforcedCrossSection(
        diameter=400,
        concrete_material=concrete,
        cover=25,
    )
