"""Latex formula representation."""
from dataclasses import dataclass


def to_text(value: str | float) -> str:
    r"""Convert string to a latex text string (\text{variable}). All characters that are not used as a variable in the corresponding documents
    should be text strings.

    Parameters
    ----------
    value: str | float
        The float, int or string to be converted to latex text string.

    Returns
    -------
    str
        The latex text

    """
    return f"\\text{{{value}}}"


def variable_with_subscript(variable: str, subscript: str) -> str:
    r"""Return a string which will output: variable_{\text{subscript}} in latex.

    Parameters
    ----------
    variable: str
        The variable name.
    subscript: str
        The subscript of the variable.

    Returns
    -------
    str
        The latex representation of the variable with subscript.

    """
    return f"{variable}_{{\\text{{{subscript}}}}}"


def max_curly_brackets(*args: str | float) -> str:
    """Return a string which will output: max{arg_1, arg_2, ..., arg_N} in latex and it will also automatically ensure floats are converted to latex
    text.

    Parameters
    ----------
    args: str
        The arguments of the max function.

    Returns
    -------
    str
        The latex representation of the max operator.

    """
    arguments = []
    for arg in args:
        max_operation_argument = arg
        if isinstance(arg, (int, float)):  # check if arg is float or int, so it can be converted to latex text
            max_operation_argument = to_text(arg)
        arguments.append(str(max_operation_argument))
    return f"\\max \\left\\{{{'; '.join(arguments)}\\right\\}}"


def fraction(numerator: str | float, denominator: str | float) -> str:
    r"""Return a string which will output: \frac{numerator}{denominator} in latex.

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
    if isinstance(numerator, float):
        numerator = to_text(numerator)
    if isinstance(denominator, float):
        denominator = to_text(denominator)
    return f"\\frac{{{numerator}}}{{{denominator}}}"


def conditional(*args: list[float | str]) -> str:
    """Return a string which will output a conditional statement with curly brackets with the given arguments and conditions in latex.

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
        string_value = to_text(value) if isinstance(value, (int, float)) else value
        string_parts.append(f"{string_value} & \\text{{voor }}{condition} \\\\ ")

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
