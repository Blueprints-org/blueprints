"""Tests for constants classes for the calculation of nominal concrete cover."""

from dataclasses import dataclass, field

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.nominal_cover_constants import (
    AbrasionClass,
    CastingSurface,
    NominalConcreteCoverConstantsBase,
)
from blueprints.type_alias import MM


@dataclass(frozen=True)
class DummyConstants(NominalConcreteCoverConstantsBase):
    """Dummy constants for testing purposes."""

    CODE_PREFIX: str = "DUMMY_PREFIX-"
    CODE_SUFFIX: str = ":DUMMY_SUFFIX"
    COVER_INCREASE_FOR_ABRASION_CLASS: dict[AbrasionClass, MM] = field(default_factory=dict)
    COVER_INCREASE_FOR_UNEVEN_SURFACE: MM = 5
    DEFAULT_DELTA_C_DEV: MM = 5

    def __post_init__(self) -> None:
        """Post-initialization method to set default values."""
        if not self.COVER_INCREASE_FOR_ABRASION_CLASS:
            abrasion_class_cover_increase = {
                "NA": 0,
                "XM1": 5,
                "XM2": 10,
                "XM3": 15,
            }
            object.__setattr__(self, "COVER_INCREASE_FOR_ABRASION_CLASS", abrasion_class_cover_increase)

    @staticmethod
    def minimum_cover_with_regard_to_casting_surface(c_min_dur, casting_surface) -> MM:  # noqa: ANN001, ARG004
        """Dummy method for testing purposes."""
        return 0

    @staticmethod
    def minimum_cover_with_regard_to_casting_surface_latex(casting_surface) -> str:  # noqa: ANN001, ARG004
        """Dummy method for testing purposes."""
        return ""


class TestNominalConcreteCoverConstantsBase:
    """Tests for the base class for constants for the calculation of nominal concrete cover."""

    def test_abstract_method(self) -> None:
        """Test that the abstract method raises a TypeError."""
        with pytest.raises(TypeError):
            _ = NominalConcreteCoverConstantsBase("_", "_", 0, {}, 0)  # type: ignore[abstract]

    def test_instantiation(self) -> None:
        """Test that the class can be instantiated."""
        constants = DummyConstants()
        assert constants.COVER_INCREASE_FOR_UNEVEN_SURFACE == 5
        assert constants.COVER_INCREASE_FOR_ABRASION_CLASS == {
            "NA": 0,
            "XM1": 5,
            "XM2": 10,
            "XM3": 15,
        }
        assert constants.DEFAULT_DELTA_C_DEV == 5
        assert constants.CODE_PREFIX == "DUMMY_PREFIX-"
        assert constants.CODE_SUFFIX == ":DUMMY_SUFFIX"
        assert constants.minimum_cover_with_regard_to_casting_surface(0, CastingSurface.PERMANENTLY_EXPOSED) == 0
        assert constants.minimum_cover_with_regard_to_casting_surface_latex(CastingSurface.PERMANENTLY_EXPOSED) == ""
