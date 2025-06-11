"""Tests for constants classes for the calculation of nominal concrete cover."""

from dataclasses import dataclass, field

import pytest

from blueprints.checks.nominal_concrete_cover.constants.base import NominalConcreteCoverConstantsBase
from blueprints.checks.nominal_concrete_cover.constants.constants_en_1992_1_1_2004 import NominalConcreteCoverConstants
from blueprints.checks.nominal_concrete_cover.constants.constants_nen_en_1992_1_1_a1_2020 import NominalConcreteCoverConstants2020A1
from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass, CastingSurface
from blueprints.type_alias import MM


@dataclass(frozen=True)
class DummyConstants(NominalConcreteCoverConstantsBase):
    """Dummy constants for testing purposes."""

    CODE_SUFFIX: str = "DUMMY"
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
            _ = NominalConcreteCoverConstantsBase("_", 0, {}, 0)  # type: ignore[abstract]

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
        assert constants.CODE_SUFFIX == "DUMMY"
        assert constants.minimum_cover_with_regard_to_casting_surface(0, CastingSurface.PERMANENTLY_EXPOSED) == 0
        assert constants.minimum_cover_with_regard_to_casting_surface_latex(CastingSurface.PERMANENTLY_EXPOSED) == ""


class TestNominalConcreteCoverConstants2004:
    """Tests for the constants class for the calculation of nominal concrete cover according to EN 1992-1-1:2004."""

    def test_instantiation(self) -> None:
        """Test that the class can be instantiated."""
        constants = NominalConcreteCoverConstants()
        assert constants.COVER_INCREASE_FOR_UNEVEN_SURFACE == 5
        assert constants.COVER_INCREASE_FOR_ABRASION_CLASS == {
            AbrasionClass.NA: 0,
            AbrasionClass.XM1: 5,
            AbrasionClass.XM2: 10,
            AbrasionClass.XM3: 15,
        }
        assert constants.DEFAULT_DELTA_C_DEV == 10

    def test_instantiation_with_custom_cover_increase_uneven_surfaces(self) -> None:
        """Test that the class cannot be instantiated with custom value for the cover increase for uneven surfaces."""
        with pytest.raises(TypeError, match=".* got an unexpected keyword argument .*"):
            _ = NominalConcreteCoverConstants(  # type: ignore[call-arg]
                COVER_INCREASE_FOR_UNEVEN_SURFACE=10,
            )

    def test_instantiation_with_custom_cover_increase_abraison_class(self) -> None:
        """Test that the class can be instantiated with custom value for the cover increase for abrasion class."""
        custom_constants = NominalConcreteCoverConstants(  # type: ignore[call-arg]
            COVER_INCREASE_FOR_ABRASION_CLASS={
                AbrasionClass.NA: 0,
            },
        )
        assert custom_constants.COVER_INCREASE_FOR_ABRASION_CLASS == {
            AbrasionClass.NA: 0,
        }

    def test_instantiation_with_custom_delta_c_dev(self) -> None:
        """Test that the class can be instantiated with custom value for the default delta c_dev."""
        custom_constants = NominalConcreteCoverConstants(  # type: ignore[call-arg]
            DEFAULT_DELTA_C_DEV=13,
        )
        assert custom_constants.DEFAULT_DELTA_C_DEV == 13

    def test_instantiation_with_default_delta_c_dev(self) -> None:
        """Test that the class can be instantiated with default value for the default delta c_dev."""
        custom_constants = NominalConcreteCoverConstants()
        assert custom_constants.DEFAULT_DELTA_C_DEV == 10  # Default value

    def test_post_init(self) -> None:
        """Test that the post-init method sets default values."""
        constants = NominalConcreteCoverConstants()
        assert constants.COVER_INCREASE_FOR_ABRASION_CLASS == {
            AbrasionClass.NA: 0,
            AbrasionClass.XM1: 5,
            AbrasionClass.XM2: 10,
            AbrasionClass.XM3: 15,
        }

    @pytest.mark.parametrize(
        ("c_min_dur", "casting_surface", "expected_result"),
        [
            (10, CastingSurface.PERMANENTLY_EXPOSED, 0),
            (10, CastingSurface.FORMWORK, 0),
            (10, CastingSurface.PREPARED_GROUND, 50),
            (10, CastingSurface.DIRECTLY_AGAINST_SOIL, 85),
        ],
    )
    def test_minimum_cover_with_regard_to_casting_surface(self, c_min_dur: MM, casting_surface: CastingSurface, expected_result: MM) -> None:
        """Test the method for the calculation of the minimum cover with regard to casting surface."""
        constants = NominalConcreteCoverConstants()
        assert constants.minimum_cover_with_regard_to_casting_surface(c_min_dur, casting_surface) == expected_result

    @pytest.mark.parametrize(
        ("casting_surface", "expected_result"),
        [
            (CastingSurface.PERMANENTLY_EXPOSED, "0 (No additional requirements for Permanently exposed)"),
            (CastingSurface.FORMWORK, "0 (No additional requirements for Formwork)"),
            (CastingSurface.PREPARED_GROUND, "k1 \\ge c_{min,dur} + 40 mm for Prepared ground (including blinding)"),
            (CastingSurface.DIRECTLY_AGAINST_SOIL, "k2 \\ge c_{min,dur} + 75 mm for Directly against soil"),
        ],
    )
    def test_minimum_cover_with_regard_to_casting_surface_latex(self, casting_surface: CastingSurface, expected_result: str) -> None:
        """Test the method for the calculation of the minimum cover with regard to casting surface in LaTeX."""
        constants = NominalConcreteCoverConstants()
        assert constants.minimum_cover_with_regard_to_casting_surface_latex(casting_surface) == expected_result


class TestNominalConcreteCoverConstants2020A1:
    """Tests for the constants class for the calculation of nominal concrete cover according to NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020."""

    def test_instantiation(self) -> None:
        """Test that the class can be instantiated."""
        constants = NominalConcreteCoverConstants2020A1()
        assert constants.COVER_INCREASE_FOR_UNEVEN_SURFACE == 5
        assert constants.COVER_INCREASE_FOR_ABRASION_CLASS == {
            AbrasionClass.NA: 0,
            AbrasionClass.XM1: 0,
            AbrasionClass.XM2: 0,
            AbrasionClass.XM3: 0,
        }
        assert constants.DEFAULT_DELTA_C_DEV == 5

    def test_instantiation_with_custom_cover_increase_uneven_surfaces(self) -> None:
        """Test that the class cannot be instantiated with custom value for the cover increase for uneven surfaces."""
        with pytest.raises(TypeError, match=".* got an unexpected keyword argument .*"):
            _ = NominalConcreteCoverConstants2020A1(  # type: ignore[call-arg]
                COVER_INCREASE_FOR_UNEVEN_SURFACE=10,
            )

    def test_instantiation_with_custom_cover_increase_abraison_class(self) -> None:
        """Test that the class can be instantiated with custom value for the cover increase for abrasion class."""
        custom_constants = NominalConcreteCoverConstants2020A1(  # type: ignore[call-arg]
            COVER_INCREASE_FOR_ABRASION_CLASS={
                AbrasionClass.NA: 0,
            },
        )
        assert custom_constants.COVER_INCREASE_FOR_ABRASION_CLASS == {
            AbrasionClass.NA: 0,
        }

    def test_instantiation_with_custom_delta_c_dev(self) -> None:
        """Test that the class can be instantiated with custom value for the default delta c_dev."""
        custom_constants = NominalConcreteCoverConstants2020A1(  # type: ignore[call-arg]
            DEFAULT_DELTA_C_DEV=13,
        )
        assert custom_constants.DEFAULT_DELTA_C_DEV == 13

    def test_instantiation_with_default_delta_c_dev(self) -> None:
        """Test that the class can be instantiated with default value for the default delta c_dev."""
        custom_constants = NominalConcreteCoverConstants2020A1()
        assert custom_constants.DEFAULT_DELTA_C_DEV == 5  # Default value

    def test_post_init(self) -> None:
        """Test that the post-init method sets default values."""
        constants = NominalConcreteCoverConstants2020A1()
        assert constants.COVER_INCREASE_FOR_ABRASION_CLASS == {
            AbrasionClass.NA: 0,
            AbrasionClass.XM1: 0,
            AbrasionClass.XM2: 0,
            AbrasionClass.XM3: 0,
        }

    @pytest.mark.parametrize(
        ("c_min_dur", "casting_surface", "expected_result"),
        [
            (10, CastingSurface.PERMANENTLY_EXPOSED, 0),
            (10, CastingSurface.FORMWORK, 0),
            (10, CastingSurface.PREPARED_GROUND, 20),
            (10, CastingSurface.DIRECTLY_AGAINST_SOIL, 60),
        ],
    )
    def test_minimum_cover_with_regard_to_casting_surface(self, c_min_dur: MM, casting_surface: CastingSurface, expected_result: MM) -> None:
        """Test the method for the calculation of the minimum cover with regard to casting surface."""
        constants = NominalConcreteCoverConstants2020A1()
        assert constants.minimum_cover_with_regard_to_casting_surface(c_min_dur, casting_surface) == expected_result

    @pytest.mark.parametrize(
        ("casting_surface", "expected_result"),
        [
            (CastingSurface.PERMANENTLY_EXPOSED, "0 (No additional requirements for Permanently exposed)"),
            (CastingSurface.FORMWORK, "0 (No additional requirements for Formwork)"),
            (CastingSurface.PREPARED_GROUND, "k1 \\ge c_{min,dur} + 10 mm for Prepared ground (including blinding)"),
            (CastingSurface.DIRECTLY_AGAINST_SOIL, "k2 \\ge c_{min,dur} + 50 mm for Directly against soil"),
        ],
    )
    def test_minimum_cover_with_regard_to_casting_surface_latex(self, casting_surface: CastingSurface, expected_result: str) -> None:
        """Test the method for the calculation of the minimum cover with regard to casting surface in LaTeX."""
        constants = NominalConcreteCoverConstants2020A1()
        assert constants.minimum_cover_with_regard_to_casting_surface_latex(casting_surface) == expected_result
