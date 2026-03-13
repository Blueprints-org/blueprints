"""Formula 5.9 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, M
from blueprints.validations import raise_if_negative


class Form5Dot9DesignSupportMomentReduction(Formula):
    """Class representing formula 5.9 for the calculation of the design support moment reduction, [$ΔM_{Ed}$].
    See Figure 5.4 b.
    """

    label = "5.9"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_ed_sup: KN,
        t: M,
    ) -> None:
        r"""[$ΔM_{Ed}$] Design support moment reduction [$kN$].

        Note: Regardless of the method of analysis used, where a beam or slab is continuous over a
        support which may be considered to provide no restraint to rotation (e.g. over walls), the design
        support moment, calculated on the basis of a span equal to the centre-to-centre distance
        between supports, may be reduced by an amount [$ΔM_{Ed}$].

        EN 1992-1-1:2004 art.5.3.2.2(4) - Formula (5.9)

        Parameters
        ----------
        f_ed_sup : KN
            [$F_{Ed,sup}$] Design support reaction [$kN$].
        t : M
            [$t$] breadth of the support (see Figure 5.4 b) [$m$].

            Note:  Where support bearings are used [$t$] should be taken as the bearing width.
        """
        super().__init__()
        self.f_ed_sup = f_ed_sup
        self.t = t

    @staticmethod
    def _evaluate(
        f_ed_sup: KN,
        t: M,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            f_ed_sup=f_ed_sup,
            t=t,
        )
        return f_ed_sup * t / 8

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.9."""
        return LatexFormula(
            return_symbol=r"ΔM_{Ed}",
            result=f"{self:.{n}f}",
            equation=r"\frac{F_{Ed,sup} \cdot t}{8}",
            numeric_equation=rf"\frac{{{self.f_ed_sup} \cdot {self.t}}}{{8}}",
            comparison_operator_label="=",
        )
