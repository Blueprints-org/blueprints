"""Formula 5.42 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot42ConcreteCompressiveStress(Formula):
    r"""Class representing formula 5.42 for calculating the maximum concrete compressive stress."""

    label = "5.42"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        sigma_c: MPA,
        f_ck_t: MPA,
    ) -> None:
        r"""Calculate the concrete compressive stress resulting from the prestressing force.

        NEN-EN 1992-1-1+C2:2011 art.5.10.2.2(5) - Formula (5.42)

        Parameters
        ----------
        sigma_c : MPA
            [$\sigma_{c}$] Concrete compressive stress [MPa].
        f_ck_t : MPA
            [$f_{ck}(t)$] Characteristic compressive strength of concrete at time t [MPa].
        """
        super().__init__()
        self.sigma_c = sigma_c
        self.f_ck_t = f_ck_t

    @staticmethod
    def _evaluate(
        sigma_c: MPA,
        f_ck_t: MPA,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(sigma_c=sigma_c, f_ck_t=f_ck_t)

        return sigma_c <= 0.6 * f_ck_t

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.42."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\sigma_{c} \leq 0.6 \cdot f_{ck}(t)",
            numeric_equation=rf"{self.sigma_c:.3f} \leq 0.6 \cdot {self.f_ck_t:.3f}",
            comparison_operator_label="\\to",
            unit="",
        )
