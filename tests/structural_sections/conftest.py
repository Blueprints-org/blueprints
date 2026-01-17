"""Fixtures for structural sections tests."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.structural_sections.geometric_profiles import (
    AnnularSectorProfile,
    CircularCorneredProfile,
    CircularProfile,
    HexagonalProfile,
    RectangularProfile,
    RightAngledTriangularProfile,
    TubeProfile,
    UNPSteelProfile,
)


@pytest.fixture
def rectangular_profile() -> RectangularProfile:
    """Return a RectangularProfile instance."""
    return RectangularProfile(name="Rectangle", width=100.0, height=200.0, x=100.0, y=250.0)


@pytest.fixture
def rectangular_profile_section_properties() -> SectionProperties:
    """Return a SectionProperties instance from RectangularProfile."""
    rect = RectangularProfile(name="Rectangle", width=100.0, height=200.0, x=100.0, y=250.0)
    # Calculate properties
    return rect.section_properties(geometric=True, plastic=True, warping=True)


@pytest.fixture
def circular_profile() -> CircularProfile:
    """Return a CircularProfile instance."""
    return CircularProfile(name="Circle", diameter=200.0, x=100.0, y=250.0)


@pytest.fixture
def tube_profile() -> TubeProfile:
    """Return a TubeProfile instance."""
    return TubeProfile(name="Tube", outer_diameter=100.0, inner_diameter=50.0, x=100.0, y=250.0)


@pytest.fixture
def triangular_profile() -> RightAngledTriangularProfile:
    """Return a RightAngledTriangularProfile instance."""
    return RightAngledTriangularProfile(name="Triangle", base=100.0, height=200.0, x=100.0, y=250.0)


@pytest.fixture
def qcs_profile() -> CircularCorneredProfile:
    """Return a CircularCorneredProfile instance."""
    return CircularCorneredProfile(inner_radius=50.0, outer_radius=0, x=100.0, y=250.0, thickness_vertical=0.0, thickness_horizontal=0.0)


@pytest.fixture
def hexagonal_profile() -> HexagonalProfile:
    """Return a HexagonalProfile instance."""
    return HexagonalProfile(name="Hexagon", side_length=50.0, x=100.0, y=250.0)


@pytest.fixture
def annular_sector_profile() -> AnnularSectorProfile:
    """Return an AnnularSectorProfile instance."""
    return AnnularSectorProfile(
        inner_radius=90.0,
        thickness=20.0,
        start_angle=0.0,
        end_angle=90.0,
        x=100.0,
        y=250.0,
        name="AnnularSector",
    )


@pytest.fixture
def annular_sector_profile_359_degrees() -> AnnularSectorProfile:
    """Return an AnnularSectorProfile instance."""
    return AnnularSectorProfile(
        inner_radius=90.0,
        thickness=20.0,
        start_angle=90.0,
        end_angle=90.0 + 359.0,
        x=0.0,
        y=0.0,
        name="AnnularSector",
    )


@pytest.fixture
def unp_profile() -> UNPSteelProfile:
    """Fixture to set up a UNP profile for testing."""
    return UNPSteelProfile()
