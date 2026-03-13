"""Generic concrete fixtures."""

import pytest

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality


@pytest.fixture
def fixture_concrete_material_c30_37() -> ConcreteMaterial:
    """Fixture for concrete material C30/37."""
    return ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)


@pytest.fixture
def fixture_concrete_material_c90_105() -> ConcreteMaterial:
    """Fixture for concrete material C90/105."""
    return ConcreteMaterial(concrete_class=ConcreteStrengthClass.C90_105)


@pytest.fixture
def fixture_reinforcement_steel_material_b500b() -> ReinforcementSteelMaterial:
    """Fixture for reinforcement steel material B500B."""
    return ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)
