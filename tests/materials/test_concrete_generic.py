"""Tests for the code-agnostic Concrete data container and its from_ec2 factory."""

import pytest

from blueprints.materials._material import Material
from blueprints.materials.concrete import Concrete, ConcreteMaterial, ConcreteStrengthClass


@pytest.mark.parametrize("concrete_class", list(ConcreteStrengthClass))
def test_from_ec2_reproduces_concrete_material(concrete_class: ConcreteStrengthClass) -> None:
    """Concrete.from_ec2 reproduces every characteristic value of the legacy ConcreteMaterial."""
    legacy = ConcreteMaterial(concrete_class=concrete_class)
    data = Concrete.from_ec2(concrete_class)

    assert data.name == legacy.name
    assert data.f_ck == legacy.f_ck
    assert data.f_ck_cube == legacy.f_ck_cube
    assert data.f_cm == legacy.f_cm
    assert data.f_cm_cube == legacy.f_cm_cube
    assert data.e_cm == legacy.e_cm
    assert data.modulus_of_elasticity == legacy.e_c
    assert data.f_cd == pytest.approx(legacy.f_cd)
    assert data.f_ctm == pytest.approx(legacy.f_ctm)
    assert data.sigma_cr == pytest.approx(legacy.sigma_cr)
    assert data.strain_cr == pytest.approx(legacy.strain_cr)
    assert data.f_ctk_0_05 == pytest.approx(legacy.f_ctk_0_05)
    assert data.f_ctd == pytest.approx(legacy.f_ctd)
    assert data.f_ctk_0_95 == pytest.approx(legacy.f_ctk_0_95)
    assert data.eps_c1 == pytest.approx(legacy.eps_c1)
    assert data.eps_cu1 == pytest.approx(legacy.eps_cu1)
    assert data.eps_c2 == pytest.approx(legacy.eps_c2)
    assert data.eps_cu2 == pytest.approx(legacy.eps_cu2)
    assert data.n_factor == pytest.approx(legacy.n_factor)
    assert data.eps_c3 == pytest.approx(legacy.eps_c3)
    assert data.eps_cu3 == pytest.approx(legacy.eps_cu3)
    assert data.rho_min(435.0) == pytest.approx(legacy.rho_min(435.0))


def test_shear_modulus() -> None:
    """The shear modulus is derived from the secant modulus and Poisson's ratio."""
    data = Concrete.from_ec2(ConcreteStrengthClass.C30_37)
    assert data.shear_modulus == pytest.approx(data.e_cm / (2 * (1 + data.poisson_ratio)))


def test_custom_name() -> None:
    """A custom name overrides the strength-class name."""
    data = Concrete.from_ec2(ConcreteStrengthClass.C30_37, name="My mix")
    assert data.name == "My mix"


def test_custom_e_cm() -> None:
    """A custom secant modulus overrides the Table 3.1 value."""
    data = Concrete.from_ec2(ConcreteStrengthClass.C30_37, e_cm=30000)
    assert data.e_cm == 30000
    assert data.modulus_of_elasticity == 30000


def test_non_standard_material_built_directly() -> None:
    """A non-standard concrete can be built directly through the constructor, with no design code."""
    data = Concrete(name="HPC-A", f_ck=95, f_ck_cube=110, f_cm=103, f_ctm=5.0, f_ctk_0_05=3.5, f_ctk_0_95=6.5, e_cm=44000)
    assert data.f_cd == pytest.approx(95 / 1.5)


def test_from_ec2_invalid_class_raises() -> None:
    """An invalid strength class raises a ValueError from the factory."""
    invalid_class = type("InvalidConcreteStrengthClass", (), {"value": "invalid_value"})()
    with pytest.raises(ValueError):
        Concrete.from_ec2(invalid_class)


def test_conforms_to_material_protocol() -> None:
    """A Concrete instance satisfies the Material protocol."""
    assert isinstance(Concrete.from_ec2(ConcreteStrengthClass.C30_37), Material)
