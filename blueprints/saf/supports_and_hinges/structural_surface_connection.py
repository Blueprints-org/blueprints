"""Structural surface connection definitions following SAF specification.

Surface connections define structural supports provided by planar elements,
typically modeling interaction between structures and subsoil through elastic
foundation parameters.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class StructuralSurfaceConnection:
    """Structural surface connection following SAF specification.

    Definition following https://www.saf.guide/en/stable/supports-and-hinges/structuralsurfaceconnection.html.

    Defines structural supports provided by planar elements, typically modeling
    interaction between structures and subsoil through elastic foundation parameters.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "Sn6").
    two_d_member : str
        Reference to StructuralSurfaceMember identifier (e.g., "S13").
    subsoil : str
        Type designation of subsoil (e.g., "Gravel").
    c1x : float
        Resistance to deformation in local x-direction in MN/m³.
    c1y : float
        Resistance to deformation in local y-direction in MN/m³.
    c1z : float
        Resistance to deformation in local z-direction in MN/m³.
    c2x : float
        Resistance to zP/xP angular deformation in MN/m.
    c2y : float
        Resistance to zP/yP angular deformation in MN/m.
    two_d_member_region : str, optional
        Reference to StructuralSurfaceMemberRegion if available.
    description : str, optional
        Subsoil characteristics description (e.g., "Loam/Very sandy").
    c1z_spring : str, optional
        Linearity option for C1z (non-linear unsupported).
    parent_id : str, optional
        Tracks segmented curved geometry for round-trip imports (UUID format).
    id : str, optional
        Unique identifier (UUID format recommended).

    Examples
    --------
    >>> from blueprints.saf import StructuralSurfaceConnection
    >>> # Surface connection with elastic foundation parameters
    >>> connection = StructuralSurfaceConnection(
    ...     name="Sn6",
    ...     two_d_member="S13",
    ...     subsoil="Gravel",
    ...     c1x=80.5,
    ...     c1y=35.5,
    ...     c1z=50.0,
    ...     c2x=15.5,
    ...     c2y=10.2,
    ...     description="Sandy gravel",
    ... )
    """

    name: str
    two_d_member: str
    subsoil: str
    c1x: float
    c1y: float
    c1z: float
    c2x: float
    c2y: float
    two_d_member_region: str | None = None
    description: str = ""
    c1z_spring: str | None = None
    parent_id: str | None = None
    id: str = ""
