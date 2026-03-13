"""Formula 5.36 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot36RelativeAxialForce(Formula):
    r"""Class representing formula 5.36 for the calculation of the relative axial force, [$K_{r}$]."""

    label = "5.36"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        n_ed: KN,
        ac: MM2,
        fcd: MPA,
        as_: MM2,
        fyd: MPA,
        n_bal: DIMENSIONLESS,
    ) -> None:
        r"""[$K_{r}$] Relative axial force [-].

        EN 1992-1-1:2004 art.5.8.8.3(3) - Formula (5.36)

        Parameters
        ----------
        n_ed : KN
            [$N_{Ed}$] Design value of axial load [$kN$].
        ac : MM2
            [$A_{c}$] Area of concrete cross section [$mm^2$].
        fcd : MPA
            [$f_{cd}$] Design value of concrete compressive strength [$MPa$].
        as_ : MM2
            [$A_{s}$] Total area of reinforcement [$mm^2$].
        fyd : MPA
            [$f_{yd}$] Design yield strength of reinforcement [$MPa$].
        n_bal : DIMENSIONLESS
            [$n_{bal}$] Value of n at maximum moment resistance, 0.4 may be used [-].
        """
        super().__init__()
        self.n_ed = n_ed
        self.ac = ac
        self.fcd = fcd
        self.as_ = as_
        self.fyd = fyd
        self.n_bal = n_bal

    @staticmethod
    def _evaluate(
        n_ed: KN,
        ac: MM2,
        fcd: MPA,
        as_: MM2,
        fyd: MPA,
        n_bal: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(n_ed=n_ed, as_=as_, fyd=fyd, n_bal=n_bal)
        raise_if_less_or_equal_to_zero(ac=ac, fcd=fcd)

        omega = as_ * fyd / (ac * fcd)
        nu = 1 + omega
        n = n_ed / (ac * fcd)
        return min((nu - n) / (nu - n_bal), 1)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.36."""
        return LatexFormula(
            return_symbol=r"K_{r}",
            result=f"{self:.{n}f}",
            equation=r"\min\left(\frac{\left(1 + \frac{A_{s} \cdot f_{yd}}{A_{c} \cdot f_{cd}}\right) - "
            r"\frac{N_{Ed}}{A_{c} \cdot f_{cd}}}{\left(1 + \frac{A_{s} \cdot f_{yd}}{A_{c} \cdot f_{cd}}\right) - n_{bal}}, 1\right)",
            numeric_equation=rf"\min\left(\frac{{\left(1 + \frac{{{self.as_:.{n}f} \cdot {self.fyd:.{n}f}}}{{{self.ac:.{n}f} \cdot "
            rf"{self.fcd:.{n}f}}}\right) - \frac{{{self.n_ed:.{n}f}}}{{{self.ac:.{n}f}"
            rf" \cdot {self.fcd:.{n}f}}}}}{{\left(1 + \frac{{{self.as_:.{n}f} \cdot "
            rf"{self.fyd:.{n}f}}}{{{self.ac:.{n}f} \cdot {self.fcd:.{n}f}}}\right) - {self.n_bal:.{n}f}}}, 1\right)",
            comparison_operator_label="=",
            unit="-",
        )
