"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 3 cross-sections.
"""

from dataclasses import dataclass, field
from typing import Any, ClassVar

from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_protocol import CheckProtocol
from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.en_1993_1_1_2005.ultimate_limit_states.normal_force import NormalForceClass123
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultInternalForce1D
from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS
from blueprints.utils.report import Report
from blueprints.utils.report_helpers import ReportHelpers


@dataclass(frozen=True)
class ProfileStrengthClass3(CheckProtocol):
    """Steel I-Profile strength check for class 3.

    Performs strength checks on steel I-profiles according to Eurocode 3, for class 3 cross-sections.

    Parameters
    ----------
    steel_cross_section : SteelCrossSection
        The steel cross-section, of type I-profile, to check.
    result_internal_force_1d : ResultInternalForce1D
        The load combination to apply to the profile.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    section_properties : SectionProperties | None, optional
        Pre-calculated section properties. If None, they will be calculated internally.

    Example
    -------
    from blueprints.checks.eurocode.en_1993_1_1_2005.ultimate_limit_states.steel_i_profile_strength_class_3 import ProfileStrengthClass3
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB
    from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300

    result_internal_force_1d = ResultInternalForce1D(
                result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1",
                n=100, vy=50, vz=30, mx=20, my=10, mz=5
            )

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = ProfileStrengthClass3(heb_300_s355, result_internal_force_1d, gamma_m0=1.0)
    calc.report().to_word("steel_i_profile_strength_class_3_report.docx")
    """

    steel_cross_section: SteelCrossSection
    result_internal_force_1d: ResultInternalForce1D
    gamma_m0: DIMENSIONLESS = 1.0
    section_properties: SectionProperties | None = None
    profile: Any = field(init=False, repr=False)
    material: Any = field(init=False, repr=False)

    name: str = "Check for steel I-profiles of Class 3"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization checks."""
        if not isinstance(self.steel_cross_section.profile, IProfile):
            raise TypeError("The provided profile is not an I-profile.")

        object.__setattr__(self, "profile", self.steel_cross_section.profile)
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties()
            object.__setattr__(self, "section_properties", section_properties)
        object.__setattr__(self, "material", self.steel_cross_section.material)

    def calculation_steps(self) -> dict[str, CheckProtocol | Formula | None]:
        """Perform calculation steps for all strength checks."""
        return {
            "normal force": NormalForceClass123(self.steel_cross_section, self.result_internal_force_1d, self.gamma_m0, self.section_properties),
            "bending moment z-axis": None,  # To be implemented
            "bending moment y-axis": None,  # To be implemented
            "shear force z-axis": None,  # To be implemented
            "shear force y-axis": None,  # To be implemented
            "torsion": None,  # To be implemented
            "bending and shear interaction": None,  # To be implemented
            "bending and axial interaction": None,  # To be implemented
            "bending, shear and axial interaction": None,  # To be implemented
        }

    def result(self) -> CheckResult:
        """Perform all strength checks and return the overall result."""
        checks = list(self.calculation_steps().values())
        # Only consider CheckProtocol objects for result aggregation
        unity_checks = []
        for c in checks:
            if c is None:
                return CheckResult.from_unity_check(999)
            unity_checks.append(c.result().unity_check)
        return CheckResult.from_unity_check(max(unity_checks))  # pragma: no cover  # can only be reached when all checks are added

    def report_calculation_steps(self, report: Report, n: int = 2, level: int = 2) -> None:
        """Report calculation steps for all strength checks.

        Parameters
        ----------
        report : Report
            The report object to which the calculation steps will be added.
        n : int, optional
            Formula numbering for LaTeX output (default is 2).
        level : int, optional
            Heading level for the report sections (default is 2).
        """
        for check_name, check in self.calculation_steps().items():
            report.add_heading(f"Checking: {check_name}", level=level)
            method = getattr(check, "report_calculation_steps", None)
            if callable(method):
                method(report, n=n)
            else:
                report.add_paragraph("This check does not support detailed calculation steps.")

    def report(self, n: int = 2) -> Report:
        """Returns the combined report of all strength checks."""
        report = Report("Steel I-Profile Strength Check (Class 3) Report")

        ReportHelpers.add_unity_check_summary(report, self.calculation_steps().items(), n=n)

        ReportHelpers.add_applied_documents(report, self.source_docs)

        ReportHelpers.add_applied_forces(report, self.result_internal_force_1d, n=n)

        ReportHelpers.add_material_steel_info(report, self.steel_cross_section, n=n)

        ReportHelpers.add_section_properties(
            report,
            self.section_properties,
            profile=self.steel_cross_section.profile,
            n=n,
            properties=["area", "a_sx", "a_sy", "zxx_plus", "zxx_minus", "zyy_plus", "zyy_minus", "J"],
        )

        report.add_heading("Individual checks")
        self.report_calculation_steps(report, n=n)

        report.add_heading("Conclusion")
        if self.result().is_ok:
            report.add_paragraph("The check for steel I-profile strength (Class 3) has been passed.").add_equation(
                r"Check \to OK"
            )  # pragma: no cover
        else:
            report.add_paragraph("The check for steel I-profile strength (Class 3) has NOT been passed.").add_equation(r"Check \to NOT \ OK")
        return report
