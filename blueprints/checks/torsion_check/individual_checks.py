"""Individual check classes for torsion analysis."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_2 import (
    Form6Dot2aSub1ThicknessFactor,
    Form6Dot2aSub2RebarRatio,
    Form6Dot2ShearResistance,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_3n import (
    Form6Dot3NShearCapacityWithoutRebar,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_9 import (
    Form6Dot9MaximumShearResistance,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_26 import (
    Form6Dot26ShearStressInWall,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_27 import (
    Form6Dot27ShearForceInWall,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_29 import (
    Form6Dot29CheckTorsionShearResistance,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_30 import (
    Form6Dot30DesignTorsionalResistanceMoment,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_31 import (
    Form6Dot31CheckTorsionShearResistanceRectangular,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_1n import Form9Dot1nMinimumTensileReinforcementBeam
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_4 import Form9Dot4ShearReinforcementRatio
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_5n import Form9Dot5nMinimumShearReinforcementRatio
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_6n import (
    Form9Dot6nMaximumDistanceShearReinforcement,
)
from blueprints.math_helpers import cot
from blueprints.unit_conversion import MM_TO_M

from .check_result import CheckResult
from .torsion_forces import TorsionForces
from .torsion_geometry import TorsionGeometry
from .torsion_materials import TorsionMaterials


class TorsionCheckBase(ABC):
    """Base class for individual torsion checks.

    This abstract base class defines the interface for all individual torsion
    verification checks. Each specific check inherits from this class and
    implements the execute method to perform its unique structural verification.

    Notes
    -----
    - All check classes should inherit from this base class
    - Each check must implement the execute method with its required parameters
    - Different checks may require different parameter combinations
    - Results are returned as CheckResult objects for consistent interpretation
    """

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> CheckResult:  # noqa: ANN401
        """Execute the specific structural check.

        Parameters
        ----------
        **kwargs
            Variable parameters depending on the specific check requirements.
            Common parameters include:
            - geometry : TorsionGeometry - Cross-section geometry and dimensions
            - materials : TorsionMaterials - Material properties and coefficients
            - forces : TorsionForces - Applied loads and design parameters

        Returns
        -------
        CheckResult
            Complete results including pass/fail status, utilization ratio,
            and any applicable required/provided values.
        """


@dataclass(frozen=True)
class ConcreteStrutCapacityCheck(TorsionCheckBase):
    """Verify that concrete compression struts can resist combined shear and torsion forces.

    Based on EN 1992-1-1:2004 art. 6.3.2(4).

    This is the most critical check - it ensures the concrete itself won't fail
    before the reinforcement yields. If this check fails, you must either:
    - Increase cross-section dimensions
    - Use higher strength concrete
    - Reduce applied loads


    Notes
    -----
    - This check has priority, failure means the section cannot work
    - Combines both shear (V_Ed) and torsion (T_Ed) effects
    - Accounts for concrete strength, section geometry, and stress state
    - No amount of reinforcement can fix a failing concrete strut

    Examples
    --------
    >>> check = ConcreteStrutCapacityCheck()
    >>> result = check.execute(geometry=geometry, materials=materials, forces=forces)
    >>> if not result.is_ok:
    ...     print("Concrete strut fails - increase section size!")
    >>> print(f"Concrete utilization: {result.utilization:.1%}")
    """

    def execute(
        self,
        geometry: TorsionGeometry,
        materials: TorsionMaterials,
        forces: TorsionForces,
    ) -> CheckResult:
        """Check if concrete struts can resist combined shear and torsion forces.

        Parameters
        ----------
        geometry : TorsionGeometry
            Cross-section geometry and dimensions.
        materials : TorsionMaterials
            Material properties and coefficients.
        forces : TorsionForces
            Applied loads and design parameters.

        Returns
        -------
        CheckResult
            Check results with utilization ratio and pass/fail status.
        """
        # The maximum shear resistance
        v_rd_max = Form6Dot9MaximumShearResistance(
            b_w=geometry.cs.width,
            z=geometry.lever_arm(),
            f_cd=geometry.cs.concrete_material.f_cd,
            nu_1=materials.strength_reduction_factor(),
            alpha_cw=materials.compression_chord_coefficient(sigma_cp=forces.sigma_cp),
            theta=forces.theta,
        )

        # The design torsional resistance moment
        t_rd_max = Form6Dot30DesignTorsionalResistanceMoment(
            nu=materials.strength_reduction_factor(),
            alpha_cw=materials.compression_chord_coefficient(sigma_cp=forces.sigma_cp),
            f_cd=geometry.cs.concrete_material.f_cd,
            a_k=geometry.enclosed_area(),
            t_ef_i=geometry.effective_wall_thickness(),
            theta=forces.theta,
        )

        # Check if the concrete strut can take the applied combination of forces in compression
        utilization = forces.t_ed / t_rd_max + forces.v_ed / v_rd_max
        is_ok = bool(
            Form6Dot29CheckTorsionShearResistance(
                t_ed=forces.t_ed,
                v_ed=forces.v_ed,
                t_rd_max=t_rd_max,
                v_rd_max=v_rd_max,
            )
        )
        return CheckResult(is_ok=is_ok, utilization=utilization, required=None, provided=None)


@dataclass(frozen=True)
class TorsionMomentCapacityCheck(TorsionCheckBase):
    """Check if combined shear and torsion can be resisted with minimum reinforcement.

    Based on EN 1992-1-1:2004 art. 6.3.2(5).

    This determines whether your current reinforcement is sufficient or if you
    need additional stirrups and longitudinal bars for torsion. If this check
    fails, you need to add more reinforcement according to torsion design rules.

    Parameters
    ----------
    The execute method uses geometry, materials, and forces to evaluate:
    - Torsional cracking moment capacity (T_Rd,c)
    - Shear resistance without stirrups (V_Rd,c)
    - Combined utilization ratio

    Returns
    -------
    CheckResult
        - is_ok: True if minimum reinforcement is sufficient
        - utilization: Combined demand/capacity ratio
        - If fails: additional torsion reinforcement is required

    Notes
    -----
    - This applies for solid rectangular sections.
    - This check determines if torsion effects are significant
    - Failure means you need torsion-specific reinforcement design
    - Success means minimum reinforcement rules are sufficient


    Examples
    --------
    >>> check = TorsionMomentCapacityCheck()
    >>> result = check.execute(geometry=geometry, forces=forces)
    >>> if not result.is_ok:
    ...     print("Need additional torsion reinforcement")
    ...     # Calculate required additional longitudinal bars
    >>> elif result.utilization > 0.95:
    ...     print("Close to torsion limit - consider more reinforcement")
    """

    def execute(
        self,
        geometry: TorsionGeometry,
        forces: TorsionForces,
    ) -> CheckResult:
        """Check if minimum reinforcement can resist combined shear and torsion.

        Parameters
        ----------
        geometry : TorsionGeometry
            Cross-section geometry and dimensions.
        forces : TorsionForces
            Applied loads and design parameters.

        Returns
        -------
        CheckResult
            Check results with utilization ratio and pass/fail status.
        """
        # Torsion moment capacity
        # The torsional shear stress in wall i, can be set to be equal to fctd
        tau_t_i = geometry.cs.concrete_material.f_ctd

        # The torsional cracking moment
        t_rd_c = 2 * geometry.enclosed_area() * tau_t_i * geometry.effective_wall_thickness()

        # Shear capacity
        # Coefficient for shear strength, according to art. 6.2.2 (1) from EN 1992-1-1:2004
        c_rd_c = 0.18 / geometry.cs.concrete_material.material_factor

        # Coefficient for concrete according to art. 6.2.2 (1) from EN 1992-1-1:2004
        k_1 = 0.15

        # Size effect factor according to art. 6.2.2 (1) from EN 1992-1-1:2004
        k = Form6Dot2aSub1ThicknessFactor(d=geometry.effective_depth())

        # Minimum shear capacity according to art. 6.2.2 (1) from EN 1992-1-1:2004
        v_min = Form6Dot3NShearCapacityWithoutRebar(k=k, f_ck=geometry.cs.concrete_material.f_ck)

        # Tensile rebar ratio according to art. 6.2.2 (1) from EN 1992-1-1:2004
        rho_l = Form6Dot2aSub2RebarRatio(a_sl=forces.a_sl, b_w=geometry.cs.width, d=geometry.effective_depth())

        # The design value for the shear resistance
        v_rd_c = Form6Dot2ShearResistance(
            c_rd_c=c_rd_c,
            k=k,
            rho_l=rho_l,
            f_ck=geometry.cs.concrete_material.f_ck,
            k_1=k_1,
            sigma_cp=forces.sigma_cp,
            b_w=geometry.cs.width,
            d=geometry.effective_depth(),
            v_min=v_min,
        )

        utilization = forces.t_ed / t_rd_c + forces.v_ed / v_rd_c
        is_ok = bool(
            Form6Dot31CheckTorsionShearResistanceRectangular(
                t_ed=forces.t_ed,
                t_rd_c=t_rd_c,
                v_ed=forces.v_ed,
                v_rd_c=v_rd_c,
            )
        )
        return CheckResult(is_ok=is_ok, utilization=utilization, required=None, provided=None)


@dataclass(frozen=True)
class MaxLongitudinalReinforcementCheck(TorsionCheckBase):
    """Verify that longitudinal reinforcement doesn't exceed code maximum limits.

    Based on EN 1992-1-1:2004 art. 9.2.1.1(3).

    Prevents over-reinforced sections that could lead to sudden brittle failure.

    Parameters
    ----------
    The execute method checks:
    - Maximum allowed: 4% of gross concrete area
    - Actual provided: Sum of all longitudinal reinforcement

    Returns
    -------
    CheckResult
        - is_ok: True if reinforcement ≤ 4% of concrete area
        - utilization: (provided area) / (max allowed area)
        - required: Maximum allowed reinforcement area [mm²]
        - provided: Actual total longitudinal reinforcement area [mm²]

    Notes
    -----
    - Limit: 4% of gross concrete cross-sectional area
    - Includes ALL longitudinal bars (tension + compression)
    - Consider larger cross-section if approaching this limit

    Examples
    --------
    >>> check = MaxLongitudinalReinforcementCheck()
    >>> result = check.execute(geometry=geometry)
    >>> if result.utilization > 0.8:
    ...     print(f"High reinforcement ratio: {result.utilization:.1%}")
    ...     print(f"Using {result.provided:.0f} of max {result.required:.0f} mm²")
    """

    def execute(self, geometry: TorsionGeometry) -> CheckResult:
        """Check that longitudinal reinforcement doesn't exceed 4% limit.

        Parameters
        ----------
        geometry : TorsionGeometry
            Cross-section geometry and dimensions. Used for cross-sectional area.

        Returns
        -------
        CheckResult
            Check results with required/provided areas and pass/fail status.
        """
        a_s_max = 0.04 * geometry.cs.cross_section.area
        a_s = geometry.cs.reinforcement_area_longitudinal_bars
        utilization = a_s / a_s_max if a_s_max > 0 else float("inf")
        is_ok = a_s_max >= a_s
        return CheckResult(is_ok=is_ok, utilization=utilization, required=a_s_max, provided=a_s)


@dataclass(frozen=True)
class MinTensileReinforcementCheck(TorsionCheckBase):
    """Ensure adequate minimum tension reinforcement to prevent brittle failure.

    Based on EN 1992-1-1:2004 art. 9.2.1.1(1).

    Guarantees the beam has enough steel to carry loads after concrete cracks.
    Without minimum reinforcement, the beam would fail suddenly and
    catastrophically when concrete reaches its tensile strength.

    Parameters
    ----------
    The execute method evaluates:
    - Minimum required based on concrete tensile strength and beam dimensions
    - Actual tension reinforcement provided in bottom of section

    Returns
    -------
    CheckResult
        - is_ok: True if provided ≥ minimum required
        - utilization: (min required) / (provided) - lower is better
        - required: Minimum tension reinforcement needed [mm²]
        - provided: Actual tensile reinforcement area [mm²]

    Assumptions
    -----------
    - In this version of Blueprints the actual tensile reinforcement is NOT being calculated.
    - Forces are not considered in this check (yet).
    - We will assume that the bottom bars are the tensile reinforcement.

    Notes
    -----
    - Critical safety requirement - prevents sudden failure
    - Calculated from concrete tensile strength and section width
    - Only counts reinforcement in tension zone (typically bottom bars)
    - Add more bars in the tensile zone if this check fails

    Examples
    --------
    >>> check = MinTensileReinforcementCheck()
    >>> result = check.execute(geometry=geometry, materials=materials)
    >>> if not result.is_ok:
    ...     shortage = result.required - result.provided
    ...     print(f"Need {shortage:.0f} mm² more bottom reinforcement")
    """

    def execute(self, geometry: TorsionGeometry, materials: TorsionMaterials) -> CheckResult:
        """Check that minimum tension reinforcement is provided.

        Parameters
        ----------
        geometry : TorsionGeometry
            Cross-section geometry and dimensions. Used for concrete properties,
            section width, effective depth, and tension reinforcement area.
        materials : TorsionMaterials
            Material properties and coefficients. Used for tension rebar yield strength.

        Returns
        -------
        CheckResult
            Check results with required/provided areas and pass/fail status.
        """
        # Minimum tensile reinforcement area according to formula 9.1
        a_st_min = Form9Dot1nMinimumTensileReinforcementBeam(
            f_ctm=geometry.cs.concrete_material.f_ctm,
            f_yk=materials.get_tension_rebar_material().f_yk,
            b_t=geometry.cs.width,
            d=geometry.effective_depth(),
        )

        # Assuming bottom bars are the tensile reinforcement
        # In a later version we will consider the actual forces and the actual tensile reinforcement
        a_st = sum(rebar.area for rebar in geometry.get_tension_rebars())

        utilization = a_st_min / a_st if a_st > 0 else float("inf")
        is_ok = a_st >= a_st_min
        return CheckResult(is_ok=is_ok, utilization=utilization, required=a_st_min, provided=a_st)


@dataclass(frozen=True)
class MaxShearStirrupSpacingCheck(TorsionCheckBase):
    """Verify that shear stirrup spacing meets maximum distance requirements.

    Based on EN 1992-1-1:2004 art. 9.2.2(6).

    Ensures stirrups are close enough to effectively carry shear forces and
    prevent diagonal tension cracks from growing too large. Wide stirrup
    spacing leads to poor shear resistance and potential sudden failure.

    Parameters
    ----------
    The execute method checks:
    - Maximum allowed spacing based on effective depth and stirrup angle
    - Actual spacing of stirrups designated for shear resistance

    Returns
    -------
    CheckResult
        - is_ok: True if actual spacing ≤ maximum allowed
        - utilization: (actual spacing) / (max allowed)
        - required: Maximum allowed spacing [mm]
        - provided: Actual stirrup spacing [mm]

    Notes
    -----
    - Closer stirrups = better shear resistance
    - Only considers stirrups with shear_check=True
    - Reduce stirrup spacing if this check fails

    Examples
    --------
    >>> check = MaxShearStirrupSpacingCheck()
    >>> result = check.execute(geometry=geometry, forces=forces)
    >>> if not result.is_ok:
    ...     print(f"Stirrup spacing {result.provided:.0f}mm too large")
    ...     print(f"Maximum allowed: {result.required:.0f}mm")
    """

    def execute(self, geometry: TorsionGeometry, forces: TorsionForces) -> CheckResult:
        """Check that shear stirrup spacing meets maximum limits.

        Parameters
        ----------
        geometry : TorsionGeometry
            Cross-section geometry and dimensions. Used for effective depth and
            stirrup spacing information.
        forces : TorsionForces
            Applied loads and design parameters. Used for stirrup angle (α).

        Returns
        -------
        CheckResult
            Check results with required/provided spacing and pass/fail status.
        """
        # Maximum stirrup spacing according to formula 9.6
        s_l_max = Form9Dot6nMaximumDistanceShearReinforcement(d=geometry.effective_depth(), alpha=forces.alpha)

        # Actual stirrup spacing (max distance between stirrups used for shear)
        s = max(stirrup.distance for stirrup in geometry.cs.stirrups if stirrup.shear_check)

        utilization = s / s_l_max if s_l_max > 0 else float("inf")
        is_ok = s <= s_l_max
        return CheckResult(is_ok=is_ok, utilization=utilization, required=s_l_max, provided=s)


@dataclass(frozen=True)
class MaxTorsionStirrupSpacingCheck(TorsionCheckBase):
    """Verify that torsion stirrup spacing meets maximum distance requirements.

    Based on EN 1992-1-1:2004 art. 9.2.3(3).

    Ensures stirrups are close enough to resist torsional shear flow around
    the cross-section perimeter. Torsion requires even closer stirrup spacing
    than pure shear because of the circular stress pattern.

    Parameters
    ----------
    The execute method checks:
    - Maximum allowed spacing (most restrictive of several limits)
    - Actual spacing of stirrups designated for torsion resistance

    Returns
    -------
    CheckResult
        - is_ok: True if actual spacing ≤ maximum allowed
        - utilization: (actual spacing) / (max allowed)
        - required: Maximum allowed spacing [mm]
        - provided: Actual torsion stirrup spacing [mm]

    Notes
    -----
    - Torsion spacing limits are stricter than shear-only limits
    - Maximum is minimum of: perimeter/8, shear limit, width, height
    - Only considers stirrups with torsion_check=True
    - Closer spacing improves torsional resistance

    Examples
    --------
    >>> check = MaxTorsionStirrupSpacingCheck()
    >>> result = check.execute(geometry=geometry, forces=forces)
    >>> if result.utilization > 0.9:
    ...     print(f"Torsion stirrups nearly at spacing limit: {result.provided:.0f}mm")
    ...     print(f"Consider reducing to {result.required * 0.8:.0f}mm for safety")
    """

    def execute(self, geometry: TorsionGeometry, forces: TorsionForces) -> CheckResult:
        """Check that torsion stirrup spacing meets maximum limits.

        Parameters
        ----------
        geometry : TorsionGeometry
            Cross-section geometry and dimensions. Used for effective depth,
            cross-section perimeter, width, height, and stirrup spacing.
        forces : TorsionForces
            Applied loads and design parameters. Used for stirrup angle (alpha).

        Returns
        -------
        CheckResult
            Check results with required/provided spacing and pass/fail status.
        """
        # Maximum stirrup spacing according to formula 9.6
        s_l_max = Form9Dot6nMaximumDistanceShearReinforcement(geometry.effective_depth(), forces.alpha)

        # Maximum stirrup spacing for torsion according to art. 9.2.3(3)
        s_max = min(geometry.cs.cross_section.perimeter / 8, s_l_max, geometry.cs.width, geometry.cs.height)
        s = max(stirrup.distance for stirrup in geometry.cs.stirrups if stirrup.torsion_check)

        utilization = s / s_max if s_max > 0 else float("inf")
        is_ok = s <= s_max
        return CheckResult(is_ok=is_ok, utilization=utilization, required=s_max, provided=s)


@dataclass(frozen=True)
class ShearAndTorsionStirrupAreaCheck(TorsionCheckBase):
    """Verify that total stirrup area can resist the combined shear and torsion forces.

    Based on EN 1992-1-1:2004 torsion and shear design principles.

    This is the main reinforcement design check, it determines if you have
    enough stirrup steel area to carry both shear and torsion. Combines the
    stirrup requirements from both effects and checks against provided stirrups.

    Parameters
    ----------
    The execute method calculates:
    - Required stirrup area for shear force (V_Ed)
    - Required stirrup area for torsion moment (T_Ed)
    - Total required area (shear + 2 × torsion for closed stirrups)
    - Actual provided stirrup area

    Returns
    -------
    CheckResult
        - is_ok: True if provided area ≥ required area
        - utilization: (required area) / (provided area)
        - required: Total required stirrup area per unit length [mm²/mm]
        - provided: Actual stirrup area per unit length [mm²/mm]

    Notes
    -----
    - Most important stirrup design check
    - Accounts for interaction between shear and torsion
    - Torsion contribution counts double (closed stirrup geometry)
    - Add more stirrups or larger diameter if this check fails

    Assumptions
    -----------
    - It is currently assumed that all types of stirrups present in the cross-section work in torsion and shear

    Examples
    --------
    >>> check = ShearAndTorsionStirrupAreaCheck()
    >>> result = check.execute(geometry=geometry, materials=, forces=forces)
    >>> if not result.is_ok:
    ...     deficit = result.required - result.provided
    ...     print(f"Need {deficit:.3f} mm²/mm more stirrup area")
    ...     print("Solutions: closer spacing or larger diameter stirrups")
    """

    def execute(self, geometry: TorsionGeometry, materials: TorsionMaterials, forces: TorsionForces) -> CheckResult:
        """Check that stirrup area can resist combined shear and torsion forces.

        Parameters
        ----------
        geometry : TorsionGeometry
            Cross-section geometry and dimensions.
        materials : TorsionMaterials
            Material properties and coefficients.
        forces : TorsionForces
            Applied loads and design parameters.

        Returns
        -------
        CheckResult
            Check results with required/provided stirrup areas and pass/fail status.
        """
        # Design yield strength of stirrup reinforcement
        f_ywd = materials.get_stirrup_material().f_yd

        # Required stirrups for the shear force according to art. 6.2.3(3), formula 6.8
        a_sw_s_w_v = forces.v_ed / (geometry.lever_arm() * cot(forces.theta) * f_ywd)  # [mm²/mm]

        # Shear stress in a wall of a section subject to a pure torsional moment
        tau_t_i_t_ef_i = Form6Dot26ShearStressInWall(t_ed=forces.t_ed, a_k=geometry.enclosed_area())

        # Shear force due to torsion
        v_ed_i = Form6Dot27ShearForceInWall(tau_t_i_t_ef_i=tau_t_i_t_ef_i, z_i=geometry.cs.height)

        # Required stirrups for the torsion moment according to art. 6.2.3(3), formula 6.8
        a_sw_s_w_t = v_ed_i / (geometry.cs.height * cot(forces.theta) * f_ywd)

        # Total required stirrup reinforcement
        a_sw_s_w_total = a_sw_s_w_v + a_sw_s_w_t * 2

        # Actual stirrup reinforcement
        # ATTENTION: HERE WE ARE ASSUMING THAT ALL STIRRUPS WORK IN TORSION AND SHEAR
        a_sw_prov = sum(stirrup.as_w for stirrup in geometry.cs.stirrups if stirrup.torsion_check or stirrup.shear_check) * MM_TO_M

        utilization = a_sw_s_w_total / a_sw_prov if a_sw_prov > 0 else float("inf")
        is_ok = a_sw_prov >= a_sw_s_w_total
        return CheckResult(is_ok=is_ok, utilization=utilization, required=a_sw_s_w_total, provided=a_sw_prov)


@dataclass(frozen=True)
class MinShearReinforcementRatioCheck(TorsionCheckBase):
    """Ensure minimum shear reinforcement ratio to prevent brittle shear failure.

    Based on EN 1992-1-1:2004 art. 9.2.2(5).

    Guarantees a minimum amount of stirrup steel regardless of calculated
    requirements. This prevents sudden shear failure in lightly loaded members
    and ensures some ductility even when shear forces are small.

    Parameters
    ----------
    The execute method evaluates:
    - Minimum required reinforcement ratio based on concrete and steel grades
    - Actual shear reinforcement ratio from provided stirrups

    Returns
    -------
    CheckResult
        - is_ok: True if actual ratio ≥ minimum required ratio
        - utilization: (min required) / (provided) - lower is better
        - required: Minimum reinforcement ratio [dimensionless]
        - provided: Actual reinforcement ratio [dimensionless]

    Notes
    -----
    - Minimum safety requirement for all reinforced concrete beams
    - Prevents sudden brittle failure in lightly reinforced sections
    - Based on ratio of steel area to concrete area and stirrup angle
    - Must be satisfied even when calculated shear reinforcement is minimal

    Assumptions
    -----------
    - It is currently assumed that all types of stirrups present in the cross-section work in torsion and shear

    Examples
    --------
    >>> check = MinShearReinforcementRatioCheck()
    >>> result = check.execute(geometry=geometry, materials=materials, forces=forces)
    >>> if not result.is_ok:
    ...     print(f"Minimum ratio: {result.required:.4f}")
    ...     print(f"Provided: {result.provided:.4f}")
    ...     print("Add more stirrups to meet minimum requirements")
    """

    def execute(self, geometry: TorsionGeometry, materials: TorsionMaterials, forces: TorsionForces) -> CheckResult:
        """Check that minimum shear reinforcement ratio is satisfied.

        Parameters
        ----------
        geometry : TorsionGeometry
            Cross-section geometry and dimensions.
        materials : TorsionMaterials
            Material properties and coefficients.
        forces : TorsionForces
            Applied loads and design parameters.

        Returns
        -------
        CheckResult
            Check results with required/provided ratios and pass/fail status.
        """
        # Minimum shear reinforcement ratio according to formula 9.5N
        rho_w_min = Form9Dot5nMinimumShearReinforcementRatio(
            f_ck=geometry.cs.concrete_material.f_ck,
            f_yk=materials.get_stirrup_material().f_yk,
        )

        # Actual shear reinforcement ratio
        # ATTENTION: HERE WE ARE ASSUMING THAT ALL STIRRUPS WORK IN TORSION AND SHEAR
        a_sw_prov = sum(stirrup.as_w for stirrup in geometry.cs.stirrups if stirrup.torsion_check or stirrup.shear_check) * MM_TO_M

        # Shear reinforcement ratio according to formula 9.4
        rho_w = Form9Dot4ShearReinforcementRatio(a_sw=a_sw_prov, s=1.0, b_w=geometry.cs.width, alpha=forces.alpha)

        utilization = rho_w_min / rho_w if rho_w > 0 else float("inf")
        is_ok = rho_w >= rho_w_min
        return CheckResult(is_ok=is_ok, utilization=utilization, required=rho_w_min, provided=rho_w)
