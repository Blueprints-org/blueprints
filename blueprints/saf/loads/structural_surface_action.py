"""Structural surface action (surface load) definitions following SAF specification.

Surface actions represent distributed surface loads applied to 2D members (slabs, walls, plates).
"""

from dataclasses import dataclass
from enum import Enum


class Direction(str, Enum):
    """Direction of surface action following SAF specification.

    Specifies the load direction (X, Y, or Z axis).
    """

    X = "X"
    Y = "Y"
    Z = "Z"


class ForceAction(str, Enum):
    """Type of surface action application following SAF specification.

    Specifies where the load is applied on the 2D member.
    """

    ON_2D_MEMBER = "On 2D member"
    ON_2D_MEMBER_REGION = "On 2D member region"
    ON_2D_MEMBER_DISTRIBUTION = "On 2D member distribution"


class CoordinateSystem(str, Enum):
    """Coordinate system for surface action following SAF specification.

    Global or local coordinate system reference. Local uses the member's coordinate system.
    """

    GLOBAL = "Global"
    LOCAL = "Local"


class Location(str, Enum):
    """Location type for surface action application following SAF specification.

    Specifies whether load is applied based on length or projection.
    """

    LENGTH = "Length"
    PROJECTION = "Projection"


@dataclass(frozen=True)
class StructuralSurfaceAction:
    """Structural surface action (surface load) following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralsurfaceaction.html.

    A surface action represents a distributed surface load applied to a 2D member (plate, slab,
    wall). The load is automatically applied to the entire surface or a specific region/distribution.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "PF3").
    direction : Direction
        Load direction: X, Y, or Z.
    force_action : ForceAction
        Target type: On 2D member, On 2D member region, or On 2D member distribution.
    value : float
        Load magnitude in kN/m². Positive or negative values indicate load direction.
    load_case : str
        Reference to StructuralLoadCase name.
    coordinate_system : CoordinateSystem
        Global or Local coordinate system. Local uses member's coordinate system.
    location : Location
        Load application method: Length or Projection (for inclined surfaces).
    two_d_member : str, optional
        2D member name (StructuralSurfaceMember). Required when force_action = ON_2D_MEMBER.
    two_d_member_region : str, optional
        Region name (StructuralSurfaceMemberRegion). Required when force_action = ON_2D_MEMBER_REGION.
    two_d_member_distribution : str, optional
        Distribution name (StructuralSurfaceActionDistribution). Required when force_action = ON_2D_MEMBER_DISTRIBUTION.
    action_type : str, optional
        Load classification (e.g., "Standard", "Wind", "Snow", "Self weight").
    parent_id : str, optional
        UUID for segmented curved geometry tracking.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If force_action = ON_2D_MEMBER but two_d_member is not specified.
        If force_action = ON_2D_MEMBER_REGION but two_d_member_region is not specified.
        If force_action = ON_2D_MEMBER_DISTRIBUTION but two_d_member_distribution is not specified.

    Examples
    --------
    >>> from blueprints.saf import StructuralSurfaceAction, Direction, ForceAction, CoordinateSystem, Location
    >>> # Surface load on entire 2D member
    >>> load = StructuralSurfaceAction(
    ...     name="PF1",
    ...     direction=Direction.Z,
    ...     force_action=ForceAction.ON_2D_MEMBER,
    ...     value=-10.0,
    ...     load_case="LC1",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.LENGTH,
    ...     two_d_member="S1",
    ... )

    >>> # Surface load on specific region
    >>> regional_load = StructuralSurfaceAction(
    ...     name="PF2",
    ...     direction=Direction.Z,
    ...     force_action=ForceAction.ON_2D_MEMBER_REGION,
    ...     value=-15.0,
    ...     load_case="LC1",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.PROJECTION,
    ...     two_d_member_region="R1",
    ... )
    """

    name: str
    direction: Direction
    force_action: ForceAction
    value: float
    load_case: str
    coordinate_system: CoordinateSystem
    location: Location
    two_d_member: str = ""
    two_d_member_region: str = ""
    two_d_member_distribution: str = ""
    action_type: str = ""
    parent_id: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_force_action_requirements()

    def _validate_force_action_requirements(self) -> None:
        """Validate requirements based on force_action type."""
        if self.force_action == ForceAction.ON_2D_MEMBER and not self.two_d_member:
            raise ValueError("two_d_member must be specified when force_action = ForceAction.ON_2D_MEMBER")
        if self.force_action == ForceAction.ON_2D_MEMBER_REGION and not self.two_d_member_region:
            raise ValueError("two_d_member_region must be specified when force_action = ForceAction.ON_2D_MEMBER_REGION")
        if self.force_action == ForceAction.ON_2D_MEMBER_DISTRIBUTION and not self.two_d_member_distribution:
            raise ValueError("two_d_member_distribution must be specified when force_action = ForceAction.ON_2D_MEMBER_DISTRIBUTION")
