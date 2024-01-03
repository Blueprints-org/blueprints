"""Tests for the LatexFormula class."""
import pytest

from blueprints.codes.latex_formula import LatexFormula, latex_fraction, max_curly_brackets_latex, value_to_latex_text


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


@pytest.mark.parametrize(
    ("arg_1", "arg_2", "arg_3", "expected_output"),
    [
        (r"a+b", r"\text{500}", r"c-d", r"\max \left\{a+b; \text{500}; c-d\right\}"),
        (r"a+b", 500, r"c-d", r"\max \left\{a+b; \text{500}; c-d\right\}"),
    ],
)
def test_max_curly_brackets_latex(
    arg_1: str | float,
    arg_2: str | float,
    arg_3: str | float,
    expected_output: str,
) -> None:
    """Test the max_curly_brackets_latex function."""
    result = max_curly_brackets_latex(arg_1, arg_2, arg_3)
    assert result == expected_output


def test_latex_fraction() -> None:
    """Test the latex_fraction function."""
    # Example values
    numerator = 5.0
    denominator = 10.0

    # Expected result
    expected_result = r"\frac{\text{5.0}}{\text{10.0}}"

    assert latex_fraction(numerator=numerator, denominator=denominator) == expected_result
