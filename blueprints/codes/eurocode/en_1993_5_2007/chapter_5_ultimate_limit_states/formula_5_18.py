"""Formula 5.18 from EN 1993-5:2007: Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1993_5_2007 import EN_1993_5_2007
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot18CompressionCheckUProfilesClass1And2(ComparisonFormula):
    r"""Class representing formula 5.18 for U-profiles of class 1 and 2: [$\frac{N_{Ed}}{N_{pl,Rd}} \leq 0.25$]."""

    label = "5.18"
    source_document = EN_1993_5_2007

    def __init__(
        self,
        n_ed: KN,
        n_pl_rd: KN,
    ) -> None:
        r"""Compression check for U-profiles of class 1 and 2.
        Design axial force [$N_{Ed}$] should not exceed 25% of plastic resistance [$N_{pl,Rd}$].

        EN 1993-5:2007 art. 5.2.3 (10) - Formula (5.18)

        Parameters
        ----------
        n_ed : KN
            [$N_{Ed}$] Design value of the compression force [$kN$].
        n_pl_rd : KN
            [$N_{pl,Rd}$] Plastic design resistance of the cross-section [$kN$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_pl_rd = n_pl_rd

    @staticmethod
    def _evaluate_lhs(
        n_ed: KN,
        n_pl_rd: KN,
    ) -> float:
        """Evaluates the left-hand side of the comparison; see __init__ for details."""
        raise_if_less_or_equal_to_zero(n_pl_rd=n_pl_rd)
        return n_ed / n_pl_rd

    @staticmethod
    def _evaluate_rhs(*_, **_kwargs) -> float:
        """Evaluates the right-hand side of the comparison; see __init__ for details."""
        return 0.25

    @staticmethod
    def _evaluate(
        n_ed: KN,
        n_pl_rd: KN,
    ) -> bool:
        """Evaluates the comparison; see __init__ for details."""
        return (
            Form5Dot18CompressionCheckUProfilesClass1And2._evaluate_lhs(n_ed=n_ed, n_pl_rd=n_pl_rd)
            <= Form5Dot18CompressionCheckUProfilesClass1And2._evaluate_rhs()
        )

    @property
    def unity_check(self) -> float:
        """Returns the unity check value."""
        return self.lhs

    def __bool__(self) -> bool:
        """Allow truth-checking of the check object itself."""
        return self._evaluate(self.n_ed, self.n_pl_rd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.18."""
        _equation: str = r"\frac{N_{Ed}}{N_{pl,Rd}} \leq 0.25"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"N_{pl,Rd}": f"{self.n_pl_rd:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if bool(self) else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label=r"\to",
            unit="",
        )
