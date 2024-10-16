"""Tests for the LatexFormula class."""

import pytest

from blueprints.codes.latex_formula import LatexFormula, latex_fraction, latex_max_curly_brackets, latex_min_curly_brackets, latex_replace_symbols


@pytest.fixture
def fixture_latex_formula() -> LatexFormula:
    """Fixture for testing."""
    return LatexFormula(
        return_symbol="E",
        result="500",
        equation="mc^2",
        numeric_equation="5*10^2",
        comparison_operator_label="=",
    )


class TestLatexFormula:
    """Test for LatexFormula."""

    def test_short(self, fixture_latex_formula: LatexFormula) -> None:
        """Test the short representation."""
        # Expected result
        expected_result = "E = 500"

        assert fixture_latex_formula.short == expected_result

    def test_complete(self, fixture_latex_formula: LatexFormula) -> None:
        """Test the complete representation."""
        # Expected result
        expected_result = "E = mc^2 = 5*10^2 = 500"
        assert fixture_latex_formula.complete == expected_result

    def test_str(self, fixture_latex_formula: LatexFormula) -> None:
        """Test the string representation."""
        # Expected result
        expected_result = "E = mc^2 = 5*10^2 = 500"
        assert str(fixture_latex_formula) == expected_result


def test_latex_fraction() -> None:
    """Test the latex_fraction function."""
    # Example values
    numerator = 5.0
    denominator = 10.0

    # Expected result
    expected_result = r"\frac{5.0}{10.0}"

    assert latex_fraction(numerator=numerator, denominator=denominator) == expected_result


def test_latex_max_curly_brackets() -> None:
    """Test the latex_max_curly_brackets function."""
    result = latex_max_curly_brackets(r"a+b", r"500", r"c-d")
    assert result == r"\max \left\{a+b; 500; c-d\right\}"


def test_latex_min_curly_brackets() -> None:
    """Test the latex_max_curly_brackets function."""
    result = latex_min_curly_brackets(r"a+b", r"500", r"c-d")
    assert result == r"\min \left\{a+b; 500; c-d\right\}"


# Success tests using pytest
@pytest.mark.parametrize("latex_template, replacements, unique_check, expected", [
    (r"\frac{A}{B}", {'A': 'x', 'B': 'y'}, True, r"\frac{x}{y}"),
    (r"\frac{A}{B}", {'A': 'x', 'B': 'y'}, False, r"\frac{x}{y}"),
    (r"\frac{A}{B}", {'A': 'x', 'B': 'y'}, False, r"\frac{x}{y}"),
    (r"\frac{A}{B}", {'A': 'x', 'B': 'y'}, False, r"\frac{x}{y}"),
    (
        r"\frac{k_{mod}}{\gamma_{R}}", 
        {'k_{mod}': '0.9', r'\gamma_{R}': '1.2'},
        False,
        r"\frac{0.9}{1.2}", 
    ),
])
def test_latex_replace_symbols_success(latex_template, replacements, unique_check, expected):
    """Test successful symbol replacements in LaTeX strings."""
    result = latex_replace_symbols(latex_template, replacements, unique_check)
    assert result == expected

# Error tests using pytest
@pytest.mark.parametrize("latex_template, replacements, unique_check, expected_exception", [
    (r"\frac{A}{B}", {'C': 'x'}, True, "Symbol 'C' not found in the template."),
    (r"\frac{A}{A}", {'A': 'x'}, True, "Symbol 'A' found multiple times in the template."),
])
def test_latex_replace_symbols_error(
    latex_template,
    replacements,
    unique_check,
    expected_exception
):
    """Test error conditions when replacing symbols in LaTeX strings."""
    with pytest.raises(ValueError, match=expected_exception):
        latex_replace_symbols(latex_template, replacements, unique_check)
