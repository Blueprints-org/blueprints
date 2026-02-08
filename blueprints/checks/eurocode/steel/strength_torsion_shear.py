"""Module for checking torsional shear stress resistance with shear force present (Eurocode 2, formula 6.23)."""

from dataclasses import dataclass
from typing import ClassVar, Literal

import numpy as np
from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.steel.strength_shear import CheckStrengthShearClass12IProfile
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_19 import Form6Dot19CheckDesignElasticShearResistance
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
class CheckStrengthTorsionShearClass12IProfile:
    """Class to perform torsion resistance check with extra shear force for I profiles cross section 1 and 2 (Eurocode 3), using St. Venant torsion.

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
        The applied torsional moment (positive value, in kNm).
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
    from blueprints.checks.eurocode.steel.strength_torsion_shear import CheckStrengthTorsionShearClass12IProfile
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    m_x = 10  # Applied torsional moment in kNm
    v = 100  # Applied shear force in kN
    axis = "Vz"  # Shear force applied in z-direction

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthTorsionShearClass12IProfile(heb_300_s355, mx, v=v, axis=axis, gamma_m0=1.0)
    calc.report().to_word("torsion_and_shear_strength.docx", language="nl")

    """

    steel_cross_section: SteelCrossSection
    m_x: KNM = 0
    v: KN = 0
    axis: Literal["Vz", "Vy"] = "Vz"
    gamma_m0: DIMENSIONLESS = 1.0
    section_properties: SectionProperties | None = None
    name: str = "Torsion strength check for steel I-profiles class 1 and 2"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties and check profile type."""
        if not isinstance(self.steel_cross_section.profile, IProfile):
            raise TypeError("The provided profile is not an I-profile.")
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties()
            object.__setattr__(self, "section_properties", section_properties)

    def calculation_formula(self) -> dict[str, Formula | float]:
        """Calculate torsion resistance check.

        Returns
        -------
        dict[str, Formula | float]
            Calculation results keyed by formula number. Returns an empty dict if no torsion is applied.
        """
        shear_calculation = CheckStrengthShearClass12IProfile(
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
        unit_sig_zxy = unit_stress.get_stress()[0]["sig_zxy"]
        unit_max_sig_zxy = float(np.max(np.abs(unit_sig_zxy)))

        tau_t_ed = abs(self.m_x) * unit_max_sig_zxy
        v_ed = abs(self.v) * KN_TO_N

        v_pl_t_rd = Form6Dot26VplTRdIOrHSection(
            tau_t_ed=tau_t_ed, f_y=self.steel_cross_section.yield_strength, gamma_m0=self.gamma_m0, v_pl_rd=v_pl_rd
        )

        check_torsion_with_shear = Form6Dot25CheckCombinedShearForceAndTorsionalMoment(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd)

        return {
            "unit_shear_stress": unit_max_sig_zxy,
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
        provided = abs(self.v) * KN_TO_N
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
        if self.m_x == 0:
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
        m_x_val = f"{self.m_x:.{n}f}"
        unit_stress_val = f"{formulas['unit_shear_stress']:.{n}f}"
        axis_label = "(vertical) z" if self.axis == "Vz" else "(horizontal) y"
        total_stress_val = f"{formulas['unit_shear_stress'] * self.m_x:.{n}f}"

        report.add_paragraph(
            rf"Profile {profile_name} with steel quality {steel_quality} "
            rf"is loaded with a torsion of {m_x_val} kNm a shear force of {abs(self.v):.{n}f} kN in the {axis_label}-direction. "
            rf"First, the unit torsional stress (at 1 kNm) is defined as {unit_stress_val} MPa. "
            rf"With the applied torsion, this results in a torsional stress of {total_stress_val} MPa. "
            rf"The shear area and resistance (without torsion) are calculated as follows:"
        )

        shear_area_formula = formulas["shear_area"]
        raw_shear_resistance_formula = formulas["raw_shear_resistance"]
        resistance_formula = formulas["resistance"]
        check_formula = formulas["check"]

        assert isinstance(shear_area_formula, Formula), "Expected Formula for shear_area"
        assert isinstance(raw_shear_resistance_formula, Formula), "Expected Formula for raw_shear_resistance"
        assert isinstance(resistance_formula, Formula), "Expected Formula for resistance"
        assert isinstance(check_formula, Formula), "Expected Formula for check"

        report.add_formula(shear_area_formula, n=n, split_after=[(2, "="), (7, "+"), (3, "=")])
        report.add_formula(raw_shear_resistance_formula, n=n)
        report.add_paragraph("Next, the combined torsion and shear resistance is calculated as follows:")
        report.add_formula(resistance_formula, n=n)
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(check_formula, n=n)
        if self.result().is_ok:
            report.add_paragraph("The check for torsion satisfies the requirements.")
        else:
            report.add_paragraph("The check for torsion does NOT satisfy the requirements.")
        return report


@dataclass(frozen=True)
class CheckStrengthTorsionShearClass34:
    """Class to perform torsion resistance check with extra shear force for cross section class 3 and 4 (Eurocode 3), using St. Venant torsion.

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
        The steel cross-section to check.
    m_x : KNM
        The applied torsional moment (positive value, in kNm).
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
    from blueprints.checks.eurocode.steel.strength_torsion_shear import CheckStrengthTorsionShearClass34
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    m_x = 10  # Applied torsional moment in kNm
    v = 100  # Applied shear force in kN
    axis = "Vz"  # Shear force applied in z-direction

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthTorsionShearClass34(heb_300_s355, m_x, v=v, axis=axis, gamma_m0=1.0)
    calc.report().to_word("torsion_and_shear_strength.docx", language="nl")

    """

    steel_cross_section: SteelCrossSection
    m_x: KNM = 0
    v: KN = 0
    axis: Literal["Vz", "Vy"] = "Vz"
    gamma_m0: DIMENSIONLESS = 1.0
    section_properties: SectionProperties | None = None
    name: str = "Torsion strength check for steel class 3 and 4"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties and check profile type."""
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties()
            object.__setattr__(self, "section_properties", section_properties)

    def calculation_formula(self) -> dict[str, Formula | float]:
        """Calculate torsion resistance check.

        Returns
        -------
        dict[str, Formula | float]
            Calculation results keyed by formula number. Returns an empty dict if no torsion is applied.
        """
        rif1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="N/A",
            result_for=ResultFor.LOAD_CASE,
            load_case="N/A",
            vy=self.v if self.axis == "Vy" else 0,
            vz=self.v if self.axis == "Vz" else 0,
            mx=self.m_x,
        )

        stress = self.steel_cross_section.profile.calculate_stress(rif1d)
        sig_zxy = stress.get_stress()[0]["sig_zxy"]
        max_sig_zxy = float(np.max(np.abs(sig_zxy)))

        shear_resistance = self.steel_cross_section.yield_strength / np.sqrt(3) / self.gamma_m0

        check_torsion_with_shear = Form6Dot19CheckDesignElasticShearResistance(
            tau_ed=max_sig_zxy, f_y=self.steel_cross_section.yield_strength, gamma_m0=self.gamma_m0
        )

        return {
            "shear_stress": max_sig_zxy,
            "resistance": shear_resistance,
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
        provided = 0 if self.m_x == 0 else abs(self.v) * KN_TO_N
        provided = steps["shear_stress"]
        required = steps["resistance"]
        return CheckResult.from_comparison(provided=provided, required=float(required))

    def report(self, n: int = 2) -> Report:
        """Returns the report for the elastic torsion check (Class 3/4).

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the elastic torsion check.
        """
        report = Report("Check: elastic torsion with shear force on steel beam (Class 3/4)")
        if self.m_x == 0:
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
        m_x_val = f"{self.m_x:.{n}f}"
        axis_label = "(vertical) z" if self.axis == "Vz" else "(horizontal) y"
        shear_stress_val = f"{formulas['shear_stress']:.{n}f}"

        report.add_paragraph(
            rf"Profile {profile_name} with steel quality {steel_quality} "
            rf"is loaded with a torsion of {m_x_val} kNm and a shear force of {abs(self.v):.{n}f} kN in the {axis_label}-direction. "
            rf"For class 3/4 sections, the combined shear stress from torsion and shear is calculated using elastic theory. "
            rf"The maximum combined shear stress is: {shear_stress_val} N/mm²."
        )

        tau_max = round(self.steel_cross_section.yield_strength / (np.sqrt(3) * self.gamma_m0), n)
        report.add_paragraph("The maximum allowed elastic shear stress is calculated as follows:")
        report.add_paragraph(rf"$f_y / (\sqrt{{3}} \cdot \gamma_{{M0}})$ = {tau_max} N/mm².")

        report.add_paragraph("The unity check is calculated as follows:")
        check_formula = formulas["check"]
        assert isinstance(check_formula, Formula), "Expected Formula for check"
        report.add_formula(check_formula, n=n)
        if self.result().is_ok:
            report.add_paragraph("The check for elastic torsion with shear satisfies the requirements.")
        else:
            report.add_paragraph("The check for elastic torsion with shear does NOT satisfy the requirements.")
        return report
