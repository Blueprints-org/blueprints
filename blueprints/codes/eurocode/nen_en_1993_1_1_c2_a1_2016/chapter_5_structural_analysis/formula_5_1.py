"""Formula 5.1 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N


class From5Dot1CriteriumDisregardSecondOrderEffects(ComparisonFormula):
    r"""Class representing formula 5.1 to check whether second order effects of a structure can be disregarded
    or not.
    """

    label = "5.1"
    source_document = EN_1993_1_1_C2_A1_2016

    def __init__(self, f_cr: N, f_ed: N) -> None:
        r"""Check if second order effects of a structure can be disregarded.

        NEN-EN 1993-1-1+C2+A1:2016 - Formula (5.1)

        Parameters
        ----------
        f_cr: N
            [$F_{cr}$] Elastic critical buckling load for global instability mode based on initial elastic stiffness.
        f_ed: N
            [$F_{Ed}$] Design loading on the structure.
        """
        super().__init__()
        self.f_cr = f_cr
        self.f_ed = f_ed

    @staticmethod
    def _evaluate_lhs(f_cr: N, f_ed: N, *args, **kwargs) -> float:
        """Evaluates the left-hand side of the comparison. See __init__ for details."""
        return f_cr / f_ed

    @staticmethod
    def _evaluate_rhs(*args, **kwargs) -> float:
        """Evaluates the right-hand side of the comparison. See __init__ for details."""
        return 10

    @property
    def unity_check(self) -> float:
        """Returns the unity check value."""
        return self.rhs / self.lhs

    @staticmethod
    def _evaluate(f_cr: N, f_ed: N) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        lhs = From5Dot1CriteriumDisregardSecondOrderEffects._evaluate_lhs(f_cr=f_cr, f_ed=f_ed)
        rhs = From5Dot1CriteriumDisregardSecondOrderEffects._evaluate_rhs()
        return lhs >= rhs

    def __bool__(self) -> bool:
        """Allow truth-checking of the check object itself."""
        return self._evaluate(f_cr=self.f_cr, f_ed=self.f_ed)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 5.1."""
        _equation: str = r"\alpha_{cr} = \frac{F_{cr}}{F_{Ed}} \ge 10"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_{cr}": f"{(self.f_cr / self.f_ed):.{n}f}",
                "F_{cr}": f"{self.f_cr:.{n}f}",
                "F_{Ed}": f"{self.f_ed:.{n}f}"},
            unique_symbol_check=False
        )
        return LatexFormula(
            return_symbol="CHECK",
            result=r"OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label=r"\to",
            unit=""
        )
