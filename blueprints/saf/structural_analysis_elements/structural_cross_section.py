"""Cross-section definition for structural analysis following SAF specification.

A cross-section together with material is a basic property of a 1D member.
"""

from dataclasses import dataclass
from enum import Enum


class CrossSectionType(str, Enum):
    """Cross-section type classification following SAF specification.

    Defines how the cross-section geometry is specified.
    """

    GENERAL = "General"
    PARAMETRIC = "Parametric"
    MANUFACTURED = "Manufactured"
    COMPOUND = "Compound"


class ShapeType(str, Enum):
    """Geometric profile shape following SAF specification.

    Used for parametric and compound cross-section types.
    """

    T_SECTION = "T Section"
    I_SECTION = "I Section"
    RECTANGULAR = "Rectangular"
    CIRCULAR = "Circular"
    L_SECTION = "L Section"
    CHANNEL = "Channel"
    ANGLE = "Angle"
    CUSTOM = "Custom"


class FormCode(str, Enum):
    """Form code identifying profile characteristics following SAF specification.

    Used for manufactured cross-section types to identify hot rolled or cold formed profiles.
    """

    HOT_ROLLED = "1"
    COLD_FORMED = "2"


@dataclass(frozen=True)
class StructuralCrossSection:
    """Structural cross-section definition following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralcrosssection.html.

    A cross-section together with material is a basic property of a 1D member.
    This class defines the geometry and properties of a cross-section.

    Attributes
    ----------
    name : str
        Unique identifier for the cross-section (e.g., "CS1", "HEB180").
    material : str
        Reference(s) to StructuralMaterial name(s). Multiple materials separated by semicolons.
    cross_section_type : CrossSectionType
        Category of profile definition: General, Parametric, Manufactured, Compound.
    shape : ShapeType, optional
        Geometric profile shape. Required for Parametric or Compound types.
    parameters : str, optional
        Dimension values in mm; semicolon-delimited (e.g., "50; 80; 500; 450").
        Required for Parametric type.
    profile : str, optional
        Industrial profile name or CompositeShapeDef reference (e.g., "HEB180").
        Required for General type. Optional for Manufactured type.
    form_code : FormCode, optional
        Identifies hot rolled (1) or cold formed (2) profiles.
        Required for Manufactured type.
    description_id : int, optional
        Manufacturer source reference code.
    a : float, optional
        Cross-sectional area in m².
    iy : float, optional
        Moment of inertia around y-axis in m⁴.
    iz : float, optional
        Moment of inertia around z-axis in m⁴.
    it : float, optional
        Torsional moment of inertia in m⁴.
    iw : float, optional
        Warping constant in m⁶.
    wply : float, optional
        Plastic modulus around y-axis in m³.
    wplz : float, optional
        Plastic modulus around z-axis in m³.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name or material is empty.
        If conditional attributes are missing based on cross_section_type.
        If geometric properties are negative.

    Examples
    --------
    >>> from blueprints.saf import StructuralCrossSection, CrossSectionType
    >>> # General cross-section (composite shape)
    >>> cs_general = StructuralCrossSection(
    ...     name="GEN_1",
    ...     material="Steel",
    ...     cross_section_type=CrossSectionType.GENERAL,
    ...     profile="GEN_1",
    ...     a=0.075484,
    ...     iy=0.000641,
    ...     iz=0.013319,
    ...     it=0.0000591,
    ... )

    >>> # Parametric cross-section
    >>> cs_param = StructuralCrossSection(
    ...     name="CS_RECT",
    ...     material="Steel",
    ...     cross_section_type=CrossSectionType.PARAMETRIC,
    ...     shape=ShapeType.RECTANGULAR,
    ...     parameters="200; 100",
    ... )

    >>> # Manufactured cross-section
    >>> from blueprints.saf import FormCode
    >>> cs_mfg = StructuralCrossSection(
    ...     name="HEB180",
    ...     material="S235",
    ...     cross_section_type=CrossSectionType.MANUFACTURED,
    ...     profile="HEB180",
    ...     form_code=FormCode.HOT_ROLLED,
    ...     a=0.065,
    ...     iy=0.000682,
    ...     iz=0.003831,
    ... )
    """

    name: str
    material: str
    cross_section_type: CrossSectionType
    shape: ShapeType | None = None
    parameters: str = ""
    profile: str = ""
    form_code: FormCode | None = None
    description_id: int | None = None
    a: float | None = None
    iy: float | None = None
    iz: float | None = None
    it: float | None = None
    iw: float | None = None
    wply: float | None = None
    wplz: float | None = None
    id: str = ""

    def __post_init__(self) -> None:
        """Validate cross-section properties based on type.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.material:
            raise ValueError("material cannot be empty")

        # Validate based on cross-section type
        if self.cross_section_type == CrossSectionType.PARAMETRIC:
            self._validate_parametric()
        elif self.cross_section_type == CrossSectionType.MANUFACTURED:
            self._validate_manufactured()
        elif self.cross_section_type == CrossSectionType.GENERAL:
            self._validate_general()
        elif self.cross_section_type == CrossSectionType.COMPOUND:
            self._validate_compound()

        # Validate geometric properties (must be positive if provided)
        self._validate_geometric_properties()

    def _validate_parametric(self) -> None:
        """Validate Parametric type requirements.

        Raises
        ------
        ValueError
            If required attributes are missing.
        """
        if self.shape is None:
            raise ValueError("shape must be specified when cross_section_type = PARAMETRIC")
        if not self.parameters:
            raise ValueError("parameters must be specified when cross_section_type = PARAMETRIC")

    def _validate_manufactured(self) -> None:
        """Validate Manufactured type requirements.

        Raises
        ------
        ValueError
            If required attributes are missing.
        """
        if self.form_code is None:
            raise ValueError("form_code must be specified when cross_section_type = MANUFACTURED")

    def _validate_general(self) -> None:
        """Validate General type requirements.

        Raises
        ------
        ValueError
            If required attributes are missing.
        """
        if not self.profile:
            raise ValueError("profile must be specified when cross_section_type = GENERAL (should reference CompositeShapeDef)")

    def _validate_compound(self) -> None:
        """Validate Compound type requirements.

        Raises
        ------
        ValueError
            If required attributes are missing.
        """
        if self.shape is None:
            raise ValueError("shape must be specified when cross_section_type = COMPOUND")
        if not self.parameters:
            raise ValueError("parameters must be specified when cross_section_type = COMPOUND")

    def _validate_geometric_properties(self) -> None:
        """Validate that all geometric properties are non-negative if provided.

        Raises
        ------
        ValueError
            If any geometric property is negative.
        """
        properties = [
            ("a", self.a),
            ("iy", self.iy),
            ("iz", self.iz),
            ("it", self.it),
            ("iw", self.iw),
            ("wply", self.wply),
            ("wplz", self.wplz),
        ]

        for prop_name, prop_value in properties:
            if prop_value is not None and prop_value < 0:
                raise ValueError(f"{prop_name} must be non-negative if specified")
