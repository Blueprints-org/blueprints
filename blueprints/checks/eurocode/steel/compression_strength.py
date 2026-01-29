"""Module for checking compression force resistance of steel cross-sections."""

from dataclasses import dataclass
from typing import ClassVar

from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import (
    formula_6_9,
    formula_6_10,
)
from blueprints.codes.formula import Formula
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.unit_conversion import KN_TO_N
from blueprints.utils.report import Report


@dataclass(frozen=True)
class CompressionStrengthClass123Check:
    """Class to perform compression force resistance check for steel cross-sections,
        for cross-section class 1, 2, and 3 (Eurocode 3).

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
    n : KN, optional
        The applied compressive force (negative value), default is 0 kN.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    section_properties : SectionProperties | None, optional
        Pre-calculated section properties. If None, they will be calculated internally.

    Example
    -------
    from blueprints.checks.eurocode.steel.compression_strength import CompressionForceCheck
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    n = -10000  # Applied compressive force in kN

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CompressionStrengthClass123Check(heb_300_s355, n, gamma_m0=1.0)
    calc.report().to_word("compression_strength.docx", language="nl")

    """

    steel_cross_section: SteelCrossSection
    n: KN = 0
    gamma_m0: DIMENSIONLESS = 1.0
    section_properties: SectionProperties | None = None
    name: str = "Compression strength check for steel profiles"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties."""
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties()
            object.__setattr__(self, "section_properties", section_properties)

    def calculation_formula(self) -> dict[str, Formula]:
        """Calculate compression force resistance check.

        Returns
        -------
        dict[str, Formula]
                Calculation results keyed by formula number. Returns an empty dict if no compression force is applied.
        """
        if self.n > 0:
            raise ValueError("Input force N (F_x) must be negative for compression check.")

        a = float(self.section_properties.area)  # type: ignore[attr-defined]
        f_y = self.steel_cross_section.yield_strength
        n_ed = -self.n * KN_TO_N
        n_c_rd = formula_6_10.Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
        check_compression = formula_6_9.Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd)
        return {
            "resistance": n_c_rd,
            "check": check_compression,
        }

    def result(self) -> CheckResult:
        """Calculate result of compression force resistance.

        Returns
        -------
        CheckResult
                True if the compression force check passes, False otherwise.
        """
        steps = self.calculation_formula()
        provided = -self.n * KN_TO_N
        required = steps["resistance"]
        return CheckResult.from_comparison(provided=provided, required=float(required))

    def report(self, n: int = 2) -> Report:
        """Returns the report for the compression force check.

        Parameters
        ----------
        n : int, optional
                Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
                Report of the compression force check.
        """
        report = Report("Check: compression force steel beam")
        if self.n == 0:
            report.add_paragraph("No compressive force was applied; therefore, no compression force check is necessary.")
            return report
        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with a compressive force of {abs(self.n):.{n}f} kN. "
            rf"The resistance is calculated as follows:"
        )
        report.add_formula(self.calculation_formula()["resistance"], n=n)
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(self.calculation_formula()["check"], n=n)
        if self.result().is_ok:
            report.add_paragraph("The check for compression force satisfies the requirements.")
        else:
            report.add_paragraph("The check for compression force does NOT satisfy the requirements.")
        return report
