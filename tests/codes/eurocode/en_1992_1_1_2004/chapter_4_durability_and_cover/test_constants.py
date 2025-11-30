"""Tests for constants for the calculation of nominal concrete cover according to EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.nominal_cover_constants import (
    AbrasionClass,
    CastingSurface,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.constants import NominalConcreteCoverConstants
from blueprints.type_alias import MM


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
        with pytest.raises(TypeError, match=r".* got an unexpected keyword argument .*"):
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
