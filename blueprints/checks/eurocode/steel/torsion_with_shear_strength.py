"""Module for checking torsional shear stress resistance with shear force present (Eurocode 2, formula 6.23)."""

from dataclasses import dataclass, field
from typing import ClassVar, Literal

import numpy as np
from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.steel.shear_strength import PlasticShearStrengthIProfileCheck
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_25 import Form6Dot25CheckCombinedShearForceAndTorsionalMoment
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_26 import Form6Dot26VplTRdIOrHSection
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN, KNM
from blueprints.unit_conversion import KN_TO_N
from blueprints.utils.report import Report


@dataclass(frozen=True)
class TorsionWithShearStrengthIProfileCheck:
    """Class to perform torsion resistance check with extra shear force for I profiles (Eurocode 3), using St. Venant torsion.

    Coordinate System:

        z (vertical, usually strong axis)
            ↑
            |     x (longitudinal beam direction, into screen)
            |    ↗
            |   /
            |  /
            | /
            |/
      ←-----O
       y (horizontal/side, usually weak axis)

    Parameters
    ----------
    steel_cross_section : SteelCrossSection
        The steel cross-section, of type I-profile, to check.
    mx : KNM
        The applied shear force (positive value, in kN).
    v : KN
        The applied shear force (positive value, in kN).
    axis : Literal["Vz", "Vy"]
        Axis along which the shear force is applied. "Vz" (default) for z (vertical), "Vy" for y (horizontal).
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    section_properties : SectionProperties | None, optional
        Pre-calculated section properties. If None, they will be calculated internally.

    Example
    -------
    from blueprints.checks.eurocode.steel.torsion_with_shear_strength import TorsionWithShearStrengthIProfileCheck
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    mx = 10  # Applied torsional moment in kNm
    v = 100  # Applied shear force in kN
    axis = "Vz"  # Shear force applied in z-direction

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = TorsionWithShearStrengthIProfileCheck(heb_300_s355, mx, v=v, axis=axis, gamma_m0=1.0)
    calc.report().to_word("torsion_and_shear_strength.docx", language="nl")

    """

    steel_cross_section: SteelCrossSection
    mx: KNM = 0
    v: KN = 0
    axis: Literal["Vz", "Vy"] = "Vz"
    gamma_m0: DIMENSIONLESS = 1.0
    section_properties: SectionProperties | None = None
    name: str = "Torsion strength check for steel I-profiles"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]
    _profile: IProfile = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties and check profile type."""
        if not isinstance(self.steel_cross_section.profile, IProfile):
            raise TypeError("The provided profile is not an I-profile.")
        object.__setattr__(self, "_profile", self.steel_cross_section.profile)
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties()
            object.__setattr__(self, "section_properties", section_properties)

    def calculation_formula(self) -> dict[str, Formula]:
        """Calculate torsion resistance check.

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number. Returns an empty dict if no torsion is applied.
        """
        shear_calculation = PlasticShearStrengthIProfileCheck(
            steel_cross_section=self.steel_cross_section,
            v=self.v,
            axis=self.axis,
            gamma_m0=self.gamma_m0,
            section_properties=self.section_properties,
        )

        shear_formulas = shear_calculation.calculation_formula()
        a_v = shear_formulas["shear_area"]
        v_pl_rd = shear_formulas["resistance"]

        rif1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="N/A",
            result_for=ResultFor.LOAD_CASE,
            load_case="N/A",
            mx=1,  # 1 kNm
        )

        unit_stress = self.steel_cross_section.profile.calculate_stress(rif1d)
        unit_sig_zx_mzz = unit_stress.get_stress()[0]["sig_zx_mzz"]
        unit_sig_zy_mzz = unit_stress.get_stress()[0]["sig_zy_mzz"]
        unit_max_mzz_zxy = np.max(np.sqrt(np.array(unit_sig_zx_mzz) ** 2 + np.array(unit_sig_zy_mzz) ** 2))

        tau_t_ed = abs(self.mx) * unit_max_mzz_zxy
        v_ed = abs(self.v) * KN_TO_N

        v_pl_t_rd = Form6Dot26VplTRdIOrHSection(
            tau_t_ed=tau_t_ed, f_y=self.steel_cross_section.yield_strength, gamma_m0=self.gamma_m0, v_pl_rd=v_pl_rd
        )

        check_torsion_with_shear = Form6Dot25CheckCombinedShearForceAndTorsionalMoment(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd)

        return {
            "unit_shear_stress": unit_max_mzz_zxy,
            "shear_area": a_v,
            "raw_shear_resistance": v_pl_rd,
            "resistance": v_pl_t_rd,
            "check": check_torsion_with_shear,
        }

    def result(self) -> CheckResult:
        """Calculate result of torsion resistance.

        Returns
        -------
        CheckResult
            True if the torsion check passes, False otherwise.
        """
        steps = self.calculation_formula()
        provided = 0 if self.mx == 0 else abs(self.v) * KN_TO_N
        required = steps["resistance"]
        return CheckResult.from_comparison(provided=provided, required=float(required))

    def report(self, n: int = 2) -> Report:
        """Returns the report for the torsion check.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the torsion check.
        """
        report = Report("Check: torsion with shear force on steel beam")
        if self.mx == 0:
            report.add_paragraph("No torsion was applied; therefore, no combined torsion with shear force check is necessary.")
            return report
        if self.v == 0:
            report.add_paragraph("No shear force was applied; therefore, no combined torsion with shear force check is necessary.")
            return report

        # Cache calculation formulas to avoid redundant recalculations
        formulas = self.calculation_formula()

        # Get information for the introduction of the report
        profile_name = self.steel_cross_section.profile.name
        steel_quality = self.steel_cross_section.material.steel_class.name
        mx_val = f"{self.mx:.{n}f}"
        unit_stress_val = f"{formulas['unit_shear_stress']:.{n}f}"
        axis_label = "(vertical) z" if self.axis == "Vz" else "(horizontal) y"
        total_stress_val = f"{formulas['unit_shear_stress'] * self.mx:.{n}f}"

        report.add_paragraph(
            rf"Profile {profile_name} with steel quality {steel_quality} "
            rf"is loaded with a torsion of {mx_val} kNm a shear force of {abs(self.v):.{n}f} kN in the {axis_label}-direction. "
            rf"First, the unit torsional stress (at 1 kNm) is defined as {unit_stress_val} MPa. "
            rf"With the applied torsion, this results in a torsional stress of {total_stress_val} MPa. "
            rf"The shear area and resistance (without torsion) are calculated as follows:"
        )

        report.add_formula(formulas["shear_area"], n=n, split_after=[(2, "="), (7, "+"), (3, "=")])
        report.add_formula(formulas["raw_shear_resistance"], n=n)
        report.add_paragraph("Next, the combined torsion and shear resistance is calculated as follows:")
        report.add_formula(formulas["resistance"], n=n)
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(formulas["check"], n=n)
        if self.result().is_ok:
            report.add_paragraph("The check for torsion satisfies the requirements.")
        else:
            report.add_paragraph("The check for torsion does NOT satisfy the requirements.")
        return report
