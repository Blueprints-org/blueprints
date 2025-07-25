"""Formula 6.48 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_negative


class Form6Dot48NetAppliedPunchingForce(Formula):
    r"""Class representing formula 6.48 for the calculation of net applied punching force [$V_{Ed,red}$] of slabs and column
    bases without shear reinforcement.
    """

    label = "6.48"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        v_ed: N,
        delta_v_ed: N,
    ) -> None:
        r"""[$V_{Ed,red}$] Calculation of net applied punching force of slabs and column bases without shear reinforcement.

        EN 1992-1-1:2004 art.6.4.4(2) - Formula (6.48)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Applied shear force [$N$].
        delta_v_ed : N
            [$\Delta V_{Ed}$] Net upward force within the control perimeter considered [$N$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.delta_v_ed = delta_v_ed

    @staticmethod
    def _evaluate(
        v_ed: N,
        delta_v_ed: N,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed=v_ed, delta_v_ed=delta_v_ed)

        return v_ed - delta_v_ed

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.48."""
        _equation: str = r"V_{Ed} - \Delta V_{Ed}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\Delta V_{Ed}": f"{self.delta_v_ed:.{n}f}",
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"V_{Ed,red}",
            result=f"{self._evaluate(self.v_ed, self.delta_v_ed):.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
