"""Module for the abstract base class Equation."""
from abc import ABC, abstractmethod


class Equation(ABC):
    """
    Abstract base class for equations used in the code.
    """

    @property
    @abstractmethod
    def equation_label(self) -> str:
        """Property for the equation label.

        Returns
        -------
        str
            The label/number associated with the equation.
            This is an abstract method and must be implemented in all subclasses.
        """

    @property
    @abstractmethod
    def source_document(self) -> str:
        """Property for the source document.

        Returns
        -------
        str
            The reference to the document where the equation originates.
            This is an abstract method and must be implemented in all subclasses.
        """

    @property
    def detailed_result(self) -> dict:
        """Property for providing the detailed result of the equation.

        Returns
        -------
        dict
            The detailed result of the equation.
            keys are strings representing the name of the partial or intermediate result.
            Values types will depend on the specific implementation, but must be a serializable type.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def result(self):
        """Abstract property for the result of the equation.

        Returns
        -------
        The result of the equation. The return type will depend on the specific implementation.
        This is an abstract method and must be implemented in all subclasses.
        """
