"""Formula 5.36 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot36RelativeAxialForce(Formula):
    r"""Class representing formula 5.36 for the calculation of the relative axial force, [$K_{r}$]."""

    label = "5.36"
    source_document = NEN_EN_1992_1_1_C2_2011

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

        NEN-EN 1992-1-1+C2:2011 art.5.8.8.3(3) - Formula (5.36)

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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.36."""
        return LatexFormula(
            return_symbol=r"K_{r}",
            result=f"{self:.3f}",
            equation=r"\min\left(\frac{\left(1 + \frac{A_{s} \cdot f_{yd}}{A_{c} \cdot f_{cd}}\right) - "
            r"\frac{N_{Ed}}{A_{c} \cdot f_{cd}}}{\left(1 + \frac{A_{s} \cdot f_{yd}}{A_{c} \cdot f_{cd}}\right) - n_{bal}}, 1\right)",
            numeric_equation=rf"\min\left(\frac{{\left(1 + \frac{{{self.as_:.3f} \cdot {self.fyd:.3f}}}{{{self.ac:.3f} \cdot "
            rf"{self.fcd:.3f}}}\right) - \frac{{{self.n_ed:.3f}}}{{{self.ac:.3f} \cdot {self.fcd:.3f}}}}}{{\left(1 + \frac{{{self.as_:.3f} \cdot "
            rf"{self.fyd:.3f}}}{{{self.ac:.3f} \cdot {self.fcd:.3f}}}\right) - {self.n_bal:.3f}}}, 1\right)",
            comparison_operator_label="=",
            unit="-",
        )
