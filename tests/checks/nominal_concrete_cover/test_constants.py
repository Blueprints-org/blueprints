"""Tests for constants classes for the calculation of nominal concrete cover."""

from dataclasses import dataclass, field

import pytest

from blueprints.checks.nominal_concrete_cover.constants.base import NominalConcreteCoverConstantsBase
from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass
from blueprints.type_alias import MM


@dataclass(frozen=True)
class DummyConstants(NominalConcreteCoverConstantsBase):
    """Dummy constants for testing purposes."""

    COVER_INCREATSE_FOR_ABRASION_CLASS: dict[AbrasionClass, MM] = field(default_factory=dict)
    COVER_INCREASE_FOR_UNEVEN_SURFACE: MM = 5
    DEFAULT_DELTA_C_DEV: MM = 5

    def __post_init__(self) -> None:
        """Post-initialization method to set default values."""
        if not self.COVER_INCREATSE_FOR_ABRASION_CLASS:
            abrasion_class_cover_increase = {
                "NA": 0,
                "XM1": 5,
                "XM2": 10,
                "XM3": 15,
            }
            object.__setattr__(self, "COVER_INCREATSE_FOR_ABRASION_CLASS", abrasion_class_cover_increase)

    @staticmethod
    def minimum_cover_with_regard_to_casting_surface(c_min_dur, casting_surface) -> MM:  # noqa: ANN001, ARG004
        """Dummy method for testing purposes."""
        return 0


class TestNominalConcreteCoverConstantsBase:
    """Tests for the base class for constants for the calculation of nominal concrete cover."""

    def test_abstract_method(self) -> None:
        """Test that the abstract method raises a TypeError."""
        with pytest.raises(TypeError):
            _ = NominalConcreteCoverConstantsBase(0, {}, 0)  # type: ignore[abstract]

    def test_instantiation(self) -> None:
        """Test that the class can be instantiated."""
        constants = DummyConstants()
        assert constants.COVER_INCREASE_FOR_UNEVEN_SURFACE == 5
        assert {
            "NA": 0,
            "XM1": 5,
            "XM2": 10,
            "XM3": 15,
        } == constants.COVER_INCREATSE_FOR_ABRASION_CLASS
        assert constants.DEFAULT_DELTA_C_DEV == 5
