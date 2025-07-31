r"""Example for torsion calculation for a rectangular reinforced concrete cross-section.
Based on the calculation example from Technische Universiteit Delft:
https://www.studeersnel.nl/nl/document/technische-universiteit-delft/concrete-structures-2/torsion/29391885
"""

from dataclasses import dataclass, field

from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.concrete.rebar import Rebar

from blueprints.codes.latex_formula import latex_max_curly_brackets
from blueprints.type_alias import MM, DEG, N, NMM, MPA, MM2, DIMENSIONLESS
from blueprints.unit_conversion import KN_TO_N, N_TO_KN, MM_TO_M

from blueprints.materials.reinforcement_steel import (
    ReinforcementSteelMaterial,
)
from blueprints.math_helpers import cot

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_2 import (
    Form6Dot2ShearResistance,
    Form6Dot2aSub1ThicknessFactor,
    Form6Dot2aSub2RebarRatio,
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
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_6n import Form9Dot6nMaximumDistanceShearReinforcement


# FIXME: Move to another module
@dataclass
class CheckResult:
    r"""Class to hold the result of a check."""

    is_ok: bool
    utilization: float
    required: float | None
    provided: float | None


@dataclass(frozen=True)
class TorsionCheck:
    r"""Class responsible for the torsion cross-section check according to art. 6.3.
    Includes the interaction between shear and torsion.


    Parameters
    ----------
    cs: RectangularReinforcedCrossSection
        The cross-section object containing geometry and reinforcement details.
    sigma_cp: MPA
        Mean compressive stress, measured positive, due to the design axial force [$MPa$].
    a_sl: MM2
        Area of the tensile reinforcement, which extends l_bd + d beyond the section considered (figure 6.3 EN 1992-1-1) [$mm²$].
    v_ed: N
        Shear force in the cross-section [$N$].
    t_ed: NMM
        Torsion moment in the cross-section [$Nmm$].
    alpha: DEG
        Angle between shear reinforcement and the beam axis perpendicular to the shear force [$°$].
        The default value is 90°.
    theta: DEG
        Angle between the concrete compression strut and the beam axis perpendicular to the shear force [$°$].
        The default value is 45°.
    """

    label = "Torsion according to art. 6.3"
    source_document = "EN 1992-1-1"

    cs: RectangularReinforcedCrossSection
    sigma_cp: MPA
    a_sl: MM2
    v_ed: N
    t_ed: NMM

    alpha: DEG = field(default=90)
    theta: DEG = field(default=45)  # FIXME: Now it is always 45 degrees as a convervatime approach. The value can and should be calculated

    # FIXME: Now the same material for all tension rebars and all stirrups is assumed
    def get_cs_tension_rebars_material(self) -> ReinforcementSteelMaterial:
        """Return the material used for all tension rebars, or raise an error if mixed."""
        tension_rebars = self.get_cs_tension_rebars()
        materials = {rebar.material for rebar in tension_rebars}

        if not materials:
            raise ValueError("No tension rebars found.")
        if len(materials) > 1:
            raise ValueError(f"Multiple materials found in tension rebars: {[m.name for m in materials]}")

        return materials.pop()

    def get_cs_stirrups_material(self) -> ReinforcementSteelMaterial:
        """Return the material used for all stirrups, or raise an error if mixed."""
        materials = {rebar.material for rebar in self.cs.stirrups}

        if not materials:
            raise ValueError("No stirrups found.")
        if len(materials) > 1:
            raise ValueError(f"Multiple materials found in stirrups: {[m.name for m in materials]}")

        return materials.pop()

    # FIXME: These methods should rather be moved to the cross-section class. Have to be updated after the work on tension calculator is finished
    def get_cs_tension_rebars(self) -> list[Rebar]:
        """Get the tension reinforcement rebars in the cross-section."""
        # FIXME: Now it gets only one line of bottom rebars
        lower_y = min(rebar.y for rebar in self.cs.longitudinal_rebars)
        return [rebar for rebar in self.cs.longitudinal_rebars if abs(rebar.y - lower_y) < 1e-3]

    def get_c_nom_center(self) -> MM:
        """Get the distance between edge and centre of the longitudinal reinforcement"""
        # FIXME: Now only takes the maximum diameter of the tension bars into account
        thickest_rebar = max(self.get_cs_tension_rebars(), key=lambda r: r.diameter)
        cs_lower_edge = min(pt[1] for pt in self.cs.cross_section.polygon.exterior.coords)
        return abs(thickest_rebar.y - cs_lower_edge)

    def get_cs_depth(self) -> MM:
        """Get effective cross-section depth"""
        return self.cs.height - self.get_c_nom_center()

    def get_cs_lever_arm(self) -> MM:
        """Get the inner lever arm of the cross-section."""
        return 0.9 * self.get_cs_depth()

    def t_ef_i(self) -> MM:
        """The effective wall thickness."""
        return max(self.cs.cross_section.area / self.cs.cross_section.perimeter, 2 * self.get_c_nom_center())

    def a_k(self) -> MM2:
        """The area enclosed by the centre-lines of the connecting walls."""
        return (self.cs.width - self.t_ef_i()) * (self.cs.height - self.t_ef_i())

    def u_k(self) -> MM:
        """The perimeter of the area a_k."""
        return 2 * (self.cs.width + self.cs.height - 2 * self.t_ef_i())

    def alpha_cw(self) -> Form6Dot11abcNCompressionChordCoefficient | DIMENSIONLESS:
        """Coefficient taking account of the state of the stress in the compression chord according to art. 6.2.3 (3) from EN 1992-1-1"""
        if self.sigma_cp is None or self.sigma_cp <= 0:
            return 1.0
        return Form6Dot11abcNCompressionChordCoefficient(
            sigma_cp=self.sigma_cp,
            f_cd=self.cs.concrete_material.f_cd,
        )

    def nu(self) -> Form6Dot6nStrengthReductionFactor:
        """Strength reduction factor for concrete cracked in shear according to art. 6.2.2 (6) from EN 1992-1-1."""
        return Form6Dot6nStrengthReductionFactor(f_ck=self.cs.concrete_material.f_ck)

    def check_concrete_strut_capacity(self) -> CheckResult:
        """Check the capacity of the concrete struts according to art. 6.3.2 (4) from EN 1992-1-1."""
        # The maximum shear resistance
        v_rd_max = Form6Dot9MaximumShearResistance(b_w=self.cs.width, z=self.get_cs_lever_arm(), f_cd=self.cs.concrete_material.f_cd, nu_1=self.nu(), alpha_cw=self.alpha_cw(), theta=self.theta)

        # The design torsional resistance moment
        t_rd_max = Form6Dot30DesignTorsionalResistanceMoment(nu=self.nu(), alpha_cw=self.alpha_cw(), f_cd=self.cs.concrete_material.f_cd, a_k=self.a_k(), t_ef_i=self.t_ef_i(), theta=self.theta)

        # Check if the applied combination of forces can be taken by the concrete strut in compression
        utilization = self.t_ed / t_rd_max + self.v_ed / v_rd_max
        is_ok = Form6Dot29CheckTorsionShearResistance(t_ed=self.t_ed, v_ed=self.v_ed, t_rd_max=t_rd_max, v_rd_max=v_rd_max)
        return CheckResult(is_ok=is_ok, utilization=utilization, required=None, provided=None)

    def check_torsion_moment_capacity(self) -> CheckResult:
        """Check whether the combination of forces can be resisted with minimum reinforcement only according to art. 6.3.2 (5) from EN 1992-1-1."""
        # Torsion moment capacity
        # The torsional shear stress in wall i, can be set to be equal to fctd
        tau_t_i = self.cs.concrete_material.f_ctd

        # The torsional cracking moment
        t_rd_c = 2 * self.a_k() * tau_t_i * self.t_ef_i()

        # Shear capacity
        # Coefficient for shear strength according to art. 6.2.2 (1) from EN 1992-1-1
        c_rd_c = 0.18 / self.cs.concrete_material.material_factor

        # Coefficient for concrete according to art. 6.2.2 (1) from EN 1992-1-1
        k_1 = 0.15

        # Size effect factor according to art. 6.2.2 (1) from EN 1992-1-1
        k = Form6Dot2aSub1ThicknessFactor(d=self.get_cs_depth())

        # Minimum shear capacity according to art. 6.2.2 (1) from EN 1992-1-1
        v_min = Form6Dot3NShearCapacityWithoutRebar(k=k, f_ck=self.cs.concrete_material.f_ck)

        # Tensile rebar ratio according to art. 6.2.2 (1) from EN 1992-1-1
        rho_l = Form6Dot2aSub2RebarRatio(a_sl=self.a_sl, b_w=self.cs.width, d=self.get_cs_depth())

        # The design value for the shear resistance
        v_rd_c = Form6Dot2ShearResistance(
            c_rd_c=c_rd_c,
            k=k,
            rho_l=rho_l,
            f_ck=self.cs.concrete_material.f_ck,
            k_1=k_1,
            sigma_cp=self.sigma_cp,
            b_w=self.cs.width,
            d=self.get_cs_depth(),
            v_min=v_min,
        )

        # Check if the section meets the minimum reinforcement requirements for the applied forces
        utilization = self.t_ed / t_rd_c + self.v_ed / v_rd_c
        is_ok = Form6Dot31CheckTorsionShearResistanceRectangular(t_ed=self.t_ed, t_rd_c=t_rd_c, v_ed=self.v_ed, v_rd_c=v_rd_c)
        return CheckResult(is_ok=is_ok, utilization=utilization, required=None, provided=None)

    def check_max_longitudinal_reinforcement_area(self) -> CheckResult:
        """Check if the maximum longitudinal reinforcement is not exceeded according to art. 9.2.1.1 (3) from EN 1992-1-1."""
        a_s_max = 0.04 * self.cs.cross_section.area
        a_s = self.cs.reinforcement_area_longitudinal_bars
        utilization = a_s / a_s_max if a_s_max > 0 else float("inf")
        is_ok = a_s_max >= a_s
        return CheckResult(is_ok=is_ok, utilization=utilization, required=a_s_max, provided=a_s)

    def check_min_tensile_reinforcement_area(self) -> CheckResult:
        """Check if the minimum tensile reinforcement is provided for a beam according to art. 9.2.1.1 (1) from EN 1992-1-1"""
        a_st_min = Form9Dot1nMinimumTensileReinforcementBeam(f_ctm=self.cs.concrete_material.f_ctm, f_yk=self.get_cs_tension_rebars_material().f_yk, b_t=self.cs.width, d=self.get_cs_depth())
        a_st = sum(rebar.area for rebar in self.get_cs_tension_rebars())
        utilization = a_st_min / a_st if a_st > 0 else float("inf")
        is_ok = a_st >= a_st_min
        return CheckResult(is_ok=is_ok, utilization=utilization, required=a_st_min, provided=a_st)

    def check_max_spacing_for_shear_stirrups(self) -> CheckResult:
        """Check if the spacing between shear stirrups is not exceeded according to art. 9.2.2 (6) from EN 1992-1-1."""
        s_l_max = Form9Dot6nMaximumDistanceShearReinforcement(self.get_cs_depth(), self.alpha)
        s = max(stirrup.distance for stirrup in self.cs.stirrups if stirrup.shear_check)
        utilization = s / s_l_max if s_l_max > 0 else float("inf")
        is_ok = s <= s_l_max
        return CheckResult(is_ok=is_ok, utilization=utilization, required=s_l_max, provided=s)

    def check_max_spacing_for_torsion_stirrups(self) -> CheckResult:
        """Check if the spacing between torsion stirrups is not exceeded according to art. 9.2.3 (3) from EN 1992-1-1."""
        s_l_max = Form9Dot6nMaximumDistanceShearReinforcement(self.get_cs_depth(), self.alpha)
        s_max = min(self.cs.cross_section.perimeter / 8, s_l_max, self.cs.width, self.cs.height)
        s = max(stirrup.distance for stirrup in self.cs.stirrups if stirrup.torsion_check)
        utilization = s / s_max if s_l_max > 0 else float("inf")
        is_ok = s <= s_max
        return CheckResult(is_ok=is_ok, utilization=utilization, required=s_max, provided=s)

    def check_shear_and_torsion_stirrups_area(self) -> CheckResult:
        """Check if the the required stirrups is enough to be able to resist the occurring combination of forces."""
        # Reinforcement design yield strength
        f_ywd = self.get_cs_stirrups_material().f_yk / 1.15

        # Required stirrups for the shear force
        a_sw_s_w_v = self.v_ed / (self.get_cs_lever_arm() * cot(self.theta) * f_ywd)

        # Shear stress in a wall of a section subject to a pure torsional moment
        tau_t_i_t_ef_i = Form6Dot26ShearStressInWall(t_ed=self.t_ed, a_k=self.a_k())

        # Shear force due to torsion
        v_ed_i = Form6Dot27ShearForceInWall(tau_t_i_t_ef_i=tau_t_i_t_ef_i, z_i=self.cs.height)

        # Required stirrups for the torsion moment
        a_sw_s_w_t = v_ed_i / (self.cs.height * cot(self.theta) * f_ywd)

        # Total required stirrup reinforcement
        a_sw_s_w_total = a_sw_s_w_v + a_sw_s_w_t * 2

        # Actual stirrup reinforcement
        # FIXME: It is currently assumed that all types of stirrups work in torsion and shear
        a_sw_prov = sum(stirrup.as_w for stirrup in self.cs.stirrups if stirrup.torsion_check or stirrup.shear_check) * MM_TO_M

        utilization = a_sw_s_w_total / a_sw_prov if a_sw_prov > 0 else float("inf")
        is_ok = a_sw_prov >= a_sw_s_w_total
        return CheckResult(is_ok=is_ok, utilization=utilization, required=a_sw_s_w_total, provided=a_sw_prov)

    def check_min_shear_reinforcement_ratio(self) -> CheckResult:
        """Minimum shear reinforcement ratio according to art. 9.2.2 (5) from EN 1992-1-1"""
        # Minimum shear reinforcement ratio
        rho_w_min = Form9Dot5nMinimumShearReinforcementRatio(f_ck=self.cs.concrete_material.f_ck, f_yk=self.get_cs_stirrups_material().f_yk)

        # Shear reinforcement ratio according to art. 9.2.2 (5) from EN 1992-1-1
        # FIXME: It is currently assumed that all types of stirrups work in torsion and shear
        a_sw_prov = sum(stirrup.as_w for stirrup in self.cs.stirrups if stirrup.torsion_check or stirrup.shear_check) * MM_TO_M
        rho_w = Form9Dot4ShearReinforcementRatio(a_sw=a_sw_prov, s=1.0, b_w=self.cs.width, alpha=self.alpha)

        utilization = rho_w_min / rho_w if rho_w > 0 else float("inf")
        is_ok = rho_w >= rho_w_min
        return CheckResult(is_ok=is_ok, utilization=utilization, required=rho_w_min, provided=rho_w)

    def check(self) -> bool:
        """Perform the checks."""
        # Reinforcement design yield strength
        f_yd = self.get_cs_tension_rebars_material().f_yk / 1.15

        # Additional tensile force in the longitudinal reinforcement due to shear according to art. 6.2.3 (7) from EN 1992-1-1
        delta_f_td = Form6Dot18AdditionalTensileForce(self.v_ed * N_TO_KN, self.theta, self.alpha)

        # Additional longitudinal reinforcement for shear
        a_sl_shear = delta_f_td * KN_TO_N / f_yd

        print("Results:")

        # FIXME: Minimum/maximimum rebar area checks should be moved to another module, they have nothing to do with torsion check
        # Also, user have to specify an element type to correctly calculate these values
        print(f"Minimum tensile reinforcement area: {self.check_min_tensile_reinforcement_area().utilization:.2f}")
        print(f"Maximum longitudinal reinforcement area: {self.check_max_longitudinal_reinforcement_area().utilization:.2f}")
        print(f"Minimum shear reinforcement ratio: {self.check_min_shear_reinforcement_ratio().utilization:.2f}")
        print(f"Maximum shear stirrup spacing: {self.check_max_spacing_for_shear_stirrups().utilization:.2f}")
        print(f"Maximum torsion stirrup spacing: {self.check_max_spacing_for_torsion_stirrups().utilization:.2f}")
        print(f"Stirrup reinforcement for shear and torsion: {self.check_shear_and_torsion_stirrups_area().utilization:.2f}")
        print(f"Concrete strut capacity: {self.check_concrete_strut_capacity().utilization:.2f}")

        if not self.check_concrete_strut_capacity().is_ok:
            # Return early if concrete strut capacity is not enough
            print("Concrete strut capacity is not enough. Increase cross-section or concrete class.")
            return False

        print(f"Torsion moment capacity: {self.check_torsion_moment_capacity().utilization:.2f}")
        if self.check_torsion_moment_capacity().is_ok:
            print("The combination of shear and torsion forces can be resisted with provided reinforcement.")
        else:
            print("Torsion moment capacity is not enough. Additional reinforcement is required to resist this combination of shear and torsion forces.")

            # Calculate additional longitudinal reinforcement for torsion
            a_sl_torsion = Form6Dot28RequiredCrossSectionalArea(u_k=self.u_k(), f_yd=f_yd, t_ed=self.t_ed, a_k=self.a_k(), theta=self.theta)
            print(f"Required additional longitudinal reinforcement for torsion (to be distributed along beam edges): {a_sl_torsion:.2f} mm²")

        print(f"The required area of the additional longitudinal reinforcement due to shear: {a_sl_shear:.2f} mm²")

        return True

    def latex(self, n: int = 1) -> str:
        """Returns the lateX string representation for the torsion check."""
        # FIXME: To be implemented
        return ""
