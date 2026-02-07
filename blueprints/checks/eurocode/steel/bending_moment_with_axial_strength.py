"""Module for checking bending moment resistance combined with axial force, of steel cross-sections (Eurocode 3)."""

from dataclasses import dataclass
from typing import ClassVar, cast

import numpy as np
from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_42
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN, KNM
from blueprints.utils.report import Report


@dataclass(frozen=True)
class BendingMomentWithAxialStrengthClass3Check:
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
    from blueprints.checks.eurocode.steel.bending_moment_strength import BendingMomentWithAxialStrengthClass3Check
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300
    my = 100  # Applied bending moment around y-axis in kNm
    mz = 130.37  # Applied bending moment around z-axis in kNm
    n = 1000  # Applied axial force in kN


    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = BendingMomentWithAxialStrengthClass3Check(heb_300_s355, my=my, mz=mz, n=n, gamma_m0=1.0)
    calc.report().to_word("bending_moment_strength.docx")
    """

    steel_cross_section: SteelCrossSection
    my: KNM = 0
    mz: KNM = 0
    n: KN = 0
    gamma_m0: DIMENSIONLESS = 1.0
    section_properties: SectionProperties | None = None
    name: str = "Bending moment strength check for steel profiles (Class 3 only)"
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
            result_for=ResultFor.LOAD_CASE, load_case="N/A", result_on=ResultOn.ON_BEAM, member="N/A", n=self.n, my=self.my, mz=self.mz
        )

        stress = self.steel_cross_section.profile.calculate_stress(rif1d)
        stress_values = stress.get_stress()[0]["sig_zz"]

        max_sig_zz = float(np.max(np.abs(stress_values)))

        check_stress = formula_6_42.Form6Dot42LongitudinalStressClass3CrossSections(
            sigma_x_ed=max_sig_zz, f_y=self.steel_cross_section.yield_strength, gamma_m0=self.gamma_m0
        )

        return {
            "stress": max_sig_zz,
            "resistance": self.steel_cross_section.yield_strength / self.gamma_m0,
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

    def report(self, n: int = 2) -> Report:
        """Returns the report for the bending moment with axial force check (Class 3).

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the bending moment with axial force check.
        """
        report = Report("Check: bending moment with axial force for steel beam")
        if self.my == 0 and self.mz == 0 and self.n == 0:
            report.add_paragraph("No bending moment or axial force was applied; therefore, no check is necessary.")
            return report

        formulas = self.calculation_formula()

        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with:"
        )

        loads = []
        if abs(self.my) > 0:
            loads.append(rf"bending moment My = {abs(self.my):.{n}f} kNm")
        if abs(self.mz) > 0:
            loads.append(rf"bending moment Mz = {abs(self.mz):.{n}f} kNm")
        if abs(self.n) > 0:
            force_type = "tension" if self.n > 0 else "compression"
            loads.append(rf"axial force N = {abs(self.n):.{n}f} kN ({force_type})")

        for i, load in enumerate(loads):
            if i == len(loads) - 1:
                report.add_paragraph(load + ".")
            else:
                report.add_paragraph(load + ",")

        report.add_paragraph("The resistance is calculated as follows, using cross-section class 3:")

        report.add_paragraph("The maximum longitudinal stress from the combined loading is:")
        report.add_equation(rf"\sigma_{{x,Ed}} = {formulas['stress']:.{n}f} \ MPa")

        report.add_paragraph("The design resistance is:")
        report.add_equation(rf"f_y / \gamma_{{M0}} = {formulas['resistance']:.{n}f} \ MPa")

        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(cast(Formula, formulas["check"]), n=n)

        if self.result().is_ok:
            report.add_paragraph("The check for bending moment with axial force satisfies the requirements.")
        else:
            report.add_paragraph("The check for bending moment with axial force does NOT satisfy the requirements.")

        return report
