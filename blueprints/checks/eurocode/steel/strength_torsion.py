"""Module for checking torsional shear stress resistance (Eurocode 2, formula 6.23)."""

from dataclasses import dataclass

import numpy as np
from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_23 import Form6Dot23CheckTorsionalMoment
from blueprints.codes.formula import Formula
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KNM
from blueprints.utils.report import Report


@dataclass(frozen=True)
class CheckStrengthStVenantTorsionClass1234:
    """Class to perform torsion resistance check using St. Venant torsion (Eurocode 3).

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
        The steel cross-section, of type I-profile, to check.
    m_x : KNM
        The applied torsional moment (in kNm).
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    section_properties : SectionProperties | None, optional
        Pre-calculated section properties. If None, they will be calculated internally.

    Example
    -------
    from blueprints.checks.eurocode.steel.torsion_strength import TorsionStrengthCheck
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    m_x = 10  # Applied torsional moment in kNm

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = TorsionStrengthCheck(heb_300_s355, m_x, gamma_m0=1.0)
    calc.report().to_word("torsion_strength.docx", language="nl")

    """

    steel_cross_section: SteelCrossSection
    m_x: KNM = 0
    gamma_m0: DIMENSIONLESS = 1.0
    section_properties: SectionProperties | None = None
    name: str = "Torsion strength check"

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties."""
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties()
            object.__setattr__(self, "section_properties", section_properties)

    @staticmethod
    def source_docs() -> list[str]:
        """List of source document identifiers used for this check.

        Returns
        -------
        list[str]
        """
        return [EN_1993_1_1_2005]

    def unit_torsional_shear_stress(self) -> float:
        """Calculate the unit torsional shear stress (at 1 kNm torsion).

        Returns
        -------
        float
            The unit torsional shear stress in MPa.
        """
        unit_stress = self.steel_cross_section.profile.unit_stress
        unit_sig_zxy = unit_stress["sig_zxy_mzz"]
        return float(np.max(np.abs(unit_sig_zxy)))

    def torsional_resistance(self) -> float:
        """Calculate the torsional resistance of the steel cross-section (EN 1993-1-1:2005 art. 6.2.7).

        Returns
        -------
        float
            The calculated torsional resistance in kNm.
        """
        unit_max_sig_zxy = self.unit_torsional_shear_stress()
        return float(self.steel_cross_section.yield_strength / self.gamma_m0 / np.sqrt(3) / unit_max_sig_zxy)

    def torsional_strength_unity_check(self) -> Formula:
        """Calculate the unity check for torsional strength of the steel cross-section (EN 1993-1-1:2005 art. 6.2.7 - Formula (6.23)).

        Returns
        -------
        Formula
            The calculated unity check for torsional strength.
        """
        t_ed = abs(self.m_x)
        t_rd = self.torsional_resistance()
        return Form6Dot23CheckTorsionalMoment(t_ed=t_ed, t_rd=t_rd)

    def result(self) -> CheckResult:
        """Calculate result of torsion resistance.

        Returns
        -------
        CheckResult
            True if the torsion check passes, False otherwise.
        """
        provided = abs(self.m_x)
        required = self.torsional_resistance()
        return CheckResult.from_comparison(provided=provided, required=float(required))

    def report(self, n: int = 2) -> Report:
        """Returns the report for the torsion check.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the torsion check.
        """
        report = Report("Check: torsion steel beam")

        # will not generate a report if no torsion is applied, as the check is not necessary in that case
        if self.m_x == 0:
            report.add_paragraph("No torsion was applied; therefore, no torsion check is necessary.")
            return report

        # generate report if torsion is applied
        report.add_paragraph(
            f"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            f"is loaded with a torsional moment of {abs(self.m_x):.{n}f} kNm."
        )
        report.add_newline(n=2)

        # unit torsional shear stress
        unit_stress_val = self.unit_torsional_shear_stress()
        report.add_paragraph(f"The unit torsional stress (at 1 kNm) is: {unit_stress_val:.{n}f} MPa.")
        report.add_newline(n=2)

        # torsional resistance
        report.add_paragraph("The torsional resistance is calculated as follows:")
        fy = self.steel_cross_section.yield_strength
        gamma_m0 = self.gamma_m0
        t_rd = self.torsional_resistance()
        eqn_1 = (
            rf"T_{{Rd}} = \frac{{f_y}}{{\gamma_{{M0}} \cdot \sqrt{{3}} \cdot \text{{unit-stress}}}} = "
            rf"\frac{{{fy:.{n}f}}}{{{gamma_m0:.{n}f} \cdot \sqrt{{3}} \cdot {unit_stress_val:.{n}f}}} = {t_rd:.{n}f} \ kNm"
        )
        report.add_equation(eqn_1)
        report.add_newline(n=2)

        # unity check
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(self.torsional_strength_unity_check(), n=n)
        report.add_newline(n=2)

        # add overall result based on the unity check
        if self.result().is_ok:
            report.add_paragraph("The check for torsion satisfies the requirements.")
        else:
            report.add_paragraph("The check for torsion does NOT satisfy the requirements.")
        return report
