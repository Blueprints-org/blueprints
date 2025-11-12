"""Formula 5.7 from EN 1993-1-1:2005: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_negative


class Form5Dot7DisregardFrameSwayImperfections(ComparisonFormula):
    r"""Class representing formula 5.7 to check if the sway imperfections of a frame in a building can be disregarded
    or not.
    """

    label = "5.7"
    source_document = EN_1993_1_1_2005

    def __init__(self, h_ed: N, v_ed: N) -> None:
        r"""Check if the sway imperfections in a frame in building can be disregarded.

        EN 1993-1-1:2005 - Formula (5.7)

        Parameters
        ----------
        h_ed: N
            [$H_{Ed}$] Design value of the total horizontal load, transferred from the storey.
            Including equivalent forces according to chapter 5.3.2 (7).
        v_ed: N
            [$V_{Ed}$] Design value of the total vertical load on the frame, transferred from the storey.
        """
        super().__init__()
        self.h_ed = h_ed
        self.v_ed = v_ed

    @staticmethod
    def _evaluate_lhs(h_ed: N, *args, **kwargs) -> float:  # noqa: ARG004
        """Evaluates the left-hand side of the comparison. See __init__ for details."""
        raise_if_negative(h_ed=h_ed)
        return h_ed

    @staticmethod
    def _evaluate_rhs(v_ed: N, *args, **kwargs) -> float:  # noqa: ARG004
        """Evaluates the right-hand side of the comparison. See __init__ for details."""
        raise_if_negative(v_ed=v_ed)
        return 0.15 * v_ed

    @property
    def unity_check(self) -> float:
        """Returns the unity check value."""
        return self.lhs / self.rhs

    @staticmethod
    def _evaluate(h_ed: N, v_ed: N) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        lhs = Form5Dot7DisregardFrameSwayImperfections._evaluate_lhs(h_ed=h_ed)
        rhs = Form5Dot7DisregardFrameSwayImperfections._evaluate_rhs(v_ed=v_ed)
        return lhs >= rhs

    def __bool__(self) -> bool:
        """Allow truth-checking of the check object itself."""
        return self._evaluate(h_ed=self.h_ed, v_ed=self.v_ed)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 5.7."""
        _equation: str = r"H_{Ed} \geq 0.15 \cdot V_{Ed}"
        _numeric_equation: str = latex_replace_symbols(
            _equation, {r"H_{Ed}": f"{self.h_ed:.{n}f}", "V_{Ed}": f"{self.v_ed:.{n}f}"}, unique_symbol_check=False
        )
        return LatexFormula(
            return_symbol="CHECK",
            result=r"OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label=r"\to",
            unit="",
        )
