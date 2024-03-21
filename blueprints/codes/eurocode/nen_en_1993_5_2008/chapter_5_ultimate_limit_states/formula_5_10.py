"""Formula 5.10 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot10ReductionFactorShear(Formula):
    """Class representing formula 5.10 for reduction factor for shear resistance of the cross-section."""

    label = "5.10"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        v_ed: KN,  # Design shear force
        v_pl_rd: KN,  # Plastic shear resistance
    ) -> None:
        """[ρ] Calculate the reduction factor for shear resistance of the cross-section based on formula 5.10 from NEN-EN 1993-5:2007(E) art.
        5.2.2(9).

        Parameters
        ----------
        v_ed : KN
            [VEd] Design shear force in [kN/m].
        v_pl_rd : KN
            [Vpl,rd] Plastic shear resistance in [kN/m].
        """
        super().__init__()
        self.v_ed: float = v_ed
        self.v_pl_rd: float = v_pl_rd

    @staticmethod
    def _evaluate(
        v_ed: KN,
        v_pl_rd: KN,
    ) -> DIMENSIONLESS:
        """Evaluates the formula for reduction factor for shear resistance."""
        raise_if_less_or_equal_to_zero(v_ed=v_ed, v_pl_rd=v_pl_rd)
        return (2 * v_ed / v_pl_rd - 1) ** 2

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.10."""
        return LatexFormula(
            return_symbol=r"\rho",
            result=str(self),
            equation=r"\left(2 \cdot \frac{V_{Ed}}{V_{pl,Rd}} - 1\right)^2",
            numeric_equation=rf"\left(2 \cdot \frac{{{self.v_ed}}}{{{self.v_pl_rd}}} - 1\right)^2",
            comparison_operator_label="=",
        )
