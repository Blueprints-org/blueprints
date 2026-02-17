"""SHSCF Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.rhs_profile import RHSProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __SHSCFProfileParameters(NamedTuple):
    """Parameters for defining a SHSCF profile."""

    name: str
    """Name of the SHSCF profile."""
    total_height: MM
    """Total height of the SHSCF profile."""
    total_width: MM
    """Total width of the SHSCF profile."""
    left_wall_thickness: MM
    """Thickness of the left wall of the SHSCF profile."""
    right_wall_thickness: MM
    """Thickness of the right wall of the SHSCF profile."""
    top_wall_thickness: MM
    """Thickness of the top wall of the SHSCF profile."""
    bottom_wall_thickness: MM
    """Thickness of the bottom wall of the SHSCF profile."""
    top_right_outer_radius: MM
    """Outer radius of the top right corner of the SHSCF profile."""
    top_left_outer_radius: MM
    """Outer radius of the top left corner of the SHSCF profile."""
    bottom_right_outer_radius: MM
    """Outer radius of the bottom right corner of the SHSCF profile."""
    bottom_left_outer_radius: MM
    """Outer radius of the bottom left corner of the SHSCF profile."""
    top_right_inner_radius: MM
    """Inner radius of the top right corner of the SHSCF profile."""
    top_left_inner_radius: MM
    """Inner radius of the top left corner of the SHSCF profile."""
    bottom_right_inner_radius: MM
    """Inner radius of the bottom right corner of the SHSCF profile."""
    bottom_left_inner_radius: MM
    """Inner radius of the bottom left corner of the SHSCF profile."""


SHSCF_PROFILES_DATABASE = {
    "SHSCF20x2": __SHSCFProfileParameters("SHSCF20x2", 20, 20, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "SHSCF25x2": __SHSCFProfileParameters("SHSCF25x2", 25, 25, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "SHSCF25x2_5": __SHSCFProfileParameters("SHSCF25x2.5", 25, 25, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "SHSCF25x3": __SHSCFProfileParameters("SHSCF25x3", 25, 25, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF30x2": __SHSCFProfileParameters("SHSCF30x2", 30, 30, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "SHSCF30x2_5": __SHSCFProfileParameters("SHSCF30x2.5", 30, 30, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "SHSCF30x3": __SHSCFProfileParameters("SHSCF30x3", 30, 30, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF40x2": __SHSCFProfileParameters("SHSCF40x2", 40, 40, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "SHSCF40x2_5": __SHSCFProfileParameters("SHSCF40x2.5", 40, 40, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "SHSCF40x3": __SHSCFProfileParameters("SHSCF40x3", 40, 40, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF40x4": __SHSCFProfileParameters("SHSCF40x4", 40, 40, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF50x2": __SHSCFProfileParameters("SHSCF50x2", 50, 50, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "SHSCF50x2_5": __SHSCFProfileParameters("SHSCF50x2.5", 50, 50, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "SHSCF50x3": __SHSCFProfileParameters("SHSCF50x3", 50, 50, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF50x4": __SHSCFProfileParameters("SHSCF50x4", 50, 50, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF50x5": __SHSCFProfileParameters("SHSCF50x5", 50, 50, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF60x2": __SHSCFProfileParameters("SHSCF60x2", 60, 60, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2),
    "SHSCF60x2_5": __SHSCFProfileParameters("SHSCF60x2.5", 60, 60, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "SHSCF60x3": __SHSCFProfileParameters("SHSCF60x3", 60, 60, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF60x4": __SHSCFProfileParameters("SHSCF60x4", 60, 60, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF60x5": __SHSCFProfileParameters("SHSCF60x5", 60, 60, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF60x6": __SHSCFProfileParameters("SHSCF60x6", 60, 60, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF60x6_3": __SHSCFProfileParameters("SHSCF60x6.3", 60, 60, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF70x2_5": __SHSCFProfileParameters("SHSCF70x2.5", 70, 70, 2.5, 2.5, 2.5, 2.5, 5, 5, 5, 5, 2.5, 2.5, 2.5, 2.5),
    "SHSCF70x3": __SHSCFProfileParameters("SHSCF70x3", 70, 70, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF70x4": __SHSCFProfileParameters("SHSCF70x4", 70, 70, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF70x5": __SHSCFProfileParameters("SHSCF70x5", 70, 70, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF70x6": __SHSCFProfileParameters("SHSCF70x6", 70, 70, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF70x6_3": __SHSCFProfileParameters("SHSCF70x6.3", 70, 70, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF80x3": __SHSCFProfileParameters("SHSCF80x3", 80, 80, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF80x4": __SHSCFProfileParameters("SHSCF80x4", 80, 80, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF80x5": __SHSCFProfileParameters("SHSCF80x5", 80, 80, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF80x6": __SHSCFProfileParameters("SHSCF80x6", 80, 80, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF80x6_3": __SHSCFProfileParameters("SHSCF80x6.3", 80, 80, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF80x8": __SHSCFProfileParameters("SHSCF80x8", 80, 80, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF90x3": __SHSCFProfileParameters("SHSCF90x3", 90, 90, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF90x4": __SHSCFProfileParameters("SHSCF90x4", 90, 90, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF90x5": __SHSCFProfileParameters("SHSCF90x5", 90, 90, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF90x6": __SHSCFProfileParameters("SHSCF90x6", 90, 90, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF90x6_3": __SHSCFProfileParameters("SHSCF90x6.3", 90, 90, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF90x8": __SHSCFProfileParameters("SHSCF90x8", 90, 90, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF100x3": __SHSCFProfileParameters("SHSCF100x3", 100, 100, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF100x4": __SHSCFProfileParameters("SHSCF100x4", 100, 100, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF100x5": __SHSCFProfileParameters("SHSCF100x5", 100, 100, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF100x6": __SHSCFProfileParameters("SHSCF100x6", 100, 100, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF100x6_3": __SHSCFProfileParameters("SHSCF100x6.3", 100, 100, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF100x8": __SHSCFProfileParameters("SHSCF100x8", 100, 100, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF100x10": __SHSCFProfileParameters("SHSCF100x10", 100, 100, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF100x12": __SHSCFProfileParameters("SHSCF100x12", 100, 100, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF100x12_5": __SHSCFProfileParameters("SHSCF100x12.5", 100, 100, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF120x3": __SHSCFProfileParameters("SHSCF120x3", 120, 120, 3, 3, 3, 3, 6, 6, 6, 6, 3, 3, 3, 3),
    "SHSCF120x4": __SHSCFProfileParameters("SHSCF120x4", 120, 120, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF120x5": __SHSCFProfileParameters("SHSCF120x5", 120, 120, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF120x6": __SHSCFProfileParameters("SHSCF120x6", 120, 120, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF120x6_3": __SHSCFProfileParameters("SHSCF120x6.3", 120, 120, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF120x8": __SHSCFProfileParameters("SHSCF120x8", 120, 120, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF120x10": __SHSCFProfileParameters("SHSCF120x10", 120, 120, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF120x12": __SHSCFProfileParameters("SHSCF120x12", 120, 120, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF120x12_5": __SHSCFProfileParameters("SHSCF120x12.5", 120, 120, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF140x4": __SHSCFProfileParameters("SHSCF140x4", 140, 140, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF140x5": __SHSCFProfileParameters("SHSCF140x5", 140, 140, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF140x6": __SHSCFProfileParameters("SHSCF140x6", 140, 140, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF140x6_3": __SHSCFProfileParameters("SHSCF140x6.3", 140, 140, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF140x8": __SHSCFProfileParameters("SHSCF140x8", 140, 140, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF140x10": __SHSCFProfileParameters("SHSCF140x10", 140, 140, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF140x12": __SHSCFProfileParameters("SHSCF140x12", 140, 140, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF140x12_5": __SHSCFProfileParameters("SHSCF140x12.5", 140, 140, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF150x4": __SHSCFProfileParameters("SHSCF150x4", 150, 150, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF150x5": __SHSCFProfileParameters("SHSCF150x5", 150, 150, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF150x6": __SHSCFProfileParameters("SHSCF150x6", 150, 150, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF150x6_3": __SHSCFProfileParameters("SHSCF150x6.3", 150, 150, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF150x8": __SHSCFProfileParameters("SHSCF150x8", 150, 150, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF150x10": __SHSCFProfileParameters("SHSCF150x10", 150, 150, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF150x12": __SHSCFProfileParameters("SHSCF150x12", 150, 150, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF150x12_5": __SHSCFProfileParameters("SHSCF150x12.5", 150, 150, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF150x16": __SHSCFProfileParameters("SHSCF150x16", 150, 150, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF160x4": __SHSCFProfileParameters("SHSCF160x4", 160, 160, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF160x5": __SHSCFProfileParameters("SHSCF160x5", 160, 160, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF160x6": __SHSCFProfileParameters("SHSCF160x6", 160, 160, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF160x6_3": __SHSCFProfileParameters("SHSCF160x6.3", 160, 160, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF160x8": __SHSCFProfileParameters("SHSCF160x8", 160, 160, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF160x10": __SHSCFProfileParameters("SHSCF160x10", 160, 160, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF160x12": __SHSCFProfileParameters("SHSCF160x12", 160, 160, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF160x12_5": __SHSCFProfileParameters("SHSCF160x12.5", 160, 160, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF160x16": __SHSCFProfileParameters("SHSCF160x16", 160, 160, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF180x4": __SHSCFProfileParameters("SHSCF180x4", 180, 180, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF180x5": __SHSCFProfileParameters("SHSCF180x5", 180, 180, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF180x6": __SHSCFProfileParameters("SHSCF180x6", 180, 180, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF180x6_3": __SHSCFProfileParameters("SHSCF180x6.3", 180, 180, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF180x8": __SHSCFProfileParameters("SHSCF180x8", 180, 180, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF180x10": __SHSCFProfileParameters("SHSCF180x10", 180, 180, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF180x12": __SHSCFProfileParameters("SHSCF180x12", 180, 180, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF180x12_5": __SHSCFProfileParameters("SHSCF180x12.5", 180, 180, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF180x16": __SHSCFProfileParameters("SHSCF180x16", 180, 180, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF200x4": __SHSCFProfileParameters("SHSCF200x4", 200, 200, 4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4),
    "SHSCF200x5": __SHSCFProfileParameters("SHSCF200x5", 200, 200, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF200x6": __SHSCFProfileParameters("SHSCF200x6", 200, 200, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF200x6_3": __SHSCFProfileParameters("SHSCF200x6.3", 200, 200, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF200x8": __SHSCFProfileParameters("SHSCF200x8", 200, 200, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF200x10": __SHSCFProfileParameters("SHSCF200x10", 200, 200, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF200x12": __SHSCFProfileParameters("SHSCF200x12", 200, 200, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF200x12_5": __SHSCFProfileParameters("SHSCF200x12.5", 200, 200, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF200x16": __SHSCFProfileParameters("SHSCF200x16", 200, 200, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF220x5": __SHSCFProfileParameters("SHSCF220x5", 220, 220, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF220x6": __SHSCFProfileParameters("SHSCF220x6", 220, 220, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF220x6_3": __SHSCFProfileParameters("SHSCF220x6.3", 220, 220, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF220x8": __SHSCFProfileParameters("SHSCF220x8", 220, 220, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF220x10": __SHSCFProfileParameters("SHSCF220x10", 220, 220, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF220x12": __SHSCFProfileParameters("SHSCF220x12", 220, 220, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF220x12_5": __SHSCFProfileParameters("SHSCF220x12.5", 220, 220, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF220x16": __SHSCFProfileParameters("SHSCF220x16", 220, 220, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF250x5": __SHSCFProfileParameters("SHSCF250x5", 250, 250, 5, 5, 5, 5, 10, 10, 10, 10, 5, 5, 5, 5),
    "SHSCF250x6": __SHSCFProfileParameters("SHSCF250x6", 250, 250, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF250x6_3": __SHSCFProfileParameters("SHSCF250x6.3", 250, 250, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF250x8": __SHSCFProfileParameters("SHSCF250x8", 250, 250, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF250x10": __SHSCFProfileParameters("SHSCF250x10", 250, 250, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF250x12": __SHSCFProfileParameters("SHSCF250x12", 250, 250, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF250x12_5": __SHSCFProfileParameters("SHSCF250x12.5", 250, 250, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF250x16": __SHSCFProfileParameters("SHSCF250x16", 250, 250, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF260x6": __SHSCFProfileParameters("SHSCF260x6", 260, 260, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF260x6_3": __SHSCFProfileParameters("SHSCF260x6.3", 260, 260, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF260x8": __SHSCFProfileParameters("SHSCF260x8", 260, 260, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF260x10": __SHSCFProfileParameters("SHSCF260x10", 260, 260, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF260x12": __SHSCFProfileParameters("SHSCF260x12", 260, 260, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF260x12_5": __SHSCFProfileParameters("SHSCF260x12.5", 260, 260, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF260x16": __SHSCFProfileParameters("SHSCF260x16", 260, 260, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF300x6": __SHSCFProfileParameters("SHSCF300x6", 300, 300, 6, 6, 6, 6, 12, 12, 12, 12, 6, 6, 6, 6),
    "SHSCF300x6_3": __SHSCFProfileParameters("SHSCF300x6.3", 300, 300, 6.3, 6.3, 6.3, 6.3, 15.8, 15.8, 15.8, 15.8, 9.4, 9.4, 9.4, 9.4),
    "SHSCF300x8": __SHSCFProfileParameters("SHSCF300x8", 300, 300, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF300x10": __SHSCFProfileParameters("SHSCF300x10", 300, 300, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF300x12": __SHSCFProfileParameters("SHSCF300x12", 300, 300, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF300x12_5": __SHSCFProfileParameters("SHSCF300x12.5", 300, 300, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF300x16": __SHSCFProfileParameters("SHSCF300x16", 300, 300, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF350x8": __SHSCFProfileParameters("SHSCF350x8", 350, 350, 8, 8, 8, 8, 20, 20, 20, 20, 12, 12, 12, 12),
    "SHSCF350x10": __SHSCFProfileParameters("SHSCF350x10", 350, 350, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF350x12": __SHSCFProfileParameters("SHSCF350x12", 350, 350, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF350x12_5": __SHSCFProfileParameters("SHSCF350x12.5", 350, 350, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF350x16": __SHSCFProfileParameters("SHSCF350x16", 350, 350, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF400x10": __SHSCFProfileParameters("SHSCF400x10", 400, 400, 10, 10, 10, 10, 25, 25, 25, 25, 15, 15, 15, 15),
    "SHSCF400x12": __SHSCFProfileParameters("SHSCF400x12", 400, 400, 12, 12, 12, 12, 36, 36, 36, 36, 24, 24, 24, 24),
    "SHSCF400x12_5": __SHSCFProfileParameters("SHSCF400x12.5", 400, 400, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF400x16": __SHSCFProfileParameters("SHSCF400x16", 400, 400, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF500x12_5": __SHSCFProfileParameters("SHSCF500x12.5", 500, 500, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF500x16": __SHSCFProfileParameters("SHSCF500x16", 500, 500, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF500x20": __SHSCFProfileParameters("SHSCF500x20", 500, 500, 20, 20, 20, 20, 60, 60, 60, 60, 40, 40, 40, 40),
    "SHSCF600x12_5": __SHSCFProfileParameters("SHSCF600x12.5", 600, 600, 12.5, 12.5, 12.5, 12.5, 37.5, 37.5, 37.5, 37.5, 25, 25, 25, 25),
    "SHSCF600x16": __SHSCFProfileParameters("SHSCF600x16", 600, 600, 16, 16, 16, 16, 48, 48, 48, 48, 32, 32, 32, 32),
    "SHSCF600x20": __SHSCFProfileParameters("SHSCF600x20", 600, 600, 20, 20, 20, 20, 60, 60, 60, 60, 40, 40, 40, 40),
}


class SHSCF(metaclass=StandardProfileMeta):
    """Geometrical representation of SHSCF steel profiles.

    This class provides access to standard cold-formed square hollow section profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a RHSProfile instance.

    Note: the corners of SHSCF profiles are not of constant thickness but are thicker,
    this feature has not been implemented yet in Blueprints.
    The corners are conservatively approximated by assuming a constant radius following the outside perimeter.

    Usage example
    -------------
        >>> profile = SHSCF.SHSCF100x6
        >>> print(isinstance(profile, RHSProfile))  # True
        >>>
        >>> # To iterate over all available SHSCF profiles:
        >>> for profile in SHSCF:
        >>>     print(isinstance(profile, RHSProfile))  # True
    """

    _factory = RHSProfile
    """Factory class for creating standard SHSCF profiles."""
    _database = SHSCF_PROFILES_DATABASE
    """Database of standard SHSCF profile parameters."""
