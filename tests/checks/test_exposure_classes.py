"""Tests for the Exposure classes."""

import pytest

from blueprints.checks.concrete_cover.exposure_classes import Carbonation, Chemical, Chloride, ChlorideSeawater, Exposure, ExposureClasses, Freeze


class DummyExposureSubclass(Exposure):
    """Dummy Exposure subclass for testing purposes."""

    DUMMY1 = "Dummy1"
    DUMMY2 = "Dummy2"
    DUMMY3 = "Dummy3"

    @staticmethod
    def description() -> str:
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
            Exposure.description()

    def test_description_implemented(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert DummyExposureSubclass.description() == "Dummy exposure subclass"


class TestCarbonation:
    """Testing Carbonation class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert Carbonation.options() == ["Not applicable", "XC1", "XC2", "XC3", "XC4"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert Carbonation.description() == "Corrosion induced by carbonation"


class TestChloride:
    """Testing Chloride class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert Chloride.options() == ["Not applicable", "XD1", "XD2", "XD3"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert Chloride.description() == "Corrosion induced by chlorides other than by sea water"


class TestChlorideSeawater:
    """Testing ChlorideSeawater class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert ChlorideSeawater.options() == ["Not applicable", "XS1", "XS2", "XS3"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert ChlorideSeawater.description() == "Corrosion induced by chlorides from sea water"


class TestFreeze:
    """Testing Freeze class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert Freeze.options() == ["Not applicable", "XF1", "XF2", "XF3", "XF4"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert Freeze.description() == "Freeze/thaw attack with or without de-icing agents"


class TestChemical:
    """Testing Chemical class."""

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert Chemical.options() == ["Not applicable", "XA1", "XA2", "XA3"]

    def test_description(self) -> None:
        """Check if the description method returns the description of the subclass."""
        assert Chemical.description() == "Chemical attack"


class TestExposureClasses:
    """Testing ExposureClasses class."""

    def test_str(self) -> None:
        """Check if the __str__ method returns the correct string representation of the exposure classes."""
        exposure_classes = ExposureClasses(
            carbonation=Carbonation("XC3"),
            chloride=Chloride("XD2"),
            chloride_seawater=ChlorideSeawater("Not applicable"),
            freeze=Freeze("XF2"),
            chemical=Chemical("XA2"),
        )
        assert str(exposure_classes) == ("XC3, XD2, XF2, XA2")


def test_comparing_different_types_raises_error() -> None:
    """Check if comparing different exposure class types, raises TypeError."""
    with pytest.raises(TypeError):
        Carbonation.XC2 > Chloride.XD1
    with pytest.raises(TypeError):
        Chloride.NA == Chemical.NA
    with pytest.raises(TypeError):
        Freeze.XF1 <= ChlorideSeawater.XS2
    with pytest.raises(TypeError):
        ChlorideSeawater.XS3 >= Chloride.XD3
    with pytest.raises(TypeError):
        Chemical.XA1 < Carbonation.XC2
    with pytest.raises(TypeError):
        Chemical.NA != Freeze.XF1
