"""Formula 2.2 from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

from blueprints.codes.eurocode.nen_9997_1_c2_2017 import NEN_9997_1_C2_2017
from blueprints.codes.latex_formula import LatexFormula
from blueprints.validations import raise_if_negative


class Form2Dot4DesignValueGeotechnicalParameter:
    """Class representing formula 2.4 for the check of the destabilizing load effect against the stabilizing load effect and friction resistance
    :math:`E_{dst;d} ≤ E_{stb;d} + T_d`.
    """

    label = "2.4"
    source_document = NEN_9997_1_C2_2017

    def __init__(self, e_dst_d: float, e_stb_d: float, t_d: float) -> None:
        """Check of the destabilizing load effect against the stabilizing load effect and friction resistance :math:`E_{dst;d} ≤ E_{stb;d} +
        T_d`.

        NEN 9997-1+C2:2017 art.2.4.7.2(1) - Formula (2.4)

        Parameters
        ----------
        e_dst_d : float
            [:math:`E_{dst;d}`] Design value of destabilizing load effect.
        e_stb_d : float
            [:math:`E_{dst;d}`] Design value of stabilizing load effect.
        t_d : float
            [:math: `T_d`] Design value of friction resistance.
        """
        self.e_dst_d = e_dst_d
        self.e_stb_d = e_stb_d
        self.t_d = t_d

    def __bool__(self) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(e_dst_d=self.e_dst_d, e_stb_d=self.e_stb_d)
        return self.e_dst_d <= self.e_stb_d + self.t_d

    def __str__(self) -> str:
        """Returns a string representation of the formula."""
        return self.latex().complete

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 2.4."""
        return LatexFormula(
            return_symbol="",
            equation="E_{dst;d} \\leq E_{stb;d} + T_d",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            numeric_equation=f"{self.e_dst_d:.2f} \\leq {self.e_stb_d:.2f} + {self.t_d:.2f}  \\to {self.e_dst_d:.2f} \\leq "
            f"{self.e_stb_d + self.t_d:.2f}",
            comparison_operator_label="\\to",
        )
