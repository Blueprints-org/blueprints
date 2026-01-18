"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 3 cross-sections according to Eurocode 3.
"""

from dataclasses import dataclass, field
from typing import Any, ClassVar

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


@dataclass(frozen=True)
class SteelIProfileStrengthClass3(CheckProtocol):
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

    Example
    -------
    from blueprints.checks.eurocode.en_1993_1_1_2005.ultimate_limit_states.steel_i_profile_strength_class_3 import SteelIProfileStrengthClass3
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB
    from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300

    result_internal_force_1d = ResultInternalForce1D(
                result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=100
            )

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = SteelIProfileStrengthClass3(heb_300_s355, result_internal_force_1d, gamma_m0=1.0)
    calc.report().to_word("steel_i_profile_strength_class_3_report.docx")
    """

    steel_cross_section: SteelCrossSection
    result_internal_force_1d: ResultInternalForce1D
    gamma_m0: DIMENSIONLESS = 1.0
    profile: Any = field(init=False, repr=False)
    properties: Any = field(init=False, repr=False)
    material: Any = field(init=False, repr=False)

    name: str = "Check for steel I-profiles of Class 3"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization checks."""
        if not isinstance(self.steel_cross_section.profile, IProfile):
            raise TypeError("The provided profile is not an I-profile.")

        object.__setattr__(self, "profile", self.steel_cross_section.profile)
        properties = self.steel_cross_section.profile.section_properties()
        object.__setattr__(self, "properties", properties)
        object.__setattr__(self, "material", self.steel_cross_section.material)

    def calculation_steps(self) -> dict[str, CheckProtocol | Formula | None]:
        """Perform calculation steps for all strength checks."""
        return {
            "normal force": NormalForceClass123(self.steel_cross_section, self.result_internal_force_1d, self.gamma_m0),
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
            if isinstance(c, CheckProtocol):
                unity_checks.append(c.result().unity_check)
        if not unity_checks:
            return CheckResult.from_unity_check(999)
        return CheckResult.from_unity_check(max(unity_checks))

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
        """
        Returns the combined report of all strength checks.

        Parameters
        ----------
        n : int, optional
            Formula numbering for LaTeX output (default is 2).

        Returns
        -------
        Report
            Combined report of all strength checks.
        """
        # Create report
        report = Report("Steel I-Profile Strength Check (Class 3) Report")
        report.add_heading("Utilization summary")
        rows = []
        for check_name, check in self.calculation_steps().items():
            if isinstance(check, CheckProtocol):
                utilization = f"{check.result().unity_check:.{n}f}"
                status = "OK" if check.result().is_ok else "NOT OK"
            elif check is None:
                utilization = "Not implemented"
                status = "NOT OK"
            else:  # Formula or other
                utilization = "N/A"
                status = "N/A"
            rows.append(
                [
                    check_name.capitalize(),
                    utilization,
                    status,
                ]
            )
        report.add_table(
            headers=["Check", "Utilization", "Status"],
            rows=rows,
        )
        report.add_paragraph(f"Overall result: {'OK' if self.result().is_ok else 'NOT OK'}", bold=True)

        # Add applied documents
        report.add_heading("Applied code documents")
        report.add_paragraph("The following documents were applied in this check:")
        report.add_list(self.source_docs)

        # Add applied forces
        report.add_heading("Applied forces")
        report.add_paragraph("The following internal forces were applied in this check:")
        report.add_table(
            headers=["Type", "Value"],
            rows=[
                ["Normal force $N$", f"{self.result_internal_force_1d.n:.{n}f} kN"],
                ["Shear force $V_z$", f"{self.result_internal_force_1d.vz:.{n}f} kN"],
                ["Shear force $V_y$", f"{self.result_internal_force_1d.vy:.{n}f} kN"],
                ["Bending moment $M_y$", f"{self.result_internal_force_1d.my:.{n}f} kNm"],
                ["Bending moment $M_z$", f"{self.result_internal_force_1d.mz:.{n}f} kNm"],
                ["Torsion $T$", f"{self.result_internal_force_1d.mx:.{n}f} kNm"],
            ],
        )

        # Add material and profile properties
        report.add_heading("Applied material and profile")
        report.add_paragraph("The following material properties were used in this check:")
        report.add_table(
            headers=["Property", "Value"],
            rows=[
                ["Material", str(self.steel_cross_section.material.name)],
                ["Yield Strength $f_y$", f"{self.steel_cross_section.yield_strength:.{n}f} MPa"],
                ["Ultimate Strength $f_u$", f"{self.steel_cross_section.ultimate_strength:.{n}f} MPa"],
                ["Elastic Modulus $E$", f"{self.steel_cross_section.material.e_modulus:.{n}f} MPa"],
            ],
        )
        report.add_paragraph("The following section properties were used in this check:")
        report.add_table(
            headers=["Property", "Value"],
            rows=[
                ["Profile", str(self.steel_cross_section.profile.name)],
                ["Area $A$", f"{self.properties.area:.{n}f} $mm^2$"],
                ["Moment of Inertia $I_y$", f"{min(self.properties.zxx_plus, self.properties.zxx_minus):.{n}f} $mm^4$"],
                ["Moment of Inertia $I_z$", f"{min(self.properties.zyy_plus, self.properties.zyy_minus):.{n}f} $mm^4$"],
            ],
        )

        # Add calculation steps
        report.add_heading("Individual checks")
        self.report_calculation_steps(report, n=n)

        # Add conclusion
        report.add_heading("Conclusion")
        check_result = self.result()
        if check_result.is_ok:
            report.add_paragraph("The check for steel I-profile strength (Class 3) has been passed.")
            report.add_equation(r"Check \to OK", tag=None)
        else:
            report.add_paragraph("The check for steel I-profile strength (Class 3) has ").add_paragraph("NOT", bold=True).add_paragraph(
                " been passed."
            )
            report.add_equation(r"Check \to NOT \ OK", tag=None)

        return report
