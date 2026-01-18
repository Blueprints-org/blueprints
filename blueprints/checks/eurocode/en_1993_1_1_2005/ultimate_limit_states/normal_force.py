"""Steel cross-section strength check according to Eurocode 3.

This module provides strength checks for steel cross-sections of class 1, 2 and 3 according to Eurocode 3.
"""

from dataclasses import dataclass
from typing import ClassVar

from blueprints.checks.check_protocol import CheckProtocol
from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import (
    formula_6_5,
    formula_6_6,
    formula_6_9,
    formula_6_10,
)
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultInternalForce1D
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS
from blueprints.unit_conversion import KN_TO_N
from blueprints.utils.report import Report


@dataclass(frozen=True)
class NormalForceClass123(CheckProtocol):
    """Class to perform normal force resistance check.

    Performs strength checks on steel I-profiles according to Eurocode 3, for class 1, 2 and 3 cross-sections.

    Parameters
    ----------
    steel_cross_section : SteelCrossSection
        The SteelCrossSection to check.
    result_internal_force_1d : ResultInternalForce1D
        The load combination to apply to the profile.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    from blueprints.checks.eurocode.en_1993_1_1_2005.ultimate_limit_states.normal_force import NormalForceClass123
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB
    from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300

    result_internal_force_1d = ResultInternalForce1D(
                result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=100
            )

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = NormalForceClass123(heb_300_s355, result_internal_force_1d, gamma_m0=1.0)
    calc.report().to_word("normal_force_check_report.docx")

    """

    steel_cross_section: SteelCrossSection
    result_internal_force_1d: ResultInternalForce1D
    gamma_m0: DIMENSIONLESS = 1.0

    name: str = "Normal force check for steel profiles of Class 1, 2 and 3"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties."""
        object.__setattr__(self, "profile", self.steel_cross_section.profile)
        properties = self.steel_cross_section.profile.section_properties()
        object.__setattr__(self, "properties", properties)
        object.__setattr__(self, "material", self.steel_cross_section.material)

    def calculation_steps(self) -> dict[str, Formula]:
        """Perform calculation steps for normal force resistance check.

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number. Returns an empty dict if no normal force is applied.
        """
        if self.result_internal_force_1d.n == 0:
            return {}
        if self.result_internal_force_1d.n > 0:  # tension, based on chapter 6.2.3
            a = self.properties.area if self.properties.area is not None else 0
            f_y = self.steel_cross_section.yield_strength
            n_ed = self.result_internal_force_1d.n * KN_TO_N
            n_t_rd = formula_6_6.Form6Dot6DesignPlasticResistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
            check_tension = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)
            return {
                "en_1993_1_1_2005 f6.6": n_t_rd,
                "en_1993_1_1_2005 f6.5": check_tension,
            }

        # compression, based on chapter 6.2.4
        a = self.properties.area if self.properties.area is not None else 0
        f_y = self.steel_cross_section.yield_strength
        n_ed = -self.result_internal_force_1d.n * KN_TO_N
        n_c_rd = formula_6_10.Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
        check_compression = formula_6_9.Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd)
        return {
            "en_1993_1_1_2005 f6.10": n_c_rd,
            "en_1993_1_1_2005 f6.9": check_compression,
        }

    def result(self) -> CheckResult:
        """Calculate result of normal force resistance.

        Returns
        -------
        CheckResult
            True if the normal force check passes, False otherwise.
        """
        steps = self.calculation_steps()
        if self.result_internal_force_1d.n == 0:
            return CheckResult.from_unity_check(0)
        if self.result_internal_force_1d.n > 0:
            provided = self.result_internal_force_1d.n * KN_TO_N
            required = steps["en_1993_1_1_2005 f6.6"]
            return CheckResult.from_comparison(provided=provided, required=required)
        # compression
        provided = -self.result_internal_force_1d.n * KN_TO_N
        required = steps["en_1993_1_1_2005 f6.10"]
        return CheckResult.from_comparison(provided=provided, required=required)

    def report(self) -> Report:
        """Returns the report for the normal force check.

        Returns
        -------
        Report
            Report of the normal force check.
        """
        report = Report("Normal force - Check report")
        report.add_heading("Applied code documents")
        report.add_paragraph("The following documents were applied in this check:")
        report.add_list(self.source_docs)

        report.add_heading("Applied forces")
        report.add_table(headers=["Type", "Value"], rows=[["Normal force", str(self.result_internal_force_1d.n) + " kN"]])

        report.add_heading("Applied profile and material")
        report.add_table(
            headers=["Profile", "Material"], rows=[[str(self.steel_cross_section.profile.name), str(self.steel_cross_section.material.name)]]
        )

        report.add_heading("Calculation steps")
        if self.result_internal_force_1d.n == 0:
            report.add_paragraph("Checking normal force not needed as no normal force applied.").add_newline()
        elif self.result_internal_force_1d.n > 0:
            report.add_paragraph(r"Checking normal force (tension) using chapter 6.2.3.").add_newline()
        elif self.result_internal_force_1d.n < 0:
            report.add_paragraph(r"Checking normal force (compression) using chapter 6.2.4.").add_newline()

        # add calculation steps to report
        if self.result_internal_force_1d.n != 0:
            for step in self.calculation_steps().values():
                report.add_formula(step)

        report.add_heading("Result")
        if self.result().is_ok:
            report.add_paragraph("The check for normal force has been passed.")
            report.add_equation(r"Check \to OK", tag=None)
        else:
            report.add_paragraph("The check for normal force has ").add_paragraph("NOT", bold=True).add_paragraph(" been passed.")
            report.add_equation(r"Check \to NOT \ OK", tag=None)

        return report
