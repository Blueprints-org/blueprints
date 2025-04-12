"""Fixtures for structural sections tests."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.structural_sections.cross_section_circle import CircularCrossSection
from blueprints.structural_sections.cross_section_quarter_circular_spandrel import QuarterCircularSpandrelCrossSection
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
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
def qcs_cross_section() -> QuarterCircularSpandrelCrossSection:
    """Return a QuarterCircularSpandrelCrossSection instance."""
    return QuarterCircularSpandrelCrossSection(radius=50.0, x=100.0, y=250.0)
