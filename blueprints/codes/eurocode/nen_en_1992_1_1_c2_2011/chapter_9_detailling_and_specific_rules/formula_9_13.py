"""Formula 9.13 from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailling and specific rules."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, MM
from blueprints.validations import raise_if_negative


class Form9Dot13TensileForceToBeAnchored(Formula):
    """Class representing the formula 9.13 for the calculation of the tensile force to be anchored for."""

    label = "9.13"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        r: MM,
        z_e: MM,
        z_i: MM,
    ) -> None:
        r"""[$F_s$] Tensile force to be anchored [$kN$].

        NEN-EN 1992-1-1+C2:2011 art.9.8.2.2(2) - Formula (9.13)

        Parameters
        ----------
        r: MM
            [$R$] The resultant of ground pressure within x from figure 9.13 [$mm$].
        z_e: MM
            [$z_e$] The external lever arm, see figure 9.13, i.e. distance between the reinforcement and the horizontal force $F_c$ [$mm$].
        z_i: MM
            [$z_i$] Internal lever arm, see figure 9.13, i.e. distance between $R$ and the vertical force $N_{Ed}$ [$mm$].
        """
        super().__init__()
        self.r = r
        self.z_e = z_e
        self.z_i = z_i

    @staticmethod
    def _evaluate(
        r: MM,
        z_e: MM,
        z_i: MM,
    ) -> KN:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(r=r, z_e=z_e, z_i=z_i)
        return r * z_e / z_i

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 9.13."""
        return LatexFormula(
            return_symbol=r"F_s",
            result=f"{self:.2f}",
            equation=r"R \cdot z_e / z_i",
            numeric_equation=rf"{self.r:.2f} \cdot {self.z_e:.2f} / {self.z_i:.2f}",
            comparison_operator_label="=",
        )
