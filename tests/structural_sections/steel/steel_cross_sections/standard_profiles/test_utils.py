"""Tests for utility functions in standard steel cross-section profiles."""

from __future__ import annotations

import pytest

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.utils import AsCrossSection


class TestAsCrossSection:
    """Tests for the AsCrossSection descriptor."""

    def test_descriptor_initialization(self) -> None:
        """Test that the descriptor is properly initialized with a function."""

        def mock_function(obj: object) -> str:  # noqa: ARG001
            return "mock_result"

        descriptor = AsCrossSection(mock_function)
        # Test that the descriptor holds the function (using indirect testing since _func is private)
        assert hasattr(descriptor, "_func")

    def test_descriptor_get_with_instance(self) -> None:
        """Test that the descriptor returns a bound method when accessed on an instance."""

        def create_from_instance(instance: object, multiplier: int = 1) -> str:
            return f"{getattr(instance, 'value', 'unknown')}_multiplied_{multiplier}"

        class MockClass:
            def __init__(self, value: str) -> None:
                self.value = value

            method = AsCrossSection(create_from_instance)

        obj = MockClass("test")
        bound_method = obj.method

        # Test that the bound method works correctly
        result = bound_method(multiplier=2)
        assert result == "test_multiplied_2"

        # Test with default parameters
        result_default = bound_method()
        assert result_default == "test_multiplied_1"

    def test_descriptor_get_without_instance_raises_error(self) -> None:
        """Test that accessing the descriptor on the class (not instance) raises AttributeError."""

        class MockClass:
            @classmethod
            def create_from_instance(cls) -> str:
                return "result"

            method = AsCrossSection(create_from_instance)

        with pytest.raises(AttributeError, match="Cannot access instance method on the class itself."):
            MockClass.method  # type: ignore[arg-type]

    def test_descriptor_with_args_and_kwargs(self) -> None:
        """Test that the descriptor correctly passes args and kwargs to the underlying function."""

        def test_function(
            obj: object,
            arg1: str,
            arg2: str,
            kwarg1: str | None = None,
            kwarg2: str | None = None,
        ) -> dict[str, object]:
            return {
                "obj_value": getattr(obj, "value", None),
                "arg1": arg1,
                "arg2": arg2,
                "kwarg1": kwarg1,
                "kwarg2": kwarg2,
            }

        class MockClass:
            def __init__(self, value: str) -> None:
                self.value = value

            method = AsCrossSection(test_function)

        obj = MockClass("test_obj")
        result = obj.method("pos_arg1", "pos_arg2", kwarg1="kw_val1", kwarg2="kw_val2")

        expected = {
            "obj_value": "test_obj",
            "arg1": "pos_arg1",
            "arg2": "pos_arg2",
            "kwarg1": "kw_val1",
            "kwarg2": "kw_val2",
        }
        assert result == expected

    def test_descriptor_multiple_instances(self) -> None:
        """Test that the descriptor works correctly with multiple instances of the same class."""

        def instance_method(obj: object, suffix: str = "") -> str:
            return f"{getattr(obj, 'name', '')}{suffix}"

        class MockClass:
            def __init__(self, name: str) -> None:
                self.name = name

            get_name = AsCrossSection(instance_method)

        obj1 = MockClass("first")
        obj2 = MockClass("second")

        assert obj1.get_name() == "first"
        assert obj2.get_name() == "second"
        assert obj1.get_name("_suffix") == "first_suffix"
        assert obj2.get_name("_suffix") == "second_suffix"

    def test_real_usage_with_chs_profile(self) -> None:
        """Test the descriptor with actual CHS profile usage."""
        profile = CHS.CHS21_3x2_3

        # Test that as_cross_section method exists and is callable
        assert hasattr(profile, "as_cross_section")
        assert callable(profile.as_cross_section)

        # Test that it returns a cross-section object
        cross_section = profile.as_cross_section()
        assert cross_section is not None

        # Test with corrosion parameters
        cross_section_with_corrosion = profile.as_cross_section(
            corrosion_outside=0.5,
            corrosion_inside=0.3,
        )
        assert cross_section_with_corrosion is not None

    def test_descriptor_type_annotations(self) -> None:
        """Test that the descriptor works with proper type annotations."""

        def typed_function(obj: MockClass, value: int) -> str:
            return f"{obj.data}_{value}"

        class MockClass:
            def __init__(self, data: str) -> None:
                self.data = data

            process = AsCrossSection(typed_function)

        obj = MockClass("test_data")
        result = obj.process(42)
        assert result == "test_data_42"

    def test_descriptor_exception_handling(self) -> None:
        """Test that exceptions in the underlying function are properly propagated."""

        def failing_function(_obj: object, should_fail: bool = True) -> str:
            if should_fail:
                raise ValueError("Test exception")
            return "success"

        class MockClass:
            method = AsCrossSection(failing_function)

        obj = MockClass()

        # Test that exception is raised
        with pytest.raises(ValueError, match="Test exception"):
            obj.method()

        # Test that method works when not failing
        result = obj.method(should_fail=False)
        assert result == "success"

    def test_descriptor_with_no_args_function(self) -> None:
        """Test that the descriptor works with functions that take only the instance."""

        def simple_function(obj: object) -> str:  # noqa: ARG001
            return "simple_result"

        class MockClass:
            method = AsCrossSection(simple_function)

        obj = MockClass()
        result = obj.method()
        assert result == "simple_result"
