"""Module for checking bending moment resistance combined with the presence of shear and torsion, of steel cross-sections (Eurocode 3)."""

from dataclasses import dataclass
from typing import ClassVar, Literal

from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.steel.shear_strength import PlasticShearStrengthIProfileCheck
from blueprints.checks.eurocode.steel.torsion_with_shear_strength import TorsionWithShearStrengthIProfileCheck
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import (
    formula_6_12,
    formula_6_14,
    formula_6_29,
    formula_6_29rho,
)
from blueprints.codes.formula import Formula
from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN, KNM
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM
from blueprints.utils.report import Report


@dataclass(frozen=True)
class BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck:
    """Class to perform bending moment resistance check for steel cross-sections,
    for cross-section class 3 I-profiles only (Eurocode 3).

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
    m : KNM, optional
        The applied bending moment (positive value), in kNm (default is 0 kNm).
    mx : KNM, optional
        The applied torsional moment (positive value), in kNm (default is 0 kNm).
    v : KN, optional
        The applied shear force (positive value), in kN (default is 0 kN).
    axis_m : str, optional
        Axis of bending: 'My' (bending around y) or 'Mz' (bending around z). Default is 'My'.
        Note: 'My' should be used together with 'Vz' for shear force. 'Mz' with 'Vy' for shear force.
    axis_v : str, optional
        Axis along which the shear force is applied. "Vz" (default) for z (vertical), "Vy" for y (horizontal).
        Note: 'Vz' should be used together with 'My' for bending moment. 'Vy' with 'Mz' for bending moment.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    section_properties : SectionProperties | None, optional
        Pre-calculated section properties. If None, they will be calculated internally.

    Example
    -------
    from blueprints.checks.eurocode.steel.bending_moment_strength import BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300
    m = 600  # Applied bending moment in kNm
    mx = 0  # Applied torsional moment in kNm
    v = 600  # Applied shear force in kN

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = BendingMomentWithShearAndTorsionStrengthClass3IProfileCheck(heb_300_s355, m, mx, v, axis_m="My", axis_v="Vz", gamma_m0=1.0)
    calc.report().to_word("bending_moment_strength.docx")
    """

    steel_cross_section: SteelCrossSection
    m: KNM = 0
    mx: KNM = 0
    v: KN = 0
    axis_m: Literal["My", "Mz"] = "My"
    axis_v: Literal["Vz", "Vy"] = "Vz"
    gamma_m0: DIMENSIONLESS = 1.0
    section_properties: SectionProperties | None = None
    name: str = "Bending moment strength check for steel I-profiles (Class 3 only)"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties and check profile type."""
        if not isinstance(self.steel_cross_section.profile, IProfile):
            raise TypeError("The provided profile is not an I-profile.")
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties()
            object.__setattr__(self, "section_properties", section_properties)
        if self.axis_m not in ("My", "Mz"):
            raise ValueError("Axis must be 'My' or 'Mz'.")
        if self.axis_v not in ("Vz", "Vy"):
            raise ValueError("Axis must be 'Vz' or 'Vy'.")
        if (self.axis_m == "My" and self.axis_v != "Vz") or (self.axis_m == "Mz" and self.axis_v != "Vy"):
            raise ValueError("Axis for bending moment and shear force are not compatible. Use 'My' with 'Vz' and 'Mz' with 'Vy'.")

    def calculation_formula(self) -> dict[str, Formula]:
        """Calculate bending moment resistance check (Class 3 only, units: kNm).

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number. Returns an empty dict if no moment is applied.
        """
        v_ed = abs(self.v * KN_TO_N)
        m_x = abs(self.mx * KNM_TO_NMM)
        m_ed = abs(self.m * KNM_TO_NMM)

        if m_x == 0:
            shear_resistance_calculation = PlasticShearStrengthIProfileCheck(
                self.steel_cross_section, v=self.v, axis=self.axis_v, gamma_m0=self.gamma_m0, section_properties=self.section_properties
            ).calculation_formula()
            rho = formula_6_29rho.Form6Dot29Rho(v_ed=v_ed, v_pl_rd=shear_resistance_calculation["resistance"])
        else:
            shear_resistance_calculation = TorsionWithShearStrengthIProfileCheck(
                self.steel_cross_section, mx=self.mx, v=self.v, axis=self.axis_v, gamma_m0=self.gamma_m0, section_properties=self.section_properties
            ).calculation_formula()
            rho = formula_6_29rho.Form6Dot29RhoWithTorsion(v_ed=v_ed, v_pl_t_rd=shear_resistance_calculation["resistance"])

        f_y_reduced = formula_6_29.Form6Dot29ReducedYieldStrength(rho=rho, f_y=self.steel_cross_section.yield_strength)
        w = float(self.section_properties.sxx) if self.axis_m == "My" else float(self.section_properties.syy)  # type: ignore[attr-defined]

        m_c_rd = formula_6_14.Form6Dot14MCRdClass3(w_el_min=w, f_y=f_y_reduced, gamma_m0=self.gamma_m0)
        check_moment = formula_6_12.Form6Dot12CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd)

        return {
            "a_v": shear_resistance_calculation["shear_area"],
            "v_pl(_t)_rd": shear_resistance_calculation["resistance"],
            "rho": rho,
            "f_y_reduced": f_y_reduced,
            "resistance": m_c_rd,
            "check": check_moment,
        }

    def result(self) -> CheckResult:
        """Calculate result of bending moment resistance (Class 3).

        Returns
        -------
        CheckResult
            True if the bending moment check passes, False otherwise.
        """
        steps = self.calculation_formula()
        provided = abs(self.m) * KNM_TO_NMM
        required = steps["resistance"]
        return CheckResult.from_comparison(provided=provided, required=float(required))

    def report(self, n: int = 2) -> Report:
        """Returns the report for the bending moment check (Class 3).

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the bending moment check.
        """
        report = Report(f"Check: bending moment steel beam (axis {self.axis_m})")
        if self.m == 0:
            report.add_paragraph("No bending moment was applied; therefore, no bending moment check is necessary.")
            return report

        formulas = self.calculation_formula()

        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with a bending moment of {abs(self.m):.{n}f} kNm (axis {self.axis_m}). "
        )

        if self.v > 0 or self.mx > 0:
            report.add_paragraph(
                rf"Additionally a shear force of {abs(self.v):.{n}f} kN (axis {self.axis_v})"
                + (rf" and a torsional moment of {abs(self.mx):.{n}f} kNm. " if self.mx > 0 else ". ")
            )
        report.add_paragraph("The resistance is calculated as follows, using cross-section class 3:").add_newline(2)

        if self.v > 0 or self.mx > 0:
            report.add_paragraph("First, the shear area is determined:")
            report.add_formula(formulas["a_v"], n=n, split_after=[(2, "="), (7, "+"), (3, "=")])

            report.add_paragraph("The shear resistance is calculated as:")
            report.add_formula(formulas["v_pl(_t)_rd"], n=n)

            report.add_paragraph("The reduction factor for bending moment resistance is defined as:")
            report.add_formula(formulas["rho"], n=n, options="short")

            report.add_paragraph("This gives a reduced yield strength of:")
            report.add_formula(formulas["f_y_reduced"], n=n)

            report.add_paragraph("The bending moment resistance with reduced yield strength is:")
        else:
            report.add_paragraph("The bending moment resistance is:")

        report.add_formula(formulas["resistance"], n=n)

        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(formulas["check"], n=n)

        if self.result().is_ok:
            report.add_paragraph("The check for bending moment satisfies the requirements.")
        else:
            report.add_paragraph("The check for bending moment does NOT satisfy the requirements.")

        return report
