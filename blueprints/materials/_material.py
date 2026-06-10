"""Generic material contract shared by all Blueprints materials."""

from typing import Protocol, runtime_checkable

from blueprints.type_alias import KG_M3, MPA, RATIO


@runtime_checkable
class Material(Protocol):
    """Minimal physical contract that every Blueprints material satisfies.

    Materials are implemented as code-agnostic data carriers: a material stores only
    physical properties and does not know how it was constructed. This protocol defines
    the basic properties required for any finite-element or section calculation,
    regardless of the material type (concrete, steel, reinforcement, ...).

    Material-specific strength properties are intentionally not part of this protocol
    because their shape differs per material (e.g. scalar strengths for concrete versus
    thickness-dependent strengths for steel).

    Notes
    -----
    - Structural subtyping (``typing.Protocol``); no inheritance is required.
    - Use ``isinstance(material, Material)`` to check conformance at runtime.
    """

    @property
    def name(self) -> str:
        """Name of the material.

        Returns
        -------
        str
            Identifying name of the material.
        """
        ...

    @property
    def density(self) -> KG_M3:
        """Density of the material.

        Returns
        -------
        KG_M3
            Density of the material in [$kg/m^3$].
        """
        ...

    @property
    def modulus_of_elasticity(self) -> MPA:
        """Modulus of elasticity of the material.

        Returns
        -------
        MPA
            Modulus of elasticity of the material in [$MPa$].
        """
        ...

    @property
    def poisson_ratio(self) -> RATIO:
        """Poisson's ratio of the material in the elastic range.

        Returns
        -------
        RATIO
            Poisson's ratio of the material [$-$].
        """
        ...

    @property
    def shear_modulus(self) -> MPA:
        """Shear modulus of the material.

        Returns
        -------
        MPA
            Shear modulus of the material in [$MPa$].
        """
        ...
