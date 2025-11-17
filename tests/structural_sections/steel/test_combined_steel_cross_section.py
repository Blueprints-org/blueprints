"""Tests for the CombinedSteelCrossSection class."""

import pytest

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.geometric_cross_sections import RectangularCrossSection
from blueprints.structural_sections.steel.combined_steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


def _steel_section(width: float, height: float, *, density: float = 7850.0, name: str = "Rectangle") -> SteelCrossSection:
    """Helper factory that creates a SteelCrossSection with predictable geometry."""
    return SteelCrossSection(
        cross_section=RectangularCrossSection(
            width=width,
            height=height,
            x=0.0,
            y=0.0,
            name=name,
        ),
        material=SteelMaterial(density=density),
    )


class TestCombinedSteelCrossSection:
    """Test suite for the CombinedSteelCrossSection class."""

    def test_from_steel_cross_sections_sets_internal_tuple(self) -> None:
        """Test that _from_steel_cross_sections stores the provided sections."""
        first_section = _steel_section(width=10.0, height=5.0, name="First")
        second_section = _steel_section(width=8.0, height=4.0, name="Second")

        combined = CombinedSteelCrossSection._from_steel_cross_sections((first_section, second_section))  # noqa: SLF001

        assert combined.steel_cross_sections == (first_section, second_section)

    def test_from_steel_cross_sections_requires_at_least_one_section(self) -> None:
        """Test that _from_steel_cross_sections raises when no sections are provided."""
        with pytest.raises(ValueError):
            CombinedSteelCrossSection._from_steel_cross_sections(())  # noqa: SLF001

    def test_from_steel_cross_sections_rejects_non_steel_sections(self) -> None:
        """Test that _from_steel_cross_sections validates the input types."""
        first_section = _steel_section(width=10.0, height=5.0)

        with pytest.raises(TypeError):
            CombinedSteelCrossSection._from_steel_cross_sections((first_section, object()))  # type: ignore[arg-type] #  noqa: SLF001

    def test_add_steel_cross_section_applies_transform(self) -> None:
        """Test that add_steel_cross_section applies offsets and rotations."""
        base = CombinedSteelCrossSection()
        steel = _steel_section(width=12.0, height=6.0)
        x_offset = 42.0
        y_offset = -17.5
        rotation_angle = 33.0

        updated = base.add_steel_cross_section(
            steel_cross_section=steel,
            x_offset=x_offset,
            y_offset=y_offset,
            rotation_angle=rotation_angle,
        )

        assert base.steel_cross_sections == ()
        added_section = updated.steel_cross_sections[0]
        assert added_section is not steel
        assert added_section.x_offset == x_offset
        assert added_section.y_offset == y_offset
        assert added_section.rotation_angle == rotation_angle

    def test_add_steel_cross_section_chains_sections(self) -> None:
        """Test that multiple sections can be added sequentially with preserved order."""
        combined = CombinedSteelCrossSection()
        first = _steel_section(width=10.0, height=2.0)
        second = _steel_section(width=4.0, height=7.0)

        combined = combined.add_steel_cross_section(first, x_offset=0.0, y_offset=0.0, rotation_angle=0.0).add_steel_cross_section(
            second, x_offset=80.0, y_offset=30.0, rotation_angle=90.0
        )

        assert len(combined.steel_cross_sections) == 2
        first_added, second_added = combined.steel_cross_sections
        assert first_added.x_offset == 0.0
        assert first_added.y_offset == 0.0
        assert first_added.rotation_angle == 0.0
        assert second_added.x_offset == 80.0
        assert second_added.y_offset == 30.0
        assert second_added.rotation_angle == 90.0

    def test_weight_per_meter_sums_all_sections(self) -> None:
        """Test that weight_per_meter equals the sum of the individual sections."""
        combined = CombinedSteelCrossSection()
        first = _steel_section(width=30.0, height=5.0, density=8000.0)
        second = _steel_section(width=15.0, height=4.0, density=7500.0)

        combined = combined.add_steel_cross_section(first)
        combined = combined.add_steel_cross_section(second)

        expected_weight = first.weight_per_meter + second.weight_per_meter
        assert combined.weight_per_meter == pytest.approx(expected_weight)
