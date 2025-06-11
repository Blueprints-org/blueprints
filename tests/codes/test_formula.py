"""Module for testing the Formula classes."""

import pytest

from blueprints.codes.formula import ComparisonFormula, Formula


class FormulaTest(Formula):
    """Dummy formula for testing purposes."""

    label = "Dummy testing formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        first: float,
        second: float,
    ) -> None:
        """Dummy formula for testing purposes."""
        super().__init__()
        self.first = first
        self.second = second

    @staticmethod
    def _evaluate(
        first: float,
        second: float,
    ) -> float:
        """Dummy formula for testing purposes."""
        return first + second


def test_raise_error_when_changing_value_after_initialization() -> None:
    """Test that an error is raised when changing a value after initialization."""
    first = 1
    second = 2
    dummy_testing_formula = FormulaTest(first=first, second=second)
    with pytest.raises(AttributeError):
        dummy_testing_formula.first = 3


def test_raise_not_implemented_error_detailed_result() -> None:
    """Test that an error is raised when the detailed result is not implemented."""
    first = 1
    second = 2
    dummy_testing_formula = FormulaTest(first=first, second=second)
    with pytest.raises(NotImplementedError):
        _ = dummy_testing_formula.detailed_result


class ComparisonFormulaTest(ComparisonFormula):
    """Dummy comparison formula for testing purposes."""

    label = "Dummy testing comparison formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
    ) -> None:
        """Dummy comparison formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def _evaluate(
        a: float,
        b: float,
        c: float,
    ) -> float:
        """Dummy formula for testing purposes."""
        return ComparisonFormulaTest._evaluate_lhs(a=a, b=b) <= ComparisonFormulaTest._evaluate_rhs(c=c)

    @staticmethod
    def _evaluate_lhs(a: float, b: float, **_) -> float:
        """Left-hand side value of the comparison."""
        return a + b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison."""
        return c / 2

    @property
    def unity_check(self) -> float:
        """Property to present the unity check of the formula."""
        return self.lhs / self.rhs


def test_comparison_formula_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = 10
    b = 5
    c = 40

    # check passing condition (lhs <= rhs) = True
    formula = ComparisonFormulaTest(a=a, b=b, c=c)
    assert formula

    # check failing condition (lhs > rhs) = False
    a = 30
    formula = ComparisonFormulaTest(a=a, b=b, c=c)
    assert not formula


def test_comparison_formula_lhs_property() -> None:
    """Test that the lhs property returns the correct result."""
    a = 10
    b = 5
    c = 40
    formula = ComparisonFormulaTest(a=a, b=b, c=c)

    # The lhs should be a + b = 10 + 5 = 15
    assert formula.lhs == 15


def test_comparison_formula_rhs_property() -> None:
    """Test that the rhs property returns the correct result."""
    a = 10
    b = 5
    c = 40
    formula = ComparisonFormulaTest(a=a, b=b, c=c)

    # The rhs should be c / 2 = 40 / 2 = 20
    assert formula.rhs == 20


def test_comparison_formula_unity_check_property() -> None:
    """Test that the unity check property returns the correct result."""
    a = 10
    b = 5
    c = 40
    formula = ComparisonFormulaTest(a=a, b=b, c=c)

    # The unity check should be lhs / rhs = 15 / 20 = 0.75
    assert formula.unity_check == 0.75


def test_comparison_formula_change_value_after_initialization() -> None:
    """Test that an error is raised when changing a value after initialization."""
    a = 10
    b = 5
    c = 40
    formula = ComparisonFormulaTest(a=a, b=b, c=c)

    with pytest.raises(AttributeError):
        formula.a = 30
