"""Fixtures for structural sections tests."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.structural_sections.cross_section_circle import CircularCrossSection
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection


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
