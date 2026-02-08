"""Module for checking torsional shear stress resistance (Eurocode 2, formula 6.23)."""

from dataclasses import dataclass
from typing import ClassVar

import numpy as np
from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_23 import Form6Dot23CheckTorsionalMoment
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KNM
from blueprints.unit_conversion import KNM_TO_NMM
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
    source_docs: ClassVar[list] = [EN_1993_1_1_2005]

    def __post_init__(self) -> None:
        """Post-initialization to extract section properties."""
        if self.section_properties is None:
            section_properties = self.steel_cross_section.profile.section_properties()
            object.__setattr__(self, "section_properties", section_properties)

    def calculation_formula(self) -> dict[str, Formula | float]:
        """Calculate torsion resistance check.

        Returns
        -------
        dict[str, Formula | float]
            Calculation results keyed by formula number. Returns an empty dict if no torsion is applied.
        """
        rif1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="N/A",
            result_for=ResultFor.LOAD_CASE,
            load_case="N/A",
            mx=1,  # 1 kNm
        )

        unit_stress = self.steel_cross_section.profile.calculate_stress(rif1d)
        unit_sig_zxy = unit_stress.get_stress()[0]["sig_zxy"]
        unit_max_sig_zxy = float(np.max(np.abs(unit_sig_zxy)))

        t_rd = self.steel_cross_section.yield_strength / self.gamma_m0 / np.sqrt(3) / unit_max_sig_zxy
        t_ed = abs(self.m_x)

        check_torsion = Form6Dot23CheckTorsionalMoment(t_ed=t_ed, t_rd=t_rd)

        return {
            "unit_shear_stress": unit_max_sig_zxy,
            "resistance": t_rd,
            "check": check_torsion,
        }

    def result(self) -> CheckResult:
        """Calculate result of torsion resistance.

        Returns
        -------
        CheckResult
            True if the torsion check passes, False otherwise.
        """
        steps = self.calculation_formula()
        provided = abs(self.m_x) * KNM_TO_NMM
        required = steps["resistance"] * KNM_TO_NMM
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
        if self.m_x == 0:
            report.add_paragraph("No torsion was applied; therefore, no torsion check is necessary.")
            return report

        # Cache calculation formulas to avoid redundant recalculations
        formulas = self.calculation_formula()

        # Get information for the introduction of the report
        profile_name = self.steel_cross_section.profile.name
        steel_quality = self.steel_cross_section.material.steel_class.name
        m_x_val = f"{self.m_x:.{n}f}"
        unit_stress_val = f"{formulas['unit_shear_stress']:.{n}f}"

        report.add_paragraph(
            rf"Profile {profile_name} with steel quality {steel_quality} "
            rf"is loaded with a torsion of {m_x_val} kNm. "
            rf"First, the unit torsional stress (at 1 kNm) is defined as {unit_stress_val} MPa. "
            rf"The torsional resistance is calculated as follows:"
        )

        # Get values for the formula of torsion resistance
        fy = self.steel_cross_section.yield_strength
        gamma_m0 = self.gamma_m0
        unit_stress = formulas["unit_shear_stress"]
        result = formulas["resistance"]

        eqn_1 = (
            rf"T_{{Rd}} = \frac{{f_y}}{{\gamma_{{M0}} \cdot \sqrt{{3}} \cdot \text{{unit-stress}}}} = "
            rf"\frac{{{fy:.{n}f}}}{{{gamma_m0:.{n}f} \cdot \sqrt{{3}} \cdot {unit_stress:.{n}f}}} = {result:.{n}f} \ kNm"
        )
        report.add_equation(eqn_1)
        report.add_paragraph("The unity check is calculated as follows:")
        check_formula = formulas["check"]
        assert isinstance(check_formula, Formula), "Expected Formula for check"
        report.add_formula(check_formula, n=n)
        if self.result().is_ok:
            report.add_paragraph("The check for torsion satisfies the requirements.")
        else:
            report.add_paragraph("The check for torsion does NOT satisfy the requirements.")
        return report
