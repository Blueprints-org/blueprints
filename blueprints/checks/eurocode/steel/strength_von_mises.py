"""Module for checking von Mises equivalent stress of steel cross-sections according to Eurocode 3 (EN 1993-1-1:2005)."""

from dataclasses import dataclass

import numpy as np

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import DIMENSIONLESS, KN, KNM
from blueprints.utils.report import Report


@dataclass(frozen=True)
class CheckStrengthVonMises:
    """Class to perform von Mises equivalent stress check for steel cross-sections based on Eurocode 3.

    This check calculates the maximum von Mises equivalent stress in a steel cross-section under combined
    internal forces and verifies it does not exceed the yield strength.

    **Note:** This formula is not applicable for slender structures (cross-section class 4).
    For slender structures, the effective section properties must be used.

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
    ←---O
    y (horizontal/side, usually weak axis)
    ```

    Parameters
    ----------
    steel_cross_section : SteelCrossSection
        The steel cross-section to check.
    n : KN, optional
        Axial force [kN], positive for tension, negative for compression. Default is 0 kN.
    v_y : KN, optional
        Shear force in the y-direction [kN]. Default is 0 kN.
    v_z : KN, optional
        Shear force in the z-direction [kN]. Default is 0 kN.
    m_x : KNM, optional
        Torsional moment [kNm]. Default is 0 kNm.
    m_y : KNM, optional
        Bending moment about the y-axis [kNm]. Default is 0 kNm.
    m_z : KNM, optional
        Bending moment about the z-axis [kNm]. Default is 0 kNm.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.

    Example
    -------
    ```python
    from blueprints.checks.eurocode.steel.strength_von_mises import CheckStrengthVonMises
    from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB
    from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_300_profile = HEB.HEB300.with_corrosion(0)

    heb_300_s355 = SteelCrossSection(profile=heb_300_profile, material=steel_material)
    calc = CheckStrengthVonMises(
        heb_300_s355,
        n=100,  # 100 kN axial force
        v_z=50,  # 50 kN shear force
        m_y=200,  # 200 kNm bending moment
        gamma_m0=1.0,
    )
    calc.report().to_word("von_mises_check.docx")
    ```
    """

    steel_cross_section: SteelCrossSection
    n: KN = 0
    v_y: KN = 0
    v_z: KN = 0
    m_x: KNM = 0
    m_y: KNM = 0
    m_z: KNM = 0
    gamma_m0: DIMENSIONLESS = 1.0
    name: str = "Von Mises equivalent stress check for steel"

    @staticmethod
    def source_docs() -> list[str]:
        """List of source document identifiers used for this check.

        Returns
        -------
        list[str]
        """
        return [EN_1993_1_1_2005]

    def _validate_design_resistance(self) -> None:
        """Validate that design resistance parameters are valid.

        Raises
        ------
        ValueError
            If gamma_m0 is not positive or yield_strength is not positive.
        """
        if self.gamma_m0 <= 0:
            raise ValueError(f"gamma_m0 must be positive, got {self.gamma_m0}")
        if self.steel_cross_section.yield_strength <= 0:
            raise ValueError(
                f"yield_strength must be positive, got {self.steel_cross_section.yield_strength}"
            )

    def maximum_von_mises_stress(self) -> float:
        """Calculate the maximum von Mises equivalent stress in the cross-section.

        The von Mises stress is calculated from the full 3D stress tensor at all points in the
        cross-section, and the maximum value is returned.

        Returns
        -------
        float
            The maximum von Mises equivalent stress in N/mm².
        """
        # Calculate stress distribution using sectionproperties
        stress_post = self.steel_cross_section.profile.calculate_stress(
            n=self.n,
            v_y=self.v_y,
            v_z=self.v_z,
            m_x=self.m_x,
            m_y=self.m_y,
            m_z=self.m_z,
        )

        stress_data = stress_post.get_stress()[0]
        von_mises = stress_data["sig_vm"]
        # Return the maximum von Mises stress
        return float(np.max(np.abs(von_mises)))

    def unity_check(self) -> float:
        """Calculate the unity check for von Mises equivalent stress.

        The unity check is the ratio of the maximum von Mises stress to the
        design yield strength (f_y / gamma_m0).

        Returns
        -------
        float
            The unity check value (should be ≤ 1.0 for adequate resistance).
        """
        self._validate_design_resistance()
        von_mises_stress = self.maximum_von_mises_stress()
        design_yield_strength = self.steel_cross_section.yield_strength / self.gamma_m0
        return von_mises_stress / design_yield_strength

    def result(self) -> CheckResult:
        """Calculate result of von Mises equivalent stress check.

        Returns
        -------
        CheckResult
            True if the von Mises stress check passes, False otherwise.
        """
        self._validate_design_resistance()
        return CheckResult.from_comparison(
            provided=self.maximum_von_mises_stress(),
            required=self.steel_cross_section.yield_strength / self.gamma_m0,
        )

    def report(self, n: int = 2) -> Report:
        """Returns the report for the von Mises equivalent stress check.

        Parameters
        ----------
        n : int, optional
            Number of decimal places for numerical values in the report (default is 2).

        Returns
        -------
        Report
            Report of the von Mises equivalent stress check.
        """
        report = Report("Check: von Mises equivalent stress")

        # Check if any loads are applied
        total_load = abs(self.n) + abs(self.v_y) + abs(self.v_z) + abs(self.m_x) + abs(self.m_y) + abs(self.m_z)
        if total_load == 0:
            report.add_paragraph("No internal forces were applied; therefore, no von Mises stress check is necessary.")
            return report

        # Validate design resistance before calculations
        self._validate_design_resistance()

        # Add profile and material information
        report.add_paragraph(
            f"Profile {self.steel_cross_section.profile.name} with steel quality {self.steel_cross_section.material.steel_class.name} "
            f"is loaded with the following internal forces:"
        )
        report.add_newline()

        loads = []

        # Add internal forces
        if self.n != 0:
            loads.append(f"Axial force N = {self.n:.{n}f} kN")
        if self.v_y != 0:
            loads.append(f"Shear force V_y = {self.v_y:.{n}f} kN")
        if self.v_z != 0:
            loads.append(f"Shear force V_z = {self.v_z:.{n}f} kN")
        if self.m_x != 0:
            loads.append(f"Torsional moment M_x = {self.m_x:.{n}f} kNm")
        if self.m_y != 0:
            loads.append(f"Bending moment M_y = {self.m_y:.{n}f} kNm")
        if self.m_z != 0:
            loads.append(f"Bending moment M_z = {self.m_z:.{n}f} kNm")

        report.add_list(loads)

        report.add_newline(n=2)

        # Calculate von Mises stress
        von_mises_max = self.maximum_von_mises_stress()
        design_yield = self.steel_cross_section.yield_strength / self.gamma_m0

        report.add_paragraph("The maximum von Mises equivalent stress is calculated from the 3D stress tensor: ")
        report.add_paragraph(
            f"$\\sigma_{{vm,max}}$ = {von_mises_max:.{n}f} N/mm². ",
        )

        # Design yield strength
        report.add_paragraph("The design yield strength is: ")
        report.add_paragraph(
            f"$f_y / \\gamma_{{M0}}$ = {design_yield:.{n}f} N/mm². ",
        )

        # Unity check
        unity = self.unity_check()
        report.add_paragraph("The unity check is: ")
        report.add_paragraph(
            f"$\\eta$ = $\\sigma_{{vm,max}}$ / ($f_y / \\gamma_{{M0}})$ = {unity:.{n}f} -.",
        )
        report.add_newline(n=2)

        # Conclusion
        if self.result().is_ok:
            report.add_paragraph("The von Mises equivalent stress check satisfies the requirements.")
        else:
            report.add_paragraph("The von Mises equivalent stress check does NOT satisfy the requirements.")

        return report
