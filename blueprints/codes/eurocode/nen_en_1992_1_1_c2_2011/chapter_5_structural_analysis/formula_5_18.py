"""Formula 5.18 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN, MM4, MPA, M
from blueprints.unit_conversion import M_TO_MM, N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot18ComparisonGeneralSecondOrderEffects:
    """Class representing comparison 5.18 for general second-order effects in buildings."""

    label = "5.18"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, f_ved: KN, k_1: DIMENSIONLESS, n_s: DIMENSIONLESS, length: M, e_cd: MPA, i_c: MM4) -> None:
        r"""[$CHECK$] Criteria met, based on damage accumulation.

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.3(1) - Formula (5.18)

        Parameters
        ----------
        f_ved : KN
            [$F_{v,ed}$] Total vertical load (on braced and bracing members) [$kN$].
        k_1 : DIMENSIONLESS
            [$k_1$] The value of k1 for use in a Country may be found in its National Annex. Recommend value is
            0.31 [$-$].
        n_s : DIMENSIONLESS
            [$n_s$] is the total number of storeys [$-$].
        length : M
            [$L$] is the total height of the building above level of moment restraint. [$m$].
        e_cd : MPa
            [$E_{cd}$] is the design value of the modulus of elasticity of concrete. [$MPa$].
        i_c : MM4
            [$I_c$] is the second moment of area (uncracked concrete section) of bracing member(s). [$mm^4$].
        """
        self.f_ved = f_ved
        self.k_1 = k_1
        self.n_s = n_s
        self.length = length
        self.e_cd = e_cd
        self.i_c = i_c

    @property
    def left_hand_side(self) -> KN:
        """Calculate the left hand side of the comparison.

        Returns
        -------
        KN
            Left hand side of the comparison.
        """
        return self.f_ved

    @property
    def right_hand_side(self) -> KN:
        """Calculate the right hand side of the comparison.

        Returns
        -------
        KN
            Right hand side of the comparison.
        """
        raise_if_less_or_equal_to_zero(n=(self.n_s + 1.6))
        return (self.k_1 * (self.n_s / (self.n_s + 1.6)) * ((self.e_cd * self.i_c) / (self.length * M_TO_MM) ** 2)) * N_TO_KN

    @property
    def ratio(self) -> DIMENSIONLESS:
        """Ratio between left hand side and right hand side of the comparison, commonly referred to as unity check."""
        return self.left_hand_side / self.right_hand_side

    def __bool__(self) -> bool:
        """Evaluates the comparison, for more information see the __init__ method."""
        return self.left_hand_side <= self.right_hand_side

    def __str__(self) -> str:
        """Return the result of the comparison."""
        return self.latex().complete

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.18."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"F_{V,Ed} \leq \frac{n_s}{n_s + 1.6} \cdot \frac{\sum E_{cd} \cdot I_c}{L^2}",
            numeric_equation=(
                rf"{self.left_hand_side:.3f}"
                rf"\leq \frac{{{self.n_s}}}{{{self.n_s + 1.6}}} \cdot \frac{{\sum {self.e_cd} \cdot {self.i_c}}}{{{self.length**2}}}"
            ),
            comparison_operator_label=r"\rightarrow",
        )
