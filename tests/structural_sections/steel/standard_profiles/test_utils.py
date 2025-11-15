"""Tests for utility functions in standard steel cross-section profiles."""

from __future__ import annotations

import pytest

from blueprints.structural_sections.steel.standard_profiles.utils import wrap_as_instance_method


class TestWrapAsInstanceMethod:
    """Tests for the wrap_as_instance_method decorator."""

    def test_wrapper_passes_instance_and_arguments(self) -> None:
        """Test that the wrapper forwards the instance and positional/keyword arguments."""
        calls = []

        def original(instance: Dummy, factor: int, *, offset: int = 0) -> int:
            calls.append((instance, factor, offset))
            return instance.base * factor + offset

        class Dummy:
            def __init__(self, base: int) -> None:
                self.base = base

            @wrap_as_instance_method(original)
            def method(self) -> None:
                pytest.fail("Placeholder should not execute.")

        dummy = Dummy(base=3)
        result = dummy.method(4, offset=2)

        assert result == 14
        assert calls == [(dummy, 4, 2)]

    def test_wrapper_preserves_original_metadata(self) -> None:
        """Test that the wrapper retains metadata defined on the original function."""

        def original(instance: DummyValue) -> str:
            """Original function docstring."""
            return f"value={instance.value}"

        class DummyValue:
            def __init__(self, value: int) -> None:
                self.value = value

            @wrap_as_instance_method(original)
            def method(self) -> None:
                pytest.fail("Placeholder should not execute.")

        assert DummyValue.method.__name__ == original.__name__
        assert DummyValue.method.__doc__ == original.__doc__

        dummy = DummyValue(value=7)
        assert dummy.method() == "value=7"

    def test_decorator_can_be_reused_across_classes(self) -> None:
        """Test that a single decorator instance can wrap multiple class methods."""

        def original(instance, increment: int = 0) -> int:  # noqa: ANN001
            return instance.base + increment

        class Alpha:
            def __init__(self, base: int) -> None:
                self.base = base

            @wrap_as_instance_method(original)
            def as_value(self) -> None:
                pytest.fail("Placeholder should not execute.")

        class Beta:
            def __init__(self, base: int) -> None:
                self.base = base

            @wrap_as_instance_method(original)
            def as_value(self) -> None:
                pytest.fail("Placeholder should not execute.")

        assert Alpha(base=2).as_value(increment=3) == 5
        assert Beta(base=10).as_value(increment=1) == 11

    def test_decorator_can_be_used_across_multiple_methods(self) -> None:
        """Test that a single decorator instance can wrap multiple methods within the same class."""

        def custom_increment(instance: Counter, step: int = 1) -> int:
            instance.count += step
            return instance.count

        def custom_subtract(instance: Counter, value: int) -> int:
            instance.count -= value
            return instance.count

        class Counter:
            def __init__(self) -> None:
                self.count = 0

            @wrap_as_instance_method(custom_increment)
            def increment(self) -> None:
                pytest.fail("Placeholder should not execute.")

            @wrap_as_instance_method(custom_subtract)
            def subtract(self) -> None:
                pytest.fail("Placeholder should not execute.")

        counter = Counter()
        assert counter.increment() == 1
        assert counter.subtract(5) == -4
        assert counter.increment(7) == 3
