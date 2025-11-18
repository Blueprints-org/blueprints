"""Formula 5.1 from EN 1993-1-1:2005: Chapter 5 - Structural Analysis."""

from enum import Enum
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N


class AnalysisType(Enum):
    """Enumeration for analysis types."""
    ELASTIC = "elastic analysis"
    PLASTIC = "plastic analysis"


class From5Dot1CriteriumDisregardSecondOrderEffects(ComparisonFormula):
    r"""Class representing formula 5.1 to check whether second order effects of a structure can be disregarded
    or not.
    """

    label = "5.1"
    source_document = EN_1993_1_1_2005

    def __init__(self, f_cr: N, f_ed: N, analysis_type: AnalysisType) -> None:
        r"""Check if second order effects of a structure can be disregarded.

        EN 1993-1-1:2005 - Formula (5.1)

        Parameters
        ----------
        f_cr: N
            [$F_{cr}$] Elastic critical buckling load for global instability mode based on initial elastic stiffness.
        f_ed: N
            [$F_{Ed}$] Design loading on the structure.
        analysis_type: AnalysisType
            [$\text{analysis type}$] Type of analysis being performed (elastic or plastic).
        """
        super().__init__()
        self.f_cr = f_cr
        self.f_ed = f_ed
        self.analysis_type = analysis_type

    _analysis_type_map = {
        AnalysisType.ELASTIC: 10, AnalysisType.PLASTIC: 15}

    @staticmethod
    def _evaluate_lhs(f_cr: N, f_ed: N, *args, **kwargs) -> float:
        """Evaluates the left-hand side of the comparison. See __init__ for details."""
        return f_cr / f_ed

    @staticmethod
    def _evaluate_rhs(analysis_type: AnalysisType, *args, **kwargs) -> float:
        """Evaluates the right-hand side of the comparison. See __init__ for details."""
        if not isinstance(analysis_type, AnalysisType):
            raise ValueError("analysis_type must be an instance of AnalysisType Enum.")
        return From5Dot1CriteriumDisregardSecondOrderEffects._analysis_type_map[analysis_type]

    @property
    def unity_check(self) -> float:
        """Returns the unity check value."""
        return self.rhs / self.lhs

    @staticmethod
    def _evaluate(f_cr: N, f_ed: N, analysis_type: AnalysisType) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        lhs = From5Dot1CriteriumDisregardSecondOrderEffects._evaluate_lhs(f_cr=f_cr, f_ed=f_ed)
        rhs = From5Dot1CriteriumDisregardSecondOrderEffects._evaluate_rhs(analysis_type=analysis_type)
        return lhs >= rhs

    def __bool__(self) -> bool:
        """Allow truth-checking of the check object itself."""
        return self._evaluate(f_cr=self.f_cr, f_ed=self.f_ed, analysis_type=self.analysis_type)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 5.1."""
        _equation: str = r"\alpha_{cr} = \frac{F_{cr}}{F_{Ed}} \ge limit"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_{cr}": f"{(self.f_cr / self.f_ed):.{n}f}",
                "F_{cr}": f"{self.f_cr:.{n}f}",
                "F_{Ed}": f"{self.f_ed:.{n}f}",
                "limit": f"{From5Dot1CriteriumDisregardSecondOrderEffects._analysis_type_map[self.analysis_type]:d}"},
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
