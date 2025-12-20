"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 1, 2 and 3 cross-sections according to Eurocode 3.
"""

from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import (
    formula_6_5,
    formula_6_6,
    formula_6_9,
    formula_6_10,
)
from blueprints.codes.formula import Formula
from blueprints.saf.results.result_internal_force_1d import ResultInternalForce1D
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.type_alias import DIMENSIONLESS
from blueprints.unit_conversion import KN_TO_N


class NormalForceClass123:
    """Class to perform normal force resistance check.

    Checks normal force resistance for steel I-profiles according to Eurocode 3, chapter 6.2.3 (tension) and 6.2.4 (compression).

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
        self,
        profile: ISteelProfile,
        properties: SectionProperties,
        result_internal_force_1d: ResultInternalForce1D,
        gamma_m0: DIMENSIONLESS = 1.0,
    ) -> None:
        self.profile = profile
        self.properties = properties
        self.result_internal_force_1d = result_internal_force_1d
        self.gamma_m0 = gamma_m0

    def calculation_steps(self) -> list[Formula]:
        """Perform calculation steps for normal force resistance check.

        Returns
        -------
        list of Formula
            Calculation results. Returns an empty list if no normal force is applied.
        """
        if self.result_internal_force_1d.n == 0:
            return []
        if self.result_internal_force_1d.n > 0:  # tension, based on chapter 6.2.3
            a = self.properties.area if self.properties.area is not None else 0
            f_y = min(element.yield_strength for element in self.profile.elements)
            n_ed = self.result_internal_force_1d.n * KN_TO_N
            n_t_rd = formula_6_6.Form6Dot6DesignPlasticRestistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
            check_tension = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)
            return [n_t_rd, check_tension]

        # compression, based on chapter 6.2.4
        a = self.properties.area if self.properties.area is not None else 0
        f_y = min(element.yield_strength for element in self.profile.elements)
        n_ed = -self.result_internal_force_1d.n * KN_TO_N
        n_c_rd = formula_6_10.Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
        check_compression = formula_6_9.Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd)
        return [n_c_rd, check_compression]

    def check(self) -> CheckResult:
        """Check normal force resistance.

        Returns
        -------
        CheckResult
            True if the normal force check passes, False otherwise.
        """
        if len(self.calculation_steps()) == 0:
            return CheckResult.from_bool(True)

        provided = abs(self.result_internal_force_1d.n * KN_TO_N)
        required = self.calculation_steps()[0]
        return CheckResult.from_comparison(provided=provided, required=required)

    def latex(self, n: int = 1, latex_format: str = "long") -> str:
        """Returns the LaTeX string representation for the normal force check.

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
            LaTeX representation of the normal force check.
        """
        allowed_formats = {"long", "summary"}
        if latex_format not in allowed_formats:
            raise ValueError(f"latex_format must be one of {allowed_formats}, got '{latex_format}'")

        if self.result_internal_force_1d.n == 0:
            text = r"\text{Checking normal force not needed as no normal force applied.} \newline CHECK \to OK"
        elif self.result_internal_force_1d.n > 0:
            text = r"\text{Checking normal force (tension) using chapter 6.2.3.}"
        elif self.result_internal_force_1d.n < 0:
            text = r"\text{Checking normal force (compression) using chapter 6.2.4.}"

        if self.result_internal_force_1d.n != 0:
            if latex_format == "summary":
                text += rf"\newline {self.calculation_steps()[-1].latex(n=n)} "
            else:  # long
                for step in self.calculation_steps():
                    text += rf"\newline \text{{With formula {step.label}:}} \newline {step.latex(n=n)} "
        return text
