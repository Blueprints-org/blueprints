"""Module for the abstract base class Formula."""

import operator
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self

from blueprints.codes.latex_formula import LatexFormula


class Formula(float, ABC):
    """Abstract base class for formulas used in the codes."""

    def __new__(cls, *args, **kwargs) -> "Formula":
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
        """Abstract method for the latex representation of the formula.

        Parameters
        ----------
        n : int, optional
            The number of decimal places to round the result to.

        Returns
        -------
        LatexFormula
            The latex representation of the formula.
            This is an abstract method and must be implemented in all subclasses.
        """


class ComparisonFormula(Formula):
    """Base class for comparison formulas used in the codes."""

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
        return self._lhs  # type: ignore[attr-defined]

    @property
    def rhs(self) -> float:
        """Property for getting the right-hand side of the comparison.

        Returns
        -------
        float
            The right-hand side value of the comparison.
        """
        return self._rhs  # type: ignore[attr-defined]

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
