"""Tests for the Rebar class."""

import math

import pytest

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.unit_conversion import MM2_TO_M2


def test_rebar_initialization() -> None:
    """Test Rebar initialization with valid input."""
    material = ReinforcementSteelMaterial(density=7850, steel_quality=ReinforcementSteelQuality.B500B)
    rebar = Rebar(diameter=16, x=100, y=200, material=material)

    assert rebar.diameter == 16
    assert rebar.x == 100
    assert rebar.y == 200
    assert rebar.material == material
    assert rebar.relative_start_position == 0.0
    assert rebar.relative_end_position == 1.0
    assert rebar.name == "⌀16mm/B500B"


def test_rebar_invalid_diameter() -> None:
    """Test Rebar initialization with invalid diameter."""
    material = ReinforcementSteelMaterial(density=7850, steel_quality=ReinforcementSteelQuality.B500B)
    with pytest.raises(ValueError, match="The diameter of the rebar must be greater than zero"):
        Rebar(diameter=-5, x=100, y=200, material=material)


def test_rebar_invalid_relative_start_position() -> None:
    """Test Rebar initialization with invalid relative start position."""
    material = ReinforcementSteelMaterial(density=7850, steel_quality=ReinforcementSteelQuality.B500B)
    with pytest.raises(ValueError, match="start position"):
        Rebar(diameter=16, x=100, y=200, material=material, relative_start_position=-0.1)


def test_rebar_invalid_relative_end_position() -> None:
    """Test Rebar initialization with invalid relative end position."""
    material = ReinforcementSteelMaterial(density=7850, steel_quality=ReinforcementSteelQuality.B500B)
    with pytest.raises(ValueError, match="end position"):
        Rebar(diameter=16, x=100, y=200, material=material, relative_end_position=1.1)


def test_rebar_weight_per_meter() -> None:
    """Test weight per meter calculation."""
    material = ReinforcementSteelMaterial(density=7850.0, steel_quality=ReinforcementSteelQuality.B500B)
    rebar = Rebar(diameter=16.0, x=100, y=200, material=material)

    assert pytest.approx(rebar.weight_per_meter, 0.0001) == 7850.0 * (math.pi * (8.0**2.0) * MM2_TO_M2)
