"""Test the bolt geometry."""

import math

import pytest

from blueprints.materials.fastener_steel import FastenerClass, FastenerMaterial
from blueprints.structural_sections.fasteners.bolts import (
    BoltElement,
    BoltPositionParallel,
    BoltPositionPerpendicular,
    BoltSize,
    HoleType,
    PlateAttachment,
)


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

    @pytest.mark.parametrize(
        ("size", "normal", "oversized"),
        [
            (BoltSize.M12, 13.0, 14.5),
            (BoltSize.M20, 22.0, 24.0),
            (BoltSize.M24, 26.0, 28.0),
        ],
    )
    def test_hole_diameters(self, size: BoltSize, normal: float, oversized: float) -> None:
        """A normal hole leaves the standard clearance, an oversized one more."""
        assert size.hole_diameter_normal == pytest.approx(expected=normal)
        assert size.hole_diameter_oversized == pytest.approx(expected=oversized)

    @pytest.mark.parametrize("size", list(BoltSize))
    def test_an_oversized_hole_is_never_smaller_than_a_normal_one(self, size: BoltSize) -> None:
        """Both grow with the bolt, and the two can never be swapped unnoticed."""
        assert size.hole_diameter_normal > size.diameter
        assert size.hole_diameter_oversized >= size.hole_diameter_normal


class TestBoltElement:
    """Validation of the bolt geometry record."""

    @staticmethod
    def _bolt(*attachments: PlateAttachment, bolt_class: FastenerClass = FastenerClass.CLASS_8_8, preload_force: float | None = None) -> BoltElement:
        """Builds an M20 bolt with the given attachments."""
        return BoltElement(
            material=FastenerMaterial(bolt_class=bolt_class),
            size=BoltSize.M20,
            attachments=tuple(attachments),
            preload_force=preload_force,
        )

    def test_the_dimensions_follow_the_size(self) -> None:
        """The bolt hands through the properties of its size rather than keeping its own copy."""
        bolt = self._bolt()

        assert bolt.diameter == pytest.approx(expected=BoltSize.M20.diameter)
        assert bolt.gross_area == pytest.approx(expected=BoltSize.M20.gross_area)
        assert bolt.tensile_stress_area == pytest.approx(expected=BoltSize.M20.tensile_stress_area)

    @pytest.mark.parametrize(
        ("hole_type", "expected"),
        [
            (HoleType.NORMAL, 22.0),
            (HoleType.OVERSIZED, 24.0),
            (HoleType.SLOTTED_PERPENDICULAR, 22.0),
        ],
    )
    def test_the_hole_diameter_is_filled_in_from_the_size(self, hole_type: HoleType, expected: float) -> None:
        """An attachment without an explicit d0 gets the diameter that its hole type implies."""
        bolt = self._bolt(PlateAttachment(plate_id="P1", hole_type=hole_type))

        assert bolt.attachments[0].d0 == pytest.approx(expected=expected)

    def test_an_explicit_hole_diameter_is_left_alone(self) -> None:
        """A caller who measured the hole keeps that value, however unusual it is."""
        bolt = self._bolt(PlateAttachment(plate_id="P1", hole_type=HoleType.NORMAL, d0=21.5))

        assert bolt.attachments[0].d0 == pytest.approx(expected=21.5)

    def test_filling_in_the_hole_diameter_keeps_every_other_field(self) -> None:
        """Regression: the attachment is rebuilt to set d0, and the two bolt positions used to fall back to
        their defaults in the process. They feed the bearing resistance of Table 3.4, so losing them would
        change a result rather than raise.
        """
        bolt = self._bolt(
            PlateAttachment(
                plate_id="P1",
                plate_thickness=20.0,
                p1=60.0,
                e1=40.0,
                bolt_position_parallel=BoltPositionParallel.INNER,
                bolt_position_perpendicular=BoltPositionPerpendicular.INNER,
            )
        )
        attachment = bolt.attachments[0]

        assert attachment.d0 == pytest.approx(expected=22.0)
        assert attachment.bolt_position_parallel is BoltPositionParallel.INNER
        assert attachment.bolt_position_perpendicular is BoltPositionPerpendicular.INNER
        assert attachment.plate_thickness == pytest.approx(expected=20.0)
        assert attachment.p1 == pytest.approx(expected=60.0)
        assert attachment.e1 == pytest.approx(expected=40.0)

    def test_attachment_for_plate_finds_the_record(self) -> None:
        """Each plate the bolt passes through is reachable by its own identifier."""
        bolt = self._bolt(
            PlateAttachment(plate_id="P1", plate_thickness=20.0),
            PlateAttachment(plate_id="P2", plate_thickness=15.0),
        )

        assert bolt.attachment_for_plate("P2").plate_thickness == pytest.approx(expected=15.0)

    def test_attachment_for_an_unknown_plate_is_none(self) -> None:
        """An identifier the bolt does not pass through returns nothing rather than raising."""
        bolt = self._bolt(PlateAttachment(plate_id="P1"))

        assert bolt.attachment_for_plate("P9") is None

    @pytest.mark.parametrize("bolt_class", [FastenerClass.CLASS_8_8, FastenerClass.CLASS_10_9])
    def test_a_preload_is_accepted_for_the_classes_that_allow_it(self, bolt_class: FastenerClass) -> None:
        """Art. 3.1.2(1) restricts preloading to classes 8.8 and 10.9."""
        bolt = self._bolt(bolt_class=bolt_class, preload_force=50.0)

        assert bolt.preload_force == pytest.approx(expected=50.0)

    @pytest.mark.parametrize("bolt_class", [FastenerClass.CLASS_4_6, FastenerClass.CLASS_6_8])
    def test_a_preload_is_rejected_for_the_other_classes(self, bolt_class: FastenerClass) -> None:
        """A class that may not be preloaded refuses the force instead of ignoring it."""
        with pytest.raises(ValueError, match="cannot be preloaded"):
            self._bolt(bolt_class=bolt_class, preload_force=50.0)
