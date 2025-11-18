"""Steel I-Profile strength check according to Eurocode 3."""

import numpy as np
from sectionproperties.post.post import SectionProperties

from blueprints.checks.loads.load_combination import LoadCombination
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5, formula_6_6, formula_6_9, formula_6_10
from blueprints.codes.formula import Formula
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.type_alias import DIMENSIONLESS
from blueprints.unit_conversion import KN_TO_N


class SteelIProfileStrengthClass3:
    """Steel I-Profile strength check for class 3.

    This class performs strength checks on steel I-profiles according to Eurocode 3, for class 3 cross-sections.

    Parameters
    ----------
    profile : ISteelProfile
        The steel I-profile to check.
    load_combination : LoadCombination
        The load combination to apply to the profile.
    """

    def __init__(
        self, profile: ISteelProfile, properties: SectionProperties, load_combination: LoadCombination, gamma_m0: DIMENSIONLESS = 1.0
    ) -> None:
        """Initialize the steel I-profile strength check.

        Parameters
        ----------
        profile : ISteelProfile
            The steel I-profile to check.
        properties: SectionProperties
            The section properties of the profile.
        load_combination : LoadCombination
            The load combination to apply to the profile.
        gamma_m0 : DIMENSIONLESS
            Partial safety factor for resistance of cross-sections, default is 1.0.
        """
        self.profile = profile
        self.properties = properties
        self.load_combination = load_combination
        self.gamma_m0 = gamma_m0

    class NormalForceCheck:
        """Class to perform normal force resistance check."""

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
            list
                Calculation results and check objects.
            """
            if self.load_combination.normal_force == 0:
                return []
            if self.load_combination.normal_force > 0:  # tension, based on chapter 6.2.3
                n_ed = self.load_combination.normal_force * KN_TO_N
                a = self.properties.area
                f_y = np.inf
                for element in self.profile.elements:
                    f_y = element.yield_strength if f_y > element.yield_strength else f_y
                n_t_rd = formula_6_6.Form6Dot6DesignPlasticRestistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=self.gamma_m0)
                check_tension = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)
                return [n_t_rd, check_tension]

            # compression
            n_ed = -self.load_combination.normal_force * KN_TO_N
            a = self.properties.area
            f_y = np.inf
            for element in self.profile.elements:
                f_y = element.yield_strength if f_y > element.yield_strength else f_y
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

        def latex(self, n: int = 1, short: bool = False) -> str:
            """Returns the lateX string representation for Nominal concrete cover check."""
            if self.load_combination.normal_force == 0:
                return r"\text{Normal force check: no normal force applied.} \\ CHECK \to OK"

            if self.load_combination.normal_force > 0:
                text = "\\text{Normal force check: tension checks applied using chapter 6.2.3.}"
                n_t_rd, check = self.calculation_steps()
                if not short:
                    text += f"\\\\\\text{{With formula 6.6:}}\\\\{n_t_rd.latex(n=n)}"
                    text += "\\\\\\text{With formula 6.5:}"
                text += f"\\\\{check.latex(n=n)}"
                return text

            text = "\\text{Normal force check: compression checks applied using chapter 6.2.4.}"
            n_c_rd, check = self.calculation_steps()
            if not short:
                text += f"\\\\\\text{{With formula 6.10:}}\\\\{n_c_rd.latex(n=n)}"
                text += "\\\\\\text{With formula 6.9:}"
            text += f"\\\\{check.latex(n=n)}"
            return text

    # To be extended with more checks (shear, bending, torsion, various combinations and finally complete check)
    # ones the presented structure above is discussed and decided upon
