"""Module for checking bending moment resistance of steel cross-sections."""

from dataclasses import dataclass
from typing import ClassVar, Literal

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import (
    formula_6_12,
    formula_6_13,
    formula_6_14,
)
from blueprints.codes.formula import Formula
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KNM
from blueprints.unit_conversion import KNM_TO_NMM
from blueprints.utils.report import Report


@dataclass(frozen=True)
class CheckStrengthBendingClass12:
    """Class to perform bending moment resistance check for steel cross-sections,
    for cross-section class 1 and 2 only, based on 1993-1-1:2005 chapter 6.2.5.

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
    m : KNM, optional
        The applied bending moment (positive value), in kNm (default is 0 kNm).
    axis : str, optional
        Axis of bending: 'My' (bending around y) or 'Mz' (bending around z). Default is 'My'.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    from blueprints.checks.eurocode.steel.strength_bending import CheckStrengthBendingClass12
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(0)
    m = 355 * 1.868  # Applied bending moment in kNm

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthBendingClass12(heb_300_s355, m, axis='My', gamma_m0=1.0)
    calc.report().to_word("bending_moment_strength.docx", language="fy")
    """

    steel_cross_section: SteelCrossSection
    m: KNM = 0
    axis: Literal["My", "Mz"] = "My"
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Bending moment strength check for steel profiles (Class 1 and 2 only)"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties."""
        if self.axis not in ("My", "Mz"):
            raise ValueError("Axis must be 'My' or 'Mz'.")

    def calculation_formula(self) -> dict[str, Formula]:
        """Calculate bending moment resistance check (Class 1 and 2 only).

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number.
        """
        f_y = self.steel_cross_section.yield_strength
        # For bending about y, the relevant section modulus is sxx; for bending about z, it is syy.
        # This is because of the orientation of the axes defined in Blueprints vs. SectionProperties.
        props = self.steel_cross_section.profile.section_properties()
        w = float(props.sxx or 0) if self.axis == "My" else float(props.syy or 0)

        m_ed = abs(self.m) * KNM_TO_NMM  # convert kNm to Nmm
        m_c_rd = formula_6_13.Form6Dot13MCRdClass1And2(w_pl=w, f_y=f_y, gamma_m0=self.gamma_m0)
        check_moment = formula_6_12.Form6Dot12CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd)

        return {
            "resistance": m_c_rd,
            "check": check_moment,
        }

    def result(self) -> CheckResult:
        """Calculate result of bending moment resistance (Class 1 and 2).

        Returns
        -------
        CheckResult
            True if the bending moment check passes, False otherwise.
        """
        steps = self.calculation_formula()
        provided = abs(self.m) * KNM_TO_NMM
        required = steps["resistance"]
        return CheckResult.from_comparison(provided=provided, required=float(required))

    def report(self, n: int = 2) -> Report:
        """Returns the report for the bending moment check (Class 1 and 2).

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the bending moment check.
        """
        report = Report(f"Check: bending moment steel beam (axis {self.axis})")
        if self.m == 0:
            report.add_paragraph("No bending moment was applied; therefore, no bending moment check is necessary.")
            return report

        calculation = self.calculation_formula()
        # Compute result from existing calculation to avoid recalculating formulas
        provided = abs(self.m) * KNM_TO_NMM
        required = calculation["resistance"]
        result = CheckResult.from_comparison(provided=provided, required=float(required))

        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with a bending moment of {abs(self.m):.{n}f} kNm (axis {self.axis}). "
            rf"The resistance is calculated as follows, using cross-section class 1 or 2:"
        )
        report.add_formula(calculation["resistance"], n=n)
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(calculation["check"], n=n)
        if result.is_ok:
            report.add_paragraph("The check for bending moment satisfies the requirements.")
        else:
            report.add_paragraph("The check for bending moment does NOT satisfy the requirements.")
        return report


@dataclass(frozen=True)
class CheckStrengthBendingClass3:
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
    m : KNM, optional
        The applied bending moment (positive value), in kNm (default is 0 kNm).
    axis : str, optional
        Axis of bending: 'My' (bending around y) or 'Mz' (bending around z). Default is 'My'.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    from blueprints.checks.eurocode.steel.strength_bending import CheckStrengthBendingClass3
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(0)
    m = 355 * 1.677  # Applied bending moment in kNm

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthBendingClass3(heb_300_s355, m, axis='My', gamma_m0=1.0)
    calc.report().to_word("bending_moment_strength.docx", language="de")
    """

    steel_cross_section: SteelCrossSection
    m: KNM = 0
    axis: Literal["My", "Mz"] = "My"
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Bending moment strength check for steel profiles (Class 3 only)"
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties."""
        if self.axis not in ("My", "Mz"):
            raise ValueError("Axis must be 'My' or 'Mz'.")

    def calculation_formula(self) -> dict[str, Formula]:
        """Calculate bending moment resistance check (Class 3 only).

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number.
        """
        f_y = self.steel_cross_section.yield_strength
        # For bending about y, the relevant section modulus is sxx; for bending about z, it is syy.
        # This is because of the orientation of the axes defined in Blueprints vs. SectionProperties.
        props = self.steel_cross_section.profile.section_properties()
        w = min(float(props.zxx_plus), float(props.zxx_minus)) if self.axis == "My" else min(float(props.zyy_plus), float(props.zyy_minus))  # type: ignore[attr-defined]

        m_ed = abs(self.m) * KNM_TO_NMM  # convert kNm to Nmm
        m_c_rd = formula_6_14.Form6Dot14MCRdClass3(w_el_min=w, f_y=f_y, gamma_m0=self.gamma_m0)
        check_moment = formula_6_12.Form6Dot12CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd)

        return {
            "resistance": m_c_rd,
            "check": check_moment,
        }

    def result(self) -> CheckResult:
        """Calculate result of bending moment resistance (Class 3).

        Returns
        -------
        CheckResult
            True if the bending moment check passes, False otherwise.
        """
        steps = self.calculation_formula()
        provided = abs(self.m) * KNM_TO_NMM
        required = steps["resistance"]
        return CheckResult.from_comparison(provided=provided, required=float(required))

    def report(self, n: int = 2) -> Report:
        """Returns the report for the bending moment check (Class 3).

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the bending moment check.
        """
        report = Report(f"Check: bending moment steel beam (axis {self.axis})")
        if self.m == 0:
            report.add_paragraph("No bending moment was applied; therefore, no bending moment check is necessary.")
            return report

        calculation = self.calculation_formula()
        # Compute result from existing calculation to avoid recalculating formulas
        provided = abs(self.m) * KNM_TO_NMM
        required = calculation["resistance"]
        result = CheckResult.from_comparison(provided=provided, required=float(required))

        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with a bending moment of {abs(self.m):.{n}f} kNm (axis {self.axis}). "
            rf"The resistance is calculated as follows, using cross-section class 3:"
        )
        report.add_formula(calculation["resistance"], n=n)
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(calculation["check"], n=n)
        if result.is_ok:
            report.add_paragraph("The check for bending moment satisfies the requirements.")
        else:
            report.add_paragraph("The check for bending moment does NOT satisfy the requirements.")
        return report
