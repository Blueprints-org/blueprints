"""Tests for the LatexFormula class."""
import pytest

from blueprints.codes.latex_formula import LatexFormula, max_curly_brackets_latex, value_to_latex_text


@pytest.fixture()
def fixture_latex_formula() -> LatexFormula:
    """Fixture for testing."""
    return LatexFormula(return_symbol="E", result="500", equation="mc^2", numeric_equation="5*10^2", comparison_operator_label="=")


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


def test_value_to_latex_text() -> None:
    """Test the value_to_latex_text function."""
    # Example values
    value = 5.0

    # Expected result
    expected_result = r"\text{5.0}"

    assert value_to_latex_text(value=value) == expected_result


def test_max_curly_brackets_latex() -> None:
    """Test the max_curly_brackets_latex function."""
    # Example values
    arg_1 = r"\text{a} + \text{b}"
    arg_2 = r"\text{500}"
    arg_3 = r"\text{c-d}"

    # Expected result
    expected_result = r"max \left\{\text{a} + \text{b}; \text{500}; \text{c-d}\right\}"

    assert max_curly_brackets_latex(arg_1, arg_2, arg_3) == expected_result
