"""Formula 5.19 from NEN-EN 1993-5:2008: Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_5_2008 import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import KN
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot19CompressionCheckClass3Profiles(Formula):
    r"""Class representing formula 5.19 for class 3 profiles: [$\frac{N_{Ed}}{N_{pl,Rd}} \leq 0.1$]."""

    label = "5.19"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        n_ed: KN,
        n_pl_rd: KN,
    ) -> None:
        r"""Compression check for class 3 profiles: design axial force [$N_{Ed}$] should not exceed 10% of plastic resistance [$N_{pl,Rd}$].

        NEN-EN 1993-5:2008 art. 5.2.3 (10) - Formula (5.19)

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
    def _evaluate(
        n_ed: KN,
        n_pl_rd: KN,
    ) -> bool:
        """Evaluates the comparison; see __init__ for details."""
        raise_if_negative(n_ed=n_ed)
        raise_if_less_or_equal_to_zero(n_pl_rd=n_pl_rd)
        return (n_ed / n_pl_rd) <= 0.1

    def __bool__(self) -> bool:
        """Allow truth-checking of the check object itself."""
        return self._evaluate(self.n_ed, self.n_pl_rd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.19."""
        _equation: str = r"\frac{N_{Ed}}{N_{pl,Rd}} \leq 0.1"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.3f}",
                r"N_{pl,Rd}": f"{self.n_pl_rd:.3f}",
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
