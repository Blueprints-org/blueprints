# mypy: disable-error-code="operator"
"""Tests for the Exposure classes."""

from functools import total_ordering

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.exposure_classes import (
    Exposure,
    ExposureClassesBase,
)


@total_ordering
class DummyExposureSubclass(Exposure):
    """Dummy Exposure subclass for testing purposes."""

    NA = "Not applicable"
    DUMMY1 = "DUMMY1"
    DUMMY2 = "DUMMY2"
    DUMMY3 = "DUMMY3"

    @staticmethod
    def exposure_class_description() -> str:
        """Return the description of the DummyExposureSubclass."""
        return "Dummy exposure subclass"

    def description_of_the_environment(self) -> str:
        """Return the description of the environment."""
        return "Dummy environment"


@total_ordering
class DummyCarbonation(Exposure):
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


@total_ordering
class DummyChloride(Exposure):
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


@total_ordering
class DummyChlorideSeawater(Exposure):
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


@total_ordering
class DummyFreezeThaw(Exposure):
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


@total_ordering
class DummyChemical(Exposure):
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


class DummyExposureClasses(ExposureClassesBase):
    """Dummy ExposureClassesBase subclass for testing purposes."""

    def __init__(
        self,
        dummy_carbonation: DummyCarbonation,
        dummy_chloride: DummyChloride,
        dummy_chloride_seawater: DummyChlorideSeawater,
        dummy_freeze_thaw: DummyFreezeThaw,
        dummy_chemical: DummyChemical,
    ) -> None:
        """Initialize the DummyExposureClassesBase with dummy exposure classes."""
        self.dummy_carbonation = dummy_carbonation
        self.dummy_chloride = dummy_chloride
        self.dummy_chloride_seawater = dummy_chloride_seawater
        self.dummy_freeze_thaw = dummy_freeze_thaw
        self.dummy_chemical = dummy_chemical


class TestExposure:
    """Testing Exposure parent class."""

    def test_initiate_abc_class(self) -> None:
        """Check if initiating the Exposure class raises a TypeError."""
        with pytest.raises(TypeError):
            _ = Exposure()  # type: ignore[abstract, call-arg]

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
        assert DummyExposureSubclass.DUMMY1 > DummyExposureSubclass.NA

    def test_greather_than_equal_to_operator(self) -> None:
        """Check if the >= operator is working correctly."""
        # Testing greater than
        assert DummyExposureSubclass.DUMMY3 >= DummyExposureSubclass.DUMMY2
        assert DummyExposureSubclass.DUMMY2 >= DummyExposureSubclass.DUMMY1
        assert DummyExposureSubclass.DUMMY1 >= DummyExposureSubclass.NA
        # Testing equal to
        assert DummyExposureSubclass.DUMMY3 >= DummyExposureSubclass.DUMMY3
        assert DummyExposureSubclass.DUMMY1 >= DummyExposureSubclass.DUMMY1

    def test_lesser_than_operator(self) -> None:
        """Check if the < operator is working correctly."""
        assert DummyExposureSubclass.DUMMY1 < DummyExposureSubclass.DUMMY2
        assert DummyExposureSubclass.DUMMY2 < DummyExposureSubclass.DUMMY3
        assert DummyExposureSubclass.NA < DummyExposureSubclass.DUMMY1

    def test_lesser_than_equal_to_operator(self) -> None:
        """Check if the <= operator is working correctly."""
        # Testing lesser than
        assert DummyExposureSubclass.DUMMY1 <= DummyExposureSubclass.DUMMY2
        assert DummyExposureSubclass.DUMMY2 <= DummyExposureSubclass.DUMMY3
        assert DummyExposureSubclass.NA <= DummyExposureSubclass.DUMMY1
        # Testing equal to
        assert DummyExposureSubclass.DUMMY1 <= DummyExposureSubclass.DUMMY1
        assert DummyExposureSubclass.DUMMY3 <= DummyExposureSubclass.DUMMY3

    def test_options(self) -> None:
        """Check if the options method returns all the possible options within an exposure class."""
        assert DummyExposureSubclass.options() == ["Not applicable", "DUMMY1", "DUMMY2", "DUMMY3"]

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyExposureSubclass.exposure_class_description() == "Dummy exposure subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyExposureSubclass.DUMMY1.description_of_the_environment() == "Dummy environment"

    def test_notation(self) -> None:
        """Check if the notation method returns the correct notation."""
        assert DummyExposureSubclass.notation() == "DUMMY"
        assert DummyExposureSubclass.DUMMY1.notation() == "DUMMY"
        assert DummyExposureSubclass.DUMMY2.notation() == "DUMMY"
        assert DummyExposureSubclass.DUMMY3.notation() == "DUMMY"

    def test_notation_raises_error(self) -> None:
        """Check if the notation method raises an error when called on the base class."""

        class BadNotation(Exposure):
            """Dummy Exposure subclass with bad notation."""

            NA = "Not applicable"
            DUMMY1 = "dummy1"
            DUMMY2 = "DUMMY"
            DUMMY3 = "Dummy3"

            @staticmethod
            def exposure_class_description() -> str:
                """Dummy implementation of abstract method."""
                return ""

            def description_of_the_environment(self) -> str:
                """Dummy implementation of abstract method."""
                return ""

        with pytest.raises(ValueError):
            _ = BadNotation.notation()

    def test_hash_same_severity(self) -> None:
        """Check if instances with the same severity have the same hash value."""
        # Same instance should have same hash
        assert hash(DummyExposureSubclass.DUMMY1) == hash(DummyExposureSubclass.DUMMY1)
        assert hash(DummyExposureSubclass.DUMMY2) == hash(DummyExposureSubclass.DUMMY2)
        assert hash(DummyExposureSubclass.DUMMY3) == hash(DummyExposureSubclass.DUMMY3)
        assert hash(DummyExposureSubclass.NA) == hash(DummyExposureSubclass.NA)

    def test_hash_different_severity(self) -> None:
        """Check if instances with different severity have different hash values."""
        # Different severities should have different hash values
        assert hash(DummyExposureSubclass.DUMMY1) != hash(DummyExposureSubclass.DUMMY2)
        assert hash(DummyExposureSubclass.DUMMY2) != hash(DummyExposureSubclass.DUMMY3)
        assert hash(DummyExposureSubclass.NA) != hash(DummyExposureSubclass.DUMMY1)

    def test_hash_different_types_same_severity(self) -> None:
        """Check if instances of different types but same severity have different hash values."""
        # Different types should have different hash values even with same severity level
        # XC1 and XD1 both have severity 1, but should have different hashes
        assert hash(DummyCarbonation.XC1) != hash(DummyChloride.XD1)
        assert hash(DummyCarbonation.NA) != hash(DummyChloride.NA)

    def test_hash_consistency_with_equality(self) -> None:
        """Check if hash is consistent with equality (objects that compare equal have the same hash)."""
        # Equal objects must have the same hash
        exposure1 = DummyExposureSubclass.DUMMY1
        exposure2 = DummyExposureSubclass.DUMMY1
        if exposure1 == exposure2:
            assert hash(exposure1) == hash(exposure2)

    def test_hash_allows_use_in_set(self) -> None:
        """Check if Exposure instances can be used in sets (requires hashable)."""
        exposure_set = {
            DummyExposureSubclass.DUMMY1,
            DummyExposureSubclass.DUMMY2,
            DummyExposureSubclass.DUMMY3,
            DummyExposureSubclass.NA,
        }
        assert len(exposure_set) == 4
        assert DummyExposureSubclass.DUMMY1 in exposure_set
        assert DummyExposureSubclass.DUMMY2 in exposure_set

    def test_hash_allows_use_in_dict(self) -> None:
        """Check if Exposure instances can be used as dictionary keys (requires hashable)."""
        exposure_dict = {
            DummyExposureSubclass.DUMMY1: "severity 1",
            DummyExposureSubclass.DUMMY2: "severity 2",
            DummyExposureSubclass.DUMMY3: "severity 3",
            DummyExposureSubclass.NA: "not applicable",
        }
        assert len(exposure_dict) == 4
        assert exposure_dict[DummyExposureSubclass.DUMMY1] == "severity 1"
        assert exposure_dict[DummyExposureSubclass.NA] == "not applicable"


class TestCarbonation:
    """Testing Carbonation class."""

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyCarbonation.exposure_class_description() == "Dummy carbonation subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyCarbonation.XC1.description_of_the_environment() == "Dummy environment"

    def test_notation(self) -> None:
        """Check if the notation method returns the correct notation."""
        assert DummyCarbonation.notation() == "XC"


class TestChloride:
    """Testing Chloride class."""

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyChloride.exposure_class_description() == "Dummy chloride subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyChloride.XD1.description_of_the_environment() == "Dummy environment"

    def test_notation(self) -> None:
        """Check if the notation method returns the correct notation."""
        assert DummyChloride.notation() == "XD"


class TestChlorideSeawater:
    """Testing ChlorideSeawater class."""

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyChlorideSeawater.exposure_class_description() == "Dummy chloride seawater subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyChlorideSeawater.XS1.description_of_the_environment() == "Dummy environment"

    def test_notation(self) -> None:
        """Check if the notation method returns the correct notation."""
        assert DummyChlorideSeawater.notation() == "XS"


class TestFreezeThaw:
    """Testing FreezeThaw class."""

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyFreezeThaw.exposure_class_description() == "Dummy freeze thaw subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyFreezeThaw.XF1.description_of_the_environment() == "Dummy environment"

    def test_notation(self) -> None:
        """Check if the notation method returns the correct notation."""
        assert DummyFreezeThaw.notation() == "XF"


class TestChemical:
    """Testing Chemical class."""

    def test_exposure_class_description_implemented(self) -> None:
        """Check if the exposure_class_description method returns the description of the subclass."""
        assert DummyChemical.exposure_class_description() == "Dummy chemical subclass"

    def test_description_of_the_environment(self) -> None:
        """Check if the description_of_the_environment method returns the description of the environment."""
        assert DummyChemical.XA1.description_of_the_environment() == "Dummy environment"

    def test_notation(self) -> None:
        """Check if the notation method returns the correct notation."""
        assert DummyChemical.notation() == "XA"


class TestExposureClasses:
    """Testing ExposureClasses class."""

    def test_str(self) -> None:
        """Check if the __str__ method returns the correct string representation of the exposure classes."""
        exposure_classes = DummyExposureClasses(
            dummy_carbonation=DummyCarbonation("XC1"),
            dummy_chloride=DummyChloride("XD1"),
            dummy_chloride_seawater=DummyChlorideSeawater("Not applicable"),
            dummy_freeze_thaw=DummyFreezeThaw("XF1"),
            dummy_chemical=DummyChemical("XA1"),
        )
        assert str(exposure_classes) == "XC1, XD1, XF1, XA1"

    def test_str_x0(self) -> None:
        """Check if the __str__ method returns the correct string representation of the exposure classes
        when all exposure classes are not applicable.
        """
        exposureclasses = DummyExposureClasses(
            dummy_carbonation=DummyCarbonation("Not applicable"),
            dummy_chloride=DummyChloride("Not applicable"),
            dummy_chloride_seawater=DummyChlorideSeawater("Not applicable"),
            dummy_freeze_thaw=DummyFreezeThaw("Not applicable"),
            dummy_chemical=DummyChemical("Not applicable"),
        )
        assert str(exposureclasses) == "X0"

    def test_no_risk(self) -> None:
        """Check if the no_risk method returns True if the exposure classes are all not applicable."""
        exposureclasses = DummyExposureClasses(
            dummy_carbonation=DummyCarbonation("Not applicable"),
            dummy_chloride=DummyChloride("Not applicable"),
            dummy_chloride_seawater=DummyChlorideSeawater("Not applicable"),
            dummy_freeze_thaw=DummyFreezeThaw("Not applicable"),
            dummy_chemical=DummyChemical("Not applicable"),
        )
        assert exposureclasses.no_risk is True

    def test_no_risk_false(self) -> None:
        """Check if the no_risk method returns False if at least one exposure class is applicable."""
        exposureclasses = DummyExposureClasses(
            dummy_carbonation=DummyCarbonation("XC1"),
            dummy_chloride=DummyChloride("XD1"),
            dummy_chloride_seawater=DummyChlorideSeawater("Not applicable"),
            dummy_freeze_thaw=DummyFreezeThaw("XF1"),
            dummy_chemical=DummyChemical("XA1"),
        )
        assert exposureclasses.no_risk is False

    def test_iter(self) -> None:
        """Check if the __iter__ method returns an iterator over the exposure classes."""
        exposure_classes = DummyExposureClasses(
            dummy_carbonation=DummyCarbonation("XC1"),
            dummy_chloride=DummyChloride("XD1"),
            dummy_chloride_seawater=DummyChlorideSeawater("XS1"),
            dummy_freeze_thaw=DummyFreezeThaw("XF1"),
            dummy_chemical=DummyChemical("XA1"),
        )
        iterator = iter(exposure_classes)
        assert next(iterator) == DummyCarbonation("XC1")
        assert next(iterator) == DummyChloride("XD1")
        assert next(iterator) == DummyChlorideSeawater("XS1")
        assert next(iterator) == DummyFreezeThaw("XF1")
        assert next(iterator) == DummyChemical("XA1")

    def test_from_exposure_list(self) -> None:
        """Check if the from_exposure_list method creates an instance from a sequence of exposure classes."""
        carbonation = "XC1"
        chloride = "XD1"
        chloride_seawater = "XS1"
        freeze_thaw = "XF1"
        exposure_classes = DummyExposureClasses.from_exposure_list([carbonation, chloride, chloride_seawater, freeze_thaw])
        assert exposure_classes.dummy_carbonation == DummyCarbonation(carbonation)
        assert exposure_classes.dummy_chloride == DummyChloride(chloride)
        assert exposure_classes.dummy_chloride_seawater == DummyChlorideSeawater(chloride_seawater)
        assert exposure_classes.dummy_freeze_thaw == DummyFreezeThaw(freeze_thaw)
        assert exposure_classes.dummy_chemical == DummyChemical("Not applicable")

    def test_from_exposure_list_empty(self) -> None:
        """Check if the from_exposure_list method creates an instance with all exposure classes as not applicable."""
        exposure_classes = DummyExposureClasses.from_exposure_list([])
        assert exposure_classes.dummy_carbonation == DummyCarbonation("Not applicable")
        assert exposure_classes.dummy_chloride == DummyChloride("Not applicable")
        assert exposure_classes.dummy_chloride_seawater == DummyChlorideSeawater("Not applicable")
        assert exposure_classes.dummy_freeze_thaw == DummyFreezeThaw("Not applicable")
        assert exposure_classes.dummy_chemical == DummyChemical("Not applicable")


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
