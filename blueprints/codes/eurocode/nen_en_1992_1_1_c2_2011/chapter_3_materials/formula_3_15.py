"""Formula 3.15 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class Form3Dot15DesignValueCompressiveStrength(Formula):
    """Class representing formula 3.15 for the calculation of the concrete compressive strength design value."""

    label = "3.15"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_cc: DIMENSIONLESS,
        f_ck: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> None:
        r"""[$f_{cd}$] Design value concrete compressive strength [$MPa$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.6(1) - Formula (3.15)

        Parameters
        ----------
        alpha_cc : DIMENSIONLESS
            [$\alpha_{cc}$] Coefficient taking long term effects on compressive strength into
            account and unfavorable effect due to positioning loading [$-$]
            Normally between 0.8 and 1, see national appendix. Recommended value: 1.0
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength [$MPa$].
        gamma_c : DIMENSIONLESS
            [$\gamma_{c}$] Partial safety factor concrete, see 2.4.2.4 [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.alpha_cc = alpha_cc
        self.f_ck = f_ck
        self.gamma_c = gamma_c

    @staticmethod
    def _evaluate(
        alpha_cc: DIMENSIONLESS,
        f_ck: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if alpha_cc < 0:
            raise ValueError(f"Invalid alpha_cc: {alpha_cc}. alpha_cc cannot be negative")
        if f_ck < 0:
            raise ValueError(f"Invalid f_ck: {f_ck}. f_ck cannot be negative")
        if gamma_c <= 0:
            raise ValueError(f"Invalid gamma_c: {gamma_c}. gamma_c cannot be negative or zero")
        return alpha_cc * f_ck / gamma_c

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.15."""
        return LatexFormula(
            return_symbol=r"f_{cd}",
            result=f"{self:.3f}",
            equation=r"\alpha_{cc} \cdot f_{ck} / \gamma_C",
            numeric_equation=rf"{self.alpha_cc:.3f} \cdot {self.f_ck:.3f} / {self.gamma_c:.3f}",
            comparison_operator_label="=",
        )
