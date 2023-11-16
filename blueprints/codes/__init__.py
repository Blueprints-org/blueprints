"""Module for the abstract base class Equation."""
from abc import ABC, abstractmethod


class Equation(ABC):
    """
    Abstract base class for equations used in the code.
    """

    @property
    def equation_number(self) -> str:
        """
        Property for the equation number.

        Returns
        -------
        str
            The number associated with the equation.
            This method can be optionally overridden in subclasses.
        """
        raise NotImplementedError

    @property
    def source_document(self) -> str:
        """
        Property for the source document.

        Returns
        -------
        str
            The reference to the document where the equation originates.
            This method can be optionally overridden in subclasses.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def result(self):
        """
        Abstract property for the result of the equation.

        Returns
        -------
        The result of the equation. The return type will depend on the specific implementation.
        This is an abstract method and must be implemented in all subclasses.
        """
