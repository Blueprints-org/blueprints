"""Tests for the code-agnostic Steel data container and its from_en10025 factory."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStandardGroup, SteelStrengthClass
from blueprints.materials._material import Material
from blueprints.materials.steel import Steel, SteelMaterial, StrengthRow

THICK_GRADES = [grade for grade in SteelStrengthClass if grade.standard_group is not SteelStandardGroup.EN_10219_1]
THIN_ONLY_GRADES = [grade for grade in SteelStrengthClass if grade.standard_group is SteelStandardGroup.EN_10219_1]


@pytest.mark.parametrize("grade", list(SteelStrengthClass))
def test_from_en10025_reproduces_steel_material_thin_band(grade: SteelStrengthClass) -> None:
    """Steel.from_en10025 reproduces the legacy strengths and name for the <=40 mm band."""
    legacy = SteelMaterial(steel_class=grade)
    data = Steel.from_en10025(grade)
    assert data.name == legacy.name
    assert data.f_yk(40) == legacy.yield_strength(40)
    assert data.f_uk(40) == legacy.ultimate_strength(40)


@pytest.mark.parametrize("grade", THICK_GRADES)
def test_from_en10025_reproduces_thick_band(grade: SteelStrengthClass) -> None:
    """For grades with a >40 mm band, the strengths match the legacy values."""
    legacy = SteelMaterial(steel_class=grade)
    data = Steel.from_en10025(grade)
    assert data.f_yk(60) == legacy.yield_strength(60)
    assert data.f_uk(80) == legacy.ultimate_strength(80)


@pytest.mark.parametrize("grade", THIN_ONLY_GRADES)
def test_thin_only_grade_raises_above_40(grade: SteelStrengthClass) -> None:
    """Grades without a >40 mm band expose only the <=40 mm row and raise above it."""
    data = Steel.from_en10025(grade)
    with pytest.raises(ValueError):
        data.f_yk(60)


def test_f_yd_applies_material_factor() -> None:
    """The design yield strength divides the characteristic value by the partial factor."""
    data = Steel.from_en10025(SteelStrengthClass.S355, material_factor=1.1)
    assert data.f_yd(40) == pytest.approx(data.f_yk(40) / 1.1)


def test_lookup_rejects_non_positive_thickness() -> None:
    """A non-positive thickness raises a ValueError."""
    data = Steel.from_en10025(SteelStrengthClass.S355)
    with pytest.raises(ValueError):
        data.f_yk(0)


def test_modulus_and_shear_modulus() -> None:
    """The modulus of elasticity and derived shear modulus take their default values."""
    data = Steel.from_en10025(SteelStrengthClass.S355)
    assert data.modulus_of_elasticity == 210_000.0
    assert data.shear_modulus == pytest.approx(210_000.0 / (2 * (1 + 0.3)))


def test_custom_name() -> None:
    """A custom name overrides the grade name."""
    data = Steel.from_en10025(SteelStrengthClass.S355, name="USA alloy")
    assert data.name == "USA alloy"


def test_non_standard_material_built_directly() -> None:
    """A non-standard steel can be built directly from explicit strength tables."""
    data = Steel(
        name="custom",
        f_y_table=(StrengthRow(max_thickness=50.0, strength=400.0),),
        f_u_table=(StrengthRow(max_thickness=50.0, strength=520.0),),
    )
    assert data.f_yk(25) == 400.0
    assert data.f_uk(50) == 520.0


def test_conforms_to_material_protocol() -> None:
    """A Steel instance satisfies the Material protocol."""
    assert isinstance(Steel.from_en10025(SteelStrengthClass.S355), Material)
