"""Module for checking plastic shear force resistance of steel(Eurocode 3)."""

from dataclasses import dataclass
from typing import ClassVar, Literal

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
class CheckStrengthShearClass12IProfile:
    """Class to perform plastic shear force resistance check for steel I-profiles of cross-section class 1 and 2 (Eurocode 3).

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
    from blueprints.checks.eurocode.steel.strength_shear import CheckStrengthShearClass12IProfile
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    v = 100  # Applied shear force in kN

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthShearClass12IProfile(heb_300_s355, v, axis="Vz", gamma_m0=1.0)
    calc.report().to_word("shear_strength.docx", language="nl")

    """

    steel_cross_section: SteelCrossSection
    v: KN = 0
    axis: Literal["Vz", "Vy"] = "Vz"
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Plastic shear strength check for steel I-profiles"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties and check profile type."""
        if not isinstance(self.steel_cross_section.profile, IProfile):
            raise TypeError("The provided profile is not an I-profile.")

    def calculation_formula(self) -> dict[str, Formula]:
        """Calculate plastic shear force resistance check.

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number. Returns an empty dict if no shear force is applied.
        """
        # Get parameters from profile, average top and bottom flange properties
        a = float(self.steel_cross_section.profile.area)  # type: ignore[attr-defined]
        b1 = self.steel_cross_section.profile.top_flange_width  # type: ignore[attr-defined]
        b2 = self.steel_cross_section.profile.bottom_flange_width  # type: ignore[attr-defined]
        tf1 = self.steel_cross_section.profile.top_flange_thickness  # type: ignore[attr-defined]
        tf2 = self.steel_cross_section.profile.bottom_flange_thickness  # type: ignore[attr-defined]
        tw = self.steel_cross_section.profile.web_thickness  # type: ignore[attr-defined]
        hw = self.steel_cross_section.profile.total_height - (  # type: ignore[attr-defined]
            self.steel_cross_section.profile.top_flange_thickness + self.steel_cross_section.profile.bottom_flange_thickness  # type: ignore[attr-defined]
        )
        r1 = self.steel_cross_section.profile.top_radius  # type: ignore[attr-defined]
        r2 = self.steel_cross_section.profile.bottom_radius  # type: ignore[attr-defined]

        if self.axis == "Vz" and self.steel_cross_section.fabrication_method in ["hot-rolled", "cold-formed"]:
            av = formula_6_18_sub_av.Form6Dot18SubARolledIandHSection(a=a, b1=b1, b2=b2, hw=hw, r1=r1, r2=r2, tf1=tf1, tf2=tf2, tw=tw, eta=1.0)
        elif self.axis == "Vz" and self.steel_cross_section.fabrication_method == "welded":
            av = formula_6_18_sub_av.Form6Dot18SubDWeldedIHandBoxSection(hw_list=[hw], tw_list=[tw], eta=1.0)
        else:  # axis == "Vy"
            av = formula_6_18_sub_av.Form6Dot18SubEWeldedIHandBoxSection(a=a, hw_list=[hw], tw_list=[tw])

        f_y = self.steel_cross_section.yield_strength
        v_ed = abs(self.v) * KN_TO_N
        v_pl_rd = formula_6_18.Form6Dot18DesignPlasticShearResistance(a_v=av, f_y=f_y, gamma_m0=self.gamma_m0)
        check_shear = formula_6_17.Form6Dot17CheckShearForce(v_ed=v_ed, v_c_rd=v_pl_rd)
        return {
            "shear_area": av,
            "resistance": v_pl_rd,
            "check": check_shear,
        }

    def result(self) -> CheckResult:
        """Calculate result of plastic shear force resistance.

        Returns
        -------
        CheckResult
            True if the shear force check passes, False otherwise.
        """
        steps = self.calculation_formula()
        provided = abs(self.v) * KN_TO_N
        required = steps["resistance"]
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
        if self.v == 0:
            report.add_paragraph("No shear force was applied; therefore, no shear force check is necessary.")
            return report
        axis_label = "(vertical) z" if self.axis == "Vz" else "(horizontal) y"
        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with a shear force of {abs(self.v):.{n}f} kN in the {axis_label}-direction. "
            rf"The shear area $A_v$ is calculated as follows:"
        )
        formulas = self.calculation_formula()
        report.add_formula(formulas["shear_area"], n=n, split_after=[(2, "="), (7, "+"), (3, "=")])
        report.add_paragraph("The shear resistance is calculated as follows:")
        report.add_formula(formulas["resistance"], n=n)
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(formulas["check"], n=n)
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
        The steel cross-section, of type I-profile, to check.
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
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def calculation_formula(self) -> dict[str, Formula | float | int]:
        """Calculate plastic shear force resistance check.

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number. Returns an empty dict if no shear force is applied.
        """
        unit_stress = self.steel_cross_section.profile.unit_stress
        unit_sig_zxy = unit_stress["sig_zxy_vy"] if self.axis == "Vz" else unit_stress["sig_zxy_vx"]
        sig_zxy = float(np.max(np.abs(unit_sig_zxy))) * self.v

        resistance = float(self.steel_cross_section.yield_strength / np.sqrt(3) / self.gamma_m0 / sig_zxy * self.v * KN_TO_N)

        check_shear = formula_6_19.Form6Dot19CheckDesignElasticShearResistance(
            tau_ed=sig_zxy, f_y=self.steel_cross_section.yield_strength, gamma_m0=self.gamma_m0
        )

        return {
            "shear_stress": sig_zxy,
            "resistance": resistance,
            "check": check_shear,
        }

    def result(self) -> CheckResult:
        """Calculate result of plastic shear force resistance.

        Returns
        -------
        CheckResult
            True if the shear force check passes, False otherwise.
        """
        steps = self.calculation_formula()
        provided = abs(self.v) * KN_TO_N
        required = steps["resistance"]
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
        if self.v == 0:
            report.add_paragraph("No shear force was applied; therefore, no shear force check is necessary.")
            return report
        axis_label = "(vertical) z" if self.axis == "Vz" else "(horizontal) y"
        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with a shear force of {abs(self.v):.{n}f} kN in the {axis_label}-direction. "
            rf"The shear stress $\tau_{{ed}}$ is calculated using elastic theory. "
        )
        formulas = self.calculation_formula()
        report.add_paragraph(f"The maximum shear stress is: {formulas['shear_stress']:.{n}f} N/mm². ")

        tau_max = round(self.steel_cross_section.yield_strength / (np.sqrt(3) * self.gamma_m0), n)
        report.add_paragraph("The maximum allowed shear stress is calculated as follows:")
        report.add_paragraph(rf"$f_y / (\sqrt{{3}} \cdot \gamma_{{M0}})$ = {tau_max} N/mm². ")

        report.add_paragraph("The unity check is calculated as follows:")
        check_formula = formulas["check"]
        assert isinstance(check_formula, Formula), "Expected Formula for check"
        report.add_formula(check_formula, n=n)
        if self.result().is_ok:
            report.add_paragraph("The check for elastic shear force satisfies the requirements.")
        else:
            report.add_paragraph("The check for elastic shear force does NOT satisfy the requirements.")
        return report
