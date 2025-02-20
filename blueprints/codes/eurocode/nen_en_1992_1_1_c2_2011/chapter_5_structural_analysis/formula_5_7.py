"""Formula 5.7 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import M
from blueprints.validations import raise_if_negative


class Form5Dot7EffectiveFlangeWidth(Formula):
    """Class representing formula 5.7 for the calculation of effective flange width [$b_{eff}$] for a T beam or L beam.
    See Figure 5.3.
    """

    label = "5.7"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        *b_eff_i: M,
        b_w: M,
        b: M,
    ) -> None:
        r"""[$b_{eff}$] Effective flange width for a T beam or L beam [$m$].

        NEN-EN 1992-1-1+C2:2011 art.5.3.2.1(3) - Formula (5.7)

        Parameters
        ----------
        b_eff_i : M
            [$b_{eff,i}$] Effective flange width of the i-th flange [$m$].
        b_w : M
            [$b_{w}$] Width of the web [$m$].
        b : M
            [$b$] Total width of the flange [$m$].

        Notes
        -----
        where [$b_{eff,i}$] is the effective flange width of the i-th flange
        """
        super().__init__()
        self.b_eff_i = b_eff_i
        self.b_w = b_w
        self.b = b

    @staticmethod
    def _evaluate(
        *b_eff_i: M,
        b_w: M,
        b: M,
    ) -> M:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            **{f"b_eff_{i}": b_eff for i, b_eff in enumerate(b_eff_i)},
            b_w=b_w,
            b=b,
        )
        return min(sum(b_eff_i) + b_w, b)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.7."""
        return LatexFormula(
            return_symbol=r"b_{eff}",
            result=f"{self:.3f}",
            equation=r"\sum b_{eff,i}+b_w\le b",
            numeric_equation=rf"\sum ({'+'.join(str(b_eff) for b_eff in self.b_eff_i)})+{self.b_w}\le {self.b}",
            comparison_operator_label="=",
        )
