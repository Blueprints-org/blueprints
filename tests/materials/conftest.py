"""Generic concrete fixtures."""

import pytest

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass


@pytest.fixture()
def fixture_concrete_material_c30_37() -> ConcreteMaterial:
    """Fixture for concrete material C30/37."""
    return ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)


@pytest.fixture()
def fixture_concrete_material_c90_105() -> ConcreteMaterial:
    """Fixture for concrete material C90/105."""
    return ConcreteMaterial(concrete_class=ConcreteStrengthClass.C90_105)
