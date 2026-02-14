"""Module for checking torsional shear stress resistance with shear force present (Eurocode 2, formula 6.23)."""

from dataclasses import dataclass
from typing import Literal

import numpy as np
from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.steel.strength_shear import CheckStrengthShearClass12
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
    name: str = "Torsion strength check for steel class 1 and 2"

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties and check profile type."""
        implemented_shapes = (IProfile,)
        if type(self.steel_cross_section.profile) not in implemented_shapes:
            raise NotImplementedError(f"The provided profile shape {type(self.steel_cross_section.profile).__name__} has not been implemented yet.")

    @staticmethod
    def source_docs() -> list[str]:
        """List of source document identifiers used for this check.

        Returns
        -------
        list[str]
        """
        return [EN_1993_1_1_2005]

    def unit_torsional_shear_stress(self) -> float:
        """Calculate the unit torsional shear stress (at 1 kNm torsion).

        Returns
        -------
        float
            The unit torsional shear stress in MPa.
        """

        unit_stress = self.steel_cross_section.profile.unit_stress
        unit_sig_zxy = unit_stress["sig_zxy_mzz"]
        return float(np.max(np.abs(unit_sig_zxy)))

    def shear_area(self) -> Formula:
        """Calculate the shear area of the I-profile cross-section.

        Returns
        -------
        Formula
            The calculated shear area formula.
        """
        shear_calculation = CheckStrengthShearClass12(
            steel_cross_section=self.steel_cross_section,
            v=self.v,
            axis=self.axis,
            gamma_m0=self.gamma_m0,
            
        )
        return shear_calculation.shear_area()

    def raw_shear_resistance(self) -> Formula:
        """Calculate the plastic shear resistance without torsion.

        Returns
        -------
        Formula
            The calculated plastic shear resistance formula.
        """
        shear_calculation = CheckStrengthShearClass12(
            steel_cross_section=self.steel_cross_section,
            v=self.v,
            axis=self.axis,
            gamma_m0=self.gamma_m0,
            
        )
        return shear_calculation.plastic_resistance()

    def combined_resistance(self) -> Formula:
        """Calculate the combined torsion and shear resistance (EN 1993-1-1:2005 art. 6.2.7 - Formula (6.26)).

        Returns
        -------
        Formula
            The calculated combined resistance formula.
        """
        v_pl_rd = self.raw_shear_resistance()
        unit_max_sig_zxy = self.unit_torsional_shear_stress()
        tau_t_ed = abs(self.m_x) * unit_max_sig_zxy

        return Form6Dot26VplTRdIOrHSection(tau_t_ed=tau_t_ed, f_y=self.steel_cross_section.yield_strength, gamma_m0=self.gamma_m0, v_pl_rd=v_pl_rd)

    def combined_unity_check(self) -> Formula:
        """Calculate the unity check for combined shear force and torsional moment (EN 1993-1-1:2005 art. 6.2.7 - Formula (6.25)).

        Returns
        -------
        Formula
            The calculated unity check formula.
        """
        v_ed = abs(self.v) * KN_TO_N
        v_pl_t_rd = self.combined_resistance()

        return Form6Dot25CheckCombinedShearForceAndTorsionalMoment(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd)

    def result(self) -> CheckResult:
        """Calculate result of torsion resistance.

        Returns
        -------
        CheckResult
            True if the torsion check passes, False otherwise.
        """
        provided = 0 if self.m_x == 0 else abs(self.v) * KN_TO_N
        required = float(self.combined_resistance())
        return CheckResult.from_comparison(provided=provided, required=required)

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

        # will not generate a report if no torsion or shear is applied
        if self.m_x == 0:
            report.add_paragraph("No torsion was applied; therefore, no combined torsion with shear force check is necessary.")
            return report
        if self.v == 0:
            report.add_paragraph("No shear force was applied; therefore, no combined torsion with shear force check is necessary.")
            return report

        # introduction
        profile_name = self.steel_cross_section.profile.name
        steel_quality = self.steel_cross_section.material.steel_class.name
        axis_label = "(vertical) z" if self.axis == "Vz" else "(horizontal) y"
        report.add_paragraph(
            f"Profile {profile_name} with steel quality {steel_quality} "
            f"is loaded with a torsion of {self.m_x:.{n}f} kNm and a shear force of {abs(self.v):.{n}f} kN in the {axis_label}-direction."
        )
        report.add_newline(n=2)

        # unit torsional shear stress
        unit_stress_val = self.unit_torsional_shear_stress()
        total_stress_val = unit_stress_val * self.m_x
        report.add_paragraph(
            f"The unit torsional stress (at 1 kNm) is: {unit_stress_val:.{n}f} MPa. "
            f"With the applied torsion, this results in a torsional stress of {total_stress_val:.{n}f} MPa."
        )
        report.add_newline(n=2)

        # shear area and resistance (without torsion)
        report.add_paragraph("The shear area and resistance (without torsion) are calculated as follows:")
        report.add_formula(self.shear_area(), n=n, split_after=[(2, "="), (7, "+"), (3, "=")])
        report.add_formula(self.raw_shear_resistance(), n=n)
        report.add_newline(n=2)

        # combined torsion and shear resistance
        report.add_paragraph("The combined torsion and shear resistance is calculated as follows:")
        report.add_formula(self.combined_resistance(), n=n)
        report.add_newline(n=2)

        # unity check
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(self.combined_unity_check(), n=n)
        report.add_newline(n=2)

        # add overall result
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
    name: str = "Torsion strength check for steel class 3 and 4"

    @staticmethod
    def source_docs() -> list[str]:
        """List of source document identifiers used for this check.

        Returns
        -------
        list[str]
        """
        return [EN_1993_1_1_2005]

    def combined_shear_stress(self) -> float:
        """Calculate the combined shear stress from torsion and shear using elastic theory.

        Returns
        -------
        float
            The maximum combined shear stress in MPa.
        """

        stress = self.steel_cross_section.profile.calculate_stress(
            v_y=self.v if self.axis == "Vy" else 0,
            v_z=self.v if self.axis == "Vz" else 0,
            m_x=self.m_x,
        )
        sig_zxy = stress.get_stress()[0]["sig_zxy"]
        return float(np.max(np.abs(sig_zxy)))

    def elastic_resistance(self) -> float:
        """Calculate the elastic shear resistance.

        Returns
        -------
        float
            The calculated elastic shear resistance in MPa.
        """
        return float(self.steel_cross_section.yield_strength / np.sqrt(3) / self.gamma_m0)

    def combined_unity_check(self) -> Formula:
        """Calculate the unity check for combined elastic shear and torsion (EN 1993-1-1:2005 art. 6.2.6 - Formula (6.19)).

        Returns
        -------
        Formula
            The calculated unity check formula.
        """
        tau_ed = self.combined_shear_stress()
        return Form6Dot19CheckDesignElasticShearResistance(tau_ed=tau_ed, f_y=self.steel_cross_section.yield_strength, gamma_m0=self.gamma_m0)

    def result(self) -> CheckResult:
        """Calculate result of torsion resistance.

        Returns
        -------
        CheckResult
            True if the torsion check passes, False otherwise.
        """
        provided = self.combined_shear_stress()
        required = self.elastic_resistance()
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

        # will not generate a report if no torsion or shear is applied
        if self.m_x == 0:
            report.add_paragraph("No torsion was applied; therefore, no combined torsion with shear force check is necessary.")
            return report
        if self.v == 0:
            report.add_paragraph("No shear force was applied; therefore, no combined torsion with shear force check is necessary.")
            return report

        # introduction
        profile_name = self.steel_cross_section.profile.name
        steel_quality = self.steel_cross_section.material.steel_class.name
        axis_label = "(vertical) z" if self.axis == "Vz" else "(horizontal) y"
        report.add_paragraph(
            f"Profile {profile_name} with steel quality {steel_quality} "
            f"is loaded with a torsion of {self.m_x:.{n}f} kNm and a shear force of {abs(self.v):.{n}f} kN in the {axis_label}-direction. "
            f"For class 3/4 sections, the combined shear stress from torsion and shear is calculated using elastic theory."
        )
        report.add_newline(n=2)

        # combined shear stress
        shear_stress_val = self.combined_shear_stress()
        report.add_paragraph(f"The maximum combined shear stress is: {shear_stress_val:.{n}f} N/mm².")
        report.add_newline(n=2)

        # elastic resistance
        tau_max = self.elastic_resistance()
        report.add_paragraph("The maximum allowed elastic shear stress is calculated as follows:")
        report.add_paragraph(rf"$f_y / (\sqrt{{3}} \cdot \gamma_{{M0}})$ = {tau_max:.{n}f} N/mm².")
        report.add_newline(n=2)

        # unity check
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(self.combined_unity_check(), n=n)
        report.add_newline(n=2)

        # add overall result
        if self.result().is_ok:
            report.add_paragraph("The check for elastic torsion with shear satisfies the requirements.")
        else:
            report.add_paragraph("The check for elastic torsion with shear does NOT satisfy the requirements.")
        return report
