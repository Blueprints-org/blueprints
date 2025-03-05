"""Formula 5.21 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM4, MPA
from blueprints.validations import raise_if_negative


class Form5Dot21NominalStiffness(Formula):
    r"""Class representing formula 5.21 for the calculation of the nominal stiffness of slender compression members
    with arbitrary cross-section, [$EI$] [$Nmm^2$].
    """

    label = "5.21"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, k_c: DIMENSIONLESS, e_cd: MPA, i_c: MM4, k_s: DIMENSIONLESS, e_s: MPA, i_s: MM4) -> None:
        r"""[$EI$] Nominal stiffness of slender compression members with arbitrary cross-section.

        NEN-EN 1992-1-1+C2:2011 art.5.8.7.2(2) or (3) - Formula (5.21)

        Parameters
        ----------
        k_c : DIMENSIONLESS
            [$K_{c}$] is a factor for effects of cracking, creep etc. see 5.8.7.2 (2) or (3).
        e_cd : MPA
            [$E_{cd}$] is the design value of the modulus of elasticity of concrete, see 5.8.6 (3)
        i_c : MPA
            [$I_{c}$] is the moment of inertia of concrete cross section.
        k_s : DIMENSIONLESS
            [$K_{s}$] is a factor for contribution of reinforcement, see 5.8.7.2 (2) or (3).
        e_s : MPA
            [$E_{s}$] is the design value of the modulus of elasticity of reinforcement, 5.8.6 (3).
        i_s : MPA
            [$I_{s}$] is the second moment of area of reinforcement, about the centre of area of the concrete.
        """
        super().__init__()
        self.k_c = k_c
        self.e_cd = e_cd
        self.i_c = i_c
        self.k_s = k_s
        self.e_s = e_s
        self.i_s = i_s

    @staticmethod
    def _evaluate(k_c: DIMENSIONLESS, e_cd: MPA, i_c: MPA, k_s: DIMENSIONLESS, e_s: MPA, i_s: MPA) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(k_c=k_c, e_cd=e_cd, i_c=i_c, k_s=k_s, e_s=e_s, i_s=i_s)
        return k_c * e_cd * i_c + k_s * e_s * i_s

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.21."""
        return LatexFormula(
            return_symbol=r"EI",
            result=f"{self:.3f}",
            equation=r"K_{c} \cdot E_{cd} \cdot I_{c} + K_{s} \cdot E_{s} \cdot I_{s}",
            numeric_equation=rf"{self.k_c:.3f} \cdot {self.e_cd:.3f} \cdot {self.i_c:.3f} + {self.k_s:.3f} \cdot {self.e_s:.3f} \cdot {self.i_s:.3f}",
            comparison_operator_label="=",
        )
