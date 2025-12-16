"""Module for testing the Formula classes."""

import operator
from collections.abc import Callable
from typing import Any

import pytest

from blueprints.codes.formula import ComparisonFormula, DoubleComparisonFormula, Formula


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


class DoubleComparisonFormulaTestLessLess(DoubleComparisonFormula):
    """
    Dummy double comparison formula for testing purposes.
    lhs < val < rhs.
    """

    label = "Dummy testing comparison formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
    ) -> None:
        """Dummy double comparison formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the left-hand side or lower bound (operator.lt or operator.le)."""
        return operator.lt

    @classmethod
    def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the right-hand side or upper bound (operator.lt or operator.le)."""
        return operator.lt

    @staticmethod
    def _evaluate_lhs(a: float, **_) -> float:
        """Left-hand side value of the double comparison, lower bound."""
        return a

    @staticmethod
    def _evaluate_val(b: float, **_) -> float:
        """Value of the comparison to check against the bounds."""
        return b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison, upper bound."""
        return c


def test_double_comparison_formula_less_less_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = -30
    b = -20
    c = -10

    # check passing condition (lhs < val < rhs) = True
    formula = DoubleComparisonFormulaTestLessLess(a=a, b=b, c=c)
    assert formula

    a = 10
    b = 20
    c = 30

    # check passing condition (lhs < val < rhs) = True
    formula = DoubleComparisonFormulaTestLessLess(a=a, b=b, c=c)
    assert formula

    # check failing condition (lhs = val < rhs) = False
    b = 10
    formula = DoubleComparisonFormulaTestLessLess(a=a, b=b, c=c)
    assert not formula

    # check failing condition (lhs < val = rhs) = False
    b = 30
    formula = DoubleComparisonFormulaTestLessLess(a=a, b=b, c=c)
    assert not formula

    # check failing condition (lhs > val < rhs) = False
    b = 5
    formula = DoubleComparisonFormulaTestLessLess(a=a, b=b, c=c)
    assert not formula

    # check failing condition (lhs < val > rhs) = False
    b = 35
    formula = DoubleComparisonFormulaTestLessLess(a=a, b=b, c=c)
    assert not formula


class DoubleComparisonFormulaTestLessOrEqualLess(DoubleComparisonFormula):
    """
    Dummy double comparison formula for testing purposes.
    lhs <= val < rhs.
    """

    label = "Dummy testing comparison formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
    ) -> None:
        """Dummy double comparison formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the left-hand side or lower bound (operator.lt or operator.le)."""
        return operator.le

    @classmethod
    def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the right-hand side or upper bound (operator.lt or operator.le)."""
        return operator.lt

    @staticmethod
    def _evaluate_lhs(a: float, **_) -> float:
        """Left-hand side value of the double comparison, lower bound."""
        return a

    @staticmethod
    def _evaluate_val(b: float, **_) -> float:
        """Value of the comparison to check against the bounds."""
        return b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison, upper bound."""
        return c


def test_double_comparison_formula_less_or_equal_less_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = 10
    b = 20
    c = 30

    # check passing condition (lhs <= val < rhs) = True
    formula = DoubleComparisonFormulaTestLessOrEqualLess(a=a, b=b, c=c)
    assert formula

    # check passing condition (lhs <= val < rhs) = True
    b = 10
    formula = DoubleComparisonFormulaTestLessOrEqualLess(a=a, b=b, c=c)
    assert formula

    # check failing condition (lhs <= val = rhs) = False
    b = 30
    formula = DoubleComparisonFormulaTestLessOrEqualLess(a=a, b=b, c=c)
    assert not formula

    # check failing condition (lhs > val < rhs) = False
    b = 5
    formula = DoubleComparisonFormulaTestLessOrEqualLess(a=a, b=b, c=c)
    assert not formula

    # check failing condition (lhs < val > rhs) = False
    b = 35
    formula = DoubleComparisonFormulaTestLessOrEqualLess(a=a, b=b, c=c)
    assert not formula


class DoubleComparisonFormulaTestLessLessOrEqual(DoubleComparisonFormula):
    """
    Dummy double comparison formula for testing purposes.
    lhs < val <= rhs.
    """

    label = "Dummy testing comparison formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
    ) -> None:
        """Dummy double comparison formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the left-hand side or lower bound (operator.lt or operator.le)."""
        return operator.lt

    @classmethod
    def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the right-hand side or upper bound (operator.lt or operator.le)."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(a: float, **_) -> float:
        """Left-hand side value of the double comparison, lower bound."""
        return a

    @staticmethod
    def _evaluate_val(b: float, **_) -> float:
        """Value of the comparison to check against the bounds."""
        return b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison, upper bound."""
        return c


def test_double_comparison_formula_less_less_or_equal_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = 10
    b = 20
    c = 30

    # check passing condition (lhs < val <= rhs) = True
    formula = DoubleComparisonFormulaTestLessLessOrEqual(a=a, b=b, c=c)
    assert formula

    # check passing condition (lhs < val <= rhs) = True
    b = 30
    formula = DoubleComparisonFormulaTestLessLessOrEqual(a=a, b=b, c=c)
    assert formula

    # check failing condition (lhs = val < rhs) = False
    b = 10
    formula = DoubleComparisonFormulaTestLessLessOrEqual(a=a, b=b, c=c)
    assert not formula

    # check failing condition (lhs > val < rhs) = False
    b = 5
    formula = DoubleComparisonFormulaTestLessLessOrEqual(a=a, b=b, c=c)
    assert not formula

    # check failing condition (lhs < val > rhs) = False
    b = 35
    formula = DoubleComparisonFormulaTestLessLessOrEqual(a=a, b=b, c=c)
    assert not formula


class DoubleComparisonFormulaTestLessOrEqualLessOrEqual(DoubleComparisonFormula):
    """
    Dummy double comparison formula for testing purposes.
    lhs <= val <= rhs.
    """

    label = "Dummy testing comparison formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
    ) -> None:
        """Dummy double comparison formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the left-hand side or lower bound (operator.lt or operator.le)."""
        return operator.le

    @classmethod
    def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the right-hand side or upper bound (operator.lt or operator.le)."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(a: float, **_) -> float:
        """Left-hand side value of the double comparison, lower bound."""
        return a

    @staticmethod
    def _evaluate_val(b: float, **_) -> float:
        """Value of the comparison to check against the bounds."""
        return b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison, upper bound."""
        return c


def test_double_comparison_formula_less_or_equal_less_or_equal_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = 10
    b = 20
    c = 30

    # check passing condition (lhs <= val <= rhs) = True
    formula = DoubleComparisonFormulaTestLessOrEqualLessOrEqual(a=a, b=b, c=c)
    assert formula

    # check passing condition (lhs <= val <= rhs) = True
    b = 10
    formula = DoubleComparisonFormulaTestLessOrEqualLessOrEqual(a=a, b=b, c=c)
    assert formula

    # check passing condition (lhs <= val <= rhs) = True
    b = 30
    formula = DoubleComparisonFormulaTestLessOrEqualLessOrEqual(a=a, b=b, c=c)
    assert formula

    # check failing condition (lhs > val < rhs) = False
    b = 5
    formula = DoubleComparisonFormulaTestLessOrEqualLessOrEqual(a=a, b=b, c=c)
    assert not formula

    # check failing condition (lhs < val > rhs) = False
    b = 35
    formula = DoubleComparisonFormulaTestLessOrEqualLessOrEqual(a=a, b=b, c=c)
    assert not formula


class DoubleComparisonFormulaTestGreaterLess(DoubleComparisonFormula):
    """
    Dummy double comparison formula for testing purposes.
    lhs > val < rhs.
    """

    label = "Dummy testing comparison formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
    ) -> None:
        """Dummy double comparison formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the left-hand side or lower bound (operator.lt or operator.le)."""
        return operator.gt

    @classmethod
    def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the right-hand side or upper bound (operator.lt or operator.le)."""
        return operator.lt

    @staticmethod
    def _evaluate_lhs(a: float, **_) -> float:
        """Left-hand side value of the double comparison, lower bound."""
        return a

    @staticmethod
    def _evaluate_val(b: float, **_) -> float:
        """Value of the comparison to check against the bounds."""
        return b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison, upper bound."""
        return c


def test_double_comparison_formula_greater_less_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = 10
    b = 20
    c = 30

    # check raise error due to invalid operator
    with pytest.raises(ValueError):
        DoubleComparisonFormulaTestGreaterLess(a=a, b=b, c=c)


class DoubleComparisonFormulaTestGreaterOrEqualLess(DoubleComparisonFormula):
    """
    Dummy double comparison formula for testing purposes.
    lhs >= val < rhs.
    """

    label = "Dummy testing comparison formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
    ) -> None:
        """Dummy double comparison formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the left-hand side or lower bound (operator.lt or operator.le)."""
        return operator.ge

    @classmethod
    def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the right-hand side or upper bound (operator.lt or operator.le)."""
        return operator.lt

    @staticmethod
    def _evaluate_lhs(a: float, **_) -> float:
        """Left-hand side value of the double comparison, lower bound."""
        return a

    @staticmethod
    def _evaluate_val(b: float, **_) -> float:
        """Value of the comparison to check against the bounds."""
        return b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison, upper bound."""
        return c


def test_double_comparison_formula_greater_or_equal_less_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = 10
    b = 20
    c = 30

    # check raise error due to invalid operator
    with pytest.raises(ValueError):
        DoubleComparisonFormulaTestGreaterOrEqualLess(a=a, b=b, c=c)


class DoubleComparisonFormulaTestLessGreater(DoubleComparisonFormula):
    """
    Dummy double comparison formula for testing purposes.
    lhs < val > rhs.
    """

    label = "Dummy testing comparison formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
    ) -> None:
        """Dummy double comparison formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the left-hand side or lower bound (operator.lt or operator.le)."""
        return operator.lt

    @classmethod
    def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the right-hand side or upper bound (operator.lt or operator.le)."""
        return operator.gt

    @staticmethod
    def _evaluate_lhs(a: float, **_) -> float:
        """Left-hand side value of the double comparison, lower bound."""
        return a

    @staticmethod
    def _evaluate_val(b: float, **_) -> float:
        """Value of the comparison to check against the bounds."""
        return b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison, upper bound."""
        return c


def test_double_comparison_formula_less_greater_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = 10
    b = 20
    c = 30

    # check raise error due to invalid operator
    with pytest.raises(ValueError):
        DoubleComparisonFormulaTestLessGreater(a=a, b=b, c=c)


class DoubleComparisonFormulaTestLessGreaterOrEqual(DoubleComparisonFormula):
    """
    Dummy double comparison formula for testing purposes.
    lhs < val >= rhs.
    """

    label = "Dummy testing comparison formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
    ) -> None:
        """Dummy double comparison formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the left-hand side or lower bound (operator.lt or operator.le)."""
        return operator.lt

    @classmethod
    def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the right-hand side or upper bound (operator.lt or operator.le)."""
        return operator.ge

    @staticmethod
    def _evaluate_lhs(a: float, **_) -> float:
        """Left-hand side value of the double comparison, lower bound."""
        return a

    @staticmethod
    def _evaluate_val(b: float, **_) -> float:
        """Value of the comparison to check against the bounds."""
        return b

    @staticmethod
    def _evaluate_rhs(c: float, **_) -> float:
        """Right-hand side value of the comparison, upper bound."""
        return c


def test_double_comparison_formula_less_greater_or_equal_evaluation() -> None:
    """Test that the formula returns the correct result."""
    a = 10
    b = 20
    c = 30

    # check raise error due to invalid operator
    with pytest.raises(ValueError):
        DoubleComparisonFormulaTestLessGreaterOrEqual(a=a, b=b, c=c)
