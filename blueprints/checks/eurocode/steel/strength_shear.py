"""Module for checking plastic shear force resistance of steel(Eurocode 3)."""

from dataclasses import dataclass
from typing import Literal

import numpy as np

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_17, formula_6_18, formula_6_18_sub_av, formula_6_19
from blueprints.codes.formula import Formula
from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.unit_conversion import KN_TO_N
from blueprints.utils.report import Report


@dataclass(frozen=True)
class CheckStrengthShearClass12:
    """Class to perform plastic shear force resistance check for steel of cross-section class 1 and 2 based on EN 1993-1-1:2005 art. 6.2.6.

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
    v : KN
        The applied shear force (in kN).
    axis : Literal["Vz", "Vy"]
        Axis along which the shear force is applied. "Vz" (default) for z (vertical), "Vy" for y (horizontal).
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    from blueprints.checks.eurocode.steel.strength_shear import CheckStrengthShearClass12
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    v = 100  # Applied shear force in kN

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthShearClass12(heb_300_s355, v, axis="Vz", gamma_m0=1.0)
    calc.report().to_word("shear_strength.docx", language="nl")

    """

    steel_cross_section: SteelCrossSection
    v: KN = 0
    axis: Literal["Vz", "Vy"] = "Vz"
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Plastic shear strength check for steel"

    def __post_init__(self) -> None:
        """Check on implemented_shapes."""
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

    def shear_area(self) -> Formula:
        """Calculate the shear area of the steel cross-section.

        Based on the applied shear force axis and fabrication method
        (EN 1993-1-1:2005 art. 6.2.6(3) - Formulas (6.18a/d/e)).
        """
        if isinstance(self.steel_cross_section.profile, IProfile):
            # Get parameters from profile, average top and bottom flange properties
            a = float(self.steel_cross_section.profile.area)
            b1 = self.steel_cross_section.profile.top_flange_width
            b2 = self.steel_cross_section.profile.bottom_flange_width
            tf1 = self.steel_cross_section.profile.top_flange_thickness
            tf2 = self.steel_cross_section.profile.bottom_flange_thickness
            tw = self.steel_cross_section.profile.web_thickness
            hw = self.steel_cross_section.profile.total_height - (
                self.steel_cross_section.profile.top_flange_thickness + self.steel_cross_section.profile.bottom_flange_thickness
            )
            r1 = self.steel_cross_section.profile.top_radius
            r2 = self.steel_cross_section.profile.bottom_radius

            assert all(param is not None for param in [a, b1, b2, tf1, tf2, tw, hw, r1, r2]), (
                "All profile parameters must be defined for I-profile shear area calculation."
            )

            if self.axis == "Vz" and self.steel_cross_section.fabrication_method in ["hot-rolled", "cold-formed"]:
                return formula_6_18_sub_av.Form6Dot18SubARolledIandHSection(a=a, b1=b1, b2=b2, hw=hw, r1=r1, r2=r2, tf1=tf1, tf2=tf2, tw=tw, eta=1.0)
            if self.axis == "Vz" and self.steel_cross_section.fabrication_method == "welded":
                return formula_6_18_sub_av.Form6Dot18SubDWeldedIHandBoxSection(hw_list=[hw], tw_list=[tw], eta=1.0)
            # when axis == "Vy"
            return formula_6_18_sub_av.Form6Dot18SubEWeldedIHandBoxSection(a=a, hw_list=[hw], tw_list=[tw])
        raise NotImplementedError("Profile type is not supported")  # pragma: no cover

    def plastic_resistance(self) -> Formula:
        """Calculate the shear force plastic resistance of the steel cross-section (EN 1993-1-1:2005 art. 6.2.6(2) - Formula (6.18)).

        Returns
        -------
        Formula
            The calculated shear force resistance.
        """
        a_v = self.shear_area()
        f_y = self.steel_cross_section.yield_strength
        return formula_6_18.Form6Dot18DesignPlasticShearResistance(a_v=a_v, f_y=f_y, gamma_m0=self.gamma_m0)

    def shear_strength_unity_check(self) -> Formula:
        """Calculate the unity check for shear strength of the steel cross-section (EN 1993-1-1:2005 art. 6.2.6(2) - Formula (6.17)).

        Returns
        -------
        Formula
            The calculated unity check for shear strength.
        """
        v_ed = abs(self.v * KN_TO_N)
        v_pl_rd = self.plastic_resistance()
        return formula_6_17.Form6Dot17CheckShearForce(v_ed=v_ed, v_c_rd=v_pl_rd)

    def result(self) -> CheckResult:
        """Calculate result of plastic shear force resistance.

        Returns
        -------
        CheckResult
            True if the shear force check passes, False otherwise.
        """
        provided = abs(self.v) * KN_TO_N
        required = self.plastic_resistance()
        return CheckResult.from_comparison(provided=provided, required=required)

    def report(self, n: int = 2) -> Report:
        """Returns the report for the plastic shear force check.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the plastic shear force check.
        """
        report = Report("Check: shear force steel I-beam")

        # will not generate a report if no shear force is applied, as the check is not necessary in that case
        if self.v == 0:
            report.add_paragraph("No shear force was applied; therefore, no shear force check is necessary.")
            return report

        # generate report if shear force is applied
        axis_label = "(vertical) z" if self.axis == "Vz" else "(horizontal) y"
        report.add_paragraph(
            f"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            f"is loaded with a shear force of {abs(self.v):.{n}f} kN in the {axis_label}-direction."
        )
        report.add_newline(n=2)

        # shear area
        report.add_paragraph("The shear area is calculated as follows:")
        report.add_formula(self.shear_area(), n=n, split_after=[(2, "="), (7, "+"), (3, "=")])
        report.add_newline(n=2)

        # resistance
        report.add_paragraph("The shear resistance is calculated as follows:")
        report.add_formula(self.plastic_resistance(), n=n)
        report.add_newline(n=2)

        # unity check
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(self.shear_strength_unity_check(), n=n)
        report.add_newline(n=2)

        # add overall result based on the unity check
        if self.result().is_ok:
            report.add_paragraph("The check for plastic shear force satisfies the requirements.")
        else:
            report.add_paragraph("The check for plastic shear force does NOT satisfy the requirements.")
        return report


@dataclass(frozen=True)
class CheckStrengthShearClass34:
    """Class to perform plastic shear force resistance check for steel cross-section class 3 and 4 (Eurocode 3).

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
    v : KN
        The applied shear force (in kN).
    axis : Literal["Vz", "Vy"]
        Axis along which the shear force is applied. "Vz" (default) for z (vertical), "Vy" for y (horizontal).
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    section_properties : SectionProperties | None, optional
        Pre-calculated section properties. If None, they will be calculated internally.

    Example
    -------
    from blueprints.checks.eurocode.steel.strength_shear import CheckStrengthShearClass34
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    v = 100  # Applied shear force in kN

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthShearClass34(heb_300_s355, v, axis="Vz", gamma_m0=1.0)
    calc.report().to_word("shear_strength.docx", language="nl")

    """

    steel_cross_section: SteelCrossSection
    v: KN = 0
    axis: Literal["Vz", "Vy"] = "Vz"
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Elastic shear strength check"

    @staticmethod
    def source_docs() -> list[str]:
        """List of source document identifiers used for this check.

        Returns
        -------
        list[str]
        """
        return [EN_1993_1_1_2005]

    def shear_stress(self) -> float:
        """Calculate the maximum shear stress in the steel cross-section using elastic theory.

        Returns
        -------
        float
            The maximum shear stress in N/mm².
        """
        unit_stress = self.steel_cross_section.profile.unit_stress
        unit_sig_zxy = unit_stress["sig_zxy_vy"] if self.axis == "Vz" else unit_stress["sig_zxy_vx"]
        return float(np.max(np.abs(unit_sig_zxy))) * abs(self.v)

    def elastic_resistance(self) -> float:
        """Calculate the shear force elastic resistance of the steel cross-section (EN 1993-1-1:2005 art. 6.2.6).

        Returns
        -------
        float
            The calculated shear force resistance in N.
        """
        sig_zxy = self.shear_stress()
        return float(self.steel_cross_section.yield_strength / np.sqrt(3) / self.gamma_m0 / sig_zxy * abs(self.v) * KN_TO_N)

    def shear_strength_unity_check(self) -> Formula:
        """Calculate the unity check for shear strength of the steel cross-section (EN 1993-1-1:2005 art. 6.2.6 - Formula (6.19)).

        Returns
        -------
        Formula
            The calculated unity check for shear strength.
        """
        tau_ed = self.shear_stress()
        return formula_6_19.Form6Dot19CheckDesignElasticShearResistance(
            tau_ed=tau_ed, f_y=self.steel_cross_section.yield_strength, gamma_m0=self.gamma_m0
        )

    def result(self) -> CheckResult:
        """Calculate result of elastic shear force resistance.

        Returns
        -------
        CheckResult
            True if the shear force check passes, False otherwise.
        """
        provided = abs(self.v) * KN_TO_N
        required = self.elastic_resistance()
        return CheckResult.from_comparison(provided=provided, required=required)

    def report(self, n: int = 2) -> Report:
        """Returns the report for the elastic shear force check.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the elastic shear force check.
        """
        report = Report("Check: shear force steel I-beam (Class 3/4)")

        # will not generate a report if no shear force is applied, as the check is not necessary in that case
        if self.v == 0:
            report.add_paragraph("No shear force was applied; therefore, no shear force check is necessary.")
            return report

        # generate report if shear force is applied
        axis_label = "(vertical) z" if self.axis == "Vz" else "(horizontal) y"
        report.add_paragraph(
            f"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            f"is loaded with a shear force of {abs(self.v):.{n}f} kN in the {axis_label}-direction. "
            f"The shear stress is calculated using elastic theory."
        )
        report.add_newline(n=2)

        # shear stress calculation
        tau_ed = self.shear_stress()
        report.add_paragraph(f"The maximum shear stress is: {tau_ed:.{n}f} N/mm².")
        report.add_newline(n=2)

        # maximum allowed stress
        tau_max = round(self.steel_cross_section.yield_strength / (np.sqrt(3) * self.gamma_m0), n)
        report.add_paragraph("The maximum allowed shear stress is calculated as follows:")
        report.add_paragraph(f"$f_y / (\\sqrt{{3}} \\cdot \\gamma_{{M0}})$ = {tau_max} N/mm².")
        report.add_newline(n=2)

        # unity check
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(self.shear_strength_unity_check(), n=n)
        report.add_newline(n=2)

        # add overall result based on the unity check
        if self.result().is_ok:
            report.add_paragraph("The check for elastic shear force satisfies the requirements.")
        else:
            report.add_paragraph("The check for elastic shear force does NOT satisfy the requirements.")
        return report
