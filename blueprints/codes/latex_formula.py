"""Latex formula representation."""
from dataclasses import dataclass


def value_to_latex_text(value: str | float) -> str:
    r"""Convert value to a latex text string (\text{variable}).

    Parameters
    ----------
    value: str | float
        The variable name of the variable to be converted to latex text string.

    Returns
    -------
    str
        The latex text

    """
    return f"\\text{{{value}}}"


def max_curly_brackets_latex(*args: str) -> str:
    """Return a string which will output: max{arg_1, arg_2, ..., arg_N} in latex.

    Parameters
    ----------
    args: str
        The arguments of the max function.

    Returns
    -------
    str
        The latex string

    """
    return f"max \\left\\{{{'; '.join(args)}\\right\\}}"


@dataclass(frozen=True)
class LatexFormula:
    """Latex formula representation.
    Depending on the context this could include the unit, the formula, the result, etc.

    Attributes
    ----------
    return_symbol: str
        The symbol to return
    result: str
        The result of the formula
    equation: str, default ""
        The formula with symbols
    numeric_equation: str, default ""
        The formula with values (numbers)
    comparison_operator_label: str, default "="
        The label for the comparison operators between the return symbol and the result.
        Could be changed for inequalities.
    """

    return_symbol: str
    result: str
    equation: str = ""
    numeric_equation: str = ""
    comparison_operator_label: str = "="

    @property
    def complete(self) -> str:
        """Complete representation of the formula.

        Returns
        -------
        str
            Return symbol = equation = numeric_equation = result

        """
        all_sub_equations = [self.return_symbol, self.equation, self.numeric_equation, self.result]
        return f" {self.comparison_operator_label} ".join([eq for eq in all_sub_equations if eq != ""])

    @property
    def short(self) -> str:
        """Minimal representation of the formula.

        Returns
        -------
        str
            Return symbol = result

        """
        return f"{self.return_symbol} {self.comparison_operator_label} {self.result}"

    def __str__(self) -> str:
        """String representation of the formula."""
        return self.complete
