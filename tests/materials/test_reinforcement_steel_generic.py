"""Tests for the code-agnostic ReinforcementSteel data container and its from_ec2 factory."""

import pytest

from blueprints.materials._material import Material
from blueprints.materials.reinforcement_steel import (
    ReinforcementSteel,
    ReinforcementSteelMaterial,
    ReinforcementSteelQuality,
)


@pytest.mark.parametrize("quality", list(ReinforcementSteelQuality))
def test_from_ec2_reproduces_reinforcement_steel_material(quality: ReinforcementSteelQuality) -> None:
    """ReinforcementSteel.from_ec2 reproduces every characteristic value of the legacy material."""
    legacy = ReinforcementSteelMaterial(steel_quality=quality)
    data = ReinforcementSteel.from_ec2(quality)

    assert data.name == legacy.name
    assert data.f_yk == legacy.f_yk
    assert data.f_yd == pytest.approx(legacy.f_yd)
    assert data.f_tk == pytest.approx(legacy.f_tk)
    assert data.eps_uk == legacy.eps_uk
    assert data.modulus_of_elasticity == legacy.e_s
    assert data.ductility_factor_k == pytest.approx(legacy.ductility_factor_k)


def test_shear_modulus() -> None:
    """The shear modulus is derived from the modulus of elasticity and Poisson's ratio."""
    data = ReinforcementSteel.from_ec2(ReinforcementSteelQuality.B500B)
    assert data.shear_modulus == pytest.approx(data.modulus_of_elasticity / (2 * (1 + data.poisson_ratio)))


def test_custom_name() -> None:
    """A custom name overrides the steel-quality name."""
    data = ReinforcementSteel.from_ec2(ReinforcementSteelQuality.B500B, name="custom rebar")
    assert data.name == "custom rebar"


def test_non_standard_material_built_directly() -> None:
    """A non-standard reinforcement steel can be built directly through the constructor."""
    data = ReinforcementSteel(name="B700", f_yk=700.0, f_tk=805.0, eps_uk=600.0)
    assert data.f_yd == pytest.approx(700.0 / 1.15)
    assert data.ductility_factor_k == pytest.approx(805.0 / 700.0)


def test_conforms_to_material_protocol() -> None:
    """A ReinforcementSteel instance satisfies the Material protocol."""
    assert isinstance(ReinforcementSteel.from_ec2(ReinforcementSteelQuality.B500B), Material)
