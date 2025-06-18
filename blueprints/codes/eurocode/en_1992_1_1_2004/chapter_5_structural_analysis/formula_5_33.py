"""Formula 5.33 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN, M
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot33NominalSecondOrderMoment(Formula):
    """Class representing formula 5.33 for the calculation of the nominal 2nd order moment, [$M_{2}$]."""

    label = "5.33"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        n_ed: KN,
        curvature: DIMENSIONLESS,
        l_o: M,
        c: DIMENSIONLESS,
    ) -> None:
        r"""[$M_{2}$] Nominal 2nd order moment [$kNm$].

        EN 1992-1-1:2004 art.5.8.8.2 - Formula (5.33)

        Parameters
        ----------
        n_ed : KN
            [$N_{Ed}$] Design value of axial force [$kN$].
        curvature : DIMENSIONLESS
            [$\frac{1}{r}$] Curvature (1/r), see 5.8.8.3 [$1/m$].
        l_o : M
            [$l_{o}$] Effective length, see 5.8.3.2 [$m$].
        c : DIMENSIONLESS
            [$c$] Factor depending on the curvature distribution, see 5.8.8.2 (4). [-].
        """
        super().__init__()
        self.n_ed = n_ed
        self.curvature = curvature
        self.l_o = l_o
        self.c = c

    @staticmethod
    def _evaluate(
        n_ed: KN,
        curvature: float,
        l_o: M,
        c: float,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_ed=n_ed, curvature=curvature, l_o=l_o, c=c)

        return n_ed * curvature * (l_o**2) / c

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.33."""
        return LatexFormula(
            return_symbol=r"M_{2}",
            result=f"{self:.{n}f}",
            equation=r"N_{Ed} \cdot \left(\frac{1}{r}\right) \cdot \frac{l_{o}^2}{c}",
            numeric_equation=rf"{self.n_ed:.{n}f} \cdot \left({self.curvature:.{n}f}\right) " rf"\cdot \frac{{{self.l_o:.{n}f}^2}}{{{self.c:.{n}f}}}",
            comparison_operator_label="=",
            unit="kNm",
        )
