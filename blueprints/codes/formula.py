"""Module for the abstract base class Formula."""

import operator
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Sequence
from typing import Self

from blueprints.codes.latex_formula import LatexFormula


class Formula(float, ABC):
    """Abstract base class for formulas used in the codes."""

    def __new__(cls, *args, **kwargs) -> Self:
        """Method for creating a new instance of the class."""
        result = cls._evaluate(*args, **kwargs)
        instance = float.__new__(cls, result)
        instance._initialized = False  # noqa: SLF001
        return instance

    def __init__(self, *args, **kwargs) -> None:
        """Method for initializing a new instance of the class."""
        super().__init__(*args, **kwargs)
        self._initialized = True

    def __setattr__(self, name: str, value: str | float) -> None:
        """Override the __setattr__ method to prevent modifications after initialization.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : str | float
            The value to be assigned to the attribute.
        """
        if getattr(self, "_initialized", False) and name in self.__dict__:
            raise AttributeError(f"Attribute '{name}' of '{type(self).__name__}' object is read-only and cannot be modified after initialization.")
        super().__setattr__(name, value)

    @property
    @abstractmethod
    def label(self) -> str:
        """Property for the formula label.

        For example, "5.2" for formula 5.2.

        Returns
        -------
        str
            The label/number associated with the formula.
            This is an abstract method and must be implemented in all subclasses.
        """

    @property
    @abstractmethod
    def source_document(self) -> str:
        """Property for the source document.

        For example, "EN 1992-1-1:2004"
        Try to use the official and complete name of the document including publishing year, if possible.

        Returns
        -------
        str
            The reference to the document where the formula originates.
            This is an abstract method and must be implemented in all subclasses.
        """

    @property
    def detailed_result(self) -> dict:
        """Property for providing the detailed result of the formula.

        Returns
        -------
        dict
            The detailed result of the formula.
            Keys are strings representing the name of the partial or intermediate result.
            Values types will depend on the specific implementation, but must be a serializable type.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _evaluate(*args, **kwargs) -> float | bool:
        """Abstract method for the logic of the formula.

        Returns
        -------
        float | bool
            The result of the formula.
            This is an abstract method and must be implemented in all subclasses.
        """

    @abstractmethod
    def latex(self, n: int = 3) -> LatexFormula:
        """Abstract method for the latex representation of the formula, given in math mode.

        Parameters
        ----------
        n : int, optional
            The number of decimal places to round the result to.

        Returns
        -------
        LatexFormula
            The latex representation of the formula, given in math mode.
            This is an abstract method and must be implemented in all subclasses.
        """


class ComparisonFormula(Formula):
    """Base class for comparison formulas used in the codes."""

    _lhs: float
    _rhs: float

    def __new__(cls, *args, **kwargs) -> Self:
        """Method for creating a new instance of the class."""
        lhs = cls._evaluate_lhs(*args, **kwargs)
        rhs = cls._evaluate_rhs(*args, **kwargs)
        result = cls._evaluate(*args, **kwargs)
        instance = float.__new__(cls, result)
        instance._lhs = lhs  # noqa: SLF001
        instance._rhs = rhs  # noqa: SLF001
        instance._initialized = False  # noqa: SLF001
        return instance

    @classmethod
    @abstractmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Abstract property for the comparison operator (e.g., operator.le, operator.ge, etc.)."""

    @staticmethod
    @abstractmethod
    def _evaluate_lhs(*args, **kwargs) -> float:
        """Abstract method for the logic of the left-hand side of the comparison formula.

        Returns
        -------
        float
            The left-hand side value of the comparison.
        """

    @staticmethod
    @abstractmethod
    def _evaluate_rhs(*args, **kwargs) -> float:
        """Abstract method for the logic of the right-hand side of the comparison formula.

        Returns
        -------
        float
            The right-hand side value of the comparison.
        """

    @property
    def lhs(self) -> float:
        """Property for getting the left-hand side of the comparison.

        Returns
        -------
        float
            The left-hand side value of the comparison.
        """
        return self._lhs

    @property
    def rhs(self) -> float:
        """Property for getting the right-hand side of the comparison.

        Returns
        -------
        float
            The right-hand side value of the comparison.
        """
        return self._rhs

    @property
    def unity_check(self) -> float:
        """Property to present the unity check of the formula.

        A unity check is the ratio between the left-hand side (lhs) and right-hand side (rhs) of a comparison formula.
        The calculation is operator-dependent to ensure a unity check less than 1 always indicates the condition is satisfied:

        - For le (<=) and lt (<): unity_check = lhs / rhs
        - For ge (>=) and gt (>): unity_check = rhs / lhs
        - For eq (==) and other operators: unity_check = lhs / rhs

        A unity check < 1 indicates the condition is satisfied. A unity check >= 1 indicates the condition is not satisfied.

        Examples
        --------
        lhs = 0.11, rhs = 0.1, Formula: lhs <= rhs, unity_check = 1.1  # NOT satisfied
        lhs = 0.09, rhs = 0.1, Formula: lhs <= rhs, unity_check = 0.9  # satisfied
        lhs = 0.2, rhs = 0.1, Formula: lhs >= rhs, unity_check = 0.5  # satisfied
        lhs = 0.05, rhs = 0.1, Formula: lhs >= rhs, unity_check = 2.0  # NOT satisfied

        Returns
        -------
        float
            The unity check ratio.
        """
        comparison_op = self._comparison_operator()
        match comparison_op:
            case operator.le | operator.lt:
                return self.lhs / self.rhs
            case operator.ge | operator.gt:
                return self.rhs / self.lhs
            case _:  # handles operator.eq and any other operators
                return self.lhs / self.rhs

    def __bool__(self) -> bool:
        """Return whether the comparison condition is satisfied.

        Returns True if the unity check is less than or equal to 1.0, indicating the condition is satisfied.
        This allows ComparisonFormula instances to be used directly in boolean contexts.

        Examples
        --------
        formula = SomeComparisonFormula(...)
        if formula:  # Equivalent to: if formula.unity_check <= 1.0
            print("Condition satisfied")

        Returns
        -------
        bool
            True if unity_check <= 1.0 (condition is satisfied), False otherwise.
        """
        return self.unity_check <= 1.0

    @classmethod
    def _evaluate(cls, *args, **kwargs) -> bool:
        """Implements the comparison using the class-level operator."""
        lhs = cls._evaluate_lhs(*args, **kwargs)
        rhs = cls._evaluate_rhs(*args, **kwargs)
        comparison = cls._comparison_operator
        return comparison()(lhs, rhs)


class AggregatedComparisonFormula(ComparisonFormula):
    """Class for aggregating comparison formulas used in the codes.
    Examples: (angle < angle_max) and (height > height_min).
    """

    def __new__(cls, *args, **kwargs) -> Self:
        """Method for creating a new instance of the class."""
        result = cls._evaluate(*args, **kwargs)
        instance = float.__new__(cls, result)
        instance._initialized = False  # noqa: SLF001
        return instance

    def __init__(self, aggregation: Callable[[Iterable[bool]], bool], comparison_formulas: Sequence[ComparisonFormula]) -> None:
        """Method for initializing a new instance of the class.

        Parameters
        ----------
        aggregation : Callable[[Iterable[bool]], bool]
            Type of aggregation function to be used for the comparison formulas. Must be either all or any.
        comparison_formulas : Sequence[ComparisonFormula]
            Sequence of ComparisonFormula instances to be aggregated.
        """
        super().__init__()
        self.aggregation = aggregation
        self.comparison_formulas = comparison_formulas

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Disabled comparison operator for AggregatedComparisonFormula, as it is not relevant for this class."""
        raise NotImplementedError("The _comparison_operator is not relevant for AggregatedComparisonFormula.")

    @staticmethod
    def _evaluate_lhs(*args, **kwargs) -> float:
        """Disabled evaluation of the left-hand side for AggregatedComparisonFormula, as it is not relevant for this class."""
        raise NotImplementedError("The _evaluate_lhs is not relevant for AggregatedComparisonFormula.")

    @staticmethod
    def _evaluate_rhs(*args, **kwargs) -> float:
        """Disabled evaluation of the right-hand side for AggregatedComparisonFormula, as it is not relevant for this class."""
        raise NotImplementedError("The _evaluate_rhs is not relevant for AggregatedComparisonFormula.")

    @property
    def lhs(self) -> float:
        """Disabled property for getting the left-hand side of the comparison, as it is not relevant for this class."""
        raise NotImplementedError("The lhs property is not relevant for AggregatedComparisonFormula.")

    @property
    def rhs(self) -> float:
        """Disabled property for getting the right-hand side of the comparison, as it is not relevant for this class."""
        raise NotImplementedError("The rhs property is not relevant for AggregatedComparisonFormula.")

    @property
    def unity_check(self) -> float:
        """Property to present the unity check of the formula.

        A unity check is the ratio between the left-hand side (lhs) and right-hand side (rhs) of a comparison formula.
        For an aggregated comparison formula, the unity check is determined by the aggregation function (all or any)
        applied to the unity checks of the individual comparison formulas:

        - If aggregation is all, the unity check is the maximum of the unity checks of the individual formulas.
        - If aggregation is any, the unity check is the minimum of the unity checks of the individual formulas.

        A unity check <= 1 indicates the condition is satisfied. A unity check > 1 indicates the condition is not satisfied.

        Examples
        --------
        formula1.unity_check = 0.9
        formula2.unity_check = 1.1

        aggregated_formula = AggregatedComparisonFormula(all, [formula1, formula2])
        aggregated_formula.unity_check  # Returns 1.1, as the maximum of the unity checks is taken for 'all' aggregation.

        aggregated_formula = AggregatedComparisonFormula(any, [formula1, formula2])
        aggregated_formula.unity_check  # Returns 0.9, as the minimum of the unity checks is taken for 'any' aggregation.

        Returns
        -------
        float
            The unity check ratio.
        """
        return (
            max(formula.unity_check for formula in self.comparison_formulas)
            if self.aggregation is all
            else min(formula.unity_check for formula in self.comparison_formulas)
        )

    def __bool__(self) -> bool:
        """Return whether the comparison condition is satisfied.

        Returns True if the unity check is less than or equal to 1.0, indicating the condition is satisfied.
        This allows ComparisonFormula instances to be used directly in boolean contexts.

        Examples
        --------
        formula = SomeComparisonFormula(...)
        if formula:  # Equivalent to: if formula.unity_check <= 1.0
            print("Condition satisfied")

        Returns
        -------
        bool
            True if unity_check <= 1.0 (condition is satisfied), False otherwise.
        """
        return self.unity_check <= 1.0

    @classmethod
    def _evaluate(cls, *args, **kwargs) -> bool:
        """Implements the comparison using the class-level operator.

        Raises
        ------
        ValueError
            If the aggregation function is not provided or is neither ``all`` nor ``any``.
            Also raised if no comparison formulas are provided, or if any provided
            formula is not an instance of :class:`ComparisonFormula`.
        """
        aggregation_func: Callable[[Iterable[bool]], bool] = kwargs.get("aggregation", args[0] if args else None)
        if aggregation_func is None:
            raise ValueError("Aggregation function must be provided as a keyword argument 'aggregation' or as the first positional argument.")
        if aggregation_func not in (all, any):
            raise ValueError("Aggregation function must be either 'all' or 'any'.")
        comparison_formulas: Sequence[ComparisonFormula] = kwargs.get("comparison_formulas", args[1] if len(args) == 2 else None)
        if comparison_formulas is None:
            raise ValueError("Comparison formulas must be provided as a keyword argument 'comparison_formulas' or as the second positional argument.")
        if not comparison_formulas:
            raise ValueError("At least one comparison formula must be provided.")
        if not all(isinstance(formula, ComparisonFormula) for formula in comparison_formulas):
            raise ValueError("All provided comparison formulas must be instances of ComparisonFormula.")
        return aggregation_func(formula.__bool__() for formula in comparison_formulas)


class DoubleComparisonFormula(Formula):
    """Base class for double comparison formulas used in the codes.
    Examples: angle_min < angle < angle_max or angle_min > angle > angle_max.

    Note that the comparison operators must point in the same direction for both sides:
    - Ascending: operator.lt (<) or operator.le (<=)
    - Descending: operator.gt (>) or operator.ge (>=)
    Mixed directions (e.g., < and >) are not allowed.
    """

    _lhs: float
    _val: float
    _rhs: float

    def __new__(cls, *args, **kwargs) -> Self:
        """Method for creating a new instance of the class."""
        lhs = cls._evaluate_lhs(*args, **kwargs)
        val = cls._evaluate_val(*args, **kwargs)
        rhs = cls._evaluate_rhs(*args, **kwargs)
        result = cls._evaluate(*args, **kwargs)
        instance = float.__new__(cls, result)
        instance._lhs = lhs  # noqa: SLF001
        instance._val = val  # noqa: SLF001
        instance._rhs = rhs  # noqa: SLF001
        instance._initialized = False  # noqa: SLF001
        return instance

    @classmethod
    @abstractmethod
    def _comparison_operator_lhs(cls) -> Callable[[float, float], bool]:
        """Abstract property for the comparison operator of the left-hand side or lower bound
        Must be one of: operator.lt (<), operator.le (<=), operator.gt (>), operator.ge (>=).
        Must point in the same direction as _comparison_operator_rhs (both ascending or both descending).
        """

    @classmethod
    @abstractmethod
    def _comparison_operator_rhs(cls) -> Callable[[float, float], bool]:
        """Abstract property for the comparison operator of the right-hand side or upper bound
        Must be one of: operator.lt (<), operator.le (<=), operator.gt (>), operator.ge (>=).
        Must point in the same direction as _comparison_operator_lhs (both ascending or both descending).
        """

    @staticmethod
    @abstractmethod
    def _evaluate_lhs(*args, **kwargs) -> float:
        """Abstract method for the logic of the left-hand side of the double comparison formula.

        Returns
        -------
        float
            The left-hand side value of the comparison.
        """

    @staticmethod
    @abstractmethod
    def _evaluate_val(*args, **kwargs) -> float:
        """Abstract method for the logic of the value to be checked against the bounds.

        Returns
        -------
        float
            The middle value of the comparison.
        """

    @staticmethod
    @abstractmethod
    def _evaluate_rhs(*args, **kwargs) -> float:
        """Abstract method for the logic of the right-hand side of the double comparison formula.

        Returns
        -------
        float
            The right-hand side value of the comparison.
        """

    @property
    def lhs(self) -> float:
        """Property for getting the left-hand side of the double comparison.

        Returns
        -------
        float
            The left-hand side value of the comparison.
        """
        return self._lhs

    @property
    def val(self) -> float:
        """Property for getting the middle value of the double comparison to be checked against the bounds.

        Returns
        -------
        float
            The left-hand side value of the comparison.
        """
        return self._val

    @property
    def rhs(self) -> float:
        """Property for getting the right-hand side of the double comparison.

        Returns
        -------
        float
            The right-hand side value of the comparison.
        """
        return self._rhs

    def __bool__(self) -> bool:
        """Return whether the double comparison condition is satisfied.
        Returns True if the comparison e.g. lhs < val < rhs is satisfied.
        This allows DoubleComparisonFormula instances to be used directly in boolean contexts.

        Examples
        --------
        formula = SomeDoubleComparisonFormula(...)
        if formula:  # Equivalent to: if formula.__bool__
            print("Condition satisfied")

        Returns
        -------
        bool
            True if e.g. lhs < val < rhs (condition is satisfied), False otherwise.
        """
        # Check of valid comparison operators is done in the _evaluate method.
        return self._comparison_operator_lhs()(self.lhs, self.val) and self._comparison_operator_rhs()(self.val, self.rhs)

    @classmethod
    def _evaluate(cls, *args, **kwargs) -> bool:
        """Implements the double comparison using the class-level operator."""
        lhs = cls._evaluate_lhs(*args, **kwargs)
        val = cls._evaluate_val(*args, **kwargs)
        rhs = cls._evaluate_rhs(*args, **kwargs)
        comparison_lhs = cls._comparison_operator_lhs()
        comparison_rhs = cls._comparison_operator_rhs()

        # Check that the comparison operators are valid and consistent. Both operators must point in the same direction:
        # either both ascending (< or <=) or both descending (> or >=). Mixed directions would not make logical sense
        # in a double comparison. _evaluate will always be called when creating an instance of the class, so this check
        # will always be performed.
        ascending_comparison_operators = {operator.lt, operator.le}
        descending_comparison_operators = {operator.gt, operator.ge}

        if not (
            {comparison_lhs, comparison_rhs} <= ascending_comparison_operators or {comparison_lhs, comparison_rhs} <= descending_comparison_operators
        ):
            raise ValueError(
                "Invalid comparison operators for double comparison formula. Both operators must point in the same direction: "
                "either both ascending ('operator.lt' or 'operator.le') or both descending ('operator.gt' or 'operator.ge')."
            )

        # Return the result of the double comparison
        return comparison_lhs(lhs, val) and comparison_rhs(val, rhs)
