"""Module for checking bending moment resistance combined with axial force, of steel cross-sections (Eurocode 3)."""

from dataclasses import dataclass
from typing import ClassVar, cast

import numpy as np
from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.steel.shear_strength import PlasticShearStrengthIProfileCheck
from blueprints.checks.eurocode.steel.torsion_with_shear_strength import TorsionWithShearStrengthIProfileCheck
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_29rho, formula_6_42, formula_6_45
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN, KNM
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM
from blueprints.utils.report import Report


@dataclass(frozen=True)
class BendingShearAxialStrengthClass3IProfileCheck:
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
    my : KNM, optional
        The applied bending moment around the y-axis (positive value, in kNm), default is 0 kNm.
    mz : KNM, optional
        The applied bending moment around the z-axis (positive value, in kNm), default is 0 kNm.
    n : KN, optional
        The applied axial force (positive value for tension, negative for compression), in kN (default is 0 kN).
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    section_properties : SectionProperties | None, optional
        Pre-calculated section properties. If None, they will be calculated internally.

    Example
    -------
    from blueprints.checks.eurocode.steel.bending_moment_strength import BendingShearAxialStrengthClass3IProfileCheck
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300
    n = 1000  # Applied axial force in kN
    v_y = 1111  # Applied shear force in y-direction in kN
    v_z = 50  # Applied shear force in z-direction in kN
    m_x = 10  # Applied torsional moment in kNm
    m_y = 100  # Applied bending moment around y-axis in kNm
    m_z = 80  # Applied bending moment around z-axis in kNm

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = BendingShearAxialStrengthClass3IProfileCheck(heb_300_s355, m_y=m_y, m_z=m_z, n=n, v_y=v_y, v_z=v_z, m_x=m_x, gamma_m0=1.0)
    calc.report().to_word("bending_shear_axial_strength.docx")
    """

    steel_cross_section: SteelCrossSection
    n: KN = 0
    v_y: KN = 0
    v_z: KN = 0
    m_x: KNM = 0
    m_y: KNM = 0
    m_z: KNM = 0
    gamma_m0: DIMENSIONLESS = 1.0
    section_properties: SectionProperties | None = None
    name: str = "Bending moment with shear and axial force strength check for steel profiles (Class 3 I-profiles only)"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties."""
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties()
            object.__setattr__(self, "section_properties", section_properties)

    def calculation_formula(self) -> dict[str, Formula | float]:
        """Calculate bending moment resistance check (Class 3 only, units: kNm).

        Returns
        -------
        dict[str, Formula | float]
            Calculation results keyed by formula number. Returns an empty dict if no moment is applied.
        """
        rif1d = ResultInternalForce1D(
            result_for=ResultFor.LOAD_CASE, load_case="N/A", result_on=ResultOn.ON_BEAM, member="N/A", n=self.n, my=self.m_y, mz=self.m_z
        )

        stress = self.steel_cross_section.profile.calculate_stress(rif1d)
        stress_values = stress.get_stress()[0]["sig_zz"]

        max_sig_zz = float(np.max(np.abs(stress_values)))

        v_y = self.v_y * KN_TO_N
        v_z = self.v_z * KN_TO_N
        m_x = self.m_x * KNM_TO_NMM

        if m_x == 0:  # calculate rho without torsion, see if shear in y or z direction governs
            shear_resistance_calculation_y = PlasticShearStrengthIProfileCheck(
                self.steel_cross_section, v=self.v_y, axis="Vy", gamma_m0=self.gamma_m0, section_properties=self.section_properties
            ).calculation_formula()
            rho_y = formula_6_29rho.Form6Dot29Rho(v_ed=v_y, v_pl_rd=shear_resistance_calculation_y["resistance"])

            shear_resistance_calculation_z = PlasticShearStrengthIProfileCheck(
                self.steel_cross_section, v=self.v_z, axis="Vz", gamma_m0=self.gamma_m0, section_properties=self.section_properties
            ).calculation_formula()
            rho_z = formula_6_29rho.Form6Dot29Rho(v_ed=v_z, v_pl_rd=shear_resistance_calculation_z["resistance"])
            rho = rho_y if rho_y > rho_z else rho_z
            shear_resistance_calculation = shear_resistance_calculation_y if rho_y > rho_z else shear_resistance_calculation_z

        else:  # calculate rho with torsion, see if shear in y or z direction governs
            shear_resistance_calculation_y = TorsionWithShearStrengthIProfileCheck(
                self.steel_cross_section, mx=self.m_x, v=self.v_y, axis="Vy", gamma_m0=self.gamma_m0, section_properties=self.section_properties
            ).calculation_formula()
            rho_y = formula_6_29rho.Form6Dot29RhoWithTorsion(v_ed=v_y, v_pl_t_rd=shear_resistance_calculation_y["resistance"])
            shear_resistance_calculation_z = TorsionWithShearStrengthIProfileCheck(
                self.steel_cross_section, mx=self.m_x, v=self.v_z, axis="Vz", gamma_m0=self.gamma_m0, section_properties=self.section_properties
            ).calculation_formula()
            rho_z = formula_6_29rho.Form6Dot29RhoWithTorsion(v_ed=v_z, v_pl_t_rd=shear_resistance_calculation_z["resistance"])
            rho = rho_y if rho_y > rho_z else rho_z
            shear_resistance_calculation = shear_resistance_calculation_y if rho_y > rho_z else shear_resistance_calculation_z

        f_y_reduced = formula_6_45.Form6Dot45ReducedYieldStrength(rho=rho, f_y=self.steel_cross_section.yield_strength)

        check_stress = formula_6_42.Form6Dot42LongitudinalStressClass3CrossSections(sigma_x_ed=max_sig_zz, f_y=f_y_reduced, gamma_m0=self.gamma_m0)

        return {
            "a_v": shear_resistance_calculation["shear_area"],
            "v_pl(_t)_rd": shear_resistance_calculation["resistance"],
            "rho": rho,
            "f_y_reduced": f_y_reduced,
            "stress": max_sig_zz,
            "resistance": f_y_reduced / self.gamma_m0,
            "check": check_stress,
        }

    def result(self) -> CheckResult:
        """Calculate result of bending moment resistance (Class 3).

        Returns
        -------
        CheckResult
            True if the bending moment check passes, False otherwise.
        """
        steps = self.calculation_formula()
        provided = steps["stress"]
        required = steps["resistance"]
        return CheckResult.from_comparison(provided=provided, required=float(required))

    def report(self, n: int = 2) -> Report:  # noqa: C901, PLR0912
        """Returns the report for the bending moment with axial force check (Class 3).

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the bending moment with shear and axial force check.
        """
        report = Report("Check: bending moment with shear and axial force for steel beam")
        if self.m_y == 0 and self.m_z == 0 and self.n == 0 and self.v_y == 0 and self.v_z == 0 and self.m_x == 0:
            report.add_paragraph("No bending moment, shear force, torsional moment, or axial force was applied; therefore, no check is necessary.")
            return report

        formulas = self.calculation_formula()

        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with:"
        )

        loads = []
        if abs(self.m_y) > 0:
            loads.append(rf"bending moment My = {abs(self.m_y):.{n}f} kNm")
        if abs(self.m_z) > 0:
            loads.append(rf"bending moment Mz = {abs(self.m_z):.{n}f} kNm")
        if abs(self.n) > 0:
            force_type = "tension" if self.n > 0 else "compression"
            loads.append(rf"axial force N = {abs(self.n):.{n}f} kN ({force_type})")
        if abs(self.v_y) > 0:
            loads.append(rf"shear force Vy = {abs(self.v_y):.{n}f} kN")
        if abs(self.v_z) > 0:
            loads.append(rf"shear force Vz = {abs(self.v_z):.{n}f} kN")
        if abs(self.m_x) > 0:
            loads.append(rf"torsional moment Mx = {abs(self.m_x):.{n}f} kNm")

        for i, load in enumerate(loads):
            if i == len(loads) - 1:
                report.add_paragraph(load + ".")
            else:
                report.add_paragraph(load + ",")

        report.add_paragraph("The resistance is calculated as follows, using cross-section class 3:").add_newline(2)

        if abs(self.v_y) > 0 or abs(self.v_z) > 0 or abs(self.m_x) > 0:
            report.add_paragraph("First, the shear area is determined:")
            report.add_formula(formulas["a_v"], n=n, split_after=[(2, "="), (7, "+"), (3, "=")])

            report.add_paragraph("The shear resistance is calculated as:")
            report.add_formula(formulas["v_pl(_t)_rd"], n=n)

            report.add_paragraph("The reduction factor for bending moment resistance is defined as:")
            report.add_formula(cast(Formula, formulas["rho"]), n=n, options="short")

            report.add_paragraph("This gives a reduced yield strength of:")
            report.add_formula(formulas["f_y_reduced"], n=n)

        report.add_paragraph("The maximum longitudinal stress from the combined loading is:")
        report.add_equation(rf"\sigma_{{x,Ed}} = {formulas['stress']:.{n}f} \ MPa")

        report.add_paragraph("The design resistance is:")
        report.add_equation(rf"f_y / \gamma_{{M0}} = {formulas['resistance']:.{n}f} \ MPa")

        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(cast(Formula, formulas["check"]), n=n)

        if self.result().is_ok:
            report.add_paragraph("The check for bending moment with shear and axial force satisfies the requirements.")
        else:
            report.add_paragraph("The check for bending moment with shear and axial force does NOT satisfy the requirements.")

        return report
