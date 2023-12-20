import pytest
from blueprints.codes.latex_formula import LatexFormula


class TestLatexFormula:
    """Test for LatexFormula."""

    @staticmethod
    def fixture_1() -> LatexFormula:
        """Fixture for testing."""
        return LatexFormula(return_symbol="E", result="500", equation="E=mc^2", numeric_equation="5*10^2", comparison_operator_label="=")

    def test_short(self) -> None:
        """Test the short representation."""
        # Example values
        formula = self.fixture_1()

        # Expected result
        expected_result = "E = 500"

        assert formula.short == expected_result

    def test_complete(self) -> None:
        """Test the complete representation."""
        # Example values
        formula = self.fixture_1()

        # Expected result
        expected_result = "E = E=mc^2 = 5*10^2 = 500"
        assert formula.complete == expected_result

    def test_str(self) -> None:
        """Test the string representation."""
        # Example values
        formula = self.fixture_1()

        # Expected result
        expected_result = "E = E=mc^2 = 5*10^2 = 500"
        assert str(formula) == expected_result
