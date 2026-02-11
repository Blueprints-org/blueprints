"""Module for checking tension force resistance of steel cross-sections."""

from dataclasses import dataclass

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import (
    formula_6_5,
    formula_6_6,
)
from blueprints.codes.formula import Formula
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.unit_conversion import KN_TO_N
from blueprints.utils.report import Report
from blueprints.validations import NegativeValueError


@dataclass(frozen=True)
class CheckStrengthTensionClass1234:
    """Tension force resistance check for steel cross-sections (class 1,2,3 and 4) based on EN 1993-1-1:2005 art. 6.2.3.

    Coordinate System:
    ```
        z (vertical)
            ↑
            |     x (longitudinal beam direction, into screen)
            |    ↗
            |   /
            |  /
            | /
            |/
      ←-----O
       y (horizontal/side)
    ```

    Parameters
    ----------
    steel_cross_section : SteelCrossSection
        The steel cross-section to check.
    n : KN, optional
        The applied tensile force (positive value), default is 0 kN.
        Will raise an error if a negative value is provided, as this check is only for tension.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    ```python
    from blueprints.checks import CheckStrengthTensionClass1234
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel import SteelCrossSection
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(corrosion=1.5)
    n = 10000  # Applied tensile force in kN

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthTensionClass1234(steel_cross_section=heb_300_s355, n=n, gamma_m0=1.0)
    calc.report().to_word(path="tension_strength.docx")
    ```

    Raises
    ------
    NegativeValueError
        If the applied force is not tension (i.e., if n < 0).

    """

    steel_cross_section: SteelCrossSection
    n: KN = 0
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Tension strength check for steel profiles"

    def __post_init__(self) -> None:
        """Post-initialization to validate input parameters."""
        if self.n < 0:
            raise NegativeValueError(value_name="n (tensile force)", value=self.n)

    @staticmethod
    def source_docs() -> list[str]:
        """List of source document identifiers used for this check.

        Returns
        -------
        list[str]
        """
        return [EN_1993_1_1_2005]

    def plastic_resistance(self) -> Formula:
        """Calculate the tension force plastic resistance of the steel cross-section based on the gross
        cross-sectional area and yield strength (EN 1993-1-1:2005 art. 6.2.3(2a) - Formula (6.6)).

        Returns
        -------
        Formula
            The calculated tension force resistance.
        """
        a = self.steel_cross_section.profile.section_properties().area
        f_y = self.steel_cross_section.yield_strength
        return formula_6_6.Form6Dot6DesignPlasticResistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=self.gamma_m0)

    def tensile_strength_unity_check(self) -> Formula:
        """Calculate the unity check for tensile strength of the steel cross-section based on the applied tensile
        force and the calculated resistance (EN 1993-1-1:2005 art. 6.2.3(1) - Formula (6.5)).

        Returns
        -------
        Formula
            The calculated unity check for tensile strength.
        """
        n_ed = self.n * KN_TO_N
        n_t_rd = self.plastic_resistance()
        return formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

    def result(self) -> CheckResult:
        """Calculate result of tension force resistance.

        Returns
        -------
        CheckResult
            This is the result of the tension force resistance check, which compares the provided tensile force
            with the calculated resistance. The check is satisfied if the provided tensile force does not exceed
            the resistance.
        """
        return CheckResult.from_comparison(provided=self.n * KN_TO_N, required=self.plastic_resistance())

    def report(self, n: int = 2) -> Report:
        """Returns the report for the tension force check.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Full report on the tension force check, including the applied force, calculated resistance,
            unity check, and overall result.
        """
        report = Report("Tension check of steel cross-sections")

        # will not generate a report if no tensile force is applied, as the check is not necessary in that case
        if self.n == 0:
            report.add_paragraph("No tensile force was applied; therefore, no tensile force check is necessary.")
            return report

        # generate report if tensile force is applied
        report.add_paragraph(
            f"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            f"is loaded with a tensile force of {self.n:.{n}f} kN."
        )
        report.add_newline(n=2)

        # resistance
        report.add_paragraph("The resistance is calculated as follows:")
        report.add_formula(self.plastic_resistance(), n=n)
        report.add_newline(n=2)

        # unity check
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(self.tensile_strength_unity_check(), n=n)
        report.add_newline(n=2)

        # add overall result based on the unity check
        if self.result().is_ok:
            report.add_paragraph("The check for tensile force satisfies the requirements.")
        else:
            report.add_paragraph("The check for tensile force does NOT satisfy the requirements.")
        return report
