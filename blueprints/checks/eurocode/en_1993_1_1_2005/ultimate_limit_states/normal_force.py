"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 1, 2 and 3 cross-sections according to Eurocode 3.
"""

from dataclasses import dataclass

from sectionproperties.post.post import SectionProperties

from blueprints.checks.check_result import CheckResult
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
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


@dataclass(frozen=True)
class NormalForceClass123:
    """Class to perform normal force resistance check.

    Performs strength checks on steel I-profiles according to Eurocode 3, for class 1, 2 and 3 cross-sections.

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

    Example
    -------
    from blueprints.checks.eurocode.en_1993_1_1_2005.ultimate_limit_states.normal_force import NormalForceClass123
    from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
    from blueprints.materials.steel import SteelMaterial
    from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
    from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB
    from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
    from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile

    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_profile = ISteelProfile.from_standard_profile(
        profile=HEB.HEB300,
        steel_material=steel_material,
        corrosion=0,
    )
    heb_properties = heb_profile.section_properties(geometric=True, plastic=False, warping=False)
    result_internal_force_1d = ResultInternalForce1D(
                result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=100
            )
    calc = NormalForceClass123(heb_profile, heb_properties, result_internal_force_1d, gamma_m0=1.0)
    check = calc.check()

    """

    profile: ISteelProfile
    properties: SectionProperties
    result_internal_force_1d: ResultInternalForce1D
    gamma_m0: DIMENSIONLESS = 1.0

    source_document = EN_1993_1_1_2005

    def calculation_steps(self) -> dict[str, Formula]:
        """Perform calculation steps for normal force resistance check.

        Returns
        -------
        dict[str, Formula]
            Calculation results keyed by formula number. Returns an empty dict if no normal force is applied.
        """
        if self.result_internal_force_1d.n == 0:
            return {}
        if self.result_internal_force_1d.n > 0:  # tension, based on chapter 6.2.3
            a = self.properties.area if self.properties.area is not None else 0
            f_y = min(element.yield_strength for element in self.profile.elements)
            n_ed = self.result_internal_force_1d.n * KN_TO_N
            n_t_rd = formula_6_6.Form6Dot6DesignPlasticResistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
            check_tension = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)
            return {
                "6.6": n_t_rd,
                "6.5": check_tension,
            }

        # compression, based on chapter 6.2.4
        a = self.properties.area if self.properties.area is not None else 0
        f_y = min(element.yield_strength for element in self.profile.elements)
        n_ed = -self.result_internal_force_1d.n * KN_TO_N
        n_c_rd = formula_6_10.Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
        check_compression = formula_6_9.Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd)
        return {
            "6.10": n_c_rd,
            "6.9": check_compression,
        }

    def check(self) -> CheckResult:
        """Check normal force resistance.

        Returns
        -------
        CheckResult
            True if the normal force check passes, False otherwise.
        """
        steps = self.calculation_steps()
        if self.result_internal_force_1d.n == 0:
            return CheckResult.from_unity_check(0)
        if self.result_internal_force_1d.n > 0:
            provided = self.result_internal_force_1d.n * KN_TO_N
            required = steps["6.6"]
            return CheckResult.from_comparison(provided=provided, required=required)
        # compression
        provided = -self.result_internal_force_1d.n * KN_TO_N
        required = steps["6.10"]
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
                text += rf"\newline {list(self.calculation_steps().values())[-1].latex(n=n)} "
            else:  # long
                for step in self.calculation_steps().values():
                    text += rf"\newline \text{{With formula {step.label}:}} \newline {step.latex(n=n)} "
        return text
