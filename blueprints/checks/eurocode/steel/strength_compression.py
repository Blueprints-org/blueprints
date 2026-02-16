"""Module for checking compression force resistance of steel cross-sections based on EN 1993-1-1:2005 art. 6.2.4."""

from dataclasses import dataclass

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
class CheckStrengthCompressionClass123:
    """Class to perform compression force resistance check for steel cross-sections,
    for cross-section class 1, 2, and 3, based on EN 1993-1-1:2005 art. 6.2.4.

    Coordinate System:
    ```
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
    ```

    Parameters
    ----------
    steel_cross_section : SteelCrossSection
        The steel cross-section to check.
    n : KN, optional
        The applied compressive force (negative value), default is 0 kN.
        Will raise an error if a positive value is provided, as this check is only for compression.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    ```python
    from blueprints.checks import CheckStrengthCompressionClass123
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(1.5)
    n = -100  # Applied compressive force in kN

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthCompressionClass123(heb_300_s355, n, gamma_m0=1.0)
    calc.report().to_word("compression_strength.docx", language="nl")
    ```

    Raises
    ------
    ValueError
        If a positive value is provided for the applied force `n`, as this check is only for compression.
        The applied force must be negative to indicate compression.
    """

    steel_cross_section: SteelCrossSection
    n: KN = 0
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Compression strength check for steel profiles"

    def __post_init__(self) -> None:
        """Post-initialization to validate input parameters."""
        if self.n > 0:
            raise ValueError("Input force N (F_x) must be negative for compression check.")

    @staticmethod
    def source_docs() -> list[str]:
        """List of source document identifiers used for this check.

        Returns
        -------
        list[str]
        """
        return [EN_1993_1_1_2005]

    def plastic_resistance(self) -> Formula:
        """Calculate the compression force plastic resistance of the steel cross-section based on the gross
        cross-sectional area and yield strength (EN 1993-1-1:2005 art. 6.2.4(2) - Formula (6.10)).

        Returns
        -------
        Formula
            The calculated compression force resistance.
        """
        area = self.steel_cross_section.profile.section_properties().area
        assert area is not None, "Cross-sectional area must be defined for the steel profile."
        f_y = self.steel_cross_section.yield_strength
        return formula_6_10.Form6Dot10NcRdClass1And2And3(a=area, f_y=f_y, gamma_m0=self.gamma_m0)

    def compression_strength_unity_check(self) -> Formula:
        """Calculate the unity check for compression strength of the steel cross-section based on the applied compressive
        force and the calculated resistance (EN 1993-1-1:2005 art. 6.2.4(1) - Formula (6.9)).

        Returns
        -------
        Formula
            The calculated unity check for compression strength.
        """
        n_ed = abs(self.n * KN_TO_N)
        n_c_rd = self.plastic_resistance()
        return formula_6_9.Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd)

    def result(self) -> CheckResult:
        """Calculate result of compression force resistance.

        Returns
        -------
        CheckResult
                This is the result of the compression force resistance check, which compares the provided compressive force
            with the calculated resistance. The check is satisfied if the provided compressive force does not exceed
            the resistance.
        """
        return CheckResult.from_comparison(provided=abs(self.n * KN_TO_N), required=self.plastic_resistance())

    def report(self, n: int = 2) -> Report:
        """Returns the report for the compression force check.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Full report on the compression force check, including the applied force, calculated resistance,
            unity check, and overall result.
        """
        report = Report("Compression check of steel cross-section")

        # will not generate a report if no compressive force is applied, as the check is not necessary in that case
        if self.n == 0:
            report.add_paragraph("No compressive force was applied; therefore, no compression force check is necessary.")
            return report

        # generate report if compressive force is applied
        report.add_paragraph(
            rf"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            rf"is loaded with a compressive force of {abs(self.n):.{n}f} kN. "
        ).add_newline(n=2)

        # resistance
        report.add_paragraph(r"The resistance is calculated as follows:")
        report.add_formula(self.plastic_resistance(), n=n).add_newline(n=2)

        # unity check
        report.add_paragraph("The unity check is calculated as follows:")
        report.add_formula(self.compression_strength_unity_check(), n=n).add_newline(n=2)

        if self.result().is_ok:
            report.add_paragraph("The check for compression force satisfies the requirements.")
        else:
            report.add_paragraph("The check for compression force does NOT satisfy the requirements.")
        return report
