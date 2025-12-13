"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 3 cross-sections according to Eurocode 3.
"""

from sectionproperties.post.post import SectionProperties

from blueprints.checks.steel.strength.normal_force import NormalForceClass123
from blueprints.saf.results.result_internal_force_1d import ResultInternalForce1D
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.type_alias import DIMENSIONLESS


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

    def __init__(
        self, profile: ISteelProfile, properties: SectionProperties, result_internal_force_1d: ResultInternalForce1D, gamma_m0: DIMENSIONLESS = 1.0
    ) -> None:
        self.profile = profile
        self.properties = properties
        self.result_internal_force_1d = result_internal_force_1d
        self.gamma_m0 = gamma_m0
        self.normal_force = NormalForceClass123(self.profile, self.properties, self.result_internal_force_1d, self.gamma_m0)

    def check(self) -> bool:
        """Returns True if all strength criteria for the steel I-profile pass, False otherwise.

        Warning: Currently only normal force and single axis bending moment checks are implemented.
        """
        # check normal force
        return self.normal_force.check()

    def latex(self, n: int = 1, summary: bool = False) -> str:  # noqa: C901
        """
        Returns the combined LaTeX string representation for all strength checks.

        Parameters
        ----------
        n : int, optional
            Formula numbering for LaTeX output (default is 1).
        summary : bool, optional
            If True, returns a summary LaTeX output; otherwise, returns detailed output (default is False).

        Returns
        -------
        str
            Combined LaTeX representation of all strength checks.
        """
        all_latex = ""

        # Check normal force
        if self.result_internal_force_1d.n != 0:
            all_latex += self.normal_force.latex(n=n, summary=summary)

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

        # If the LaTeX string starts with return (\newline), remove it for cleaner output
        if all_latex.startswith(r"\newline"):
            all_latex = all_latex[8:]

        return all_latex
