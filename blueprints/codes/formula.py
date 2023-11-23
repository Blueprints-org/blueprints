"""Module for the abstract base class Formula."""
from abc import ABC, abstractmethod


class Formula(float, ABC):
    """
    Abstract base class for formulas used in the codes.
    """

    def __new__(cls, *args, **kwargs) -> "Formula":
        """Method for creating a new instance of the class."""
        result = cls.evaluate(*args, **kwargs)
        return float.__new__(cls, result)

    @property
    @abstractmethod
    def formula_label(self) -> str:
        """Property for the formula label.

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
    def evaluate(*args, **kwargs) -> float:
        """Abstract method for the logic of the formula.

        Returns
        -------
        float
            The result of the formula.
            This is an abstract method and must be implemented in all subclasses.
        """
