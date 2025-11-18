"""Steel I-Profile strength check according to Eurocode 3.

This module provides strength checks for steel I-profiles of class 3 cross-sections according to Eurocode 3.
"""

from sectionproperties.post.post import SectionProperties

from blueprints.checks.loads.load_combination import LoadCombination
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5, formula_6_6, formula_6_9, formula_6_10
from blueprints.codes.formula import Formula
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.type_alias import DIMENSIONLESS
from blueprints.unit_conversion import KN_TO_N


class SteelIProfileStrengthClass3:
    """Steel I-Profile strength check for class 3.

    Performs strength checks on steel I-profiles according to Eurocode 3, for class 3 cross-sections.

    Parameters
    ----------
    profile : ISteelProfile
        The steel I-profile to check.
    properties : SectionProperties
        The section properties of the profile.
    load_combination : LoadCombination
        The load combination to apply to the profile.
    gamma_m0 : DIMENSIONLESS, optional
        Partial safety factor for resistance of cross-sections, default is 1.0.
    """

    def __init__(
        self, profile: ISteelProfile, properties: SectionProperties, load_combination: LoadCombination, gamma_m0: DIMENSIONLESS = 1.0
    ) -> None:
        self.profile = profile
        self.properties = properties
        self.load_combination = load_combination
        self.gamma_m0 = gamma_m0

    class NormalForceCheck:
        """Class to perform normal force resistance check.

        Checks normal force resistance for steel I-profiles according to Eurocode 3, chapter 6.2.3 (tension) and 6.2.4 (compression).

        Parameters
        ----------
        profile : ISteelProfile
            The steel I-profile to check.
        properties : SectionProperties
            The section properties of the profile.
        load_combination : LoadCombination
            The load combination to apply to the profile.
        gamma_m0 : DIMENSIONLESS, optional
            Partial safety factor for resistance of cross-sections, default is 1.0.
        """

        def __init__(
            self, profile: ISteelProfile, properties: SectionProperties, load_combination: LoadCombination, gamma_m0: DIMENSIONLESS = 1.0
        ) -> None:
            self.profile = profile
            self.properties = properties
            self.load_combination = load_combination
            self.gamma_m0 = gamma_m0

        def calculation_steps(self) -> list[Formula]:
            """Perform calculation steps for normal force resistance check.

            Returns
            -------
            list of Formula
                Calculation results and check objects. Returns an empty list if no normal force is applied.
            """
            if self.load_combination.normal_force == 0:
                return []
            if self.load_combination.normal_force > 0:  # tension, based on chapter 6.2.3
                a = self.properties.area if self.properties.area is not None else 0
                f_y = min(element.yield_strength for element in self.profile.elements)
                n_ed = self.load_combination.normal_force * KN_TO_N
                n_t_rd = formula_6_6.Form6Dot6DesignPlasticRestistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
                check_tension = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)
                return [n_t_rd, check_tension]

            # compression, based on chapter 6.2.4
            a = self.properties.area if self.properties.area is not None else 0
            f_y = min(element.yield_strength for element in self.profile.elements)
            n_ed = -self.load_combination.normal_force * KN_TO_N
            n_c_rd = formula_6_10.Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
            check_compression = formula_6_9.Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd)
            return [n_c_rd, check_compression]

        def value(self) -> bool:
            """Check normal force resistance.

            Returns
            -------
            bool
                True if the normal force check passes, False otherwise.
            """
            if len(self.calculation_steps()) == 0:
                return True
            return bool(self.calculation_steps()[-1])

        def latex(self, n: int = 1, summary: bool = False) -> str:
            """Returns the LaTeX string representation for the normal force check.

            Parameters
            ----------
            n : int, optional
                Formula numbering for LaTeX output (default is 1).
            summary : bool, optional
                If True, returns a summary LaTeX output; otherwise, returns detailed output (default is False).

            Returns
            -------
            str
                LaTeX representation of the normal force check.
            """
            if self.load_combination.normal_force == 0:
                text = r"\text{Normal force check: no normal force applied.} \\ CHECK \to OK"
            elif self.load_combination.normal_force > 0:
                text = "\\text{Normal force check: tension checks applied using chapter 6.2.3.}"
            elif self.load_combination.normal_force < 0:
                text = "\\text{Normal force check: compression checks applied using chapter 6.2.4.}"

            if self.load_combination.normal_force != 0:
                if summary:
                    text += f"\\\\{self.calculation_steps()[-1].latex(n=n)}"
                else:
                    for step in self.calculation_steps():
                        text += f"\\\\\\text{{With formula {step.label}:}}\\\\{step.latex(n=n)}"
            return text

    # To be extended with more checks (shear, bending, torsion, various combinations and finally complete check)
    # ones the presented structure above is discussed and decided upon

    def value(self) -> bool:
        """Returns True if all strength criteria for the steel I-profile pass, False otherwise."""
        # Check normal force
        normal_force_check = self.NormalForceCheck(self.profile, self.properties, self.load_combination, self.gamma_m0)
        return normal_force_check.value()

    def latex(self, n: int = 1, summary: bool = False) -> str:
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
        all_latex += self.NormalForceCheck(self.profile, self.properties, self.load_combination, self.gamma_m0).latex(n=n, summary=summary)

        return all_latex
