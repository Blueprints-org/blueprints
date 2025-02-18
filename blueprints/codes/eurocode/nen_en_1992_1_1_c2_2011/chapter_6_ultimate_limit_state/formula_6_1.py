"""Formula 6.1 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN


class Form6Dot1DesignShearStrength(Formula):
    """Class representing formula 6.1 for the design shear strength, VRd."""

    label = "6.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        v_rd_s: KN,
        v_ccd: KN,
        v_td: KN,
    ) -> None:
        r"""[$V_{Rd}$] Design shear resistance of an element with shear reinforcement.

        NEN-EN 1992-1-1+C2:2011 art.6.2.1(2) - Formula (6.1)

        Parameters
        ----------
        v_rd_s : KN
            [$V_{Rd,s}$] Design shear resistance of an element with shear reinforcement [$kN$].
        v_ccd : KN
            [$V_{ccd}$] Design value of the shear force component in the compression area in case of a change in height [$kN$].
        v_td : KN
            [$V_{td}$] Design value of the shear force component of the tensile force in the reinforcement in case of a change in height [$kN$].
        """
        super().__init__()
        self.v_rd_s = v_rd_s
        self.v_ccd = v_ccd
        self.v_td = v_td

    @staticmethod
    def _evaluate(
        v_rd_s: KN,
        v_ccd: KN,
        v_td: KN,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        if v_rd_s < 0:
            raise ValueError(f"Negative v_rd_s: {v_rd_s}. v_rd_s cannot be negative")
        if v_ccd < 0:
            raise ValueError(f"Negative v_ccd: {v_ccd}. v_ccd cannot be negative")
        if v_td < 0:
            raise ValueError(f"Negative v_td: {v_td}. v_td cannot be negative")
        return v_rd_s + v_ccd + v_td

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.1."""
        return LatexFormula(
            return_symbol=r"V_{Rd}",
            result=f"{self:.3f}",
            equation=r"V_{Rd,s} + V_{ccd} + V_{td}",
            numeric_equation=rf"{self.v_rd_s:.3f} + {self.v_ccd:.3f} + {self.v_td:.3f}",
            comparison_operator_label="=",
        )
