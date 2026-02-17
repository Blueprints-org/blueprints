"""RHSCF Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.rhs_profile import RHSProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __RHSCFProfileParameters(NamedTuple):
    """Parameters for defining a RHSCF profile."""

    name: str
    """Name of the RHSCF profile."""
    total_height: MM
    """Total height of the RHSCF profile."""
    total_width: MM
    """Total width of the RHSCF profile."""
    left_wall_thickness: MM
    """Thickness of the left wall of the RHSCF profile."""
    right_wall_thickness: MM
    """Thickness of the right wall of the RHSCF profile."""
    top_wall_thickness: MM
    """Thickness of the top wall of the RHSCF profile."""
    bottom_wall_thickness: MM
    """Thickness of the bottom wall of the RHSCF profile."""
    top_right_outer_radius: MM
    """Outer radius of the top right corner of the RHSCF profile."""
    top_left_outer_radius: MM
    """Outer radius of the top left corner of the RHSCF profile."""
    bottom_right_outer_radius: MM
    """Outer radius of the bottom right corner of the RHSCF profile."""
    bottom_left_outer_radius: MM
    """Outer radius of the bottom left corner of the RHSCF profile."""
    top_right_inner_radius: MM
    """Inner radius of the top right corner of the RHSCF profile."""
    top_left_inner_radius: MM
    """Inner radius of the top left corner of the RHSCF profile."""
    bottom_right_inner_radius: MM
    """Inner radius of the bottom right corner of the RHSCF profile."""
    bottom_left_inner_radius: MM
    """Inner radius of the bottom left corner of the RHSCF profile."""


RHSCF_PROFILES_DATABASE = {
    "RHSCF40x20x2": __RHSCFProfileParameters("RHSCF40x20x2", 40, 20, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "RHSCF40x20x2_5": __RHSCFProfileParameters("RHSCF40x20x2.5", 40, 20, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF40x20x3": __RHSCFProfileParameters("RHSCF40x20x3", 40, 20, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF50x30x2": __RHSCFProfileParameters("RHSCF50x30x2", 50, 30, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "RHSCF50x30x2_5": __RHSCFProfileParameters("RHSCF50x30x2.5", 50, 30, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF50x30x3": __RHSCFProfileParameters("RHSCF50x30x3", 50, 30, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF50x30x4": __RHSCFProfileParameters("RHSCF50x30x4", 50, 30, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF60x40x2": __RHSCFProfileParameters("RHSCF60x40x2", 60, 40, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "RHSCF60x40x2_5": __RHSCFProfileParameters("RHSCF60x40x2.5", 60, 40, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF60x40x3": __RHSCFProfileParameters("RHSCF60x40x3", 60, 40, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF60x40x4": __RHSCFProfileParameters("RHSCF60x40x4", 60, 40, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF60x40x5": __RHSCFProfileParameters("RHSCF60x40x5", 60, 40, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF70x50x2": __RHSCFProfileParameters("RHSCF70x50x2", 70, 50, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "RHSCF70x50x2_5": __RHSCFProfileParameters("RHSCF70x50x2.5", 70, 50, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF70x50x3": __RHSCFProfileParameters("RHSCF70x50x3", 70, 50, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF70x50x4": __RHSCFProfileParameters("RHSCF70x50x4", 70, 50, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF70x50x5": __RHSCFProfileParameters("RHSCF70x50x5", 70, 50, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF80x40x2": __RHSCFProfileParameters("RHSCF80x40x2", 80, 40, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "RHSCF80x40x2_5": __RHSCFProfileParameters("RHSCF80x40x2.5", 80, 40, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF80x40x3": __RHSCFProfileParameters("RHSCF80x40x3", 80, 40, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF80x40x4": __RHSCFProfileParameters("RHSCF80x40x4", 80, 40, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF80x40x5": __RHSCFProfileParameters("RHSCF80x40x5", 80, 40, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF80x60x2": __RHSCFProfileParameters("RHSCF80x60x2", 80, 60, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "RHSCF80x60x2_5": __RHSCFProfileParameters("RHSCF80x60x2.5", 80, 60, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF80x60x3": __RHSCFProfileParameters("RHSCF80x60x3", 80, 60, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF80x60x4": __RHSCFProfileParameters("RHSCF80x60x4", 80, 60, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF80x60x5": __RHSCFProfileParameters("RHSCF80x60x5", 80, 60, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF90x50x2": __RHSCFProfileParameters("RHSCF90x50x2", 90, 50, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "RHSCF90x50x2_5": __RHSCFProfileParameters("RHSCF90x50x2.5", 90, 50, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF90x50x3": __RHSCFProfileParameters("RHSCF90x50x3", 90, 50, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF90x50x4": __RHSCFProfileParameters("RHSCF90x50x4", 90, 50, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF90x50x5": __RHSCFProfileParameters("RHSCF90x50x5", 90, 50, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF100x40x2_5": __RHSCFProfileParameters("RHSCF100x40x2.5", 100, 40, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF100x40x3": __RHSCFProfileParameters("RHSCF100x40x3", 100, 40, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF100x40x4": __RHSCFProfileParameters("RHSCF100x40x4", 100, 40, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF100x40x5": __RHSCFProfileParameters("RHSCF100x40x5", 100, 40, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF100x50x2_5": __RHSCFProfileParameters("RHSCF100x50x2.5", 100, 50, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF100x50x3": __RHSCFProfileParameters("RHSCF100x50x3", 100, 50, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF100x50x4": __RHSCFProfileParameters("RHSCF100x50x4", 100, 50, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF100x50x5": __RHSCFProfileParameters("RHSCF100x50x5", 100, 50, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF100x50x6": __RHSCFProfileParameters("RHSCF100x50x6", 100, 50, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF100x50x6_3": __RHSCFProfileParameters("RHSCF100x50x6.3", 100, 50, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF100x60x2_5": __RHSCFProfileParameters("RHSCF100x60x2.5", 100, 60, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF100x60x3": __RHSCFProfileParameters("RHSCF100x60x3", 100, 60, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF100x60x4": __RHSCFProfileParameters("RHSCF100x60x4", 100, 60, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF100x60x5": __RHSCFProfileParameters("RHSCF100x60x5", 100, 60, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF100x60x6": __RHSCFProfileParameters("RHSCF100x60x6", 100, 60, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF100x60x6_3": __RHSCFProfileParameters("RHSCF100x60x6.3", 100, 60, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF100x80x2_5": __RHSCFProfileParameters("RHSCF100x80x2.5", 100, 80, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF100x80x3": __RHSCFProfileParameters("RHSCF100x80x3", 100, 80, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF100x80x4": __RHSCFProfileParameters("RHSCF100x80x4", 100, 80, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF100x80x5": __RHSCFProfileParameters("RHSCF100x80x5", 100, 80, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF100x80x6": __RHSCFProfileParameters("RHSCF100x80x6", 100, 80, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF100x80x6_3": __RHSCFProfileParameters("RHSCF100x80x6.3", 100, 80, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF120x60x2_5": __RHSCFProfileParameters("RHSCF120x60x2.5", 120, 60, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "RHSCF120x60x3": __RHSCFProfileParameters("RHSCF120x60x3", 120, 60, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF120x60x4": __RHSCFProfileParameters("RHSCF120x60x4", 120, 60, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF120x60x5": __RHSCFProfileParameters("RHSCF120x60x5", 120, 60, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF120x60x6": __RHSCFProfileParameters("RHSCF120x60x6", 120, 60, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF120x60x6_3": __RHSCFProfileParameters("RHSCF120x60x6.3", 120, 60, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF120x60x8": __RHSCFProfileParameters("RHSCF120x60x8", 120, 60, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF120x80x3": __RHSCFProfileParameters("RHSCF120x80x3", 120, 80, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "RHSCF120x80x4": __RHSCFProfileParameters("RHSCF120x80x4", 120, 80, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF120x80x5": __RHSCFProfileParameters("RHSCF120x80x5", 120, 80, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF120x80x6": __RHSCFProfileParameters("RHSCF120x80x6", 120, 80, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF120x80x6_3": __RHSCFProfileParameters("RHSCF120x80x6.3", 120, 80, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF120x80x8": __RHSCFProfileParameters("RHSCF120x80x8", 120, 80, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF140x80x4": __RHSCFProfileParameters("RHSCF140x80x4", 140, 80, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF140x80x5": __RHSCFProfileParameters("RHSCF140x80x5", 140, 80, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF140x80x6": __RHSCFProfileParameters("RHSCF140x80x6", 140, 80, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF140x80x6_3": __RHSCFProfileParameters("RHSCF140x80x6.3", 140, 80, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF140x80x8": __RHSCFProfileParameters("RHSCF140x80x8", 140, 80, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF150x100x4": __RHSCFProfileParameters("RHSCF150x100x4", 150, 100, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF150x100x5": __RHSCFProfileParameters("RHSCF150x100x5", 150, 100, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF150x100x6": __RHSCFProfileParameters("RHSCF150x100x6", 150, 100, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF150x100x6_3": __RHSCFProfileParameters("RHSCF150x100x6.3", 150, 100, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF150x100x8": __RHSCFProfileParameters("RHSCF150x100x8", 150, 100, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF150x100x10": __RHSCFProfileParameters("RHSCF150x100x10", 150, 100, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF150x100x12": __RHSCFProfileParameters("RHSCF150x100x12", 150, 100, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF150x100x12_5": __RHSCFProfileParameters("RHSCF150x100x12.5", 150, 100, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF160x80x4": __RHSCFProfileParameters("RHSCF160x80x4", 160, 80, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF160x80x5": __RHSCFProfileParameters("RHSCF160x80x5", 160, 80, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF160x80x6": __RHSCFProfileParameters("RHSCF160x80x6", 160, 80, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF160x80x6_3": __RHSCFProfileParameters("RHSCF160x80x6.3", 160, 80, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF160x80x8": __RHSCFProfileParameters("RHSCF160x80x8", 160, 80, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF160x80x10": __RHSCFProfileParameters("RHSCF160x80x10", 160, 80, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF160x80x12": __RHSCFProfileParameters("RHSCF160x80x12", 160, 80, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF160x80x12_5": __RHSCFProfileParameters("RHSCF160x80x12.5", 160, 80, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF180x100x4": __RHSCFProfileParameters("RHSCF180x100x4", 180, 100, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF180x100x5": __RHSCFProfileParameters("RHSCF180x100x5", 180, 100, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF180x100x6": __RHSCFProfileParameters("RHSCF180x100x6", 180, 100, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF180x100x6_3": __RHSCFProfileParameters("RHSCF180x100x6.3", 180, 100, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF180x100x8": __RHSCFProfileParameters("RHSCF180x100x8", 180, 100, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF180x100x10": __RHSCFProfileParameters("RHSCF180x100x10", 180, 100, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF180x100x12": __RHSCFProfileParameters("RHSCF180x100x12", 180, 100, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF180x100x12_5": __RHSCFProfileParameters("RHSCF180x100x12.5", 180, 100, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF200x100x4": __RHSCFProfileParameters("RHSCF200x100x4", 200, 100, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF200x100x5": __RHSCFProfileParameters("RHSCF200x100x5", 200, 100, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF200x100x6": __RHSCFProfileParameters("RHSCF200x100x6", 200, 100, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF200x100x6_3": __RHSCFProfileParameters("RHSCF200x100x6.3", 200, 100, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF200x100x8": __RHSCFProfileParameters("RHSCF200x100x8", 200, 100, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF200x100x10": __RHSCFProfileParameters("RHSCF200x100x10", 200, 100, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF200x100x12": __RHSCFProfileParameters("RHSCF200x100x12", 200, 100, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF200x100x12_5": __RHSCFProfileParameters("RHSCF200x100x12.5", 200, 100, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF200x120x4": __RHSCFProfileParameters("RHSCF200x120x4", 200, 120, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "RHSCF200x120x5": __RHSCFProfileParameters("RHSCF200x120x5", 200, 120, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF200x120x6": __RHSCFProfileParameters("RHSCF200x120x6", 200, 120, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF200x120x6_3": __RHSCFProfileParameters("RHSCF200x120x6.3", 200, 120, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF200x120x8": __RHSCFProfileParameters("RHSCF200x120x8", 200, 120, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF200x120x10": __RHSCFProfileParameters("RHSCF200x120x10", 200, 120, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF200x120x12": __RHSCFProfileParameters("RHSCF200x120x12", 200, 120, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF200x120x12_5": __RHSCFProfileParameters("RHSCF200x120x12.5", 200, 120, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF250x150x5": __RHSCFProfileParameters("RHSCF250x150x5", 250, 150, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF250x150x6": __RHSCFProfileParameters("RHSCF250x150x6", 250, 150, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF250x150x6_3": __RHSCFProfileParameters("RHSCF250x150x6.3", 250, 150, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF250x150x8": __RHSCFProfileParameters("RHSCF250x150x8", 250, 150, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF250x150x10": __RHSCFProfileParameters("RHSCF250x150x10", 250, 150, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF250x150x12": __RHSCFProfileParameters("RHSCF250x150x12", 250, 150, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF250x150x12_5": __RHSCFProfileParameters("RHSCF250x150x12.5", 250, 150, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF250x150x16": __RHSCFProfileParameters("RHSCF250x150x16", 250, 150, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "RHSCF260x180x5": __RHSCFProfileParameters("RHSCF260x180x5", 260, 180, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "RHSCF260x180x6_3": __RHSCFProfileParameters("RHSCF260x180x6.3", 260, 180, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF260x180x8": __RHSCFProfileParameters("RHSCF260x180x8", 260, 180, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF260x180x10": __RHSCFProfileParameters("RHSCF260x180x10", 260, 180, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF260x180x12": __RHSCFProfileParameters("RHSCF260x180x12", 260, 180, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF260x180x12_5": __RHSCFProfileParameters("RHSCF260x180x12.5", 260, 180, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF260x180x16": __RHSCFProfileParameters("RHSCF260x180x16", 260, 180, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "RHSCF300x100x6": __RHSCFProfileParameters("RHSCF300x100x6", 300, 100, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF300x100x6_3": __RHSCFProfileParameters("RHSCF300x100x6.3", 300, 100, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF300x100x8": __RHSCFProfileParameters("RHSCF300x100x8", 300, 100, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF300x100x10": __RHSCFProfileParameters("RHSCF300x100x10", 300, 100, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF300x100x12": __RHSCFProfileParameters("RHSCF300x100x12", 300, 100, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF300x100x12_5": __RHSCFProfileParameters("RHSCF300x100x12.5", 300, 100, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF300x100x16": __RHSCFProfileParameters("RHSCF300x100x16", 300, 100, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "RHSCF300x150x6": __RHSCFProfileParameters("RHSCF300x150x6", 300, 150, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF300x150x6_3": __RHSCFProfileParameters("RHSCF300x150x6.3", 300, 150, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF300x150x8": __RHSCFProfileParameters("RHSCF300x150x8", 300, 150, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF300x150x10": __RHSCFProfileParameters("RHSCF300x150x10", 300, 150, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF300x150x12": __RHSCFProfileParameters("RHSCF300x150x12", 300, 150, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF300x150x12_5": __RHSCFProfileParameters("RHSCF300x150x12.5", 300, 150, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF300x150x16": __RHSCFProfileParameters("RHSCF300x150x16", 300, 150, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "RHSCF300x200x6": __RHSCFProfileParameters("RHSCF300x200x6", 300, 200, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF300x200x6_3": __RHSCFProfileParameters("RHSCF300x200x6.3", 300, 200, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF300x200x8": __RHSCFProfileParameters("RHSCF300x200x8", 300, 200, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF300x200x10": __RHSCFProfileParameters("RHSCF300x200x10", 300, 200, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF300x200x12": __RHSCFProfileParameters("RHSCF300x200x12", 300, 200, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF300x200x12_5": __RHSCFProfileParameters("RHSCF300x200x12.5", 300, 200, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF300x200x16": __RHSCFProfileParameters("RHSCF300x200x16", 300, 200, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "RHSCF350x250x6": __RHSCFProfileParameters("RHSCF350x250x6", 350, 250, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "RHSCF350x250x6_3": __RHSCFProfileParameters("RHSCF350x250x6.3", 350, 250, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "RHSCF350x250x8": __RHSCFProfileParameters("RHSCF350x250x8", 350, 250, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF350x250x10": __RHSCFProfileParameters("RHSCF350x250x10", 350, 250, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF350x250x12": __RHSCFProfileParameters("RHSCF350x250x12", 350, 250, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF350x250x12_5": __RHSCFProfileParameters("RHSCF350x250x12.5", 350, 250, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF350x250x16": __RHSCFProfileParameters("RHSCF350x250x16", 350, 250, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "RHSCF400x200x8": __RHSCFProfileParameters("RHSCF400x200x8", 400, 200, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF400x200x12_5": __RHSCFProfileParameters("RHSCF400x200x12.5", 400, 200, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF400x200x16": __RHSCFProfileParameters("RHSCF400x200x16", 400, 200, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "RHSCF400x300x8": __RHSCFProfileParameters("RHSCF400x300x8", 400, 300, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "RHSCF400x300x10": __RHSCFProfileParameters("RHSCF400x300x10", 400, 300, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "RHSCF400x300x12": __RHSCFProfileParameters("RHSCF400x300x12", 400, 300, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "RHSCF400x300x12_5": __RHSCFProfileParameters("RHSCF400x300x12.5", 400, 300, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "RHSCF400x300x16": __RHSCFProfileParameters("RHSCF400x300x16", 400, 300, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
}


class RHSCF(metaclass=StandardProfileMeta):
    """Geometrical representation of RHSCF steel profiles.

    This class provides access to standard RHSCF (cold-formed RHS) profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a RHSProfile instance with uniform wall thickness and corner radii.

    Usage example
    -------------
        >>> profile = RHSCF.RHSCF100x50x4
        >>> print(isinstance(profile, RHSProfile))  # True
        >>>
        >>> # To iterate over all available RHSCF profiles:
        >>> for profile in RHSCF:
        >>>     print(isinstance(profile, RHSProfile))  # True
    """

    _factory = RHSProfile
    """Factory class for creating standard RHSCF profiles."""
    _database = RHSCF_PROFILES_DATABASE
    """Database of standard RHSCF profile parameters."""
