"""Test suite for the RHSSteelProfile class."""

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.structural_sections.steel.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.steel_profile_sections.rhs_profile import RHSProfile


class TestRHSSteelProfile:
    """Test suite for RHSSteelProfile."""

    def test_name(self, rhs_profile: RHSProfile) -> None:
        """Test the name of the RHS profile."""
        expected_name: str = "RHS400x200x16"
        assert rhs_profile.name == expected_name

    def test_code(self, rhs_profile: RHSProfile) -> None:
        """Test the code of the RHS profile."""
        expected_alias: str = "RHS400x200x16"
        assert rhs_profile.name == expected_alias

    def test_steel_volume_per_meter(self, rhs_profile: RHSProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume: float = 0.017900  # m³/m
        assert pytest.approx(rhs_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_area(self, rhs_profile: RHSProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area: float = 17900  # mm²
        assert pytest.approx(rhs_profile.area, rel=1e-2) == expected_area

    @pytest.mark.slow
    def test_plot(self, rhs_profile: RHSProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig: Figure = rhs_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, rhs_profile: RHSProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the RHS profile shapes with mocked section properties."""
        fig: Figure = rhs_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, rhs_profile: RHSProfile) -> None:
        """Test the geometry of the RHS profile."""
        expected_geometry = rhs_profile._geometry  # noqa: SLF001
        assert expected_geometry is not None

    def test_get_profile_with_corrosion(self) -> None:
        """Test the RHS profile with corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match="The profile has fully corroded."):
            RHSProfile.from_standard_profile(
                profile=RHS.RHS400x200_16,
                corrosion_outside=16,  # mm
                corrosion_inside=0,  # mm
            )

    def test_corrosion_in_name(self) -> None:
        """Test that the name includes corrosion information."""
        rhs_profile_with_corrosion = RHSProfile.from_standard_profile(
            profile=RHS.RHS400x200_16,
            corrosion_outside=2,  # mm
            corrosion_inside=1,  # mm
        )
        expected_name_with_corrosion = "RHS400x200x16 (corrosion in: 1 mm, out: 2 mm)"
        assert rhs_profile_with_corrosion.name == expected_name_with_corrosion

    def test_immutability(self, rhs_profile: RHSProfile) -> None:
        """Test that the RHSProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            rhs_profile.name = "New Name"  # type: ignore[misc]
