"""Module for checking bending moment resistance combined with the presence of shear and torsion, of steel cross-sections (Eurocode 3)."""

from dataclasses import dataclass
from typing import ClassVar, Literal

import numpy as np

from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.steel.strength_shear import CheckStrengthShearClass12
from blueprints.checks.eurocode.steel.strength_torsion_shear import CheckStrengthTorsionShearClass12
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import (
    formula_6_12,
    formula_6_13,
    formula_6_29,
    formula_6_29rho,
)
from blueprints.codes.formula import Formula
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN, KNM
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM
from blueprints.utils.report import Report


@dataclass(frozen=True)
class CheckStrengthBendingShearClass12:
    """Class to perform bending moment resistance check for steel cross-sections,
    for cross-section class 1 and 2 only (Eurocode 3).

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
        The applied bending moment, in kNm (default is 0 kNm).
    m_x : KNM, optional
        The applied torsional moment, in kNm (default is 0 kNm).
    v : KN, optional
        The applied shear force, in kN (default is 0 kN).
    axis_m : str, optional
        Axis of bending: 'My' (bending around y) or 'Mz' (bending around z). Default is 'My'.
        Note: 'My' should be used together with 'Vz' for shear force. 'Mz' with 'Vy' for shear force.
    axis_v : str, optional
        Axis along which the shear force is applied. "Vz" (default) for z (vertical), "Vy" for y (horizontal).
        Note: 'Vz' should be used together with 'My' for bending moment. 'Vy' with 'Mz' for bending moment.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    from blueprints.checks.eurocode.steel.strength_bending_shear import CheckStrengthBendingShearClass12
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300
    m = 600  # Applied bending moment in kNm
    m_x = 0  # Applied torsional moment in kNm
    v = 600  # Applied shear force in kN

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthBendingShearClass12(
        heb_300_s355, m, m_x, v, axis_m="My", axis_v="Vz", gamma_m0=1.0
    )
    calc.report().to_word("bending_moment_strength.docx")
    """

    steel_cross_section: SteelCrossSection
    m: KNM = 0
    m_x: KNM = 0
    v: KN = 0
    axis_m: Literal["My", "Mz"] = "My"
    axis_v: Literal["Vz", "Vy"] = "Vz"
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Bending moment strength check for steel profiles (Class 1 and 2 only)"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to validate axis parameters."""
        if self.axis_m not in ("My", "Mz"):
            raise ValueError("Axis must be 'My' or 'Mz'.")
        if self.axis_v not in ("Vz", "Vy"):
            raise ValueError("Axis must be 'Vz' or 'Vy'.")
        if (self.axis_m == "My" and self.axis_v != "Vz") or (self.axis_m == "Mz" and self.axis_v != "Vy"):
            raise ValueError("Axis for bending moment and shear force are not compatible. Use 'My' with 'Vz' and 'Mz' with 'Vy'.")

    def calculation_formula(self) -> dict[str, Formula]:
        """Calculate bending moment resistance check (Class 1 and 2 only, units: kNm).

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number. Returns an empty dict if no moment is applied.
        """
        v_ed = abs(self.v * KN_TO_N)
        m_x = abs(self.m_x * KNM_TO_NMM)
        m_ed = abs(self.m * KNM_TO_NMM)

        if m_x == 0:
            shear_calc = CheckStrengthShearClass12(self.steel_cross_section, v=self.v, axis=self.axis_v, gamma_m0=self.gamma_m0)
            shear_resistance_calculation = {
                "shear_area": shear_calc.shear_area(),
                "resistance": shear_calc.plastic_resistance(),
            }
            rho = formula_6_29rho.Form6Dot29Rho(v_ed=v_ed, v_pl_rd=shear_resistance_calculation["resistance"])
        else:
            torsion_shear_calc = CheckStrengthTorsionShearClass12(
                self.steel_cross_section, m_x=self.m_x, v=self.v, axis=self.axis_v, gamma_m0=self.gamma_m0
            )
            shear_resistance_calculation = {
                "shear_area": torsion_shear_calc.shear_area(),
                "resistance": torsion_shear_calc.combined_resistance(),
            }
            rho = formula_6_29rho.Form6Dot29RhoWithTorsion(v_ed=v_ed, v_pl_t_rd=shear_resistance_calculation["resistance"])

        f_y_reduced = formula_6_29.Form6Dot29ReducedYieldStrength(rho=rho, f_y=self.steel_cross_section.yield_strength)
        section_properties = self.steel_cross_section.profile.section_properties()
        sxx = section_properties.sxx
        syy = section_properties.syy
        if sxx is None or syy is None:
            raise ValueError("Section properties must be defined to access sxx and syy")  # pragma: no cover
        w = float(sxx) if self.axis_m == "My" else float(syy)

        m_c_rd = formula_6_13.Form6Dot13MCRdClass1And2(w_pl=w, f_y=f_y_reduced, gamma_m0=self.gamma_m0)
        check_moment = formula_6_12.Form6Dot12CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd)

        return {
            "a_v": Formula(name="a_v", value=shear_resistance_calculation["shear_area"])
            if not isinstance(shear_resistance_calculation["shear_area"], Formula)
            else shear_resistance_calculation["shear_area"],
            "v_pl(_t)_rd": shear_resistance_calculation["resistance"],
            "rho": rho,
            "f_y_reduced": f_y_reduced,
            "resistance": m_c_rd,
            "check": check_moment,
        }

    def result(self) -> CheckResult:
        """Calculate result of bending moment resistance (Class 1 and 2).

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
        """Returns the report for the bending moment check (Class 1 and 2).

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
            report.add_paragraph("No bending moment was applied; therefore, no check is necessary.")
            return report

        formulas = self.calculation_formula()

        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with a bending moment of {self.m:.{n}f} kNm (axis {self.axis_m}). "
        )

        if abs(self.v) > 0 or abs(self.m_x) > 0:
            report.add_paragraph(
                rf"Additionally a shear force of {self.v:.{n}f} kN (axis {self.axis_v})"
                + (rf" and a torsional moment of {self.m_x:.{n}f} kNm. " if abs(self.m_x) > 0 else ". ")
            )
        report.add_paragraph("The resistance is calculated as follows, using cross-section class 1 or 2:").add_newline(2)

        report.add_paragraph("First, the shear area is determined:")
        report.add_formula(formulas["a_v"], n=n, split_after=[(2, "="), (7, "+"), (3, "=")])

        report.add_paragraph("The shear resistance is calculated as:")
        report.add_formula(formulas["v_pl(_t)_rd"], n=n)

        report.add_paragraph("The reduction factor for bending moment resistance is defined as:")
        report.add_formula(formulas["rho"], n=n, options="short")

        report.add_paragraph("This gives a reduced yield strength of:")
        report.add_formula(formulas["f_y_reduced"], n=n)

        report.add_paragraph("The bending moment resistance with reduced yield strength is:")

        report.add_formula(formulas["resistance"], n=n)

        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(formulas["check"], n=n)

        if self.result().is_ok:
            report.add_paragraph("The check for bending moment satisfies the requirements.")
        else:
            report.add_paragraph("The check for bending moment does NOT satisfy the requirements.")

        return report


@dataclass(frozen=True)
class CheckStrengthBendingShearClass3:
    """Class to perform bending moment resistance check for steel cross-sections,
    for cross-section class 3 only (Eurocode 3).

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
        The applied bending moment, in kNm (default is 0 kNm).
    m_x : KNM, optional
        The applied torsional moment, in kNm (default is 0 kNm).
    v : KN, optional
        The applied shear force, in kN (default is 0 kN).
    axis_m : str, optional
        Axis of bending: 'My' (bending around y) or 'Mz' (bending around z). Default is 'My'.
        Note: 'My' should be used together with 'Vz' for shear force. 'Mz' with 'Vy' for shear force.
    axis_v : str, optional
        Axis along which the shear force is applied. "Vz" (default) for z (vertical), "Vy" for y (horizontal).
        Note: 'Vz' should be used together with 'My' for bending moment. 'Vy' with 'Mz' for bending moment.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    from blueprints.checks.eurocode.steel.strength_bending_shear import CheckStrengthBendingShearClass3
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300
    m = 600  # Applied bending moment in kNm
    m_x = 0  # Applied torsional moment in kNm
    v = 600  # Applied shear force in kN

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthBendingShearClass3(
        heb_300_s355, m, m_x, v, axis_m="My", axis_v="Vz", gamma_m0=1.0
    )
    calc.report().to_word("bending_moment_strength.docx")
    """

    steel_cross_section: SteelCrossSection
    m: KNM = 0
    m_x: KNM = 0
    v: KN = 0
    axis_m: Literal["My", "Mz"] = "My"
    axis_v: Literal["Vz", "Vy"] = "Vz"
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Bending moment strength check for steel profiles (Class 3 only)"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to validate axis parameters."""
        if self.axis_m not in ("My", "Mz"):
            raise ValueError("Axis must be 'My' or 'Mz'.")
        if self.axis_v not in ("Vz", "Vy"):
            raise ValueError("Axis must be 'Vz' or 'Vy'.")
        if (self.axis_m == "My" and self.axis_v != "Vz") or (self.axis_m == "Mz" and self.axis_v != "Vy"):
            raise ValueError("Axis for bending moment and shear force are not compatible. Use 'My' with 'Vz' and 'Mz' with 'Vy'.")

    def calculation_formula(self) -> dict[str, Formula]:
        """Calculation formula."""
        return {}

    def combined_von_mises_stress(self) -> float:
        """Calculate the combined von Mises stress due to bending, shear and torsion using elastic theory.

        Returns
        -------
        float
            The maximum combined von Mises stress in MPa.
        """
        if self.v == 0 and self.m_x == 0 and self.m == 0:
            return 0.0

        v_y = self.v if self.axis_v == "Vy" else 0.0
        v_z = self.v if self.axis_v == "Vz" else 0.0
        m_y = self.m if self.axis_m == "My" else 0.0
        m_z = self.m if self.axis_m == "Mz" else 0.0

        stress_post = self.steel_cross_section.profile.calculate_stress(
            n=0,
            v_y=v_y,
            v_z=v_z,
            m_x=self.m_x,
            m_y=m_y,
            m_z=m_z,
        )

        stress_data = stress_post.get_stress()[0]
        von_mises = stress_data["sig_vm"]
        # Return the maximum von Mises stress
        return float(np.max(np.abs(von_mises)))

    def elastic_resistance(self) -> float:
        """Calculate the elastic resistance for Class 3 (yield strength).

        Returns
        -------
        float
            The calculated elastic resistance in MPa.
        """
        return float(self.steel_cross_section.yield_strength / self.gamma_m0)

    def result(self) -> CheckResult:
        """Calculate result of bending moment resistance (Class 3).

        Returns
        -------
        CheckResult
            True if the bending moment check passes, False otherwise.
        """
        provided = self.combined_von_mises_stress()
        required = self.elastic_resistance()
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
        report = Report("Check: bending moment + shear steel beam")
        if self.m == 0:
            report.add_paragraph("No bending moment was applied; therefore, no check is necessary.")
            return report

        # introduction
        profile_name = self.steel_cross_section.profile.name
        steel_quality = self.steel_cross_section.material.steel_class.name
        report.add_paragraph(
            f"Profile {profile_name} with steel quality {steel_quality} "
            f"is loaded with a bending moment of {self.m:.{n}f} kNm (axis {self.axis_m}). "
        )

        if abs(self.v) > 0 or abs(self.m_x) > 0:
            report.add_paragraph(
                f"Additionally a shear force of {self.v:.{n}f} kN (axis {self.axis_v})"
                + (f" and a torsional moment of {self.m_x:.{n}f} kNm. " if abs(self.m_x) > 0 else ". ")
            )

        report.add_paragraph(
            "For class 3 sections, the combined von Mises stress from bending, shear and torsion is calculated using elastic theory."
        )
        report.add_newline(n=2)

        # combined von Mises stress
        vm_val = self.combined_von_mises_stress()
        report.add_paragraph(f"The maximum combined von Mises stress is: {vm_val:.{n}f} N/mm².")
        report.add_newline(n=2)

        # elastic resistance
        f_y_val = self.elastic_resistance()
        report.add_paragraph("The maximum allowed yield stress is calculated as follows: ")
        report.add_paragraph(rf"$f_y / \gamma_{{M0}}$ = {f_y_val:.{n}f} N/mm².")
        report.add_newline(n=2)

        # unity check
        result = self.result()
        report.add_paragraph("The unity check is calculated as follows: ")
        report.add_paragraph(rf"$UC = \sigma_{{vm}} / (f_y / \gamma_{{M0}})$ = {vm_val:.{n}f} / {f_y_val:.{n}f} N/mm² = {vm_val / f_y_val:.{n}f}.")
        report.add_newline(n=2)

        # add overall result
        if result.is_ok:
            report.add_paragraph("The check for bending moment satisfies the requirements.")
        else:
            report.add_paragraph("The check for bending moment does NOT satisfy the requirements.")

        return report
