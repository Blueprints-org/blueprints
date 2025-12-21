"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 3 cross-sections according to Eurocode 3.
"""

from dataclasses import dataclass

from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.checks.eurocode.en_1993_1_1_2005.strength.normal_force import NormalForceClass123
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.saf.results.result_internal_force_1d import ResultInternalForce1D
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.type_alias import DIMENSIONLESS


@dataclass(frozen=True)
class SteelIProfileStrengthClass3:
    """Steel I-Profile strength check for class 3.

    Performs strength checks on steel I-profiles according to Eurocode 3, for class 3 cross-sections.

    Parameters
    ----------
    profile : ISteelProfile
        The steel I-profile to check.
    properties : SectionProperties
        The section properties of the profile.
    result_internal_force_1d : ResultInternalForce1D
        The load combination to apply to the profile.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    """

    profile: ISteelProfile
    properties: SectionProperties
    result_internal_force_1d: ResultInternalForce1D
    gamma_m0: DIMENSIONLESS = 1.0

    source_document = EN_1993_1_1_2005

    def calculation_steps(self) -> dict:
        """Perform calculation steps for all strength checks."""
        return {
            "normal_force": NormalForceClass123(self.profile, self.properties, self.result_internal_force_1d, self.gamma_m0),
            "bending_moment_my": None,  # To be implemented
            "bending_moment_mz": None,  # To be implemented
            "shear_force_vz": None,  # To be implemented
            "shear_force_vy": None,  # To be implemented
            "torsion": None,  # To be implemented
            "bending_shear_interaction": None,  # To be implemented
            "bending_axial_interaction": None,  # To be implemented
            "bending_shear_axial_interaction": None,  # To be implemented
        }

    def check(self) -> CheckResult:
        """Perform all strength checks and return the overall result."""
        results = (r for r in self.calculation_steps().values() if r is not None)
        return CheckResult.from_unity_check(max(r.check().unity_check for r in results))

    def latex(self, n: int = 1, latex_format: str = "long") -> str:  # noqa: C901
        """
        Returns the combined LaTeX string representation for all strength checks.

        Parameters
        ----------
        n : int, optional
            Formula numbering for LaTeX output (default is 1).
        latex_format : str, optional
            Output format: 'long' or 'summary'.
            'long' gives detailed output or 'summary' gives a summary.

        Returns
        -------
        str
            Combined LaTeX representation of all strength checks.
        """
        allowed_formats = {"long", "summary"}
        if latex_format not in allowed_formats:
            raise ValueError(f"latex_format must be one of {allowed_formats}, got '{latex_format}'")

        all_latex = ""

        # Check normal force
        if self.result_internal_force_1d.n != 0:
            all_latex += self.calculation_steps()["normal_force"].latex(n=n, latex_format=latex_format)

        # Check My axis bending moment (not yet implemented)
        if self.result_internal_force_1d.my != 0 and self.result_internal_force_1d.mz == 0:
            all_latex += r"\newline \newline \text{Warning: My axis bending moment check not yet implemented.}"

        # Check Mz axis bending moment (not yet implemented)
        if self.result_internal_force_1d.mz != 0 and self.result_internal_force_1d.my == 0:
            all_latex += r"\newline \newline \text{Warning: Mz axis bending moment check not yet implemented.}"

        # Check single axis shear force Vz (not yet implemented)
        if self.result_internal_force_1d.vz != 0:
            all_latex += r"\newline \newline \text{Warning: single axis shear force Vz check not yet implemented.}"

        # Check single axis shear force Vy (not yet implemented)
        if self.result_internal_force_1d.vy != 0:
            all_latex += r"\newline \newline \text{Warning: single axis shear force Vy check not yet implemented.}"

        # Check torsion (not yet implemented)
        if self.result_internal_force_1d.mx != 0:
            all_latex += r"\newline \newline \text{Warning: torsion check not yet implemented.}"

        # Check (multiple axis) bending and shear interaction (not yet implemented)
        if (
            max(abs(self.result_internal_force_1d.my), abs(self.result_internal_force_1d.mz)) > 0
            and max(abs(self.result_internal_force_1d.vy), abs(self.result_internal_force_1d.vz)) > 0
        ):
            all_latex += r"\newline \newline \text{Warning: bending and shear interaction check not yet implemented.}"

        # Check bending and axial force interaction (not yet implemented)
        if (max(abs(self.result_internal_force_1d.my), abs(self.result_internal_force_1d.mz)) > 0 and abs(self.result_internal_force_1d.n) > 0) or (
            self.result_internal_force_1d.mz != 0 and self.result_internal_force_1d.my != 0
        ):
            all_latex += r"\newline \newline \text{Warning: (multiple axis) bending and axial force interaction check not yet implemented.}"

        # Check bending, shear and axial force interaction (not yet implemented)
        if (
            max(abs(self.result_internal_force_1d.my), abs(self.result_internal_force_1d.mz)) > 0
            and max(abs(self.result_internal_force_1d.vy), abs(self.result_internal_force_1d.vz)) > 0
            and abs(self.result_internal_force_1d.n) > 0
        ):
            all_latex += r"\newline \newline \text{Warning: bending, shear and axial force interaction check not yet implemented.}"

        if all_latex == "":
            all_latex += r"\text{No internal forces applied.} \newline CHECK \to OK"

        # If the LaTeX string starts with a leading return (\newline), remove it for cleaner output
        if all_latex.startswith(r"\newline"):
            all_latex = all_latex[8:]

        return all_latex
