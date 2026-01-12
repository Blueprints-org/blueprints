"""Module for testing the Formula classes."""

import operator
from collections.abc import Callable
from typing import Any

import pytest

from blueprints.codes.formula import ComparisonFormula, DoubleComparisonFormula, Formula
from blueprints.codes.latex_formula import LatexFormula


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

    def latex(self, n: int = 3) -> LatexFormula:
        """Dummy latex implementation for testing purposes."""
        return LatexFormula(return_symbol=r"result", result=str(round(float(self), n)), equation=r"first + second")


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


class ComparisonFormulaTestLessOrEqual(ComparisonFormula):
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
    def _evaluate_lhs(a: float, b: float, **_) -> float:
        """Left-hand side value of the comparison."""
        return a + b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison."""
        return c / 2

    @classmethod
    def _comparison_operator(cls) -> Callable[[Any, Any], bool]:
        """Abstract property for the comparison operator (e.g., operator.le, operator.ge, etc.)."""
        return operator.le

    def latex(self, n: int = 3) -> LatexFormula:
        """Dummy latex implementation for testing purposes."""
        return LatexFormula(return_symbol=r"check", result=str(round(float(self), n)), equation=r"a + b \leq c / 2")


def test_comparison_formula_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = 10
    b = 5
    c = 40

    # check passing condition (lhs <= rhs) = True
    formula = ComparisonFormulaTestLessOrEqual(a=a, b=b, c=c)
    assert formula

    # check failing condition (lhs > rhs) = False
    a = 30
    formula = ComparisonFormulaTestLessOrEqual(a=a, b=b, c=c)
    assert not formula


def test_comparison_formula_lhs_property() -> None:
    """Test that the lhs property returns the correct result."""
    a = 10
    b = 5
    c = 40
    formula = ComparisonFormulaTestLessOrEqual(a=a, b=b, c=c)

    # The lhs should be a + b = 10 + 5 = 15
    assert formula.lhs == 15


def test_comparison_formula_rhs_property() -> None:
    """Test that the rhs property returns the correct result."""
    a = 10
    b = 5
    c = 40
    formula = ComparisonFormulaTestLessOrEqual(a=a, b=b, c=c)

    # The rhs should be c / 2 = 40 / 2 = 20
    assert formula.rhs == 20


def test_comparison_formula_unity_check_property() -> None:
    """Test that the unity check property returns the correct result."""
    a = 10
    b = 5
    c = 40
    formula = ComparisonFormulaTestLessOrEqual(a=a, b=b, c=c)

    # The unity check should be lhs / rhs = 15 / 20 = 0.75
    assert formula.unity_check == 0.75


def test_comparison_formula_change_value_after_initialization() -> None:
    """Test that an error is raised when changing a value after initialization."""
    a = 10
    b = 5
    c = 40
    formula = ComparisonFormulaTestLessOrEqual(a=a, b=b, c=c)

    with pytest.raises(AttributeError):
        formula.a = 30


def test_comparison_operator() -> None:
    """Test that the comparison operator is correct."""
    assert ComparisonFormulaTestLessOrEqual._comparison_operator() == operator.le  # noqa: SLF001


class ComparisonFormulaTestGreaterOrEqual(ComparisonFormula):
    """Dummy comparison formula with >= operator for testing purposes."""

    label = "Dummy testing comparison formula (>=)"
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
    def _evaluate_lhs(a: float, b: float, **_) -> float:
        """Left-hand side value of the comparison."""
        return a + b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison."""
        return c / 2

    @classmethod
    def _comparison_operator(cls) -> Callable[[Any, Any], bool]:
        """Abstract property for the comparison operator (e.g., operator.le, operator.ge, etc.)."""
        return operator.ge

    def latex(self, n: int = 3) -> LatexFormula:
        """Dummy latex implementation for testing purposes."""
        return LatexFormula(return_symbol=r"check", result=str(round(float(self), n)), equation=r"a + b \geq c / 2")


def test_comparison_formula_greater_or_equal_evaluation() -> None:
    """Test that the >= comparison formula returns the correct result."""
    a = 10
    b = 5
    c = 20

    # check passing condition (lhs >= rhs) = True
    formula = ComparisonFormulaTestGreaterOrEqual(a=a, b=b, c=c)
    assert formula

    # check failing condition (lhs < rhs) = False
    a = 2
    formula = ComparisonFormulaTestGreaterOrEqual(a=a, b=b, c=c)
    assert not formula


def test_comparison_formula_greater_or_equal_lhs_property() -> None:
    """Test that the lhs property returns the correct result for >= formula."""
    a = 10
    b = 5
    c = 20
    formula = ComparisonFormulaTestGreaterOrEqual(a=a, b=b, c=c)

    # The lhs should be a + b = 10 + 5 = 15
    assert formula.lhs == 15


def test_comparison_formula_greater_or_equal_rhs_property() -> None:
    """Test that the rhs property returns the correct result for >= formula."""
    a = 10
    b = 5
    c = 20
    formula = ComparisonFormulaTestGreaterOrEqual(a=a, b=b, c=c)

    # The rhs should be c / 2 = 20 / 2 = 10
    assert formula.rhs == 10


def test_comparison_formula_greater_or_equal_unity_check_property() -> None:
    """Test that the unity check property is inverted for >= operator.

    For >= operator, unity_check = rhs / lhs (inverted from <=).
    """
    a = 10
    b = 5
    c = 20
    formula = ComparisonFormulaTestGreaterOrEqual(a=a, b=b, c=c)

    # The unity check should be rhs / lhs = 10 / 15 = 0.667 (inverted ratio)
    assert formula.unity_check == pytest.approx(10 / 15)


class ComparisonFormulaTestEqual(ComparisonFormula):
    """Dummy comparison formula with == operator for testing purposes."""

    label = "Dummy testing comparison formula (==)"
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
    def _evaluate_lhs(a: float, b: float, **_) -> float:
        """Left-hand side value of the comparison."""
        return a + b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison."""
        return c / 2

    @classmethod
    def _comparison_operator(cls) -> Callable[[Any, Any], bool]:
        """Abstract property for the comparison operator (e.g., operator.le, operator.ge, etc.)."""
        return operator.eq

    def latex(self, n: int = 3) -> LatexFormula:
        """Dummy latex implementation for testing purposes."""
        return LatexFormula(return_symbol=r"check", result=str(round(float(self), n)), equation=r"a + b = c / 2")


def test_comparison_formula_equal_evaluation() -> None:
    """Test that the == comparison formula returns the correct result."""
    a = 5
    b = 5
    c = 20

    # check passing condition (lhs == rhs) = True
    formula = ComparisonFormulaTestEqual(a=a, b=b, c=c)
    assert formula

    # check failing condition (lhs != rhs) = False
    a = 10
    formula = ComparisonFormulaTestEqual(a=a, b=b, c=c)
    assert not formula


def test_comparison_formula_equal_lhs_property() -> None:
    """Test that the lhs property returns the correct result for == formula."""
    a = 5
    b = 5
    c = 20
    formula = ComparisonFormulaTestEqual(a=a, b=b, c=c)

    # The lhs should be a + b = 5 + 5 = 10
    assert formula.lhs == 10


def test_comparison_formula_equal_rhs_property() -> None:
    """Test that the rhs property returns the correct result for == formula."""
    a = 5
    b = 5
    c = 20
    formula = ComparisonFormulaTestEqual(a=a, b=b, c=c)

    # The rhs should be c / 2 = 20 / 2 = 10
    assert formula.rhs == 10


def test_comparison_formula_equal_unity_check_property() -> None:
    """Test that the unity check property is 1.0 when values are equal.

    For == operator, unity_check = lhs / rhs = 1.0 when condition is satisfied.
    """
    a = 5
    b = 5
    c = 20
    formula = ComparisonFormulaTestEqual(a=a, b=b, c=c)

    # The unity check should be lhs / rhs = 10 / 10 = 1.0
    assert formula.unity_check == 1.0


# Helper function to create dynamic test classes for DoubleComparisonFormula
def _create_double_comparison_formula_test_class(
    comp_op_lhs: Callable[[float, float], bool], comp_op_rhs: Callable[[float, float], bool], comp_op_ids: str = ""
) -> type[DoubleComparisonFormula]:
    """Factory function to create DoubleComparisonFormula test classes dynamically.

    Parameters
    ----------
    comp_op_lhs : Callable
        Comparison operator for the left-hand side (operator.lt, operator.le, operator.gt, operator.ge).
    comp_op_rhs : Callable
        Comparison operator for the right-hand side (operator.lt, operator.le, operator.gt, operator.ge).
    comp_op_ids: str
        Identifier string for the operator combination (for test identification).

    Returns
    -------
    type[DoubleComparisonFormula]
        A dynamically created test class.
    """

    class DynamicDoubleComparisonFormula(DoubleComparisonFormula):
        """Dynamic test class for DoubleComparisonFormula."""

        label = f"Dummy testing comparison formula for '{comp_op_ids}'"
        source_document = "Dummy testing document"

        def __init__(self, a: float, b: float, c: float) -> None:
            """Initialize the formula with three values."""
            super().__init__()
            self.a = a
            self.b = b
            self.c = c

        @classmethod
        def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
            """Return the left-hand side comparison operator."""
            return comp_op_lhs

        @classmethod
        def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
            """Return the right-hand side comparison operator."""
            return comp_op_rhs

        @staticmethod
        def _evaluate_lhs(a: float, **_) -> float:
            """Return the left-hand side value."""
            return a

        @staticmethod
        def _evaluate_val(b: float, **_) -> float:
            """Return the middle value."""
            return b

        @staticmethod
        def _evaluate_rhs(c: float, **_) -> float:
            """Return the right-hand side value."""
            return c

        def latex(self, n: int = 3) -> LatexFormula:
            """Dummy latex implementation for testing purposes."""
            return LatexFormula(return_symbol=r"check", result=str(round(float(self), n)), equation=r"a < b < c")

    return DynamicDoubleComparisonFormula


# Test parameters for ascending operator combinations (< or <=)
ASCENDING_DOUBLE_COMPARISON_PARAMS = [
    (operator.lt, operator.lt, "lt-lt"),
    (operator.le, operator.lt, "le-lt"),
    (operator.lt, operator.le, "lt-le"),
    (operator.le, operator.le, "le-le"),
]

# Test parameters for descending operator combinations (> or >=)
DESCENDING_DOUBLE_COMPARISON_PARAMS = [
    (operator.gt, operator.gt, "gt-gt"),
    (operator.ge, operator.gt, "ge-gt"),
    (operator.gt, operator.ge, "gt-ge"),
    (operator.ge, operator.ge, "ge-ge"),
]

# Test parameters for invalid (mixed direction) operator combinations
INVALID_DOUBLE_COMPARISON_PARAMS = [
    (operator.gt, operator.lt, "gt-lt"),
    (operator.gt, operator.le, "gt-le"),
    (operator.ge, operator.lt, "ge-lt"),
    (operator.ge, operator.le, "ge-le"),
    (operator.lt, operator.gt, "lt-gt"),
    (operator.lt, operator.ge, "lt-ge"),
    (operator.le, operator.ge, "le-ge"),
    (operator.le, operator.gt, "le-gt"),
]


@pytest.mark.parametrize(
    ("comp_op_lhs", "comp_op_rhs", "comp_op_ids"),
    ASCENDING_DOUBLE_COMPARISON_PARAMS,
    ids=[param[2] for param in ASCENDING_DOUBLE_COMPARISON_PARAMS],
)
def test_double_comparison_formula_ascending_operators(
    comp_op_lhs: Callable[[float, float], bool], comp_op_rhs: Callable[[float, float], bool], comp_op_ids: str
) -> None:
    """Test ascending operator combinations (< and <=).

    For ascending comparisons, values increase from left to right: lhs < val < rhs

    Parameters
    ----------
    comp_op_lhs : Callable
        Left-hand side comparison operator.
    comp_op_rhs : Callable
        Right-hand side comparison operator.
    comp_op_ids : str
        Test identifier for parametrization.
    """
    formula_class = _create_double_comparison_formula_test_class(comp_op_lhs, comp_op_rhs, comp_op_ids)

    # Test passing condition: lhs < val < rhs (or with <=)
    formula = formula_class(a=10, b=20, c=30)
    assert formula

    # Test boundary: equal to lhs
    if comp_op_lhs == operator.lt:
        # < is strict, so val == lhs should fail
        formula = formula_class(a=10, b=10, c=30)
        assert not formula
    else:
        # <= is inclusive, so val == lhs should pass
        formula = formula_class(a=10, b=10, c=30)
        assert formula

    # Test boundary: equal to rhs
    if comp_op_rhs == operator.lt:
        # < is strict, so val == rhs should fail
        formula = formula_class(a=10, b=30, c=30)
        assert not formula
    else:
        # <= is inclusive, so val == rhs should pass
        formula = formula_class(a=10, b=30, c=30)
        assert formula

    # Test failing: val > rhs
    formula = formula_class(a=10, b=35, c=30)
    assert not formula

    # Test failing: val < lhs
    formula = formula_class(a=10, b=5, c=30)
    assert not formula


@pytest.mark.parametrize(
    ("comp_op_lhs", "comp_op_rhs", "comp_op_ids"),
    DESCENDING_DOUBLE_COMPARISON_PARAMS,
    ids=[param[2] for param in DESCENDING_DOUBLE_COMPARISON_PARAMS],
)
def test_double_comparison_formula_descending_operators(
    comp_op_lhs: Callable[[float, float], bool], comp_op_rhs: Callable[[float, float], bool], comp_op_ids: str
) -> None:
    """Test descending operator combinations (> and >=).

    For descending comparisons, values decrease from left to right: lhs > val > rhs

    Parameters
    ----------
    comp_op_lhs : Callable
        Left-hand side comparison operator.
    comp_op_rhs : Callable
        Right-hand side comparison operator.
    comp_op_ids : str
        Test identifier for parametrization.
    """
    formula_class = _create_double_comparison_formula_test_class(comp_op_lhs, comp_op_rhs, comp_op_ids)

    # Test passing condition: lhs > val > rhs (or with >=)
    formula = formula_class(a=30, b=20, c=10)
    assert formula

    # Test boundary: equal to lhs
    if comp_op_lhs == operator.gt:
        # > is strict, so val == lhs should fail
        formula = formula_class(a=30, b=30, c=10)
        assert not formula
    else:
        # >= is inclusive, so val == lhs should pass
        formula = formula_class(a=30, b=30, c=10)
        assert formula

    # Test boundary: equal to rhs
    if comp_op_rhs == operator.gt:
        # > is strict, so val == rhs should fail
        formula = formula_class(a=30, b=10, c=10)
        assert not formula
    else:
        # >= is inclusive, so val == rhs should pass
        formula = formula_class(a=30, b=10, c=10)
        assert formula

    # Test failing: val < rhs
    formula = formula_class(a=30, b=5, c=10)
    assert not formula

    # Test failing: val > lhs
    formula = formula_class(a=30, b=40, c=10)
    assert not formula


@pytest.mark.parametrize(
    ("comp_op_lhs", "comp_op_rhs", "comp_op_ids"),
    INVALID_DOUBLE_COMPARISON_PARAMS,
    ids=[param[2] for param in INVALID_DOUBLE_COMPARISON_PARAMS],
)
def test_double_comparison_formula_invalid_operators(
    comp_op_lhs: Callable[[float, float], bool], comp_op_rhs: Callable[[float, float], bool], comp_op_ids: str
) -> None:
    """Test that mixed direction operator combinations raise ValueError.

    Parameters
    ----------
    comp_op_lhs : Callable
        Left-hand side comparison operator.
    comp_op_rhs : Callable
        Right-hand side comparison operator.
    comp_op_ids : str
        Test identifier for parametrization.
    """
    formula_class = _create_double_comparison_formula_test_class(comp_op_lhs, comp_op_rhs, comp_op_ids)

    with pytest.raises(ValueError, match="must point in the same direction"):
        formula_class(a=10, b=20, c=30)
