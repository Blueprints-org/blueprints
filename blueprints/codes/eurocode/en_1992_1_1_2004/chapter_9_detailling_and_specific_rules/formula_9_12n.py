"""Formula 9.12N from EN 1992-1-1:2004: Chapter 9 - Detailling and specific rules."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, MM2, MPA
from blueprints.unit_conversion import KN_TO_N
from blueprints.validations import raise_if_negative


class Form9Dot12nMinimumLongitudinalReinforcementColumns(Formula):
    """Class representing the formula 9.12N for the calculation of the minimum longitudinal reinforcement for columns."""

    label = "9.12N"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        n_ed: KN,
        f_yd: MPA,
        a_c: MM2,
    ) -> None:
        r"""[$A_{s,min}$] Minimum longitudinal reinforcement for columns [$mm^2$].

        EN 1992-1-1:2004 art.9.5.2(2) - Formula (9.12N)

        Parameters
        ----------
        n_ed: KN
            [$N_{Ed}$] Design value of axial force [$kN$].
        f_yd: MPA
            [$f_{yd}$] Design yield strength reinforcement steel [$MPa$].
        a_c: MM2
            [$A_c$] Concrete cross-sectional area [$mm^2$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.f_yd = f_yd
        self.a_c = a_c

    @staticmethod
    def _evaluate(
        n_ed: KN,
        f_yd: MPA,
        a_c: MM2,
    ) -> MM2:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(n_ed=n_ed, f_yd=f_yd, a_c=a_c)
        return max(0.1 * n_ed * KN_TO_N / f_yd, 0.002 * a_c)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 9.12N."""
        return LatexFormula(
            return_symbol=r"A_{s,min}",
            result=f"{self:.{n}f}",
            equation=r"\max( \frac{0.10 \cdot N_{Ed}}{f_{yd}}, 0.002 \cdot A_c )",
            numeric_equation=rf"\max( \frac{{0.10 \cdot {self.n_ed:.{n}f}}}{{{self.f_yd:.{n}f}}}, 0.002 \cdot {self.a_c:.{n}f} )",
            comparison_operator_label="=",
        )
