"""Tests for the ABCEnumMeta class."""

from abc import ABCMeta, abstractmethod
from enum import Enum, EnumMeta

import pytest

from blueprints.utils.abc_enum_meta import ABCEnumMeta


class MockAbstractEnum(Enum, metaclass=ABCEnumMeta):
    """Mock class for testing the ABCEnumMeta class."""

    @abstractmethod
    def test_method(self) -> int:
        """Test method for the MockAbstractEnum class."""


class MockConcreteEnum(MockAbstractEnum):
    """Mock class for testing the ABCEnumMeta class."""

    A = "a"
    B = "b"

    def test_method(self) -> int:
        """Test method for the MockConcreteEnum class."""
        return 1


class TestABCEnumMeta:
    """Test class for ABCEnumMeta."""

    def test_inheritance(self) -> None:
        """Test if ABCEnumMeta inherits from ABCMeta and EnumMeta."""
        assert issubclass(ABCEnumMeta, ABCMeta)
        assert issubclass(ABCEnumMeta, EnumMeta)

    def test_mock_abstract_enum(self) -> None:
        """Test case for MockAbstractEnum class."""
        with pytest.raises(TypeError):
            _ = MockAbstractEnum("a")

    def test_mock_concrete_enum(self) -> None:
        """Test case for MockConcreteEnum class."""
        assert MockConcreteEnum.A.value == "a"
        assert MockConcreteEnum.B.value == "b"
        assert MockConcreteEnum.B.test_method() == 1

    def test_invalid_mock_concrete_enum(self) -> None:
        """Test case for InvalidMockConcreteEnum class."""
        with pytest.raises(TypeError) as error_info:

            class InvalidMockConcreteEnum(MockAbstractEnum):
                """Mock class for testing the ABCEnumMeta class."""

                A = "a"
                B = "b"

        assert str(error_info.value).endswith("without an implementation for abstract method 'test_method'")

    def test_abc_enum_meta_attribute_error(self) -> None:
        """
        Test instantiation of class with ABCEnumMeta where no abstract methods attribute is present.
        Expect successful instantiation due to handling AttributeError (pass if AttributeError is raised).
        """

        class NoAbstractMethodsEnum(Enum, metaclass=ABCEnumMeta):
            ONE = 1
            TWO = 2

        assert NoAbstractMethodsEnum.ONE.value == 1


def test_abc_enum_meta_attribute_error_handling(attribute_error_enum_meta: ABCEnumMeta) -> None:
    """
    Test instantiation of class with custom metaclass that raises AttributeError.
    Ensure instantiation proceeds due to handling AttributeError.
    """

    class TestEnum(Enum, metaclass=attribute_error_enum_meta):
        ONE = 1
        TWO = 2

    # Check if the class was instantiated without raising an exception
    assert TestEnum.ONE.value == 1
