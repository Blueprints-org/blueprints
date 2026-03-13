"""Formula 6.23 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form6Dot23CheckShearStressInterface(Formula):
    r"""Class representing formula 6.23 for checking the shear stress at the interface between concrete cast."""

    label = "6.23"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        v_edi: MPA,
        v_rdi: MPA,
    ) -> None:
        r"""Check the shear stress at the interface between concrete cast.

        EN 1992-1-1:2004 art.6.2.5(1) - Formula (6.23)

        Parameters
        ----------
        v_edi : MPA
            [$v_{Edi}$] Design value of the shear stress at the interface [$MPa$].
        v_rdi : MPA
            [$v_{Rdi}$] Design shear strength of the interface [$MPa$].
        """
        super().__init__()
        self.v_edi = v_edi
        self.v_rdi = v_rdi

    @staticmethod
    def _evaluate(
        v_edi: MPA,
        v_rdi: MPA,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(v_edi=v_edi, v_rdi=v_rdi)

        return v_edi <= v_rdi

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.23."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"v_{Edi} \leq v_{Rdi}",
            numeric_equation=rf"{self.v_edi:.{n}f} \leq {self.v_rdi:.{n}f}",
            comparison_operator_label="\\to",
            unit="",
        )
