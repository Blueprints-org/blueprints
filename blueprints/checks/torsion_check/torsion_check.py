r"""Torsion calculation for rectangular reinforced concrete cross-sections.

Based on EN 1992-1-1:2004 and calculation example from Technische Universiteit Delft:
https://www.studeersnel.nl/nl/document/technische-universiteit-delft/concrete-structures-2/torsion/29391885
"""

from dataclasses import dataclass, field
from functools import cached_property

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_2 import (
    Form6Dot2aSub1ThicknessFactor,
    Form6Dot2aSub2RebarRatio,
    Form6Dot2ShearResistance,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_3n import (
    Form6Dot3NShearCapacityWithoutRebar,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_6n import (
    Form6Dot6nStrengthReductionFactor,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_9 import (
    Form6Dot9MaximumShearResistance,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_11abcn import (
    Form6Dot11abcNCompressionChordCoefficient,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_18 import Form6Dot18AdditionalTensileForce
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_26 import (
    Form6Dot26ShearStressInWall,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_27 import (
    Form6Dot27ShearForceInWall,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_28 import (
    Form6Dot28RequiredCrossSectionalArea,
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
from blueprints.materials.reinforcement_steel import (
    ReinforcementSteelMaterial,
)
from blueprints.math_helpers import cot
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.type_alias import DEG, DIMENSIONLESS, MM, MM2, MPA, NMM, N
from blueprints.unit_conversion import KNM_TO_NMM, N_TO_KN

# Eurocode constants
MAX_LONGITUDINAL_REINFORCEMENT_RATIO = 0.04  # Art. 9.2.1.1 (3)
CONCRETE_COEFFICIENT_CRD_C = 0.18  # Art. 6.2.2 (1) - base value
CONCRETE_COEFFICIENT_K1 = 0.15  # Art. 6.2.2 (1)
LEVER_ARM_FACTOR = 0.9  # Conservative estimate for internal lever arm
PERIMETER_FRACTION_TORSION = 8  # Art. 9.2.3 (3) - u/8 limit
DEFAULT_STIRRUP_SPACING = 1.0  # Default spacing for reinforcement ratio calculations (m)
PRECISION_TOLERANCE = 1e-3  # Tolerance for floating point comparisons
DEFAULT_ALPHA_ANGLE = 90.0  # Default stirrup angle (degrees)
DEFAULT_THETA_ANGLE = 45.0  # Default concrete strut angle (degrees) - conservative


@dataclass(frozen=True)
class TorsionCheck:
    r"""Class responsible for the torsion cross-section check according to art. 6.3.
    Includes the interaction between shear and torsion.

    This implementation follows EN 1992-1-1:2004 Chapter 6.3 for torsion design
    and checks the interaction between shear and torsion forces.

    Parameters
    ----------
    cs: RectangularReinforcedCrossSection
        The cross-section object containing geometry and reinforcement details.
    sigma_cp: MPA
        Mean compressive stress, measured positive, due to the design axial force [$MPa$].
        Must be >= 0.
    a_sl: MM2
        Area of the tensile reinforcement, which extends l_bd + d beyond the section considered
        (figure 6.3 EN 1992-1-1) [$mm²$]. Must be > 0.
    v_ed: N
        Shear force in the cross-section [$N$]. Must be >= 0.
    t_ed: NMM
        Torsion moment in the cross-section [$Nmm$]. Must be >= 0.
    alpha: DEG
        Angle between shear reinforcement and the beam axis perpendicular to the shear force [$°$].
        Must be between 45° and 90°. The default value is 90°.
    theta: DEG
        Angle between the concrete compression strut and the beam axis perpendicular to the
        shear force [$°$]. Must be between 21.8° and 45°. The default value is 45°.

    Known Limitations
    -----------------
    - Only supports rectangular cross-sections
    - Assumes uniform material properties for all tension rebars and stirrups
    - θ angle is currently fixed at 45° (conservative approach)
    - Only considers bottom layer of longitudinal reinforcement as tension reinforcement
    - Does not account for biaxial bending effects
    - Assumes all stirrups contribute to both shear and torsion resistance
    - Limited to sections without prestressing
    - Does not consider fatigue effects
    - Temperature effects on material properties are not considered
    - No consideration for time-dependent effects (creep, shrinkage)

    Raises
    ------
    ValueError
        If input parameters are outside valid ranges or if cross-section
        has no reinforcement or mixed materials.
    """

    label = "Torsion according to art. 6.3"
    source_document = "EN 1992-1-1"

    cs: RectangularReinforcedCrossSection
    sigma_cp: MPA
    a_sl: MM2
    v_ed: N
    t_ed: NMM

    alpha: DEG = field(default=DEFAULT_ALPHA_ANGLE)
    theta: DEG = field(default=DEFAULT_THETA_ANGLE)

    def __post_init__(self) -> None:
        """Validate input parameters after initialization."""
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        """Validate all input parameters."""
        if self.sigma_cp < 0:
            raise ValueError(f"sigma_cp must be >= 0, got {self.sigma_cp}")
        if self.a_sl <= 0:
            raise ValueError(f"a_sl must be > 0, got {self.a_sl}")
        if self.v_ed < 0:
            raise ValueError(f"v_ed must be >= 0, got {self.v_ed}")
        if self.t_ed < 0:
            raise ValueError(f"t_ed must be >= 0, got {self.t_ed}")
        if not 45 <= self.alpha <= 90:
            raise ValueError(f"alpha must be between 45° and 90°, got {self.alpha}°")
        if not 21.8 <= self.theta <= 45:
            raise ValueError(f"theta must be between 21.8° and 45°, got {self.theta}°")

        # Validate cross-section has reinforcement
        if not self.cs.longitudinal_rebars:
            raise ValueError("Cross-section must have longitudinal reinforcement")
        if not self.cs.stirrups:
            raise ValueError("Cross-section must have stirrup reinforcement")

    @cached_property
    def get_cs_tension_rebars_material(self) -> ReinforcementSteelMaterial:
        """Return the material used for all tension rebars, or raise an error if mixed."""
        tension_rebars = self.get_cs_tension_rebars
        materials = {rebar.material for rebar in tension_rebars}

        if not materials:
            raise ValueError("No tension rebars found.")
        if len(materials) > 1:
            raise ValueError(f"Multiple materials found in tension rebars: {[m.name for m in materials]}")

        return materials.pop()

    @cached_property
    def get_cs_stirrups_material(self) -> ReinforcementSteelMaterial:
        """Return the material used for all stirrups, or raise an error if mixed."""
        materials = {rebar.material for rebar in self.cs.stirrups}

        if not materials:
            raise ValueError("No stirrups found.")
        if len(materials) > 1:
            raise ValueError(f"Multiple materials found in stirrups: {[m.name for m in materials]}")

        return materials.pop()

    @cached_property
    def get_cs_tension_rebars(self) -> list[Rebar]:
        """Get the tension reinforcement rebars in the cross-section.

        Note: Currently only considers the bottom layer of reinforcement.
        This is a limitation that should be addressed for general bending cases.
        """
        if not self.cs.longitudinal_rebars:
            return []
        lower_y = min(rebar.y for rebar in self.cs.longitudinal_rebars)
        return [rebar for rebar in self.cs.longitudinal_rebars if abs(rebar.y - lower_y) < PRECISION_TOLERANCE]

    @cached_property
    def get_c_nom_center(self) -> MM:
        """Get the distance between edge and centre of the longitudinal reinforcement.

        Note: Currently uses the largest diameter tension bar. For more accurate results,
        should consider stirrup diameter and spacing requirements per EN 1992-1-1.
        """
        tension_rebars = self.get_cs_tension_rebars
        if not tension_rebars:
            raise ValueError("No tension rebars found for cover calculation")

        thickest_rebar = max(tension_rebars, key=lambda r: r.diameter)
        cs_lower_edge = min(pt[1] for pt in self.cs.cross_section.polygon.exterior.coords)
        return abs(thickest_rebar.y - cs_lower_edge)

    @cached_property
    def get_cs_depth(self) -> MM:
        """Get effective cross-section depth."""
        return self.cs.height - self.get_c_nom_center

    @cached_property
    def get_cs_lever_arm(self) -> MM:
        """Get the inner lever arm of the cross-section.

        Uses conservative factor of 0.9 for internal lever arm estimation.
        """
        return LEVER_ARM_FACTOR * self.get_cs_depth

    @cached_property
    def t_ef_i(self) -> MM:
        """The effective wall thickness according to EN 1992-1-1 Art. 6.3.2."""
        area_to_perimeter = self.cs.cross_section.area / self.cs.cross_section.perimeter
        min_thickness = 2 * self.get_c_nom_center
        return max(area_to_perimeter, min_thickness)

    @cached_property
    def a_k(self) -> MM2:
        """The area enclosed by the centre-lines of the connecting walls."""
        effective_width = self.cs.width - self.t_ef_i
        effective_height = self.cs.height - self.t_ef_i

        if effective_width <= 0 or effective_height <= 0:
            raise ValueError(f"Invalid effective dimensions: width={effective_width}, height={effective_height}")

        return effective_width * effective_height

    @cached_property
    def u_k(self) -> MM:
        """The perimeter of the area a_k."""
        return 2 * (self.cs.width + self.cs.height - 2 * self.t_ef_i)

    @cached_property
    def alpha_cw(self) -> Form6Dot11abcNCompressionChordCoefficient | DIMENSIONLESS:
        """Coefficient taking account of the state of the stress in the compression chord according to art. 6.2.3 (3) from EN 1992-1-1"""
        if self.sigma_cp <= 0:
            return 1.0
        return Form6Dot11abcNCompressionChordCoefficient(
            sigma_cp=self.sigma_cp,
            f_cd=self.cs.concrete_material.f_cd,
        )

    @cached_property
    def nu(self) -> Form6Dot6nStrengthReductionFactor:
        """Strength reduction factor for concrete cracked in shear according to art. 6.2.2 (6) from EN 1992-1-1."""
        return Form6Dot6nStrengthReductionFactor(f_ck=self.cs.concrete_material.f_ck)

    def check_concrete_strut_capacity(self) -> CheckResult:
        """Check the capacity of the concrete struts according to art. 6.3.2 (4) from EN 1992-1-1."""
        # The maximum shear resistance
        v_rd_max = Form6Dot9MaximumShearResistance(
            b_w=self.cs.width,
            z=self.get_cs_lever_arm,
            f_cd=self.cs.concrete_material.f_cd,
            nu_1=self.nu,
            alpha_cw=self.alpha_cw,
            theta=self.theta,
        )

        # The design torsional resistance moment
        t_rd_max = Form6Dot30DesignTorsionalResistanceMoment(
            nu=self.nu,
            alpha_cw=self.alpha_cw,
            f_cd=self.cs.concrete_material.f_cd,
            a_k=self.a_k,
            t_ef_i=self.t_ef_i,
            theta=self.theta,
        )

        # Check if the applied combination of forces can be taken by the concrete strut in compression
        if t_rd_max <= 0 or v_rd_max <= 0:
            raise ValueError(f"Invalid resistance values: t_rd_max={t_rd_max}, v_rd_max={v_rd_max}")

        utilization = self.t_ed / t_rd_max + self.v_ed / v_rd_max
        is_ok = bool(
            Form6Dot29CheckTorsionShearResistance(
                t_ed=self.t_ed,
                v_ed=self.v_ed,
                t_rd_max=t_rd_max,
                v_rd_max=v_rd_max,
            )
        )
        return CheckResult(
            is_ok=is_ok,
            utilization=utilization,
            required=None,
            provided=None,
        )

    def check_torsion_moment_capacity(self) -> CheckResult:
        """Check whether the combination of forces can be resisted with minimum reinforcement only according to art. 6.3.2 (5) from EN 1992-1-1."""
        # Torsion moment capacity
        # The torsional shear stress in wall i, can be set to be equal to fctd
        tau_t_i = self.cs.concrete_material.f_ctd

        # The torsional cracking moment
        t_rd_c = 2 * self.a_k * tau_t_i * self.t_ef_i

        # Shear capacity
        # Coefficient for shear strength according to art. 6.2.2 (1) from EN 1992-1-1
        c_rd_c = CONCRETE_COEFFICIENT_CRD_C / self.cs.concrete_material.material_factor

        # Coefficient for concrete according to art. 6.2.2 (1) from EN 1992-1-1
        k_1 = CONCRETE_COEFFICIENT_K1

        # Size effect factor according to art. 6.2.2 (1) from EN 1992-1-1
        k = Form6Dot2aSub1ThicknessFactor(d=self.get_cs_depth)

        # Minimum shear capacity according to art. 6.2.2 (1) from EN 1992-1-1
        v_min = Form6Dot3NShearCapacityWithoutRebar(k=k, f_ck=self.cs.concrete_material.f_ck)

        # Tensile rebar ratio according to art. 6.2.2 (1) from EN 1992-1-1
        rho_l = Form6Dot2aSub2RebarRatio(a_sl=self.a_sl, b_w=self.cs.width, d=self.get_cs_depth)

        # The design value for the shear resistance
        v_rd_c = Form6Dot2ShearResistance(
            c_rd_c=c_rd_c,
            k=k,
            rho_l=rho_l,
            f_ck=self.cs.concrete_material.f_ck,
            k_1=k_1,
            sigma_cp=self.sigma_cp,
            b_w=self.cs.width,
            d=self.get_cs_depth,
            v_min=v_min,
        )

        # Check if the section meets the minimum reinforcement requirements for the applied forces
        if t_rd_c <= 0 or v_rd_c <= 0:
            raise ValueError(f"Invalid concrete resistance values: t_rd_c={t_rd_c}, v_rd_c={v_rd_c}")

        utilization = self.t_ed / t_rd_c + self.v_ed / v_rd_c
        is_ok = bool(
            Form6Dot31CheckTorsionShearResistanceRectangular(
                t_ed=self.t_ed,
                t_rd_c=t_rd_c,
                v_ed=self.v_ed,
                v_rd_c=v_rd_c,
            )
        )
        return CheckResult(
            is_ok=is_ok,
            utilization=utilization,
            required=None,
            provided=None,
        )

    def check_max_longitudinal_reinforcement_area(self) -> CheckResult:
        """Check if the maximum longitudinal reinforcement is not exceeded according to art. 9.2.1.1 (3) from EN 1992-1-1."""
        a_s_max = MAX_LONGITUDINAL_REINFORCEMENT_RATIO * self.cs.cross_section.area
        a_s = self.cs.reinforcement_area_longitudinal_bars

        if a_s_max <= 0:
            raise ValueError(f"Invalid maximum reinforcement area: {a_s_max}")

        utilization = a_s / a_s_max
        is_ok = a_s <= a_s_max
        return CheckResult(
            is_ok=is_ok,
            utilization=utilization,
            required=a_s_max,
            provided=a_s,
        )

    def check_min_tensile_reinforcement_area(self) -> CheckResult:
        """Check if the minimum tensile reinforcement is provided for a beam according to art. 9.2.1.1 (1) from EN 1992-1-1"""
        a_st_min = Form9Dot1nMinimumTensileReinforcementBeam(
            f_ctm=self.cs.concrete_material.f_ctm,
            f_yk=self.get_cs_tension_rebars_material.f_yk,
            b_t=self.cs.width,
            d=self.get_cs_depth,
        )
        a_st = sum(rebar.area for rebar in self.get_cs_tension_rebars)

        if a_st <= 0:
            return CheckResult(is_ok=False, utilization=float("inf"), required=a_st_min, provided=a_st)

        utilization = a_st_min / a_st
        is_ok = a_st >= a_st_min
        return CheckResult(is_ok=is_ok, utilization=utilization, required=a_st_min, provided=a_st)

    def check_max_spacing_for_shear_stirrups(self) -> CheckResult:
        """Check if the spacing between shear stirrups is not exceeded according to art. 9.2.2 (6) from EN 1992-1-1."""
        s_l_max = Form9Dot6nMaximumDistanceShearReinforcement(d=self.get_cs_depth, alpha=self.alpha)

        shear_stirrups = [stirrup for stirrup in self.cs.stirrups if stirrup.shear_check]
        if not shear_stirrups:
            return CheckResult(is_ok=False, utilization=float("inf"), required=s_l_max, provided=None)

        spacing = max(stirrup.distance for stirrup in shear_stirrups)

        if s_l_max <= 0:
            raise ValueError(f"Invalid maximum spacing: {s_l_max}")

        utilization = spacing / s_l_max
        is_ok = spacing <= s_l_max
        return CheckResult(
            is_ok=is_ok,
            utilization=utilization,
            required=s_l_max,
            provided=spacing,
        )

    def check_max_spacing_for_torsion_stirrups(self) -> CheckResult:
        """Check if the spacing between torsion stirrups is not exceeded according to art. 9.2.3 (3) from EN 1992-1-1."""
        s_l_max = Form9Dot6nMaximumDistanceShearReinforcement(d=self.get_cs_depth, alpha=self.alpha)
        s_max = min(self.cs.cross_section.perimeter / PERIMETER_FRACTION_TORSION, s_l_max, self.cs.width, self.cs.height)

        torsion_stirrups = [stirrup for stirrup in self.cs.stirrups if stirrup.torsion_check]
        if not torsion_stirrups:
            return CheckResult(is_ok=False, utilization=float("inf"), required=s_max, provided=None)

        spacing = max(stirrup.distance for stirrup in torsion_stirrups)

        if s_max <= 0:
            raise ValueError(f"Invalid maximum spacing: {s_max}")

        utilization = spacing / s_max
        is_ok = spacing <= s_max
        return CheckResult(is_ok=is_ok, utilization=utilization, required=s_max, provided=spacing)

    def check_shear_and_torsion_stirrups_area(self) -> CheckResult:
        """Check if the the required stirrups is enough to be able to resist the occurring combination of forces."""
        # Reinforcement design yield strength
        f_ywd = self.get_cs_stirrups_material.f_yd

        # Required stirrups for the shear force
        a_sw_s_w_v = self.v_ed / (self.get_cs_lever_arm * cot(self.theta) * f_ywd)

        # Shear stress in a wall of a section subject to a pure torsional moment
        tau_t_i_t_ef_i = Form6Dot26ShearStressInWall(t_ed=self.t_ed, a_k=self.a_k)

        # Shear force due to torsion
        v_ed_i = Form6Dot27ShearForceInWall(tau_t_i_t_ef_i=tau_t_i_t_ef_i, z_i=self.cs.height)

        # Required stirrups for the torsion moment
        a_sw_s_w_t = v_ed_i / (self.cs.height * cot(self.theta) * f_ywd)

        # Total required stirrup reinforcement
        a_sw_s_w_total = a_sw_s_w_v + a_sw_s_w_t * 2

        # Actual stirrup reinforcement (area per unit length)
        # Note: Assumes all stirrups with torsion or shear check contribute to resistance
        relevant_stirrups = [stirrup for stirrup in self.cs.stirrups if stirrup.torsion_check or stirrup.shear_check]
        if not relevant_stirrups:
            return CheckResult(is_ok=False, utilization=float("inf"), required=a_sw_s_w_total, provided=0.0)

        # Calculate provided stirrup area per unit length (already in correct units)
        a_sw_prov = sum(stirrup.as_w for stirrup in relevant_stirrups)

        if a_sw_prov <= 0:
            return CheckResult(is_ok=False, utilization=float("inf"), required=a_sw_s_w_total, provided=a_sw_prov)

        utilization = a_sw_s_w_total / a_sw_prov
        is_ok = a_sw_prov >= a_sw_s_w_total
        return CheckResult(is_ok=is_ok, utilization=utilization, required=a_sw_s_w_total, provided=a_sw_prov)

    def check_min_shear_reinforcement_ratio(self) -> CheckResult:
        """Minimum shear reinforcement ratio according to art. 9.2.2 (5) from EN 1992-1-1"""
        # Minimum shear reinforcement ratio
        rho_w_min = Form9Dot5nMinimumShearReinforcementRatio(
            f_ck=self.cs.concrete_material.f_ck,
            f_yk=self.get_cs_stirrups_material.f_yk,
        )

        # Shear reinforcement ratio according to art. 9.2.2 (5) from EN 1992-1-1
        # Note: Assumes all stirrups with torsion or shear check contribute to resistance
        relevant_stirrups = [stirrup for stirrup in self.cs.stirrups if stirrup.torsion_check or stirrup.shear_check]
        if not relevant_stirrups:
            return CheckResult(is_ok=False, utilization=float("inf"), required=rho_w_min, provided=0.0)

        a_sw_prov = sum(stirrup.as_w for stirrup in relevant_stirrups)
        rho_w = Form9Dot4ShearReinforcementRatio(a_sw=a_sw_prov, s=DEFAULT_STIRRUP_SPACING, b_w=self.cs.width, alpha=self.alpha)

        if rho_w <= 0:
            return CheckResult(is_ok=False, utilization=float("inf"), required=rho_w_min, provided=rho_w)

        utilization = rho_w_min / rho_w
        is_ok = rho_w >= rho_w_min
        return CheckResult(is_ok=is_ok, utilization=utilization, required=rho_w_min, provided=rho_w)

    def get_all_check_results(self) -> dict[str, CheckResult]:
        """Get all check results as a dictionary.

        Returns
        -------
        dict[str, CheckResult]
            Dictionary containing all check results with descriptive keys.
        """
        return {
            "min_tensile_reinforcement": self.check_min_tensile_reinforcement_area(),
            "max_longitudinal_reinforcement": self.check_max_longitudinal_reinforcement_area(),
            "min_shear_reinforcement_ratio": self.check_min_shear_reinforcement_ratio(),
            "max_shear_stirrup_spacing": self.check_max_spacing_for_shear_stirrups(),
            "max_torsion_stirrup_spacing": self.check_max_spacing_for_torsion_stirrups(),
            "stirrup_reinforcement_area": self.check_shear_and_torsion_stirrups_area(),
            "concrete_strut_capacity": self.check_concrete_strut_capacity(),
            "torsion_moment_capacity": self.check_torsion_moment_capacity(),
        }

    def get_additional_reinforcement_requirements(self) -> dict[str, float]:
        """Calculate additional reinforcement requirements.

        Returns
        -------
        dict[str, float]
            Dictionary containing additional reinforcement areas in mm².
        """
        f_yd = self.get_cs_tension_rebars_material.f_yd

        # Additional tensile force due to shear
        delta_f_td = Form6Dot18AdditionalTensileForce(self.v_ed * N_TO_KN, self.theta, self.alpha)
        a_sl_shear = delta_f_td * KN_TO_N / f_yd

        # Additional longitudinal reinforcement for torsion (if needed)
        a_sl_torsion = 0.0
        if not self.check_torsion_moment_capacity().is_ok:
            a_sl_torsion = Form6Dot28RequiredCrossSectionalArea(
                u_k=self.u_k,
                f_yd=f_yd,
                t_ed=self.t_ed,
                a_k=self.a_k,
                theta=self.theta,
            )

        return {
            "additional_longitudinal_shear": a_sl_shear,
            "additional_longitudinal_torsion": a_sl_torsion,
        }

    def check(self) -> bool:
        """Perform all torsion checks and return overall result.

        Returns
        -------
        bool
            True if all checks pass, False otherwise.

        Note
        ----
        This method performs calculations but does not print results.
        Use get_all_check_results() to access detailed results.
        """
        check_results = self.get_all_check_results()

        # Check concrete strut capacity first (critical check)
        if not check_results["concrete_strut_capacity"].is_ok:
            return False

        # All other checks must pass
        return all(result.is_ok for result in check_results.values())

    def print_results(self) -> None:
        """Print formatted check results to console."""
        check_results = self.get_all_check_results()
        additional_reinf = self.get_additional_reinforcement_requirements()

        print("=== Torsion Check Results ===")
        print(f"Minimum tensile reinforcement area: {check_results['min_tensile_reinforcement'].utilization:.2f}")
        print(f"Maximum longitudinal reinforcement area: {check_results['max_longitudinal_reinforcement'].utilization:.2f}")
        print(f"Minimum shear reinforcement ratio: {check_results['min_shear_reinforcement_ratio'].utilization:.2f}")
        print(f"Maximum shear stirrup spacing: {check_results['max_shear_stirrup_spacing'].utilization:.2f}")
        print(f"Maximum torsion stirrup spacing: {check_results['max_torsion_stirrup_spacing'].utilization:.2f}")
        print(f"Stirrup reinforcement for shear and torsion: {check_results['stirrup_reinforcement_area'].utilization:.2f}")
        print(f"Concrete strut capacity: {check_results['concrete_strut_capacity'].utilization:.2f}")

        if not check_results["concrete_strut_capacity"].is_ok:
            print("❌ Concrete strut capacity is not enough. Increase cross-section or concrete class.")
            return

        print(f"Torsion moment capacity: {check_results['torsion_moment_capacity'].utilization:.2f}")

        if check_results["torsion_moment_capacity"].is_ok:
            print("✅ The combination of shear and torsion forces can be resisted with provided reinforcement.")
        else:
            print("❌ Torsion moment capacity is not enough. Additional reinforcement is required.")
            print(f"Required additional longitudinal reinforcement for torsion: {additional_reinf['additional_longitudinal_torsion']:.2f} mm²")

        print(f"Required additional longitudinal reinforcement due to shear: {additional_reinf['additional_longitudinal_shear']:.2f} mm²")

        # Overall result
        overall_result = self.check()
        print(f"\n{'✅ OVERALL: PASS' if overall_result else '❌ OVERALL: FAIL'}")

    def latex(self, n: int = 1) -> str:
        """Returns the LaTeX string representation for the torsion check.

        Parameters
        ----------
        n : int
            Equation numbering start value.

        Returns
        -------
        str
            LaTeX formatted string representation.

        Note
        ----
        LaTeX generation is not yet implemented.
        """
        # TODO: Implement LaTeX generation for torsion check
        return ""


if __name__ == "__main__":
    # Example implementation of torsion check for a rectangular RC beam
    # Based on EN 1992-1-1:2004 Chapter 6.3

    from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
    from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
    from blueprints.structural_sections.concrete.covers import CoversRectangular
    from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
    from blueprints.unit_conversion import KN_TO_N, NMM_TO_KNM

    print("=== Torsion Check Example ===")
    print("Rectangular RC beam subjected to combined shear and torsion")
    print("Following EN 1992-1-1:2004 Chapter 6.3\n")

    # 1. Define material properties
    print("1. Material Properties:")
    concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C35_45)
    steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)
    print(f"   Concrete: {concrete.concrete_class}")
    print(f"   Steel: {steel.steel_quality}\n")

    # 2. Define cross-section geometry
    print("2. Cross-section Geometry:")
    cs = RectangularReinforcedCrossSection(
        width=400,  # mm
        height=600,  # mm
        covers=CoversRectangular(upper=40, right=40, lower=40, left=40),
        concrete_material=concrete,
    )
    print(f"   Width: {cs.width} mm")
    print(f"   Height: {cs.height} mm")
    print("   Concrete cover: 40 mm (all sides)\n")

    # 3. Add reinforcement
    print("3. Reinforcement Details:")
    # Longitudinal reinforcement
    cs.add_longitudinal_reinforcement_by_quantity(
        n=2,
        diameter=16,
        edge="upper",
        material=steel,
    )
    cs.add_longitudinal_reinforcement_by_quantity(
        n=2,
        diameter=20,
        edge="lower",
        material=steel,
    )
    print("   Longitudinal: 2Ø16 (top) + 2Ø20 (bottom)")

    # Stirrups for shear and torsion
    cs.add_stirrup_along_edges(diameter=10, distance=200, material=steel, shear_check=True, torsion_check=False)
    cs.add_stirrup_along_edges(diameter=10, distance=75, material=steel, shear_check=False, torsion_check=True)
    # cs.plot(show=True)
    print("   Stirrups: Ø10 @ 200mm (shear) + Ø10 @ 75mm (torsion)\n")

    # 4. Define loading
    print("4. Applied Forces:")
    v_ed = 327 * KN_TO_N  # Shear force in N
    t_ed = 60 * KNM_TO_NMM  # Torsion moment in Nmm
    sigma_cp = 0  # Concrete compressive stress in cross-section due to axial loading and/or prestressing, assuming zero for this example
    a_sl = 628  # The area of the tensile reinforcement, which extends lbd + d beyond the section considered

    print(f"   Shear force (V_Ed): {v_ed * N_TO_KN:.0f} kN")
    print(f"   Torsion moment (T_Ed): {t_ed * NMM_TO_KNM:.0f} kNm")
    print(f"   Axial stress (σ_cp): {sigma_cp:.0f} MPa")
    print(f"   Extended tension reinforcement (A_sl): {a_sl:.0f} mm²\n")

    # 5. Perform torsion check
    print("5. Performing Torsion Check:")
    torsion_check = TorsionCheck(
        cs=cs,
        sigma_cp=sigma_cp,
        a_sl=a_sl,
        v_ed=v_ed,
        t_ed=t_ed,
    )

    # Print detailed results
    torsion_check.print_results()

    # Get additional reinforcement requirements
    additional_reinf = torsion_check.get_additional_reinforcement_requirements()

    print("\n6. Design Recommendations:")
    if additional_reinf["additional_longitudinal_torsion"] > 0:
        print(f"   • Add {additional_reinf['additional_longitudinal_torsion']:.0f} mm² longitudinal reinforcement for torsion")
    if additional_reinf["additional_longitudinal_shear"] > 0:
        print(f"   • Add {additional_reinf['additional_longitudinal_shear']:.0f} mm² longitudinal reinforcement for shear")

    # Overall assessment
    overall_check = torsion_check.check()
    print("\n7. Final Assessment:")
    if overall_check:
        print("   ✅ Cross-section is adequate for combined shear and torsion")
    else:
        print("   ❌ Cross-section requires modification")
        print("   💡 Consider increasing section size or concrete class")

    print(f"\n{'=' * 50}")
    print("Example completed. Check results above for design adequacy.")
    print("For detailed calculations, refer to EN 1992-1-1:2004 Chapter 6.3")
