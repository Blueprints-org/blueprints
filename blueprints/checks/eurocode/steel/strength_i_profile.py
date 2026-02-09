"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 3 cross-sections.
"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, cast

from blueprints.checks.check_protocol import CheckProtocol
from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.steel import strength_bending, strength_compression, strength_tension
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN, KNM
from blueprints.utils import report_helpers
from blueprints.utils.report import Report


@dataclass(frozen=True)
class CheckStrengthIProfileClass3:
    """Steel I-Profile strength check for class 3.

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

    Performs strength checks on steel I-profiles according to Eurocode 3, for class 3 cross-sections.

    Parameters
    ----------
    steel_cross_section : SteelCrossSection
        The steel cross-section, of type I-profile, to check.

    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    ignore_checks : list[str] | None, optional
        List of check names to ignore during calculation. Options:
        "compression", "tension", "bending about z", "bending about y", "shear z", "shear y", "torsion",
        "bending and shear", "bending and axial", "bending, shear and axial"

    Example
    -------
    from blueprints.checks.eurocode.steel.strength_i_profile import CheckStrengthIProfileClass3
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    n = -100  # Applied compressive force in kN
    v_y = 100  # Applied shear force in y-direction in kN
    v_z = 20    # Applied shear force in z-direction in kN
    m_x = 3    # Applied torsional moment in kNm
    m_y = 50   # Applied bending moment about y-axis in kNm
    m_z = 80   # Applied bending moment about z-axis in kNm

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthIProfileClass3(heb_300_s355, n, v_y, v_z, m_x, m_y, m_z, gamma_m0=1.0)
    calc.report().to_word("compression_strength.docx", language="nl")
    """

    steel_cross_section: SteelCrossSection
    n: KN = 0
    v_y: KN = 0
    v_z: KN = 0
    m_x: KNM = 0
    m_y: KNM = 0
    m_z: KNM = 0

    gamma_m0: DIMENSIONLESS = 1.0
    ignore_checks: list[str] | None = None

    material: Any = field(init=False, repr=False)
    result_internal_force_1d: ResultInternalForce1D = field(init=False, repr=False)

    name: str = "Check for steel I-profiles of Class 3"
    source_docs: ClassVar[list[Any]] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization checks and type enforcement for forces/moments."""
        if not isinstance(self.steel_cross_section.profile, IProfile):
            raise TypeError("The provided profile is not an I-profile.")

        object.__setattr__(
            self,
            "result_internal_force_1d",
            ResultInternalForce1D(
                result_on=ResultOn.ON_BEAM,
                member="N/A",
                result_for=ResultFor.LOAD_CASE,
                load_case="N/A",
                n=self.n,
                vy=self.v_y,
                vz=self.v_z,
                mx=self.m_x,
                my=self.m_y,
                mz=self.m_z,
            ),
        )

    def subchecks(self) -> dict[str, CheckProtocol | CheckResult | None]:
        """Perform calculation steps for all strength checks, optionally ignoring specified checks."""
        all_checks: dict[str, CheckProtocol | CheckResult | None] = {
            "compression": cast(
                CheckProtocol,
                strength_compression.CheckStrengthCompressionClass123(self.steel_cross_section, self.n, self.gamma_m0),
            ),
            "tension": cast(
                CheckProtocol,
                strength_tension.CheckStrengthTensionClass1234(self.steel_cross_section, self.n, self.gamma_m0),
            ),
            "bending about z": cast(
                CheckProtocol,
                strength_bending.CheckStrengthBendingClass3(self.steel_cross_section, self.m_z, axis="Mz", gamma_m0=self.gamma_m0),
            ),
            "bending about y": cast(
                CheckProtocol,
                strength_bending.CheckStrengthBendingClass3(self.steel_cross_section, self.m_y, axis="My", gamma_m0=self.gamma_m0),
            ),
            "shear z": None,
            "shear y": None,
            "torsion": None,
            "torsion and shear z": None,
            "torsion and shear y": None,
            "bending and shear": None,
            "bending and axial": None,
            "bending, shear and axial": None,
        }
        # Only perform compression check if n < 0, tension if n > 0
        if self.n > 0:
            all_checks["compression"] = CheckResult.from_unity_check(unity_check=0.0)
        elif self.n < 0:
            all_checks["tension"] = CheckResult.from_unity_check(unity_check=0.0)

        if self.ignore_checks:
            return {k: v for k, v in all_checks.items() if k not in self.ignore_checks}
        return all_checks

    def result(self) -> CheckResult:
        """Perform all strength checks and return the overall result."""
        checks = self.subchecks().values()
        unity_checks = [c.result().unity_check for c in checks if type(c) not in [CheckResult, type(None)]]  # type: ignore[union-attr]
        filtered_unity_checks: list[float] = [0.0] + [float(uc) for uc in unity_checks if isinstance(uc, int | float)]
        return CheckResult.from_unity_check(max(filtered_unity_checks))

    def report(self, n: int = 2) -> Report:
        """Returns the combined report of all strength checks."""
        report = Report("Steel I-Profile Strength Check (Class 3) Report")

        report_helpers.add_unity_check_summary(report, self.subchecks(), n=n)
        report.add_newline(2)
        report.add_paragraph("The following checks have not been implemented yet:")
        not_implemented_checks = [
            "Shear in z-direction",
            "Shear in y-direction",
            "Torsion",
            "Torsion with shear in z-direction",
            "Torsion with shear in y-direction",
            "Bending with shear",
            "Bending with axial",
            "Bending with shear and axial",
        ]
        report.add_list(not_implemented_checks)

        report_helpers.add_applied_forces(report, self.result_internal_force_1d, n=n)

        report_helpers.add_material_steel_info(report, self.steel_cross_section, n=n)

        report_helpers.add_section_properties(
            report,
            self.steel_cross_section.profile.section_properties(),
            profile=self.steel_cross_section.profile,
            n=n,
            properties=["area", "a_sx", "a_sy", "zxx_plus", "zxx_minus", "zyy_plus", "zyy_minus", "j"],
        )

        report.add_heading("Calculation")
        for subcheck in self.subchecks().values():
            if isinstance(subcheck, CheckProtocol):
                sub_report = subcheck.report(n=n)
                report.add_heading(str(sub_report.title), level=2)
                report += sub_report

        report.add_heading("Conclusion")
        if self.result().is_ok:
            report.add_paragraph("The check for steel I-profile strength (Class 3) has been passed.").add_equation(r"Check \to OK")
        else:
            report.add_paragraph("The check for steel I-profile strength (Class 3) has NOT been passed.").add_equation(r"Check \to NOT \ OK")

        return report
