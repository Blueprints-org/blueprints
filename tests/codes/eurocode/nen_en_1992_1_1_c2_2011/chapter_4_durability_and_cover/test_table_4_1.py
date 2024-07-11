"""Tests for the Exposure classes
according to Table 4.1 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement.
"""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    FreezeThaw,
)


class TestCarbonation:
    """Testing Carbonation class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert Carbonation.options() == ["Not applicable", "XC1", "XC2", "XC3", "XC4"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert Carbonation.exposure_class_description() == "Corrosion induced by carbonation"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert Carbonation.XC1.description_of_the_environment() == "Dry or permanently wet"
        assert Carbonation.XC2.description_of_the_environment() == "Wet, rarely dry"
        assert Carbonation.XC3.description_of_the_environment() == "Moderate humidity"
        assert Carbonation.XC4.description_of_the_environment() == "Cyclic wet and dry"
        assert Carbonation.NA.description_of_the_environment() == "Not applicable"


class TestChloride:
    """Testing Chloride class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert Chloride.options() == ["Not applicable", "XD1", "XD2", "XD3"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert Chloride.exposure_class_description() == "Corrosion induced by chlorides other than by sea water"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert Chloride.XD1.description_of_the_environment() == "Moderate humidity"
        assert Chloride.XD2.description_of_the_environment() == "Wet, rarely dry"
        assert Chloride.XD3.description_of_the_environment() == "Cyclic wet and dry"
        assert Chloride.NA.description_of_the_environment() == "Not applicable"


class TestChlorideSeawater:
    """Testing ChlorideSeawater class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert ChlorideSeawater.options() == ["Not applicable", "XS1", "XS2", "XS3"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert ChlorideSeawater.exposure_class_description() == "Corrosion induced by chlorides from sea water"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert ChlorideSeawater.XS1.description_of_the_environment() == "Exposed to airborne salt but not in direct contact with sea water"
        assert ChlorideSeawater.XS2.description_of_the_environment() == "Permanently submerged"
        assert ChlorideSeawater.XS3.description_of_the_environment() == "Tidal, splash and spray zones"
        assert ChlorideSeawater.NA.description_of_the_environment() == "Not applicable"


class TestFreeze:
    """Testing Freeze class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert FreezeThaw.options() == ["Not applicable", "XF1", "XF2", "XF3", "XF4"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert FreezeThaw.exposure_class_description() == "Freeze/thaw attack with or without de-icing agents"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert FreezeThaw.XF1.description_of_the_environment() == "Moderate water saturation, without de-icing agent"
        assert FreezeThaw.XF2.description_of_the_environment() == "Moderate water saturation, with de-icing agent"
        assert FreezeThaw.XF3.description_of_the_environment() == "High water saturation, without de-icing agents"
        assert FreezeThaw.XF4.description_of_the_environment() == "High water saturation with de-icing agents or sea water"
        assert FreezeThaw.NA.description_of_the_environment() == "Not applicable"


class TestChemical:
    """Testing Chemical class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert Chemical.options() == ["Not applicable", "XA1", "XA2", "XA3"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert Chemical.exposure_class_description() == "Chemical attack"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert Chemical.XA1.description_of_the_environment() == "Slightly aggressive chemical environment according to EN 206-1, Table 2"
        assert Chemical.XA2.description_of_the_environment() == "Moderately aggressive chemical environment according to EN 206-1, Table 2"
        assert Chemical.XA3.description_of_the_environment() == "Highly aggressive chemical environment according to EN 206-1, Table 2"
        assert Chemical.NA.description_of_the_environment() == "Not applicable"


def test_comparing_different_types_raises_error() -> None:
    """Check if comparing different exposure class types, raises TypeError."""
    with pytest.raises(TypeError):
        _ = Carbonation.XC2 > Chloride.XD1
    with pytest.raises(TypeError):
        _ = Chloride.NA == Chemical.NA
    with pytest.raises(TypeError):
        _ = FreezeThaw.XF1 <= ChlorideSeawater.XS2
    with pytest.raises(TypeError):
        _ = ChlorideSeawater.XS3 >= Chloride.XD3
    with pytest.raises(TypeError):
        _ = Chemical.XA1 < Carbonation.XC2
    with pytest.raises(TypeError):
        _ = Chemical.NA != FreezeThaw.XF1
