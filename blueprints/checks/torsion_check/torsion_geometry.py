"""Geometric calculations for torsion analysis."""

from dataclasses import dataclass

from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.type_alias import MM, MM2


@dataclass(frozen=True)
class TorsionGeometry:
    """Handles geometric calculations and dimensional properties for torsion analysis.

    This is a provisional interface for torsion geometry calculations of a `RectangularReinforcedCrossSection`.
    In later versions, this class might be discarded in favor of direct methods on the cross-section of rectangular,
    circular, or other reinforced concrete sections found in Blueprints.

    This class provides methods to calculate critical geometric parameters required
    for torsional resistance verification according to EN 1992-1-1:2004. It operates
    on reinforced concrete rectangular cross-sections and computes properties like
    effective depth, lever arms, wall thickness, and enclosed areas.

    Parameters
    ----------
    cs : RectangularReinforcedCrossSection
        The reinforced concrete cross-section to analyze. Must contain concrete
        material properties, reinforcement layout, and geometric dimensions.

    Notes
    -----
    - All calculations assume rectangular cross-sections
    - Methods follow EN 1992-1-1:2004 geometric definitions
    - Frozen dataclass ensures immutable geometric properties
    - Works with blueprints structural sections framework

    Examples
    --------
    >>> from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
    >>> geometry = TorsionGeometry(cs=cross_section)
    >>> effective_depth = geometry.effective_depth()
    >>> enclosed_area = geometry.enclosed_area()
    """

    cs: RectangularReinforcedCrossSection

    def get_tension_rebars(self) -> list[Rebar]:
        """Get the tension reinforcement rebars in the cross-section.

        Identifies the longitudinal reinforcement bars located at the tensile
        edge (bottom) of the cross-section. These bars are assumed to be in
        the tension zone for typical loading conditions.

        Returns
        -------
        list[Rebar]
            List of reinforcement bars positioned at the lowest vertical
            coordinate (y-position) within the cross-section.

        Notes
        -----
        - Important: Assumes simple bending with tension at bottom edge
        - In future versions, actual force analysis will be considered
        - Uses 1e-3 tolerance to group bars at same vertical level
        - Required for minimum tensile reinforcement calculations

        Examples
        --------
        >>> tension_bars = geometry.get_tension_rebars()
        >>> total_tension_area = sum(bar.area for bar in tension_bars)
        """
        lower_y = min(rebar.y for rebar in self.cs.longitudinal_rebars)
        return [rebar for rebar in self.cs.longitudinal_rebars if abs(rebar.y - lower_y) < 1e-3]

    def get_c_nom_center(self) -> MM:
        """Get the distance between edge and centre of the longitudinal reinforcement.

        Calculates the concrete cover distance from the bottom edge of the cross-section
        to the center of the tension reinforcement. Uses the thickest bottom bar to
        determine the representative cover distance.

        Returns
        -------
        MM
            Distance from concrete edge to rebar center [mm]. This includes
            the nominal cover plus half the diameter of the thickest tension bar.

        Notes
        -----
        - Important: Uses thickest tension bar for most conservative cover estimate
        - In later versions, actual force analysis will refine this
        - Critical for effective depth and lever arm calculations
        - Affects both strength and serviceability calculations
        - Assumes standard concrete cover requirements are met

        Examples
        --------
        >>> cover_distance = geometry.get_c_nom_center()
        >>> print(f"Concrete cover to bar center: {cover_distance:.1f} mm")
        """
        thickest_rebar = max(self.get_tension_rebars(), key=lambda r: r.diameter)
        cs_lower_edge = min(pt[1] for pt in self.cs.cross_section.polygon.exterior.coords)
        return abs(thickest_rebar.y - cs_lower_edge)

    def effective_depth(self) -> MM:
        """Get effective cross-section depth for structural calculations.

        Calculates the distance from the compression face to the center of the
        tension reinforcement. This is the primary dimension used in bending,
        shear, and torsion resistance calculations.

        Returns
        -------
        MM
            Effective depth [mm], calculated as total height minus concrete
            cover to center of tension reinforcement.

        Notes
        -----
        - Fundamental parameter for all strength calculations
        - Used in shear span ratios and size effect factors
        - Affects lever arms and moment resistance
        - Critical input for minimum reinforcement requirements

        Examples
        --------
        >>> d = geometry.effective_depth()
        >>> print(f"Effective depth: {d:.1f} mm")
        """
        return self.cs.height - self.get_c_nom_center()

    def lever_arm(self) -> MM:
        """Get the internal lever arm for moment and shear resistance calculations.

        Calculates the approximate distance between the centers of compression
        and tension forces in the cross-section. Uses the simplified assumption
        of **0.9 times the effective depth**, which is commonly used in design.

        Returns
        -------
        MM
            Internal lever arm [mm], calculated as **0.9 × effective depth**.
            Represents the moment arm between compression and tension resultants.

        Notes
        -----
        - Simplified assumption: z = 0.9 × d (conservative approximation)
        - Used in shear reinforcement design calculations
        - More precise calculations would consider actual stress distribution
        - Standard approximation for preliminary design and checking

        Examples
        --------
        >>> z = geometry.lever_arm()
        >>> print(f"Lever arm: {z:.1f} mm")
        """
        return 0.9 * self.effective_depth()

    def effective_wall_thickness(self) -> MM:
        """Calculate the effective wall thickness for torsion analysis (t_eff_i).

        Based on EN 1992-1-1:2004 art. 6.3.2(1)

        Determines the representative thickness of the cross-section walls for
        torsional resistance calculations. Uses the more conservative value between
        the area-to-perimeter ratio and twice the concrete cover.

        Returns
        -------
        MM
            Effective wall thickness [mm]. This represents the thickness of an
            equivalent thin-walled section for torsion calculations.

        Notes
        -----
        - Based on EN 1992-1-1:2004 torsion theory
        - Uses max(A/perimeter, 2×cover) for solid sections
        - Critical parameter for enclosed area and torsional resistance
        - Affects distribution of torsional shear stresses

        Examples
        --------
        >>> t_eff = geometry.effective_wall_thickness()
        >>> print(f"Effective wall thickness: {t_eff:.1f} mm")
        """
        return max(self.cs.cross_section.area / self.cs.cross_section.perimeter, 2 * self.get_c_nom_center())

    def enclosed_area(self) -> MM2:
        """Calculate the area enclosed by the center-lines of the connecting walls (A_k).

        Based on EN 1992-1-1:2004 art. 6.3.2(1)

        Computes the area inside the cross-section boundaries reduced by the
        effective wall thickness. This area is used in torsional shear stress
        calculations and represents the area bounded by the centerlines of the
        effective wall thickness.

        Returns
        -------
        MM2
            Enclosed area [mm²] calculated as:
            (width - t_eff) × (height - t_eff)

        Notes
        -----
        - Key parameter in torsional resistance calculations
        - Used to calculate torsional shear flow and stresses
        - Based on thin-walled cross-section theory (EN 1992-1-1:2004 art. 6.3.2(1))
        - Affects torsional cracking moment and ultimate resistance

        Examples
        --------
        >>> a_k = geometry.enclosed_area()
        >>> print(f"Enclosed area: {a_k:.0f} mm²")
        """
        t_ef = self.effective_wall_thickness()
        return (self.cs.width - t_ef) * (self.cs.height - t_ef)

    def perimeter(self) -> MM:
        """Calculate the perimeter of the enclosed area center-line (u_k).

        Computes the perimeter of the area enclosed by the center-lines of the
        effective wall thickness. This perimeter is used in torsional shear
        stress calculations and stirrup spacing requirements.

        Returns
        -------
        MM
            Perimeter [mm] calculated as:
            2 × (width + height - 2 × t_eff)

        Notes
        -----
        - Used in torsional shear flow calculations
        - Critical for stirrup spacing limitations
        - Based on thin-walled cross-section theory (EN 1992-1-1:2004 art. 6.3.2(1))

        Examples
        --------
        >>> perimeter = geometry.perimeter()
        >>> max_stirrup_spacing = perimeter / 8
        >>> print(f"Enclosed perimeter: {perimeter:.1f} mm")
        """
        t_ef = self.effective_wall_thickness()
        return 2 * (self.cs.width + self.cs.height - 2 * t_ef)
