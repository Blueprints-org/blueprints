"""Material definition for structural analysis following SAF specification.

A material definition with properties such as elasticity modulus, density,
and design properties for structural analysis.
"""

from dataclasses import dataclass
from enum import Enum


class MaterialType(str, Enum):
    """Material type classification following SAF specification.

    Defines the material category for structural analysis.
    """

    CONCRETE = "Concrete"
    STEEL = "Steel"
    TIMBER = "Timber"
    ALUMINIUM = "Aluminium"
    MASONRY = "Masonry"
    OTHER = "Other"


@dataclass(frozen=True)
class StructuralMaterial:
    """Structural material definition following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralmaterial.html.

    Defines material properties for use in structural cross-sections and analysis.
    Properties include mechanical characteristics such as elasticity modulus,
    shear modulus, density, and thermal properties.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "S235", "C25/30").
        Should match the quality designation for consistency.
    material_type : MaterialType
        Material classification: Concrete, Steel, Timber, Aluminium, Masonry, Other.
    quality : str
        Standard grade designation (e.g., "S235", "C25/30", "C18").
    subtype : str, optional
        Classification such as "Hot rolled" or "Cold formed".
    unit_mass : float, optional
        Self-weight measured in kg/m³.
    e_modulus : float, optional
        Young's modulus of elasticity in MPa.
    g_modulus : float, optional
        Shear modulus (modulus of rigidity) in MPa.
    poisson_coefficient : float, optional
        Poisson's ratio (dimensionless) typically 0-0.5.
    thermal_expansion : float, optional
        Coefficient of thermal expansion in 1/K.
    design_properties : str, optional
        Custom characteristics formatted as "label|value" pairs separated by semicolons.
        Example: "Fy|355;Fu|510" for yield and ultimate strengths.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name or quality is empty.
        If elastic moduli or coefficients have invalid values.

    Examples
    --------
    >>> from blueprints.saf import StructuralMaterial, MaterialType
    >>> # Steel material
    >>> steel = StructuralMaterial(
    ...     name="S235",
    ...     material_type=MaterialType.STEEL,
    ...     quality="S235",
    ...     subtype="Hot rolled",
    ...     unit_mass=7850.0,
    ...     e_modulus=210000.0,
    ...     g_modulus=81000.0,
    ...     poisson_coefficient=0.3,
    ...     thermal_expansion=1.2e-5,
    ... )

    >>> # Concrete material
    >>> concrete = StructuralMaterial(
    ...     name="C25/30",
    ...     material_type=MaterialType.CONCRETE,
    ...     quality="C25/30",
    ...     unit_mass=2400.0,
    ...     e_modulus=31000.0,
    ...     design_properties="fck|25;fcm|33",
    ... )
    """

    name: str
    material_type: MaterialType
    quality: str
    subtype: str = ""
    unit_mass: float | None = None
    e_modulus: float | None = None
    g_modulus: float | None = None
    poisson_coefficient: float | None = None
    thermal_expansion: float | None = None
    design_properties: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate material properties.

        Raises
        ------
        ValueError
            If required fields are empty or properties have invalid values.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.quality:
            raise ValueError("quality cannot be empty")

        # Validate optional moduli (must be positive if provided)
        if self.e_modulus is not None and self.e_modulus <= 0:
            raise ValueError("e_modulus must be positive if specified")
        if self.g_modulus is not None and self.g_modulus <= 0:
            raise ValueError("g_modulus must be positive if specified")

        # Validate Poisson coefficient (typically 0 to 0.5)
        if self.poisson_coefficient is not None and (self.poisson_coefficient < 0 or self.poisson_coefficient > 0.5):
            raise ValueError("poisson_coefficient must be between 0 and 0.5 if specified")

        # Validate thermal expansion (must be positive)
        if self.thermal_expansion is not None and self.thermal_expansion <= 0:
            raise ValueError("thermal_expansion must be positive if specified")

        # Validate unit mass (must be positive)
        if self.unit_mass is not None and self.unit_mass <= 0:
            raise ValueError("unit_mass must be positive if specified")

        # Validate design properties format
        if self.design_properties:
            self._validate_design_properties()

    def _validate_design_properties(self) -> None:
        """Validate design properties format.

        Format: "label|value" pairs separated by semicolons.
        Example: "Fy|355;Fu|510"

        Raises
        ------
        ValueError
            If format is invalid.
        """
        properties = self.design_properties.split(";")
        for prop_raw in properties:
            prop = prop_raw.strip()
            if not prop:
                continue
            if "|" not in prop:
                raise ValueError(f'Invalid design property format "{prop}". Expected "label|value" format.')
            parts = prop.split("|")
            if len(parts) != 2:
                raise ValueError(f'Invalid design property format "{prop}". Should contain exactly one "|" separator.')
            label, value = parts
            if not label.strip() or not value.strip():
                raise ValueError(f'Invalid design property format "{prop}". Label and value cannot be empty.')
