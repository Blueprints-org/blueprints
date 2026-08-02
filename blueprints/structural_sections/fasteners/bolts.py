"""Bolt geometry definitions.

This module provides representations of bolt geometry that are independent of material properties
(which live in `blueprints.materials.fastener_steel`). A single `BoltElement` can hold multiple `PlateAttachment`
records so the same bolt can be referenced from several plates (e.g. lap joints). This keeps the
geometry separate from the material while making it straightforward to list bolts later.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import StrEnum

from blueprints.materials.fastener_steel import FastenerMaterial
from blueprints.materials.steel import SteelStrengthClass
from blueprints.type_alias import KN, MM, MM2

__all__ = [
    "BoltCategory",
    "BoltElement",
    "BoltGapFilling",
    "BoltPositionParallel",
    "BoltPositionPerpendicular",
    "BoltSize",
    "HoleType",
    "PlateAttachment",
]


class BoltSize(StrEnum):
    """Bolt sizes of the ISO metric coarse thread series.

    The nominal diameter and the tensile stress area are properties of the thread, not of any
    Eurocode. They are held here because the resistance formulas of EN 1993-1-8 take them as input:
    the tensile stress area where the shear plane passes through the threads, and the gross area
    where it passes through the shank. Also applies to threaded rods and anchors, which share the
    same thread geometry.
    """

    M3 = "M3"
    M3_5 = "M3.5"
    M4 = "M4"
    M4_5 = "M4.5"
    M5 = "M5"
    M6 = "M6"
    M7 = "M7"
    M8 = "M8"
    M10 = "M10"
    M12 = "M12"
    M14 = "M14"
    M16 = "M16"
    M18 = "M18"
    M20 = "M20"
    M22 = "M22"
    M24 = "M24"
    M27 = "M27"
    M30 = "M30"
    M33 = "M33"
    M36 = "M36"
    M39 = "M39"
    M42 = "M42"
    M45 = "M45"
    M48 = "M48"
    M52 = "M52"
    M56 = "M56"
    M60 = "M60"
    M64 = "M64"
    M68 = "M68"
    M72 = "M72"
    M76 = "M76"
    M80 = "M80"
    M85 = "M85"
    M90 = "M90"
    M95 = "M95"
    M100 = "M100"
    M105 = "M105"
    M110 = "M110"
    M115 = "M115"
    M120 = "M120"
    M125 = "M125"
    M130 = "M130"
    M140 = "M140"
    M150 = "M150"

    @property
    def diameter(self) -> MM:
        """[$d$] Nominal diameter of the bolt [$mm$].

        Returns
        -------
        MM
            The number of the designation, so 20 mm for M20.
        """
        return float(self.value.removeprefix("M"))

    @property
    def gross_area(self) -> MM2:
        """[$A$] Gross cross-section of the bolt shank [$mm^2$].

        Returns
        -------
        MM2
            The area of a circle of the nominal diameter, which is the area to use where the shear
            plane passes through the unthreaded shank.
        """
        return math.pi * self.diameter**2 / 4

    @property
    def tensile_stress_area(self) -> MM2:
        """[$A_s$] Tensile stress area of the bolt [$mm^2$].

        Returns
        -------
        MM2
            The tensile stress area of the ISO metric coarse thread, which is the area to use for the
            tension resistance and where the shear plane passes through the threaded portion.
        """
        return _BOLT_PARAMETERS[self].tensile_stress_area

    @property
    def hole_diameter_normal(self) -> MM:
        """Nominal diameter of a normal bolt hole [$mm$].

        Returns
        -------
        MM
            The diameter of the hole for a normal sized hole.
        """
        return _BOLT_PARAMETERS[self].hole_diameter_normal

    @property
    def hole_diameter_oversized(self) -> MM:
        """Nominal diameter of an oversized bolt hole [$mm$].

        Returns
        -------
        MM
            The diameter of the oversized hole.
        """
        return _BOLT_PARAMETERS[self].hole_diameter_oversized


@dataclass(frozen=True)
class BoltParameters:
    """Named container for bolt parameter triplets.

    Fields:
    - tensile_stress_area: tensile stress area A_s in mm^2
    - hole_diameter_normal: nominal hole diameter for a normal hole in mm
    - hole_diameter_oversized: nominal hole diameter for an oversized hole in mm
    """

    tensile_stress_area: MM2
    hole_diameter_normal: MM
    hole_diameter_oversized: MM


# Defines bolt parameters in a dictionary for each BoltSize using a named
# container which makes access clearer and improves readability.
_BOLT_PARAMETERS: dict[BoltSize, BoltParameters] = {
    BoltSize.M3: BoltParameters(5.0, 3.4, 3.6),
    BoltSize.M3_5: BoltParameters(6.8, 3.9, 4.2),
    BoltSize.M4: BoltParameters(8.8, 4.6, 4.8),
    BoltSize.M4_5: BoltParameters(11.3, 5.0, 5.3),
    BoltSize.M5: BoltParameters(14.2, 5.5, 5.8),
    BoltSize.M6: BoltParameters(20.1, 6.6, 7.0),
    BoltSize.M7: BoltParameters(28.9, 7.6, 8.0),
    BoltSize.M8: BoltParameters(36.6, 9.0, 10.0),
    BoltSize.M10: BoltParameters(58.0, 11.0, 12.0),
    BoltSize.M12: BoltParameters(84.3, 13.0, 14.5),
    BoltSize.M14: BoltParameters(115.0, 16.0, 18.0),
    BoltSize.M16: BoltParameters(157.0, 18.0, 20.0),
    BoltSize.M18: BoltParameters(192.0, 20.0, 22.0),
    BoltSize.M20: BoltParameters(245.0, 22.0, 24.0),
    BoltSize.M22: BoltParameters(303.0, 24.0, 26.0),
    BoltSize.M24: BoltParameters(353.0, 26.0, 28.0),
    BoltSize.M27: BoltParameters(459.0, 30.0, 32.0),
    BoltSize.M30: BoltParameters(561.0, 33.0, 36.0),
    BoltSize.M33: BoltParameters(694.0, 36.0, 38.0),
    BoltSize.M36: BoltParameters(817.0, 39.0, 42.0),
    BoltSize.M39: BoltParameters(976.0, 42.0, 45.0),
    BoltSize.M42: BoltParameters(1121.0, 45.0, 48.0),
    BoltSize.M45: BoltParameters(1306.0, 48.0, 52.0),
    BoltSize.M48: BoltParameters(1473.0, 51.0, 56.0),
    BoltSize.M52: BoltParameters(1758.0, 55.0, 62.0),
    BoltSize.M56: BoltParameters(2030.0, 59.0, 66.0),
    BoltSize.M60: BoltParameters(2362.0, 63.0, 70.0),
    BoltSize.M64: BoltParameters(2676.0, 67.0, 74.0),
    BoltSize.M68: BoltParameters(3060.0, 71.0, 78.0),
    BoltSize.M72: BoltParameters(3460.0, 75.0, 82.0),
    BoltSize.M76: BoltParameters(3889.0, 79.0, 86.0),
    BoltSize.M80: BoltParameters(4344.0, 83.0, 91.0),
    BoltSize.M85: BoltParameters(4948.0, 88.0, 96.0),
    BoltSize.M90: BoltParameters(5591.0, 93.0, 101.0),
    BoltSize.M95: BoltParameters(6276.0, 98.0, 107.0),
    BoltSize.M100: BoltParameters(6995.0, 104.0, 112.0),
    BoltSize.M105: BoltParameters(7755.0, 109.0, 117.0),
    BoltSize.M110: BoltParameters(8556.0, 114.0, 122.0),
    BoltSize.M115: BoltParameters(9395.0, 119.0, 127.0),
    BoltSize.M120: BoltParameters(10274.0, 124.0, 132.0),
    BoltSize.M125: BoltParameters(11191.0, 129.0, 137.0),
    BoltSize.M130: BoltParameters(12149.0, 134.0, 144.0),
    BoltSize.M140: BoltParameters(14181.0, 144.0, 155.0),
    BoltSize.M150: BoltParameters(16370.0, 155.0, 165.0),
}


class BoltPositionParallel(StrEnum):
    """Position of the bolt in the direction of load transfer, which selects the expression for alpha_d."""

    END = "End bolt"
    INNER = "Inner bolt"


class BoltPositionPerpendicular(StrEnum):
    """Position of the bolt perpendicular to the direction of load transfer, which selects the expression for k_1."""

    EDGE = "Edge bolt"
    INNER = "Inner bolt"


class HoleType(StrEnum):
    """Hole shape, with the reduction on the bearing resistance from note 1 of Table 3.4.

    The note reduces the bearing resistance to 0.8 times its value for a bolt in an oversized hole,
    and to 0.6 times its value for a slotted hole whose long axis is perpendicular to the
    direction of load transfer. It prints no factor for a slotted hole whose long axis is parallel to
    that direction, so that case is not offered here.
    """

    NORMAL = "Normal round hole"
    OVERSIZED = "Oversized hole"
    SLOTTED_PERPENDICULAR = "Slotted hole, long axis perpendicular to the load transfer"


class BoltCategory(StrEnum):
    """Bolt category, which selects the expression for alpha_b."""

    BEARING = "Bearing type"
    FRICTION = "Friction type"


class BoltGapFilling(StrEnum):
    """Whether the gap of the bolt hole is filled with resin or not. A filled gap would be an injection bolt."""

    EMPTY = "Empty gap"
    RESIN = "Gap filled with resin"


@dataclass(frozen=True)
class PlateAttachment:
    """Geometry of a bolt where it passes through a particular plate.

    This keeps plate-local geometric data (hole diameter, edge/spacing distances, plate
    thickness) separate from the bolt material and global bolt properties. Multiple
    attachments allow a single bolt to be referenced from several plates.

    Parameters
    ----------
    plate_id: str
        Arbitrary identifier for the plate (e.g. a name or index) that is meaningful to the
        caller. Used to later find the attachment for a specific plate.
    plate_thickness: MM | None
        Thickness of the plate the bolt passes through in mm. Optional when unknown.
    plate_material: SteelStrengthClass
        Material of the plate the bolt passes through. Default is S235.
    p1: MM | None
        Spacing to the next bolt in the loading direction (mm).
    e1: MM | None
        Edge distance to the plate edge in the loading direction (mm).
    p2: MM | None
        Spacing to the next bolt in the direction perpendicular to the load transfer (mm).
    e2: MM | None
        Edge distance to the plate edge in the direction perpendicular to the load transfer (mm).
    e3 : MM | None
        Edge distance to the plate edge in the direction perpendicular to the load transfer (mm).
        This is used for slotted holes where the long axis is perpendicular to the load transfer direction.
    e4 : MM | None
        Edge distance to the plate edge in the loading direction (mm).
        This is used for slotted holes where the long axis is perpendicular to the load transfer direction.
    hole_type: HoleType
        Shape/type of the hole (normal, oversized, slotted perpendicular). Default is normal.
    bolt_position_parallel: BoltPositionParallel
        Position of the bolt in the direction of load transfer (end or inner). Default is end.
    bolt_position_perpendicular: BoltPositionPerpendicular
        Position of the bolt perpendicular to the direction of load transfer (edge or inner). Default is edge.
    d0: MM | None
        Hole diameter in mm. Automatically set by BoltElement based on hole_type if not provided.
    gap_filling: BoltGapFilling | None
        Whether the bolt hole is gap filled (e.g. with resin) or empty.
    """

    plate_id: str
    plate_thickness: MM | None = None
    plate_material: SteelStrengthClass = SteelStrengthClass.S235
    p1: MM | None = None
    p2: MM | None = None
    e1: MM | None = None
    e2: MM | None = None
    e3: MM | None = None
    e4: MM | None = None
    hole_type: HoleType = HoleType.NORMAL
    bolt_position_parallel: BoltPositionParallel = BoltPositionParallel.END
    bolt_position_perpendicular: BoltPositionPerpendicular = BoltPositionPerpendicular.EDGE
    d0: MM | None = None
    gap_filling: BoltGapFilling | None = None


@dataclass(frozen=True)
class BoltElement:
    """Geometry record for an individual bolt coupled to a material.

    This class intentionally keeps material (a `FastenerMaterial`) separate from plate-local
    geometry (the `attachments` tuple). It is frozen and lightweight so callers can safely
    create many bolts and keep them in sequences or other containers.

    Parameters
    ----------
    material: FastenerMaterial
        The material object describing the bolt strength and deformation behaviour.
    size: BoltSize
        Standard ISO metric designation describing the nominal diameter and thread area.
    attachments: tuple[PlateAttachment, ...]
        One record per plate the bolt passes through. Defaults to an empty tuple.
    label: str | None
        Optional human-readable label for the bolt (e.g. "Bolt A1").
    preload_force: KN | None
        Prestressing (preload) force applied to the bolt [$kN$] (default: None, i.e. not preloaded).

    Example
    -------
    >>> from blueprints.materials.bolts import FastenerMaterial, FastenerClass
    ... from blueprints.structural_sections.bolts.bolt_geometry import BoltElement, BoltSize, PlateAttachment, HoleType
    ...
    ... s235 = SteelStrengthClass.S235
    ... bolt = BoltElement(
    ...     material=FastenerMaterial(bolt_class=FastenerClass.CLASS_8_8),
    ...     size=BoltSize.M20,
    ...     attachments=(
    ...         PlateAttachment(plate_id="P1", plate_thickness=20.0, plate_material=s235, hole_type=HoleType.NORMAL),
    ...         PlateAttachment(plate_id="P2", plate_thickness=15.0, plate_material=s235, hole_type=HoleType.OVERSIZED),
    ...         PlateAttachment(plate_id="P3", plate_thickness=10.0, plate_material=s235, hole_type=HoleType.SLOTTED_PERPENDICULAR),
    ...     ),
    ...     label="Bolt A1",
    ...     preload_force=50.0,  # kN
    ... )
    ... # Print the plate-provided hole diameter if present, otherwise a bolt-size recommendation.
    ... print(bolt.attachment_for_plate("P1").d0)
    """

    material: FastenerMaterial
    size: BoltSize
    attachments: tuple[PlateAttachment, ...] = field(default_factory=tuple)
    label: str | None = None
    preload_force: KN | None = None

    def __post_init__(self) -> None:
        """
        Checks if preload_force is set for a bolt that cannot be preloaded, and raises a ValueError if so.

        When a PlateAttachment is created without an explicit d0, computes and sets it based on the bolt
        size and the attachment's hole_type.
        """
        if self.material.can_be_preloaded is False and self.preload_force is not None:
            raise ValueError(f"Bolt class {self.material.bolt_class} cannot be preloaded.")

        updated_attachments = []
        for att in self.attachments:
            if att.d0 is None:
                # Compute d0 based on bolt size and hole type
                computed_d0 = self.size.hole_diameter_oversized if att.hole_type == HoleType.OVERSIZED else self.size.hole_diameter_normal
                # Create a new attachment with d0 set
                new_att = PlateAttachment(
                    plate_id=att.plate_id,
                    plate_thickness=att.plate_thickness,
                    plate_material=att.plate_material,
                    p1=att.p1,
                    p2=att.p2,
                    e1=att.e1,
                    e2=att.e2,
                    e3=att.e3,
                    e4=att.e4,
                    hole_type=att.hole_type,
                    d0=computed_d0,
                    gap_filling=att.gap_filling,
                )
                updated_attachments.append(new_att)
            else:
                updated_attachments.append(att)
        # Use object.__setattr__ because this dataclass is frozen
        object.__setattr__(self, "attachments", tuple(updated_attachments))

    @property
    def diameter(self) -> MM:
        """Nominal bolt diameter (mm)."""
        return self.size.diameter

    @property
    def gross_area(self) -> MM2:
        """Gross cross-sectional area of the bolt shank (mm^2)."""
        return self.size.gross_area

    @property
    def tensile_stress_area(self) -> MM2:
        """Tensile stress area of the threaded portion (mm^2)."""
        return self.size.tensile_stress_area

    def attachment_for_plate(self, plate_id: str) -> PlateAttachment | None:
        """Return the attachment record for the given `plate_id`, or None if missing."""
        for att in self.attachments:
            if att.plate_id == plate_id:
                return att
        return None
