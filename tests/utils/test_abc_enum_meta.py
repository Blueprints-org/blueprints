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

    def test_mock_abstract_enum_is_abstract(self) -> None:
        """Test case for MockAbstractEnum class to check if it's an abstract class."""
        assert MockAbstractEnum.__abstractmethods__ == frozenset({"test_method"})

    def test_abstract_enum_with_memebers_raises_type_error(self) -> None:
        """Test case for MockAbstractEnumWithMembers class to check if it raises a TypeError."""
        with pytest.raises(TypeError) as error_info:

            class MockAbstractEnumWithMembers(Enum, metaclass=ABCEnumMeta):
                """Mock class with members for testing the ABCEnumMeta class."""

                A = "a"

                @abstractmethod
                def test_method(self) -> int:
                    """Test method for the MockAbstractEnum class."""

        assert (
            str(error_info.value)
            == "Can't instantiate abstract class 'MockAbstractEnumWithMembers' without an implementation for abstract method 'test_method'"
        )

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
        """Test instantiation of class with ABCEnumMeta where no abstract methods attribute is present."""

        class NoAbstractMethodsEnum(Enum, metaclass=ABCEnumMeta):
            ONE = 1
            TWO = 2

        assert NoAbstractMethodsEnum.ONE.value == 1
