"""Formula 5.10 from EN 1993-5:2007 Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1993_5_2007 import EN_1993_5_2007
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot10ReductionFactorShearArea(Formula):
    """Class representing formula 5.10 for reduction factor for shear area."""

    label = "5.10"
    source_document = EN_1993_5_2007

    def __init__(
        self,
        v_ed: KN,
        v_pl_rd: KN,
    ) -> None:
        r"""[$\rho$] Calculate the reduction factor for shear area of the cross-section [$-$].

        EN 1993-5:2007(E) art.5.2.2(9) - Formula (5.10)

        Parameters
        ----------
        v_ed : KN
            [$V_{Ed}$] Design shear force in [$kN$].
        v_pl_rd : KN
            [$V_{pl,Rd}$] Plastic shear resistance in [$kN$].
        """
        super().__init__()
        self.v_ed: KN = v_ed
        self.v_pl_rd: KN = v_pl_rd

    @staticmethod
    def _evaluate(
        v_ed: KN,
        v_pl_rd: KN,
    ) -> DIMENSIONLESS:
        """Evaluates the formula for reduction factor for shear area."""
        raise_if_less_or_equal_to_zero(v_ed=v_ed, v_pl_rd=v_pl_rd)
        return (2 * v_ed / v_pl_rd - 1) ** 2

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 5.10."""
        return LatexFormula(
            return_symbol=r"\rho",
            result=f"{self:.{n}f}",
            equation=r"\left(2 \cdot \frac{V_{Ed}}{V_{pl,Rd}} - 1\right)^2",
            numeric_equation=rf"\left(2 \cdot \frac{{{self.v_ed}}}{{{self.v_pl_rd}}} - 1\right)^2",
            comparison_operator_label="=",
        )
