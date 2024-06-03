"""Tests for the Exposure classes."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    Exposure,
    ExposureClasses,
    FreezeThaw,
)


class DummyExposureSubclass(Exposure):
    """Dummy Exposure subclass for testing purposes."""

    DUMMY1 = "Dummy1"
    DUMMY2 = "Dummy2"
    DUMMY3 = "Dummy3"

    @staticmethod
    def exposure_class_description() -> str:
        """Return the description of the DummyExposureSubclass."""
        return "Dummy exposure subclass"


class TestExposure:
    """Testing Exposure parent class."""

    def test_equal_to_operator(self) -> None:
        """Check if the == operator is working correctly."""
        assert DummyExposureSubclass.DUMMY1 == DummyExposureSubclass.DUMMY1
        assert DummyExposureSubclass.DUMMY2 == DummyExposureSubclass.DUMMY2
        assert DummyExposureSubclass.DUMMY3 == DummyExposureSubclass.DUMMY3

    def test_not_equal_to_operator(self) -> None:
        """Check if the != operator is working correctly."""
        assert DummyExposureSubclass.DUMMY1 != DummyExposureSubclass.DUMMY2
        assert DummyExposureSubclass.DUMMY2 != DummyExposureSubclass.DUMMY3
        assert DummyExposureSubclass.DUMMY3 != DummyExposureSubclass.DUMMY1

    def test_greather_than_operator(self) -> None:
        """Check if the > operator is working correctly."""
        assert DummyExposureSubclass.DUMMY3 > DummyExposureSubclass.DUMMY2
        assert DummyExposureSubclass.DUMMY2 > DummyExposureSubclass.DUMMY1

    def test_greather_than_equal_to_operator(self) -> None:
        """Check if the >= operator is working correctly."""
        # Testing greater than
        assert DummyExposureSubclass.DUMMY3 >= DummyExposureSubclass.DUMMY2
        assert DummyExposureSubclass.DUMMY2 >= DummyExposureSubclass.DUMMY1
        # Testing equal to
        assert DummyExposureSubclass.DUMMY3 >= DummyExposureSubclass.DUMMY3
        assert DummyExposureSubclass.DUMMY1 >= DummyExposureSubclass.DUMMY1

    def test_lesser_than_operator(self) -> None:
        """Check if the < operator is working correctly."""
        assert DummyExposureSubclass.DUMMY1 < DummyExposureSubclass.DUMMY2
        assert DummyExposureSubclass.DUMMY2 < DummyExposureSubclass.DUMMY3

    def test_lesser_than_equal_to_operator(self) -> None:
        """Check if the <= operator is working correctly."""
        # Testing lesser than
        assert DummyExposureSubclass.DUMMY1 <= DummyExposureSubclass.DUMMY2
        assert DummyExposureSubclass.DUMMY2 <= DummyExposureSubclass.DUMMY3
        # Testing equal to
        assert DummyExposureSubclass.DUMMY1 <= DummyExposureSubclass.DUMMY1
        assert DummyExposureSubclass.DUMMY3 <= DummyExposureSubclass.DUMMY3

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert DummyExposureSubclass.options() == ["Dummy1", "Dummy2", "Dummy3"]

    def test_description_not_implemented(self) -> None:
        """Check if the description method raises NotImplementedError if description method is not implemented."""
        with pytest.raises(NotImplementedError):
            Exposure.exposure_class_description()

    def test_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyExposureSubclass.exposure_class_description() == "Dummy exposure subclass"

    def test_description_of_the_environment_not_implemented(self) -> None:
        """Check if the description_of_the_environment method raises NotImplementedError if it is not implemented."""
        with pytest.raises(NotImplementedError):
            DummyExposureSubclass.DUMMY1.description_of_the_environment()


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


class TestExposureClasses:
    """Testing ExposureClasses class."""

    def test_str(self) -> None:
        """Check if the __str__ method returns the correct string representation of the exposure classes."""
        exposure_classes = ExposureClasses(
            carbonation=Carbonation("XC3"),
            chloride=Chloride("XD2"),
            chloride_seawater=ChlorideSeawater("Not applicable"),
            freeze=FreezeThaw("XF2"),
            chemical=Chemical("XA2"),
        )
        assert str(exposure_classes) == "XC3, XD2, XF2, XA2"

    def test_str_x0(self) -> None:
        """Check if the __str__ method returns the correct string representation of the exposure classes
        when all exposure classes are not applicable.
        """
        exposureclasses = ExposureClasses()
        assert str(exposureclasses) == "X0"

    def test_no_risk(self) -> None:
        """Check if the no_risk method returns True if the exposure classes are all not applicable."""
        exposureclasses = ExposureClasses()
        assert exposureclasses.no_risk is True

    def test_no_risk_false(self) -> None:
        """Check if the no_risk method returns False if at least one exposure class is applicable."""
        exposureclasses = ExposureClasses(
            carbonation=Carbonation("XC3"),
            chloride=Chloride("XD2"),
            chloride_seawater=ChlorideSeawater("Not applicable"),
            freeze=FreezeThaw("XF2"),
            chemical=Chemical("XA2"),
        )
        assert exposureclasses.no_risk is False


def test_comparing_different_types_raises_error() -> None:
    """Check if comparing different exposure class types, raises TypeError."""
    with pytest.raises(TypeError):
        Carbonation.XC2 > Chloride.XD1
    with pytest.raises(TypeError):
        Chloride.NA == Chemical.NA
    with pytest.raises(TypeError):
        FreezeThaw.XF1 <= ChlorideSeawater.XS2
    with pytest.raises(TypeError):
        ChlorideSeawater.XS3 >= Chloride.XD3
    with pytest.raises(TypeError):
        Chemical.XA1 < Carbonation.XC2
    with pytest.raises(TypeError):
        Chemical.NA != FreezeThaw.XF1
