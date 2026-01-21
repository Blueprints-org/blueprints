"""Steel cross-section strength check according to Eurocode 3.

This module provides strength checks for steel cross-sections of class 1, 2 and 3.
"""

from dataclasses import dataclass
from typing import Self

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import (
    formula_6_5,
    formula_6_6,
    formula_6_9,
    formula_6_10,
)
from blueprints.codes.formula import Formula
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.standard_profiles import HEB
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.unit_conversion import KN_TO_N
from blueprints.utils import Report, report_helpers


@dataclass(frozen=True, kw_only=True)
class NormalForceClass123:
    """Class to perform normal force resistance check.

    Performs strength checks on steel I-profiles according to EN 1993-1-1:2005, for class 1, 2 and 3 cross-sections.

    Parameters
    ----------
    steel_cross_section : SteelCrossSection
        The SteelCrossSection to check.
    normal_force : KN
        Normal force to apply to the profile in kN. Positive values indicate tension, negative values indicate compression.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    from blueprints.checks.eurocode.en_1993_1_1_2005.ultimate_limit_states.normal_force import NormalForceClass123
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    # Define steel cross-section
    heb_300_s355 = SteelCrossSection(
        profile=HEB.HEB300,
        material=SteelMaterial(steel_class=SteelStrengthClass.S355),
    )

    # Perform normal force check
    calc = NormalForceClass123(
        steel_cross_section=heb_300_s355,
        normal_force=100,
        gamma_m0=1.0,
    )

    # Generate report for the normal force check
    report = calc.report()
    report.to_word("normal_force_check_report.docx")

    """

    steel_cross_section: SteelCrossSection
    normal_force: KN
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Normal force check for steel profiles of Class 1, 2 and 3"

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties."""
        # object.__setattr__(self, "section_properties", self.steel_cross_section.profile.section_properties())

    @property
    def source_documents(self) -> list[str]:
        """Get list of source documents used for this calculation."""
        return [EN_1993_1_1_2005]

    def calculation_steps(self) -> dict[str, Self]:
        """Perform calculation steps for normal force resistance check.

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number. Returns an empty dict if no normal force is applied.
        """
        if self.normal_force == 0:
            return {}

        section_properties = self.steel_cross_section.profile.section_properties(geometric=True, plastic=False, warping=False)

        if self.normal_force > 0:  # tension, based on chapter 6.2.3
            a = 0.0 if section_properties.area is None else section_properties.area
            f_y = self.steel_cross_section.yield_strength
            n_ed = self.normal_force * KN_TO_N
            n_t_rd = formula_6_6.Form6Dot6DesignPlasticResistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
            check_tension = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)
            return {
                "en_1993_1_1_2005 f6.6": n_t_rd,
                "en_1993_1_1_2005 f6.5": check_tension,
            }

        # compression, based on chapter 6.2.4
        a = section_properties.area if section_properties.area is not None else 0
        f_y = self.steel_cross_section.yield_strength
        n_ed = -self.normal_force * KN_TO_N
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
        if self.normal_force == 0:
            return CheckResult.from_unity_check(0)
        if self.normal_force > 0:
            provided = self.normal_force * KN_TO_N
            required = steps["en_1993_1_1_2005 f6.6"]
            return CheckResult.from_comparison(provided=provided, required=float(required))
        # compression
        provided = -self.normal_force * KN_TO_N
        required = steps["en_1993_1_1_2005 f6.10"]
        return CheckResult.from_comparison(provided=provided, required=float(required))

    def report_calculation_steps(self, report: Report, n: int = 2) -> None:
        """Report calculation steps for all strength checks.

        Parameters
        ----------
        report : Report
            The report object to which the calculation steps will be added.
        n : int, optional
            Formula numbering for LaTeX output (default is 2).
        """
        if self.normal_force == 0:
            report.add_paragraph("Checking normal force not needed as no normal force applied.").add_newline()
        elif self.normal_force > 0:
            report.add_paragraph(r"Checking normal force (tension) using chapter 6.2.3.").add_newline()
        elif self.normal_force < 0:
            report.add_paragraph(r"Checking normal force (compression) using chapter 6.2.4.").add_newline()

        # add calculation steps to report
        if self.normal_force != 0:
            for step in self.calculation_steps().values():
                if isinstance(step, Formula):
                    report.add_formula(step, n=n)

    def report(self, n: int = 2) -> Report:
        """Returns the report for the normal force check.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the normal force check.
        """
        # Create report
        report = Report("Normal force - Check report")
        report.add_heading("Utilization summary")
        report.add_paragraph(f"The utilization for the normal force check is {self.result().unity_check:.{n}f}.").add_newline(n=2)
        report.add_paragraph(f"Overall result: {'OK' if self.result().is_ok else 'NOT OK'}", bold=True)

        # Applied documents
        report_helpers.add_applied_documents(report, self.source_documents)

        # Applied forces
        # report_helpers.add_applied_forces(report, self.normal_force, n=n)

        # Applied material and profile
        report_helpers.add_material_steel_info(report, self.steel_cross_section, n=n)
        report_helpers.add_section_properties(
            report,
            self.steel_cross_section.profile.section_properties(geometric=True, plastic=False, warping=False),
            profile=self.steel_cross_section.profile,
            n=n,
            properties=["area"],
        )

        # Calculation steps
        report.add_heading("Individual checks")
        self.report_calculation_steps(report, n=n)

        # Conclusion
        report.add_heading("Conclusion")
        if self.result().is_ok:
            report.add_paragraph("The check for normal force has been passed.").add_equation(r"Check \to OK")
        else:
            report.add_paragraph("The check for normal force has NOT been passed.").add_equation(r"Check \to NOT \ OK")

        return report


if __name__ == "__main__":
    calc = NormalForceClass123(
        steel_cross_section=SteelCrossSection(
            profile=HEB.HEB300,
            material=SteelMaterial(steel_class=SteelStrengthClass.S355),
        ),
        normal_force=100,
        gamma_m0=1.0,
    )
    print(calc.report().to_word("final.docx"))
