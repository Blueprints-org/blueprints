"""Tests for the Exposure classes."""

import pytest

from blueprints.codes.eurocode.exposure_classes import (
    CarbonationBase,
    ChemicalBase,
    ChlorideBase,
    ChlorideSeawaterBase,
    Exposure,
    ExposureClassesBase,
    FreezeThawBase,
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

    def description_of_the_environment(self) -> str:
        """Return the description of the environment."""
        return "Dummy environment"


class DummyCarbonation(CarbonationBase):
    """Dummy Carbonation subclass for testing purposes."""

    NA = "Not applicable"
    XC1 = "XC1"

    @staticmethod
    def exposure_class_description() -> str:
        """Return the description of the DummyCarbonation."""
        return "Dummy carbonation subclass"

    def description_of_the_environment(self) -> str:
        """Return the description of the environment."""
        return "Dummy environment"


class DummyChloride(ChlorideBase):
    """Dummy Chloride subclass for testing purposes."""

    NA = "Not applicable"
    XD1 = "XD1"

    @staticmethod
    def exposure_class_description() -> str:
        """Return the description of the DummyChloride."""
        return "Dummy chloride subclass"

    def description_of_the_environment(self) -> str:
        """Return the description of the environment."""
        return "Dummy environment"


class DummyChlorideSeawater(ChlorideSeawaterBase):
    """Dummy ChlorideSeawater subclass for testing purposes."""

    NA = "Not applicable"
    XS1 = "XS1"

    @staticmethod
    def exposure_class_description() -> str:
        """Return the description of the DummyChlorideSeawater."""
        return "Dummy chloride seawater subclass"

    def description_of_the_environment(self) -> str:
        """Return the description of the environment."""
        return "Dummy environment"


class DummyFreezeThaw(FreezeThawBase):
    """Dummy FreezeThaw subclass for testing purposes."""

    NA = "Not applicable"
    XF1 = "XF1"

    @staticmethod
    def exposure_class_description() -> str:
        """Return the description of the DummyFreezeThaw."""
        return "Dummy freeze thaw subclass"

    def description_of_the_environment(self) -> str:
        """Return the description of the environment."""
        return "Dummy environment"


class DummyChemical(ChemicalBase):
    """Dummy Chemical subclass for testing purposes."""

    NA = "Not applicable"
    XA1 = "XA1"

    @staticmethod
    def exposure_class_description() -> str:
        """Return the description of the DummyChemical."""
        return "Dummy chemical subclass"

    def description_of_the_environment(self) -> str:
        """Return the description of the environment."""
        return "Dummy environment"


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

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyExposureSubclass.exposure_class_description() == "Dummy exposure subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyExposureSubclass.DUMMY1.description_of_the_environment() == "Dummy environment"


class TestCarbonation:
    """Testing CarbonationBase class."""

    def test_initiate_subclasses(self) -> None:
        """Check if initiating the CarbonationBase class raises a TypeError."""
        with pytest.raises(TypeError):
            _ = CarbonationBase()  # type: ignore[abstract, call-arg]

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyCarbonation.exposure_class_description() == "Dummy carbonation subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyCarbonation.XC1.description_of_the_environment() == "Dummy environment"


class TestChloride:
    """Testing ChlorideBase class."""

    def test_initiate_subclasses(self) -> None:
        """Check if initiating the ChlorideBase class raises a TypeError."""
        with pytest.raises(TypeError):
            _ = ChlorideBase()  # type: ignore[abstract, call-arg]

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyChloride.exposure_class_description() == "Dummy chloride subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyChloride.XD1.description_of_the_environment() == "Dummy environment"


class TestChlorideSeawater:
    """Testing ChlorideSeawaterBase class."""

    def test_initiate_subclasses(self) -> None:
        """Check if initiating the ChlorideSeawaterBase class raises a TypeError."""
        with pytest.raises(TypeError):
            _ = ChlorideSeawaterBase()  # type: ignore[abstract, call-arg]

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyChlorideSeawater.exposure_class_description() == "Dummy chloride seawater subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyChlorideSeawater.XS1.description_of_the_environment() == "Dummy environment"


class TestFreezeThaw:
    """Testing FreezeThawBase class."""

    def test_initiate_subclasses(self) -> None:
        """Check if initiating the FreezeThawBase class raises a TypeError."""
        with pytest.raises(TypeError):
            _ = FreezeThawBase()  # type: ignore[abstract, call-arg]

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyFreezeThaw.exposure_class_description() == "Dummy freeze thaw subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyFreezeThaw.XF1.description_of_the_environment() == "Dummy environment"


class TestChemical:
    """Testing ChemicalBase class."""

    def test_initiate_subclasses(self) -> None:
        """Check if initiating the ChemicalBase class raises a TypeError."""
        with pytest.raises(TypeError):
            _ = ChemicalBase()  # type: ignore[abstract, call-arg]

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyChemical.exposure_class_description() == "Dummy chemical subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyChemical.XA1.description_of_the_environment() == "Dummy environment"


class TestExposureClasses:
    """Testing ExposureClasses class."""

    def test_str(self) -> None:
        """Check if the __str__ method returns the correct string representation of the exposure classes."""
        exposure_classes = ExposureClassesBase(
            carbonation=DummyCarbonation("XC1"),
            chloride=DummyChloride("XD1"),
            chloride_seawater=DummyChlorideSeawater("Not applicable"),
            freeze=DummyFreezeThaw("XF1"),
            chemical=DummyChemical("XA1"),
        )
        assert str(exposure_classes) == "XC1, XD1, XF1, XA1"

    def test_str_x0(self) -> None:
        """Check if the __str__ method returns the correct string representation of the exposure classes
        when all exposure classes are not applicable.
        """
        exposureclasses = ExposureClassesBase(
            carbonation=DummyCarbonation("Not applicable"),
            chloride=DummyChloride("Not applicable"),
            chloride_seawater=DummyChlorideSeawater("Not applicable"),
            freeze=DummyFreezeThaw("Not applicable"),
            chemical=DummyChemical("Not applicable"),
        )
        assert str(exposureclasses) == "X0"

    def test_no_risk(self) -> None:
        """Check if the no_risk method returns True if the exposure classes are all not applicable."""
        exposureclasses = ExposureClassesBase(
            carbonation=DummyCarbonation("Not applicable"),
            chloride=DummyChloride("Not applicable"),
            chloride_seawater=DummyChlorideSeawater("Not applicable"),
            freeze=DummyFreezeThaw("Not applicable"),
            chemical=DummyChemical("Not applicable"),
        )
        assert exposureclasses.no_risk is True

    def test_no_risk_false(self) -> None:
        """Check if the no_risk method returns False if at least one exposure class is applicable."""
        exposureclasses = ExposureClassesBase(
            carbonation=DummyCarbonation("XC1"),
            chloride=DummyChloride("XD1"),
            chloride_seawater=DummyChlorideSeawater("Not applicable"),
            freeze=DummyFreezeThaw("XF1"),
            chemical=DummyChemical("XA1"),
        )
        assert exposureclasses.no_risk is False


def test_comparing_different_types_raises_error() -> None:
    """Check if comparing different exposure class types, raises TypeError."""
    with pytest.raises(TypeError):
        DummyCarbonation.XC1 > DummyChloride.NA
    with pytest.raises(TypeError):
        DummyChloride.NA == DummyChemical.NA
    with pytest.raises(TypeError):
        DummyFreezeThaw.XF1 <= DummyChlorideSeawater.XS1
    with pytest.raises(TypeError):
        DummyChlorideSeawater.XS1 >= DummyChloride.XD1
    with pytest.raises(TypeError):
        DummyChemical.XA1 < DummyCarbonation.XC1
    with pytest.raises(TypeError):
        DummyChemical.NA != DummyFreezeThaw.XF1
