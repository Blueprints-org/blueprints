"""Material properties handling for torsion analysis."""

from dataclasses import dataclass

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_6n import (
    Form6Dot6nStrengthReductionFactor,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_11abcn import (
    Form6Dot11abcNCompressionChordCoefficient,
)
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.type_alias import DIMENSIONLESS, MPA

from .torsion_geometry import TorsionGeometry


@dataclass(frozen=True)
class TorsionMaterials:
    """Handles material properties and design coefficients for torsional resistance analysis.

    This is a provisional interface for torsion material calculations of a `RectangularReinforcedCrossSection`.
    In later versions, this class might be discarded in favor of direct methods on the cross-section of rectangular,
    circular, or other reinforced concrete sections found in Blueprints.

    This class manages material properties of concrete and reinforcement steel,
    and calculates design coefficients required for torsion verification according
    to EN 1992-1-1:2004. It ensures material consistency across reinforcement
    types and provides standardized access to material properties.

    Parameters
    ----------
    cs : RectangularReinforcedCrossSection
        The reinforced concrete cross-section containing concrete material
        properties, longitudinal rebars, and stirrups with their respective
        material specifications.

    Notes
    -----
    - Validates that all rebars of same type use consistent materials
    - Calculates design coefficients based on concrete grade and stress state
    - Follows EN 1992-1-1:2004 material factor definitions
    - Frozen dataclass ensures immutable material properties

    Raises
    ------
    ValueError
        If no reinforcement is found or if mixed materials are used within
        the same reinforcement type (tension bars or stirrups).

    Examples
    --------
    >>> materials = TorsionMaterials(cs=cross_section)
    >>> steel_grade = materials.get_stirrup_material()
    >>> strength_factor = materials.strength_reduction_factor()
    """

    cs: RectangularReinforcedCrossSection

    def get_tension_rebar_material(self) -> ReinforcementSteelMaterial:
        """Return the material used for all tension rebars, ensuring material consistency.

        Identifies the material grade of tension reinforcement and validates that
        all tension bars use the same steel grade. This is required for consistent
        strength calculations and compliance with design assumptions.

        Returns
        -------
        ReinforcementSteelMaterial
            The material object containing properties like yield strength (f_yk),
            design strength (f_yd), and other steel characteristics.

        Raises
        ------
        ValueError
            If no tension rebars are found in the cross-section, or if multiple
            different steel grades are used among tension bars.

        Notes
        -----
        - Uses TorsionGeometry to identify tension reinforcement location
        - Essential for minimum reinforcement and capacity calculations
        - Mixed steel grades in tension zone are not permitted
        - Material properties affect both strength and ductility requirements

        Examples
        --------
        >>> tension_steel = materials.get_tension_rebar_material()
        >>> print(f"Tension steel grade: {tension_steel.name}")
        >>> print(f"Yield strength: {tension_steel.f_yk} MPa")
        """
        geometry = TorsionGeometry(self.cs)
        tension_rebars = geometry.get_tension_rebars()
        materials = {rebar.material for rebar in tension_rebars}

        if not materials:
            raise ValueError("No tension rebars found.")
        if len(materials) > 1:
            raise ValueError(f"Multiple materials found in tension rebars: {[m.name for m in materials]}")

        return materials.pop()

    def get_stirrup_material(self) -> ReinforcementSteelMaterial:
        """Return the material used for all stirrups, ensuring material consistency.

        Identifies the material grade of stirrup reinforcement and validates that
        all stirrups use the same steel grade. This is critical for accurate
        shear and torsion resistance calculations.

        Returns
        -------
        ReinforcementSteelMaterial
            The material object containing properties like yield strength (f_yk),
            design strength (f_yd), and other steel characteristics for stirrups.

        Raises
        ------
        ValueError
            If no stirrups are found in the cross-section, or if multiple
            different steel grades are used among stirrups.

        Notes
        -----
        - Critical for shear and torsion reinforcement design
        - Mixed stirrup grades within same section are not permitted
        - Stirrup material affects both shear and torsional resistance
        - Used in minimum reinforcement ratio calculations

        Examples
        --------
        >>> stirrup_steel = materials.get_stirrup_material()
        >>> print(f"Stirrup steel grade: {stirrup_steel.name}")
        >>> print(f"Design strength: {stirrup_steel.f_yd} MPa")
        """
        materials = {rebar.material for rebar in self.cs.stirrups}

        if not materials:
            raise ValueError("No stirrups found.")
        if len(materials) > 1:
            raise ValueError(f"Multiple materials found in stirrups: {[m.name for m in materials]}")

        return materials.pop()

    def compression_chord_coefficient(self, sigma_cp: MPA | None) -> Form6Dot11abcNCompressionChordCoefficient | DIMENSIONLESS:
        """Calculate compression chord coefficient accounting for prestressing effects.

        Determines the coefficient `α_cw` that accounts for the state of stress in
        the compression chord according to EN 1992-1-1:2004 art. 6.2.3(3).
        This coefficient modifies concrete strength based on axial compression.

        Parameters
        ----------
        sigma_cp : MPA | None
            Mean compressive stress in concrete due to design axial force,
            measured at the centroidal axis. If None or non-positive,
            no axial compression effects are considered.

        Returns
        -------
        Form6Dot11abcNCompressionChordCoefficient | DIMENSIONLESS
            - 1.0 if no significant compression (conservative default)
            - Calculated coefficient (>1.0) if compression enhances concrete strength

        Notes
        -----
        - Accounts for beneficial effects of axial compression on concrete strength
        - Based on EN 1992-1-1:2004 formula 6.11abc
        - Higher compression increases concrete shear/torsion resistance
        - Conservative approach returns 1.0 when compression is negligible

        Examples
        --------
        >>> # No axial compression
        >>> alpha_cw = materials.compression_chord_coefficient(sigma_cp=None)
        >>> # With compression
        >>> alpha_cw = materials.compression_chord_coefficient(sigma_cp=2.5)
        """
        if sigma_cp is None or sigma_cp <= 0:
            return 1.0
        return Form6Dot11abcNCompressionChordCoefficient(
            sigma_cp=sigma_cp,
            f_cd=self.cs.concrete_material.f_cd,
        )

    def strength_reduction_factor(self) -> Form6Dot6nStrengthReductionFactor:
        """Calculate strength reduction factor for concrete cracked in shear (nu).

        Determines the factor ν1 that accounts for the reduction in concrete
        compressive strength due to transverse tensile strains from shear
        cracking, according to EN 1992-1-1:2004 art. 6.2.2(6).

        Returns
        -------
        Form6Dot6nStrengthReductionFactor
            Reduction factor (≤1.0) that modifies concrete compressive strength
            in members with significant shear. Lower values indicate greater
            strength reduction due to cracking effects.

        Notes
        -----
        - Based on EN 1992-1-1:2004 formula 6.6N
        - Accounts for softening of concrete due to transverse cracking
        - Higher concrete grades experience less reduction
        - Critical for maximum shear resistance calculations (V_Rd,max)
        - Used in both shear and torsional resistance evaluations

        Examples
        --------
        >>> nu_1 = materials.strength_reduction_factor()
        >>> print(f"Concrete strength reduction factor: {nu_1:.3f}")
        >>> # Higher f_ck results in higher nu_1 (less reduction)
        """
        return Form6Dot6nStrengthReductionFactor(f_ck=self.cs.concrete_material.f_ck)
