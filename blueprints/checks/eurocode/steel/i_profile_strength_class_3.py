"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 3 cross-sections.
"""

from dataclasses import dataclass, field
from typing import Any, ClassVar

from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_protocol import CheckProtocol
from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.steel import compression_strength, tension_strength
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN, KNM
from blueprints.utils import report_helpers
from blueprints.utils.report import Report


@dataclass(frozen=True)
class IProfileStrengthClass3:
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
    section_properties : SectionProperties | None, optional
        Pre-calculated section properties. If None, they will be calculated internally.
    ignore_checks : list[str] | None, optional
        List of check names to ignore during calculation. Options:
        "compression", "tension", "bending about z", "bending about y", "shear z", "shear y", "torsion",
        "bending and shear", "bending and axial", "bending, shear and axial"

    Example
    -------

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
    ignore_checks: list[str] | None = None

    profile: Any = field(init=False, repr=False)
    material: Any = field(init=False, repr=False)

    name: str = "Check for steel I-profiles of Class 3"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization checks and type enforcement for forces/moments."""
        if not isinstance(self.steel_cross_section.profile, IProfile):
            raise TypeError("The provided profile is not an I-profile.")

        # Ensure all force/moment attributes are numeric (float)
        for attr in ["n", "v_y", "v_z", "m_x", "m_y", "m_z"]:
            value = getattr(self, attr)
            try:
                value = float(value)
            except (TypeError, ValueError):
                value = 0.0
            object.__setattr__(self, attr, value)

        object.__setattr__(self, "profile", self.steel_cross_section.profile)
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties(warping=True)
            object.__setattr__(self, "section_properties", section_properties)

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

    def subchecks(self) -> dict[str, "CheckProtocol"]:
        """Perform calculation steps for all strength checks, optionally ignoring specified checks."""
        all_checks = {
            "compression": None,
            "tension": None,
            "bending about z": None,
            "bending about y": None,
            "shear z": None,
            "shear y": None,
            "torsion": None,
            "bending and shear": None,
            "bending and axial": None,
            "bending, shear and axial": None,
        }
        # Only perform compression check if n < 0, tension if n > 0
        if self.n < 0:
            all_checks["compression"] = compression_strength.CompressionStrengthClass123Check(
                self.steel_cross_section, self.n, self.gamma_m0, self.section_properties
            )
        elif self.n > 0:
            all_checks["tension"] = tension_strength.TensionStrengthCheck(self.steel_cross_section, self.n, self.gamma_m0, self.section_properties)

        if self.ignore_checks:
            return {k: v for k, v in all_checks.items() if k not in self.ignore_checks}
        return all_checks

    def result(self) -> CheckResult:
        """Perform all strength checks and return the overall result."""
        checks = list(self.subchecks().values())
        unity_checks = [c.result().unity_check for c in checks if c is not None]
        filtered_unity_checks = [0] + [uc for uc in unity_checks if isinstance(uc, int | float)]
        return CheckResult.from_unity_check(max(filtered_unity_checks))  # pragma: no cover

    def report(self, n: int = 2) -> Report:
        """Returns the combined report of all strength checks."""
        report = Report("Steel I-Profile Strength Check (Class 3) Report")

        report_helpers.add_unity_check_summary(report, self.subchecks(), n=n)

        report_helpers.add_applied_forces(report, self.result_internal_force_1d, n=n)

        report_helpers.add_material_steel_info(report, self.steel_cross_section, n=n)

        report_helpers.add_section_properties(
            report,
            self.section_properties,
            profile=self.steel_cross_section.profile,
            n=n,
            properties=["area", "a_sx", "a_sy", "zxx_plus", "zxx_minus", "zyy_plus", "zyy_minus", "j"],
        )

        report.add_heading("Calculation")
        for subcheck in self.subchecks().values():
            if subcheck is not None:
                sub_report = subcheck.report(n=n)
                report.add_heading(sub_report.title, level=2)
                report += sub_report

        report.add_heading("Conclusion")
        if self.result().is_ok:
            report.add_paragraph("The check for steel I-profile strength (Class 3) has been passed.").add_equation(
                r"Check \to OK"
            )  # pragma: no cover
        else:
            report.add_paragraph("The check for steel I-profile strength (Class 3) has NOT been passed.").add_equation(r"Check \to NOT \ OK")

        return report


if __name__ == "__main__":
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    n = 1  # Applied tensile force in kN
    v_z = 10
    v_y = 4
    m_x = 200
    m_y = 150
    m_z = 100

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = IProfileStrengthClass3(heb_300_s355, n=n, v_y=v_y, v_z=v_z, m_x=m_x, m_y=m_y, m_z=m_z, gamma_m0=1.0)
