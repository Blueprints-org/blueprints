"""Module for testing the Formula classes."""

import operator
from collections.abc import Callable
from typing import Any

import pytest

from blueprints.codes.formula import AggregatedComparisonFormula, ComparisonFormula, DoubleComparisonFormula, Formula
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


class TestAggregatedComparisonFormula:
    """Test class for AggregatedComparisonFormula."""

    def _le(self, a: float, b: float, c: float) -> ComparisonFormulaTestLessOrEqual:
        """Helper function to create a ComparisonFormulaTestLessOrEqual instance.

        Reuses the ComparisonFormulaTestLessOrEqual class defined above,
        which implements a comparison formula with the <= operator.

        # _le(a, b, c): lhs = a+b, rhs = c/2  →  passes when a+b <= c/2
        """
        return ComparisonFormulaTestLessOrEqual(a=a, b=b, c=c)

    def _ge(self, a: float, b: float, c: float) -> ComparisonFormulaTestGreaterOrEqual:
        """Helper function to create a ComparisonFormulaTestGreaterOrEqual instance.

        Reuses the ComparisonFormulaTestGreaterOrEqual class defined above,
        which implements a comparison formula with the >= operator.

        # _ge(a, b, c): lhs = a+b, rhs = c/2  →  passes when a+b >= c/2
        """
        return ComparisonFormulaTestGreaterOrEqual(a=a, b=b, c=c)

    def test_aggregated_comparison_formula_evaluate_raises_when_no_aggregation(self) -> None:
        """Test that ValueError is raised when no aggregation function is provided."""
        with pytest.raises(ValueError, match="Aggregation function must be provided"):
            AggregatedComparisonFormula._evaluate(comparison_formulas=[self._le(1, 1, 10)])  # noqa: SLF001

    def test_aggregated_comparison_formula_evaluate_raises_when_aggregation_is_none(self) -> None:
        """Test that ValueError is raised when aggregation is explicitly None."""
        with pytest.raises(ValueError, match="Aggregation function must be provided"):
            AggregatedComparisonFormula._evaluate(aggregation=None, comparison_formulas=[self._le(1, 1, 10)])  # noqa: SLF001

    def test_aggregated_comparison_formula_evaluate_raises_when_invalid_aggregation(self) -> None:
        """Test that ValueError is raised when aggregation is not 'all' or 'any'."""
        with pytest.raises(ValueError, match="Aggregation function must be either 'all' or 'any'"):
            AggregatedComparisonFormula._evaluate(aggregation=sum, comparison_formulas=[self._le(1, 1, 10)])  # noqa: SLF001

    def test_aggregated_comparison_formula_evaluate_raises_when_no_comparison_formulas(self) -> None:
        """Test that ValueError is raised when no comparison_formulas are provided."""
        with pytest.raises(ValueError, match="Comparison formulas must be provided"):
            AggregatedComparisonFormula._evaluate(aggregation=all)  # noqa: SLF001

    def test_aggregated_comparison_formula_evaluate_raises_when_comparison_formulas_is_none(self) -> None:
        """Test that ValueError is raised when comparison_formulas is explicitly None."""
        with pytest.raises(ValueError, match="Comparison formulas must be provided"):
            AggregatedComparisonFormula._evaluate(aggregation=all, comparison_formulas=None)  # noqa: SLF001

    def test_aggregated_comparison_formula_evaluate_raises_when_not_comparison_formula_instances(self) -> None:
        """Test that ValueError is raised when comparison_formulas contains non-ComparisonFormula instances."""
        with pytest.raises(ValueError, match="All provided comparison formulas must be instances of ComparisonFormula"):
            AggregatedComparisonFormula._evaluate(aggregation=all, comparison_formulas=[1.0, 2.0])  # noqa: SLF001

    def test_aggregated_comparison_formula_all_three_formulas_all_pass(self) -> None:
        """Test AggregatedComparisonFormula with 'all' when all three formulas pass."""
        # All lhs <= rhs: 1+1=2 <= 10/2=5  ✓
        f1 = self._le(1, 1, 10)
        f2 = self._le(2, 1, 10)
        f3 = self._le(1, 2, 10)
        formula = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[f1, f2, f3])
        assert formula
        assert bool(formula) is True

    def test_aggregated_comparison_formula_all_three_formulas_one_fails(self) -> None:
        """Test AggregatedComparisonFormula with 'all' when one of three formulas fails."""
        # f3 fails: 4+1=5 > 4/2=2  →  not (lhs <= rhs)
        f1 = self._le(1, 1, 10)
        f2 = self._le(2, 1, 10)
        f3 = self._le(4, 1, 4)  # lhs=5, rhs=2  →  fails
        formula = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[f1, f2, f3])
        assert not formula
        assert bool(formula) is False

    def test_aggregated_comparison_formula_all_three_formulas_unity_check_is_max(self) -> None:
        """Test that unity_check for 'all' aggregation is the maximum of individual unity checks."""
        # f1: lhs=2, rhs=5  →  uc=0.4
        # f2: lhs=3, rhs=5  →  uc=0.6
        # f3: lhs=4, rhs=5  →  uc=0.8  ← maximum
        f1 = self._le(1, 1, 10)  # lhs=2, rhs=5, uc=0.4
        f2 = self._le(2, 1, 10)  # lhs=3, rhs=5, uc=0.6
        f3 = self._le(3, 1, 10)  # lhs=4, rhs=5, uc=0.8
        formula = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[f1, f2, f3])
        assert formula.unity_check == pytest.approx(0.8)

    def test_aggregated_comparison_formula_any_three_formulas_all_fail(self) -> None:
        """Test AggregatedComparisonFormula with 'any' when all three formulas fail."""
        # All fail: lhs > rhs
        f1 = self._le(10, 1, 4)  # lhs=11, rhs=2  →  fails
        f2 = self._le(10, 2, 4)  # lhs=12, rhs=2  →  fails
        f3 = self._le(10, 3, 4)  # lhs=13, rhs=2  →  fails
        formula = AggregatedComparisonFormula(aggregation=any, comparison_formulas=[f1, f2, f3])
        assert not formula
        assert bool(formula) is False

    def test_aggregated_comparison_formula_any_three_formulas_one_passes(self) -> None:
        """Test AggregatedComparisonFormula with 'any' when one of three formulas passes."""
        # f1 passes, f2 and f3 fail
        f1 = self._le(1, 1, 10)  # lhs=2, rhs=5  →  passes
        f2 = self._le(10, 1, 4)  # lhs=11, rhs=2  →  fails
        f3 = self._le(10, 3, 4)  # lhs=13, rhs=2  →  fails
        formula = AggregatedComparisonFormula(aggregation=any, comparison_formulas=[f1, f2, f3])
        assert formula
        assert bool(formula) is True

    def test_aggregated_comparison_formula_any_three_formulas_unity_check_is_min(self) -> None:
        """Test that unity_check for 'any' aggregation is the minimum of individual unity checks."""
        # f1: lhs=2, rhs=5  →  uc=0.4  ← minimum
        # f2: lhs=3, rhs=5  →  uc=0.6
        # f3: lhs=4, rhs=5  →  uc=0.8
        f1 = self._le(1, 1, 10)
        f2 = self._le(2, 1, 10)
        f3 = self._le(3, 1, 10)
        formula = AggregatedComparisonFormula(aggregation=any, comparison_formulas=[f1, f2, f3])
        assert formula.unity_check == pytest.approx(0.4)

    def test_aggregated_comparison_formula_lhs_raises(self) -> None:
        """Test that accessing lhs raises NotImplementedError."""
        formula = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[self._le(1, 1, 10)])
        with pytest.raises(NotImplementedError):
            _ = formula.lhs

    def test_aggregated_comparison_formula_rhs_raises(self) -> None:
        """Test that accessing rhs raises NotImplementedError."""
        formula = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[self._le(1, 1, 10)])
        with pytest.raises(NotImplementedError):
            _ = formula.rhs

    def test_aggregated_comparison_formula_comparison_operator_raises(self) -> None:
        """Test that calling _comparison_operator raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="_comparison_operator is not relevant"):
            AggregatedComparisonFormula._comparison_operator()  # noqa: SLF001

    def test_aggregated_comparison_formula_evaluate_lhs_raises(self) -> None:
        """Test that calling _evaluate_lhs raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="_evaluate_lhs is not relevant"):
            AggregatedComparisonFormula._evaluate_lhs()  # noqa: SLF001

    def test_aggregated_comparison_formula_evaluate_rhs_raises(self) -> None:
        """Test that calling _evaluate_rhs raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="_evaluate_rhs is not relevant"):
            AggregatedComparisonFormula._evaluate_rhs()  # noqa: SLF001

    def test_aggregated_comparison_formula_all_of_any_and_all_passes(self) -> None:
        """Test 'all' aggregation of one 'any' and one 'all' AggregatedComparisonFormula — all pass.

        Composite structure:
            outer_all(
                inner_any(f_pass, f_fail),   # True  (any passes)
                inner_all(f_pass, f_pass),   # True  (all pass)
            )
        Expected: True
        """
        f_pass = self._le(1, 1, 10)  # lhs=2, rhs=5  →  passes
        f_fail = self._le(10, 1, 4)  # lhs=11, rhs=2 →  fails

        inner_any = AggregatedComparisonFormula(aggregation=any, comparison_formulas=[f_pass, f_fail])
        inner_all = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[f_pass, f_pass])

        outer = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[inner_any, inner_all])
        assert outer
        assert bool(outer) is True

    def test_aggregated_comparison_formula_all_of_any_and_all_fails_when_inner_all_fails(self) -> None:
        """Test 'all' aggregation fails when the inner 'all' has a failing formula.

        Composite structure:
            outer_all(
                inner_any(f_pass, f_fail),   # True
                inner_all(f_pass, f_fail),   # False  ← one fails
            )
        Expected: False
        """
        f_pass = self._le(1, 1, 10)
        f_fail = self._le(10, 1, 4)

        inner_any = AggregatedComparisonFormula(aggregation=any, comparison_formulas=[f_pass, f_fail])
        inner_all = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[f_pass, f_fail])

        outer = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[inner_any, inner_all])
        assert not outer
        assert bool(outer) is False

    def test_aggregated_comparison_formula_any_of_any_and_all_passes_when_one_inner_passes(self) -> None:
        """Test 'any' aggregation of one 'any' and one 'all' AggregatedComparisonFormula — passes when at least one inner passes.

        Composite structure:
            outer_any(
                inner_any(f_pass, f_fail),   # True  ← at least one passes
                inner_all(f_pass, f_fail),   # False
            )
        Expected: True
        """
        f_pass = self._le(1, 1, 10)
        f_fail = self._le(10, 1, 4)

        inner_any = AggregatedComparisonFormula(aggregation=any, comparison_formulas=[f_pass, f_fail])
        inner_all = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[f_pass, f_fail])

        outer = AggregatedComparisonFormula(aggregation=any, comparison_formulas=[inner_any, inner_all])
        assert outer
        assert bool(outer) is True

    def test_aggregated_comparison_formula_any_of_any_and_all_fails_when_all_inner_fail(self) -> None:
        """Test 'any' aggregation fails when both inner formulas fail.

        Composite structure:
            outer_any(
                inner_any(f_fail, f_fail),   # False
                inner_all(f_pass, f_fail),   # False
            )
        Expected: False
        """
        f_pass = self._le(1, 1, 10)
        f_fail = self._le(10, 1, 4)

        inner_any = AggregatedComparisonFormula(aggregation=any, comparison_formulas=[f_fail, f_fail])
        inner_all = AggregatedComparisonFormula(aggregation=all, comparison_formulas=[f_pass, f_fail])

        outer = AggregatedComparisonFormula(aggregation=any, comparison_formulas=[inner_any, inner_all])
        assert not outer
        assert bool(outer) is False
