"""Structural surface action thermal (thermal load) definitions following SAF specification.

Thermal actions represent temperature changes applied to 2D members (slabs, walls, plates).
"""

from dataclasses import dataclass
from enum import Enum


class Variation(str, Enum):
    """Temperature variation type following SAF specification.

    Specifies whether the temperature is constant or varies linearly across the surface.
    """

    CONSTANT = "Constant"
    LINEAR = "Linear"


@dataclass(frozen=True)
class StructuralSurfaceActionThermal:
    """Structural surface action thermal following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralsurfaceactionthermal.html.

    A thermal surface action represents a temperature change applied to a 2D member. The temperature
    can be constant across the surface or vary linearly (e.g., different temperatures on top and
    bottom surfaces).

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "LT1").
    variation : Variation
        Temperature variation type: Constant or Linear.
    temp_t : float
        Temperature at top surface in degrees Celsius/Fahrenheit.
        For Constant variation: represents the center plane temperature.
        For Linear variation: represents the top surface temperature.
    load_case : str
        Reference to StructuralLoadCase name.
    two_d_member : str
        2D member name (StructuralSurfaceMember or StructuralSurfaceActionDistribution).
    temp_b : float | None, optional
        Temperature at bottom surface in degrees Celsius/Fahrenheit.
        Required only when variation = LINEAR.
    two_d_member_region : str, optional
        Region name (StructuralSurfaceMemberRegion). Used when load applies to specific region.
    parent_id : str, optional
        UUID for segmented curved geometry tracking.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If variation = LINEAR but temp_b is not specified.

    Examples
    --------
    >>> from blueprints.saf import StructuralSurfaceActionThermal, Variation
    >>> # Constant temperature across surface
    >>> thermal_constant = StructuralSurfaceActionThermal(
    ...     name="LT1",
    ...     variation=Variation.CONSTANT,
    ...     temp_t=25.0,
    ...     load_case="LC1",
    ...     two_d_member="S1",
    ... )

    >>> # Linear temperature variation (top to bottom)
    >>> thermal_linear = StructuralSurfaceActionThermal(
    ...     name="LT2",
    ...     variation=Variation.LINEAR,
    ...     temp_t=30.0,
    ...     temp_b=10.0,
    ...     load_case="LC1",
    ...     two_d_member="S1",
    ... )

    >>> # Thermal load on specific region
    >>> thermal_region = StructuralSurfaceActionThermal(
    ...     name="LT3",
    ...     variation=Variation.CONSTANT,
    ...     temp_t=20.0,
    ...     load_case="LC2",
    ...     two_d_member="S2",
    ...     two_d_member_region="R1",
    ... )
    """

    name: str
    variation: Variation
    temp_t: float
    load_case: str
    two_d_member: str
    temp_b: float | None = None
    two_d_member_region: str = ""
    parent_id: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_variation_requirements()

    def _validate_variation_requirements(self) -> None:
        """Validate requirements based on variation type."""
        if self.variation == Variation.LINEAR and self.temp_b is None:
            raise ValueError("temp_b must be specified when variation = Variation.LINEAR")
