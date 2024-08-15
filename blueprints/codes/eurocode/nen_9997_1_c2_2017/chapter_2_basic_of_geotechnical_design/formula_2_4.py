"""Formula 2.2 from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

from blueprints.codes.eurocode.nen_9997_1_c2_2017 import NEN_9997_1_C2_2017
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form2Dot4DesignValueGeotechnicalParameter(Formula):
    """Class representing formula 2.4 for the check of the destabilizing load effect against the stabilizing load effect and friction resistance :math:`E_dst;d leq E_stb;d + T_d`."""

    label = "2.4"
    source_document = NEN_9997_1_C2_2017

    def __init__(self, E_dst_d: float, E_stb_d: float, T_d: float) -> None:
        """Check of the destabilizing load effect against the stabilizing load effect and friction resistance [:math:`E_dst;d leq E_stb;d + T_d`].

        NEN 9997-1+C2:2017 art.2.4.7.2(1) - Formula (2.4)

        Parameters
        ----------
        E_dst_d : float
            [:math:`E_dst;d`] Design value of destabilizing load effect.
        E_stb_d : float
            [:math:`E_dst;d`] Design value of stabilizing load effect.
        T_d : float
            [:math: `T_d`] Design value of friction resistance.
        """
        super().__init__()
        self.E_dst_d = E_dst_d
        self.E_stb_d = E_stb_d
        self.T_d = T_d

    @staticmethod
    def _evaluate(
        E_dst_d: float,
        E_stb_d: float,
        T_d: float
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(E_dst_d=E_dst_d, E_stb_d=E_stb_d, T_d=T_d)
        return E_dst_d <= E_stb_d + T_d

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 2.4."""
        return LatexFormula()
