"""Module for the abstract base class Formula."""

from abc import ABC, abstractmethod

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

    def __new__(cls, *args, **kwargs) -> "ComparisonFormula":
        """Method for creating a new instance of the class."""
        lhs = cls._evaluate_lhs(*args, **kwargs)
        rhs = cls._evaluate_rhs(*args, **kwargs)
        result = cls._evaluate(*args, **kwargs)
        instance = float.__new__(cls, result)
        instance._lhs = lhs  # noqa: SLF001
        instance._rhs = rhs  # noqa: SLF001
        instance._initialized = False  # noqa: SLF001
        return instance

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
    @abstractmethod
    def unity_check(self) -> float:
        """Property to present the unity check of the formula.

        Returns
        -------
        float
            The unity check.
        """
