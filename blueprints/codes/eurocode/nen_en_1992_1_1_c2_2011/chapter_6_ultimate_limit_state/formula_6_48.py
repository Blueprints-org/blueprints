"""Formula 6.48 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_negative


class Form6Dot48NetAppliedPunchingForce(Formula):
    r"""Class representing formula 6.48 for the calculation of net applied punching force [$V_{Ed,red}$] of slabs and column
    bases without shear reinforcement.
    """

    label = "6.48"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        v_ed: N,
        delta_v_ed: N,
    ) -> None:
        r"""[$V_{Ed,red}$] Calculation of net applied punching force of slabs and column bases without shear reinforcement.

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(2) - Formula (6.48)

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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.48."""
        _equation: str = r"V_{Ed} - \Delta V_{Ed}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\Delta V_{Ed}": f"{self.delta_v_ed:.3f}",
                r"V_{Ed}": f"{self.v_ed:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"V_{Ed,red}",
            result=f"{self._evaluate(self.v_ed, self.delta_v_ed):.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
