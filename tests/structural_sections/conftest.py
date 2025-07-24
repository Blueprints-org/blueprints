"""Fixtures for structural sections tests."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.structural_sections.cross_section_annular_sector import AnnularSectorCrossSection
from blueprints.structural_sections.cross_section_circle import CircularCrossSection
from blueprints.structural_sections.cross_section_cornered import CircularCorneredCrossSection
from blueprints.structural_sections.cross_section_hexagon import HexagonalCrossSection
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.cross_section_triangle import RightAngledTriangularCrossSection
from blueprints.structural_sections.cross_section_tube import TubeCrossSection


@pytest.fixture
def rectangular_cross_section() -> RectangularCrossSection:
    """Return a RectangularCrossSection instance."""
    return RectangularCrossSection(name="Rectangle", width=100.0, height=200.0, x=100.0, y=250.0)


@pytest.fixture
def rectangular_cross_section_section_properties() -> SectionProperties:
    """Return a RectangularCrossSection instance."""
    rect = RectangularCrossSection(name="Rectangle", width=100.0, height=200.0, x=100.0, y=250.0)
    # Calculate properties
    return rect.section_properties(geometric=True, plastic=True, warping=True)


@pytest.fixture
def circular_cross_section() -> CircularCrossSection:
    """Return a CircularCrossSection instance."""
    return CircularCrossSection(name="Circle", diameter=200.0, x=100.0, y=250.0)


@pytest.fixture
def tube_cross_section() -> TubeCrossSection:
    """Return a TubeCrossSection instance."""
    return TubeCrossSection(name="Tube", outer_diameter=100.0, inner_diameter=50.0, x=100.0, y=250.0)


@pytest.fixture
def triangular_cross_section() -> RightAngledTriangularCrossSection:
    """Return a RightAngledTriangularCrossSection instance."""
    return RightAngledTriangularCrossSection(name="Triangle", base=100.0, height=200.0, x=100.0, y=250.0)


@pytest.fixture
def qcs_cross_section() -> CircularCorneredCrossSection:
    """Return a CircularCorneredCrossSection instance."""
    return CircularCorneredCrossSection(inner_radius=50.0, outer_radius=0, x=100.0, y=250.0, thickness_vertical=0.0, thickness_horizontal=0.0)


@pytest.fixture
def hexagonal_cross_section() -> HexagonalCrossSection:
    """Return a HexagonalCrossSection instance."""
    return HexagonalCrossSection(name="Hexagon", side_length=50.0, x=100.0, y=250.0)


@pytest.fixture
def annular_sector_cross_section() -> AnnularSectorCrossSection:
    """Return an AnnularSectorCrossSection instance."""
    return AnnularSectorCrossSection(
        inner_radius=90.0,
        thickness=20.0,
        start_angle=0.0,
        end_angle=90.0,
        x=100.0,
        y=250.0,
        name="AnnularSector",
    )


@pytest.fixture
def annular_sector_cross_section_359_degrees() -> AnnularSectorCrossSection:
    """Return an AnnularSectorCrossSection instance."""
    return AnnularSectorCrossSection(
        inner_radius=90.0,
        thickness=20.0,
        start_angle=90.0,
        end_angle=90.0 + 359.0,
        x=0.0,
        y=0.0,
        name="AnnularSector",
    )
