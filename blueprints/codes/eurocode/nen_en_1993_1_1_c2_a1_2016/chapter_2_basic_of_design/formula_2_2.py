"""Formula 2.2 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 2: Basis of design."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form2Dot2CharacteristicValueResistance(Formula):
    """Class representing formula 2.2 for the calculation of the characteristic value of the resistance [$R_k$]."""

    label = "2.2"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(self, r_d: DIMENSIONLESS, gamma_mi: DIMENSIONLESS) -> None:
        r"""[$R_k$] Characteristic value of the resistance [$kN$].

        NEN-EN 1993-1-1+C2+A1:2016 art.2.5(2) - Formula (2.2)

        Parameters
        ----------
        r_d : DIMENSIONLESS
            [$R_d$] Design value of the resistance according to Annex D of EN 1990 [$kN$].
        gamma_mi : DIMENSIONLESS
            [$\gamma_{Mi}$] Recommended partial factors for the resistance [$-$].
        """
        super().__init__()
        self.r_d = r_d
        self.gamma_mi = gamma_mi

    @staticmethod
    def _evaluate(r_d: DIMENSIONLESS, gamma_mi: DIMENSIONLESS) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(r_d=r_d, gamma_mi=gamma_mi)
        return r_d * gamma_mi

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.10."""
        return LatexFormula(
            return_symbol=r"R_{k}",
            result=f"{self:.2f}",
            equation=r"R_d \cdot \gamma_{Mi}",
            numeric_equation=rf"{self.r_d:.2f} \cdot {self.gamma_mi:.2f}",
            comparison_operator_label="=",
        )
