"""Tests for the LatexFormula class."""

import pytest

from blueprints.codes.latex_formula import LatexFormula, latex_fraction, latex_max_curly_brackets, latex_min_curly_brackets, latex_scientific


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


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (2e6, r"2.0 \cdot 10^{6}"),
        (7.5e5, r"7.5 \cdot 10^{5}"),
        (1e-3, r"1.0 \cdot 10^{-3}"),
    ],
)
def test_latex_scientific(value: float, expected: str) -> None:
    """Test the latex_scientific function."""
    assert latex_scientific(value) == expected
