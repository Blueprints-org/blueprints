"""Tests for the CombinedSteelCrossSection class."""

import pytest

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.geometric_profiles import RectangularProfile
from blueprints.structural_sections.steel.combined_steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


def _steel_section(
    width: float,
    height: float,
    *,
    name: str = "Rectangle",
    horizontal_offset: float = 0.0,
    vertical_offset: float = 0.0,
    rotation_angle: float = 0.0,
) -> SteelCrossSection:
    """Helper factory that creates a SteelCrossSection with predictable geometry."""
    return SteelCrossSection(
        profile=RectangularProfile(
            width=width,
            height=height,
            x=0.0,
            y=0.0,
            name=name,
            horizontal_offset=horizontal_offset,
            vertical_offset=vertical_offset,
            rotation=rotation_angle,
        ),
        material=SteelMaterial(),
    )


class TestCombinedSteelCrossSection:
    """Test suite for the CombinedSteelCrossSection class."""

    def test_initialize_with_two_sections(self) -> None:
        """Test that CombinedSteelCrossSection stores the provided sections."""
        first_section = _steel_section(width=10.0, height=5.0, name="First")
        second_section = _steel_section(width=8.0, height=4.0, name="Second")

        combined = CombinedSteelCrossSection((first_section, second_section))

        assert combined.steel_cross_sections == (first_section, second_section)

    def test_initialize_with_no_sections(self) -> None:
        """Test that CombinedSteelCrossSection raises when no sections are provided."""
        combined = CombinedSteelCrossSection()
        assert len(combined.steel_cross_sections) == 0

    def test_rejects_non_steel_sections(self) -> None:
        """Test that CombinedSteelCrossSection validates the input types."""
        first_section = _steel_section(width=10.0, height=5.0)

        with pytest.raises(TypeError):
            CombinedSteelCrossSection((first_section, object()))  # type: ignore[arg-type]

    def test_add_steel_cross_section(self) -> None:
        """Test that a steel cross-section can be added correctly."""
        cross_section_1 = _steel_section(width=12.0, height=6.0)
        combined = CombinedSteelCrossSection((cross_section_1,))
        x_offset = 42.0
        y_offset = -17.5
        rotation_angle = 33.0
        cross_section_2 = _steel_section(
            width=12.0,
            height=6.0,
            horizontal_offset=x_offset,
            vertical_offset=y_offset,
            rotation_angle=rotation_angle,
        )

        updated = combined.add_steel_cross_sections(cross_section_2)

        assert combined.steel_cross_sections == (cross_section_1,)
        added_section = updated.steel_cross_sections[-1]
        assert added_section is cross_section_2
        assert added_section.profile.horizontal_offset == x_offset
        assert added_section.profile.vertical_offset == y_offset
        assert added_section.profile.rotation == rotation_angle

    def test_add_steel_cross_section_chains_sections(self) -> None:
        """Test that multiple sections can be added sequentially with preserved order."""
        first = _steel_section(width=10.0, height=2.0)
        second = _steel_section(width=4.0, height=7.0, rotation_angle=45.0)
        third = _steel_section(width=6.0, height=3.0, horizontal_offset=5.0, vertical_offset=10.0)
        forth = _steel_section(width=8.0, height=4.0)

        combined = CombinedSteelCrossSection((first,))
        combined = combined.add_steel_cross_sections(second).add_steel_cross_sections(third, forth)

        assert len(combined.steel_cross_sections) == 4
        for original, added in zip((first, second, third, forth), combined.steel_cross_sections):
            assert original is added

    def test_yield_strength_min_of_all_sections(self) -> None:
        """Test that yield_strength equals the minimum of the individual sections."""
        first = _steel_section(width=30.0, height=5.0)
        second = _steel_section(width=15.0, height=4.0)

        combined = CombinedSteelCrossSection((first, second))

        expected_yield_strength = min(first.yield_strength, second.yield_strength)
        assert combined.yield_strength == pytest.approx(expected_yield_strength)

    def test_ultimate_strength_min_of_all_sections(self) -> None:
        """Test that ultimate_strength equals the minimum of the individual sections."""
        first = _steel_section(width=30.0, height=5.0)
        second = _steel_section(width=15.0, height=4.0)

        combined = CombinedSteelCrossSection((first, second))

        expected_ultimate_strength = min(first.ultimate_strength, second.ultimate_strength)
        assert combined.ultimate_strength == pytest.approx(expected_ultimate_strength)

    def test_weight_per_meter_sums_all_sections(self) -> None:
        """Test that weight_per_meter equals the sum of the individual sections."""
        first = _steel_section(width=30.0, height=5.0)
        second = _steel_section(width=15.0, height=4.0)

        combined = CombinedSteelCrossSection((first, second))

        expected_weight = first.weight_per_meter + second.weight_per_meter
        assert combined.weight_per_meter == pytest.approx(expected_weight)
