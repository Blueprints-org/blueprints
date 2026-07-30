"""Test the bolt material properties."""

import math

import pytest

from blueprints.materials.bolts import BOLT_YOUNG_MODULUS, BoltClass, BoltMaterial, BoltSize


class TestBoltSize:
    """Validation of the ISO metric coarse thread series."""

    @pytest.mark.parametrize(
        ("size", "diameter", "tensile_stress_area"),
        [
            (BoltSize.M8, 8.0, 36.6),
            (BoltSize.M10, 10.0, 58.0),
            (BoltSize.M12, 12.0, 84.3),
            (BoltSize.M14, 14.0, 115.0),
            (BoltSize.M16, 16.0, 157.0),
            (BoltSize.M18, 18.0, 192.0),
            (BoltSize.M20, 20.0, 245.0),
            (BoltSize.M22, 22.0, 303.0),
            (BoltSize.M24, 24.0, 353.0),
            (BoltSize.M27, 27.0, 459.0),
            (BoltSize.M30, 30.0, 561.0),
            (BoltSize.M33, 33.0, 694.0),
            (BoltSize.M36, 36.0, 817.0),
        ],
    )
    def test_diameter_and_tensile_stress_area(self, size: BoltSize, diameter: float, tensile_stress_area: float) -> None:
        """The nominal diameter follows the designation and the stress area comes from the thread series."""
        assert size.diameter == pytest.approx(expected=diameter)
        assert size.tensile_stress_area == pytest.approx(expected=tensile_stress_area)

    @pytest.mark.parametrize("size", list(BoltSize))
    def test_gross_area_follows_the_nominal_diameter(self, size: BoltSize) -> None:
        """The gross area is the full circle of the shank, which is what a shear plane there sees."""
        assert size.gross_area == pytest.approx(expected=math.pi * size.diameter**2 / 4)

    @pytest.mark.parametrize("size", list(BoltSize))
    def test_the_stress_area_is_smaller_than_the_gross_area(self, size: BoltSize) -> None:
        """The thread removes material, so the two areas can never be swapped unnoticed."""
        assert size.tensile_stress_area < size.gross_area


class TestBoltMaterial:
    """Validation of the bolt material."""

    def test_defaults(self) -> None:
        """The default is a class 8.8 bolt with the properties of structural steel."""
        material = BoltMaterial()

        assert material.bolt_class is BoltClass.CLASS_8_8
        assert material.name == "8.8"
        assert material.density == pytest.approx(expected=7850.0)
        assert material.e_modulus == pytest.approx(expected=BOLT_YOUNG_MODULUS)
        assert material.poisson_ratio == pytest.approx(expected=0.3)
        assert material.thermal_coefficient == pytest.approx(expected=1.2e-5)

    def test_shear_modulus(self) -> None:
        """The shear modulus follows from the modulus of elasticity and Poisson's ratio."""
        material = BoltMaterial()

        assert material.shear_modulus == pytest.approx(expected=210_000.0 / (2 * 1.3))

    @pytest.mark.parametrize(
        ("bolt_class", "f_yb", "f_ub"),
        [
            (BoltClass.CLASS_4_6, 240, 400),
            (BoltClass.CLASS_8_8, 640, 800),
            (BoltClass.CLASS_10_9, 900, 1000),
        ],
    )
    def test_strengths_come_from_table_3_1(self, bolt_class: BoltClass, f_yb: int, f_ub: int) -> None:
        """Without a custom value the strengths are the ones the standard prints."""
        material = BoltMaterial(bolt_class=bolt_class)

        assert material.yield_strength == f_yb
        assert material.ultimate_strength == f_ub

    def test_custom_strengths_win(self) -> None:
        """A custom strength takes the bolt outside the classes of the standard, which is allowed."""
        material = BoltMaterial(bolt_class=BoltClass.CLASS_8_8, custom_yield_strength=700.0, custom_ultimate_strength=900.0)

        assert material.yield_strength == pytest.approx(expected=700.0)
        assert material.ultimate_strength == pytest.approx(expected=900.0)

    def test_custom_deformation_properties_win(self) -> None:
        """Every default can be overridden the way SteelMaterial allows it."""
        material = BoltMaterial(
            custom_name="special",
            custom_e_modulus=200_000.0,
            custom_poisson_ratio=0.28,
            custom_thermal_coefficient=1.0e-5,
        )

        assert material.name == "special"
        assert material.e_modulus == pytest.approx(expected=200_000.0)
        assert material.poisson_ratio == pytest.approx(expected=0.28)
        assert material.thermal_coefficient == pytest.approx(expected=1.0e-5)

    @pytest.mark.parametrize(
        ("bolt_class", "expected"),
        [
            (BoltClass.CLASS_4_6, False),
            (BoltClass.CLASS_6_8, False),
            (BoltClass.CLASS_8_8, True),
            (BoltClass.CLASS_10_9, True),
        ],
    )
    def test_can_be_preloaded(self, bolt_class: BoltClass, expected: bool) -> None:
        """Art.3.1.2(1) allows only classes 8.8 and 10.9 to be used as preloaded bolts."""
        assert BoltMaterial(bolt_class=bolt_class).can_be_preloaded is expected

    def test_a_custom_strength_does_not_change_the_class(self) -> None:
        """Preloading is tied to the class, not to the strength, so overriding one leaves the other."""
        material = BoltMaterial(bolt_class=BoltClass.CLASS_4_6, custom_ultimate_strength=1000.0)

        assert material.can_be_preloaded is False

    def test_the_material_is_immutable(self) -> None:
        """The dataclass is frozen, like the other materials."""
        material = BoltMaterial()

        with pytest.raises(AttributeError):
            material.bolt_class = BoltClass.CLASS_4_6  # type: ignore[misc]
