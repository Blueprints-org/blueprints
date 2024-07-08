"""Fixtures for the tests in the utils module."""

import pytest

from blueprints.utils.abc_enum_meta import ABCEnumMeta


class AttributeErrorEnumMeta(ABCEnumMeta):
    """Custom metaclass to simulate AttributeError for testing."""

    def __new__(cls, *args, **kwargs):
        # Simulate the presence of _member_map_ to bypass the initial check
        abstract_enum_cls = super().__new__(cls, *args, **kwargs)
        setattr(abstract_enum_cls, "_member_map_", True)
        raise AttributeError("Simulated AttributeError for testing")
        return abstract_enum_cls


@pytest.fixture()
def attribute_error_enum_meta():
    """Fixture that returns an instance of the AttributeErrorEnumMeta for testing."""
    return AttributeErrorEnumMeta
