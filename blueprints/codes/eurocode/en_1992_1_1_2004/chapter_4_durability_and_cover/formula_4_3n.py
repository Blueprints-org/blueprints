"""Formula 4.3N from EN 1992-1-1:2004: Chapter 4 - Durability and cover to reinforcement."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form4Dot3nCheckExecutionTolerances(Formula):
    r"""Class representing formula 4.3N for calculating the allowance in design for execution tolerances [$\Delta c_{dev}$] [$mm$].

    EN 1992-1-1:2004 art.4.4.1.3 (3) - formula (4.3N)

    Parameters
    ----------
    delta_cdev : MM
        [$\Delta c_{dev}$] Concrete cover including execution tolerances [$mm$].
    """

    label = "4.3N"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        delta_cdev: MM,
    ) -> None:
        super().__init__()
        self.delta_cdev = delta_cdev

    @staticmethod
    def _evaluate(
        delta_cdev: MM,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(delta_cdev=delta_cdev)

        return 5 <= delta_cdev <= 10

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 4.3N."""
        _equation: str = r"5 \leq \Delta c_{dev} \leq 10"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\Delta c_{dev}": f"{self.delta_cdev:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
