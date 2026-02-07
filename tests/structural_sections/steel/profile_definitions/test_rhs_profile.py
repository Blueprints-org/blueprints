"""Test suite for the RHSSteelProfile class."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.structural_sections.steel.profile_definitions.rhs_profile import RHSProfile
from blueprints.validations import NegativeValueError


class TestRHSSteelProfile:
    """Test suite for RHSSteelProfile."""

    def test_name(self, rhs_profile: RHSProfile) -> None:
        """Test the name of the RHS profile."""
        expected_name: str = "RHS400x200x16"
        assert rhs_profile.name == expected_name

    def test_maximum_element_thickness(self, rhs_profile: RHSProfile) -> None:
        """Test the maximum element thickness of the RHS profile."""
        expected_max_thickness: float = 16.0  # mm
        assert pytest.approx(rhs_profile.max_profile_thickness, rel=1e-6) == expected_max_thickness

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
        expected_geometry = rhs_profile._geometry()  # noqa: SLF001
        assert expected_geometry is not None

    def test_immutability(self, rhs_profile: RHSProfile) -> None:
        """Test that the RHSProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            rhs_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, rhs_profile: RHSProfile) -> None:
        """Test the transform method of the RHS profile."""
        transformed_profile = rhs_profile.transform(horizontal_offset=1000, vertical_offset=500, rotation=90)
        assert transformed_profile is not None
        assert isinstance(transformed_profile, RHSProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == rhs_profile.centroid.x + 1000
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == rhs_profile.centroid.y + 500
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == rhs_profile.profile_width

    def test_with_corrosion_negative_value_raises_error(self, rhs_profile: RHSProfile) -> None:
        """Test that negative corrosion value raises NegativeValueError."""
        with pytest.raises(NegativeValueError, match=r"corrosion_outside"):
            rhs_profile.with_corrosion(corrosion_outside=-1.0)

        with pytest.raises(NegativeValueError, match=r"corrosion_inside"):
            rhs_profile.with_corrosion(corrosion_inside=-1.0)

    def test_with_corrosion_zero_value(self, rhs_profile: RHSProfile) -> None:
        """Test that zero corrosion value returns the same profile."""
        result = rhs_profile.with_corrosion(corrosion_outside=0, corrosion_inside=0)
        assert result is rhs_profile

    def test_with_corrosion_valid_positive_value(self, rhs_profile: RHSProfile) -> None:
        """Test with valid positive corrosion values."""
        # RHS400x200x16 fixture: total_width=200, total_height=400, thickness=16
        corroded_profile = rhs_profile.with_corrosion(corrosion_outside=2.0, corrosion_inside=1.0)

        assert isinstance(corroded_profile, RHSProfile)
        # Outer dimensions reduced by 2*corrosion_outside
        assert pytest.approx(corroded_profile.total_width, rel=1e-6) == rhs_profile.total_width - 2 * 2.0
        assert pytest.approx(corroded_profile.total_height, rel=1e-6) == rhs_profile.total_height - 2 * 2.0
        # Wall thickness reduced by corrosion_outside + corrosion_inside
        expected_thickness = rhs_profile.top_wall_thickness - 2.0 - 1.0
        assert pytest.approx(corroded_profile.top_wall_thickness, rel=1e-6) == expected_thickness
        assert pytest.approx(corroded_profile.bottom_wall_thickness, rel=1e-6) == expected_thickness
        assert pytest.approx(corroded_profile.left_wall_thickness, rel=1e-6) == expected_thickness
        assert pytest.approx(corroded_profile.right_wall_thickness, rel=1e-6) == expected_thickness
        # Name should include corrosion
        assert corroded_profile.name == "RHS400x200x16 (corrosion inside: 1.0 mm, outside: 2.0 mm)"

    def test_with_corrosion_fully_corroded(self, rhs_profile: RHSProfile) -> None:
        """Test that fully corroded profile raises ValueError."""
        # RHS400x200x16: thickness=16, so outside+inside=16 will fully corrode
        with pytest.raises(ValueError, match=r"The profile has fully corroded"):
            rhs_profile.with_corrosion(corrosion_outside=8.0, corrosion_inside=8.0)

    def test_with_corrosion_name_shows_total_corrosion(self, rhs_profile: RHSProfile) -> None:
        """Test that applying corrosion twice shows the total corrosion in the name."""
        # First apply corrosion
        corroded_once = rhs_profile.with_corrosion(corrosion_outside=2.0, corrosion_inside=1.0)
        assert corroded_once.name == "RHS400x200x16 (corrosion inside: 1.0 mm, outside: 2.0 mm)"

        # Apply additional corrosion
        corroded_twice = corroded_once.with_corrosion(corrosion_outside=1.0, corrosion_inside=0.5)
        # Total should be 3.0 outside and 1.5 inside
        assert corroded_twice.name == "RHS400x200x16 (corrosion inside: 1.5 mm, outside: 3.0 mm)"
