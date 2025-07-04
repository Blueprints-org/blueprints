"""Formula 3.16 from EN 1992-1-1:2004: Chapter 3 - Materials."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class Form3Dot16DesignValueTensileStrength(Formula):
    """Class representing formula 3.16 for the calculation of the concrete tensile strength design value."""

    label = "3.16"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        alpha_ct: DIMENSIONLESS,
        f_ctk_0_05: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> None:
        r"""[$f_{cd}$] Design value concrete tensile strength [$MPa$].

        EN 1992-1-1:2004 art.3.1.6(2) - Formula (3.16)

        Parameters
        ----------
        alpha_ct : DIMENSIONLESS
            [$\alpha_{ct}$] Coefficient taking long term effects on tensile strength into
            account and unfavorable effect due to positioning loading [$-$]
            See national appendix. Recommended value: 1.0
        f_ctk_0_05 : MPA
            [$f_{ctk,0.05}$] Characteristic tensile strength 5% [$MPa$].
        gamma_c : DIMENSIONLESS
            [$\gamma_{c}$] Partial safety factor concrete, see 2.4.2.4 [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.alpha_ct = alpha_ct
        self.f_ctk_0_05 = f_ctk_0_05
        self.gamma_c = gamma_c

    @staticmethod
    def _evaluate(
        alpha_ct: DIMENSIONLESS,
        f_ctk_0_05: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if alpha_ct < 0:
            raise ValueError(f"Invalid alpha_ct: {alpha_ct}. alpha_ct cannot be negative")
        if f_ctk_0_05 < 0:
            raise ValueError(f"Invalid f_ctk_0_05: {f_ctk_0_05}. f_ctk_0_05 cannot be negative")
        if gamma_c <= 0:
            raise ValueError(f"Invalid gamma_c: {gamma_c}. gamma_c cannot be negative or zero")
        return alpha_ct * f_ctk_0_05 / gamma_c

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 3.16."""
        return LatexFormula(
            return_symbol=r"f_{ctd}",
            result=f"{self:.{n}f}",
            equation=r"\alpha_{ct} \cdot f_{ctk,0.05} / \gamma_C",
            numeric_equation=rf"{self.alpha_ct:.{n}f} \cdot {self.f_ctk_0_05:.{n}f} / {self.gamma_c:.{n}f}",
            comparison_operator_label="=",
        )
