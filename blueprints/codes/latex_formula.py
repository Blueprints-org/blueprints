"""Latex formula representation."""

from dataclasses import dataclass


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
    numeric_equation_with_units: str, default ""
        The formula with values (numbers) and units
    comparison_operator_label: str, default "="
        The label for the comparison operators between the return symbol and the result.
        Could be changed for inequalities.
    unit: str, default ""
        The unit of the result
    """

    return_symbol: str
    result: str
    equation: str = ""
    numeric_equation: str = ""
    numeric_equation_with_units: str = ""
    comparison_operator_label: str = "="
    unit: str = ""

    @property
    def complete(self) -> str:
        """Complete representation of the formula.

        Returns
        -------
        str
            Return symbol = equation = numeric_equation = result

        """
        all_sub_equations = [self.return_symbol, self.equation, self.numeric_equation, f"{self.result}"]
        long_formula = f" {self.comparison_operator_label} ".join([eq for eq in all_sub_equations if eq != ""])
        return long_formula + rf" \ {self.unit}" if self.unit else long_formula

    @property
    def complete_with_units(self) -> str:
        """Complete representation of the formula with units.

        Returns
        -------
        str
            Return symbol = equation = numeric_equation_with_units = result

        """
        # If numeric_equation_with_units is not provided, use numeric_equation
        numeric_equation_with_units = self.numeric_equation_with_units or self.numeric_equation

        all_sub_equations = [self.return_symbol, self.equation, numeric_equation_with_units, f"{self.result}"]
        long_formula = f" {self.comparison_operator_label} ".join([eq for eq in all_sub_equations if eq != ""])
        return long_formula + rf" \ {self.unit}" if self.unit else long_formula

    @property
    def short(self) -> str:
        """Minimal representation of the formula.

        Returns
        -------
        str
            Return symbol = result

        """
        short_formula = f"{self.return_symbol} {self.comparison_operator_label} {self.result}"
        return short_formula + rf" \ {self.unit}" if self.unit else short_formula

    def __str__(self) -> str:
        """String representation of the formula."""
        return self.complete


def latex_fraction(numerator: str | float, denominator: str | float) -> str:
    r"""Return a string which will output: \frac{numerator}{denominator} in latex.

    Examples
    --------
    >>> latex_fraction(1, 2)
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


def latex_min_curly_brackets(*args: str | float) -> str:
    r"""Return a string which will output: min{arg_1; arg_2; ...; arg_N} in latex.

    It will also automatically ensure floats are converted to latex
    text.

    Examples
    --------
    >>> latex_min_curly_brackets(1, 2)
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


def latex_max_curly_brackets(*args: str | float) -> str:
    r"""Return a string which will output: max{arg_1; arg_2; ...; arg_N} in latex.

    It will also automatically ensure floats are converted to latex
    text.

    Examples
    --------
    >>> latex_max_curly_brackets(1, 2)
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


def latex_replace_symbols(template: str, replacements: dict[str, str], unique_symbol_check: bool = True) -> str:
    r"""
    Replace symbols in a LaTeX template string based on the provided dictionary.

    This function searches the template for symbols specified in the
    replacements and replaces them with their corresponding
    values (and units). It also checks for the occurrence of symbols based on the
    unique_symbol_check parameter, raising an error if necessary.

    Examples
    --------
    >>> latex_template = r"\frac{K_{MOD}}{B}"
    >>> replacements = {"K_{MOD}": "1.0", "B": "y"}
    >>> latex_replace_symbols(latex_template, replacements)
    '\frac{1.0}{y}'

    Parameters
    ----------
    template: str
        The original LaTeX string containing symbols to replace.

    replacements: dict[str, str]
        A dictionary where keys are symbols to be replaced and values
        are their replacements.

    unique_symbol_check: bool, optional
        If True (default), raises an error if a symbol appears more
        than once in the template. If False, multiple occurrences
        will be replaced without error.

    Returns
    -------
    str
        The modified LaTeX string with symbols replaced by values (and units).

    Raises
    ------
    ValueError
        If a symbol in the dictionary is not found in the template,
        or if a symbol appears more than once when unique_symbol_check is True.
    """
    _filled_latex_string: str = template
    for symbol, replacement in replacements.items():
        occurrences = _filled_latex_string.count(symbol)

        # Check for the presence of the symbol in the template
        if occurrences == 0:
            raise ValueError(f"Symbol '{symbol}' not found in the template.")

        # If single_symbol_search is True, check for multiple occurrences
        if unique_symbol_check and occurrences > 1:
            raise ValueError(f"Symbol '{symbol}' found multiple times in the template.")

        # Replace the symbol with its replacement
        _filled_latex_string = _filled_latex_string.replace(symbol, replacement)

    return _filled_latex_string
