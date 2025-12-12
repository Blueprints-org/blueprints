"""Tests for StructuralStorey SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_storey import (
    StructuralStorey,
)


class TestValidInitialization:
    """Test valid initialization of StructuralStorey."""

    def test_ground_floor_at_origin(self) -> None:
        """Test ground floor at origin height."""
        storey = StructuralStorey(name="Ground Floor", height_level=0.0)
        assert storey.name == "Ground Floor"
        assert storey.height_level == 0.0

    def test_elevated_floor(self) -> None:
        """Test floor above origin."""
        storey = StructuralStorey(name="Level 1", height_level=3.5)
        assert storey.height_level == 3.5

    def test_basement_floor(self) -> None:
        """Test floor below origin (negative height)."""
        storey = StructuralStorey(name="Basement", height_level=-2.0)
        assert storey.height_level == -2.0

    def test_high_elevation_floor(self) -> None:
        """Test floor at high elevation."""
        storey = StructuralStorey(name="Level 10", height_level=35.0)
        assert storey.height_level == 35.0

    def test_fractional_height_level(self) -> None:
        """Test floor with fractional height."""
        storey = StructuralStorey(name="Mezzanine", height_level=1.75)
        assert storey.height_level == 1.75

    def test_with_uuid(self) -> None:
        """Test storey with UUID identifier."""
        storey = StructuralStorey(
            name="Level 2",
            height_level=7.0,
            id="39f238a5-01d0-45cf-a2eb-958170fd4f39",
        )
        assert storey.id == "39f238a5-01d0-45cf-a2eb-958170fd4f39"

    def test_multiple_storeys(self) -> None:
        """Test creating multiple storeys."""
        storeys = [
            StructuralStorey(name="Basement", height_level=-3.0),
            StructuralStorey(name="Ground Floor", height_level=0.0),
            StructuralStorey(name="Level 1", height_level=3.5),
            StructuralStorey(name="Level 2", height_level=7.0),
            StructuralStorey(name="Roof", height_level=10.5),
        ]
        assert len(storeys) == 5
        assert storeys[0].name == "Basement"
        assert storeys[4].height_level == 10.5

    def test_very_large_height(self) -> None:
        """Test storey with very large height value."""
        storey = StructuralStorey(name="Level 50", height_level=175.0)
        assert storey.height_level == 175.0

    def test_very_small_negative_height(self) -> None:
        """Test storey with large negative height (deep basement)."""
        storey = StructuralStorey(name="Deep Basement", height_level=-50.0)
        assert storey.height_level == -50.0


class TestValidation:
    """Test validation of StructuralStorey."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralStorey(name="", height_level=0.0)


class TestImmutability:
    """Test immutability of StructuralStorey."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        storey = StructuralStorey(name="Level 1", height_level=3.5)
        with pytest.raises(Exception):
            storey.name = "Level 2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that storey can be used in sets."""
        storey = StructuralStorey(name="Level 1", height_level=3.5)
        storey_set = {storey}
        assert storey in storey_set


class TestEquality:
    """Test equality of StructuralStorey."""

    def test_equal_storeys(self) -> None:
        """Test that identical storeys are equal."""
        storey1 = StructuralStorey(name="Level 1", height_level=3.5)
        storey2 = StructuralStorey(name="Level 1", height_level=3.5)
        assert storey1 == storey2

    def test_unequal_storeys_different_names(self) -> None:
        """Test that storeys with different names are not equal."""
        storey1 = StructuralStorey(name="Level 1", height_level=3.5)
        storey2 = StructuralStorey(name="Level 2", height_level=3.5)
        assert storey1 != storey2

    def test_unequal_storeys_different_heights(self) -> None:
        """Test that storeys with different heights are not equal."""
        storey1 = StructuralStorey(name="Level 1", height_level=3.5)
        storey2 = StructuralStorey(name="Level 1", height_level=7.0)
        assert storey1 != storey2
