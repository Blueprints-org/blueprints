"""Latex formula representation."""
from dataclasses import dataclass


def max_curly_brackets(*args: str | float) -> str:
    r"""Return a string which will output: max{arg_1; arg_2; ...; arg_N} in latex and it will also automatically ensure floats are converted to latex
    text.

    Examples
    --------
    >>> max_curly_brackets(1, 2)
    str(\max \left\{1; 2\right\})

    Parameters
    ----------
    args: str
        The arguments of the max function.

    Returns
    -------
    str
        The latex representation of the max function.

    """
    arguments = [str(arg) for arg in args]
    return f"\\max \\left\\{{{'; '.join(arguments)}\\right\\}}"


def min_curly_brackets(*args: str | float) -> str:
    r"""Return a string which will output: min{arg_1; arg_2; ...; arg_N} in latex and it will also automatically ensure floats are converted to latex
    text.

    Examples
    --------
    >>> min_curly_brackets(1, 2)
    str(\min \left\{1; 2\right\})

    Parameters
    ----------
    args: str
        The arguments of the min function.

    Returns
    -------
    str
        The latex representation of the min function.

    """
    arguments = [str(arg) for arg in args]
    return f"\\min \\left\\{{{'; '.join(arguments)}\\right\\}}"


def fraction(numerator: str | float, denominator: str | float) -> str:
    r"""Return a string which will output: \frac{numerator}{denominator} in latex.

    Examples
    --------
    >>> fraction(1, 2)
    str(\frac{1}{2})

    Parameters
    ----------
    numerator: str | float
        The numerator of the fraction.
    denominator: str | float
        The denominator of the fraction.

    Returns
    -------
    str
        The latex string

    """
    return f"\\frac{{{numerator}}}{{{denominator}}}"


def conditional(*args: list[float | str]) -> str:
    r"""Return a string which will output a conditional statement with curly brackets with the given arguments and conditions in latex.

    Examples
    --------
    >>> conditional([1, "a > 0"], [2, "a < 0"]
    str(\left{\matrix{1 & \text{voor }a > 0 \\ 2 & \text{voor }a < 0 }\right.)

    Parameters
    ----------
    args: list[float|str]
        A list of length 2, where the first element is the value and the second value is the condition.

    Returns
    -------
    str
        The latex string
    """
    string_parts = []
    for value, condition in args:
        string_parts.append(f"{value} & \\text{{voor }}{condition} \\\\ ")

    output = r"\left{\matrix{"
    output += "".join(string_parts)
    output = output[:-3]
    return output + r"}\right."


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
