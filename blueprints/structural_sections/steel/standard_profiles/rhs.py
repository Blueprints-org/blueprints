"""RHS Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.rhs_profile import RHSProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __RHSProfileParameters(NamedTuple):
    """Parameters for defining a RHS profile."""

    name: str
    """Name of the RHS profile."""
    total_height: MM
    """Total height of the RHS profile."""
    total_width: MM
    """Total width of the RHS profile."""
    left_wall_thickness: MM
    """Thickness of the left wall of the RHS profile."""
    right_wall_thickness: MM
    """Thickness of the right wall of the RHS profile."""
    top_wall_thickness: MM
    """Thickness of the top wall of the RHS profile."""
    bottom_wall_thickness: MM
    """Thickness of the bottom wall of the RHS profile."""
    top_right_outer_radius: MM
    """Outer radius of the top right corner of the RHS profile."""
    top_left_outer_radius: MM
    """Outer radius of the top left corner of the RHS profile."""
    bottom_right_outer_radius: MM
    """Outer radius of the bottom right corner of the RHS profile."""
    bottom_left_outer_radius: MM
    """Outer radius of the bottom left corner of the RHS profile."""
    top_right_inner_radius: MM
    """Inner radius of the top right corner of the RHS profile."""
    top_left_inner_radius: MM
    """Inner radius of the top left corner of the RHS profile."""
    bottom_right_inner_radius: MM
    """Inner radius of the bottom right corner of the RHS profile."""
    bottom_left_inner_radius: MM
    """Inner radius of the bottom left corner of the RHS profile."""


RHS_PROFILES_DATABASE = {
    "RHS50x30x2_6": __RHSProfileParameters("RHS50x30x2.6", 50, 30, 2.6, 2.6, 2.6, 2.6, 3.9, 3.9, 3.9, 3.9, 2.6, 2.6, 2.6, 2.6),
    "RHS50x30x3_2": __RHSProfileParameters("RHS50x30x3.2", 50, 30, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "RHS50x30x4": __RHSProfileParameters("RHS50x30x4", 50, 30, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS50x30x5": __RHSProfileParameters("RHS50x30x5", 50, 30, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS60x40x2_6": __RHSProfileParameters("RHS60x40x2.6", 60, 40, 2.6, 2.6, 2.6, 2.6, 3.9, 3.9, 3.9, 3.9, 2.6, 2.6, 2.6, 2.6),
    "RHS60x40x3_2": __RHSProfileParameters("RHS60x40x3.2", 60, 40, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "RHS60x40x4": __RHSProfileParameters("RHS60x40x4", 60, 40, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS60x40x5": __RHSProfileParameters("RHS60x40x5", 60, 40, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS60x40x6_3": __RHSProfileParameters("RHS60x40x6.3", 60, 40, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS80x40x3_2": __RHSProfileParameters("RHS80x40x3.2", 80, 40, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "RHS80x40x4": __RHSProfileParameters("RHS80x40x4", 80, 40, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS80x40x5": __RHSProfileParameters("RHS80x40x5", 80, 40, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS80x40x6_3": __RHSProfileParameters("RHS80x40x6.3", 80, 40, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS80x40x8": __RHSProfileParameters("RHS80x40x8", 80, 40, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS90x50x3_2": __RHSProfileParameters("RHS90x50x3.2", 90, 50, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "RHS90x50x4": __RHSProfileParameters("RHS90x50x4", 90, 50, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS90x50x5": __RHSProfileParameters("RHS90x50x5", 90, 50, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS90x50x6_3": __RHSProfileParameters("RHS90x50x6.3", 90, 50, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS90x50x8": __RHSProfileParameters("RHS90x50x8", 90, 50, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS100x50x3_2": __RHSProfileParameters("RHS100x50x3.2", 100, 50, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "RHS100x50x4": __RHSProfileParameters("RHS100x50x4", 100, 50, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS100x50x5": __RHSProfileParameters("RHS100x50x5", 100, 50, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS100x50x6_3": __RHSProfileParameters("RHS100x50x6.3", 100, 50, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS100x50x8": __RHSProfileParameters("RHS100x50x8", 100, 50, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS100x60x3_2": __RHSProfileParameters("RHS100x60x3.2", 100, 60, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "RHS100x60x4": __RHSProfileParameters("RHS100x60x4", 100, 60, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS100x60x5": __RHSProfileParameters("RHS100x60x5", 100, 60, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS100x60x6_3": __RHSProfileParameters("RHS100x60x6.3", 100, 60, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS100x60x8": __RHSProfileParameters("RHS100x60x8", 100, 60, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS120x60x4": __RHSProfileParameters("RHS120x60x4", 120, 60, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS120x60x5": __RHSProfileParameters("RHS120x60x5", 120, 60, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS120x60x6_3": __RHSProfileParameters("RHS120x60x6.3", 120, 60, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS120x60x8": __RHSProfileParameters("RHS120x60x8", 120, 60, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS120x60x10": __RHSProfileParameters("RHS120x60x10", 120, 60, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS120x80x4": __RHSProfileParameters("RHS120x80x4", 120, 80, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS120x80x5": __RHSProfileParameters("RHS120x80x5", 120, 80, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS120x80x6_3": __RHSProfileParameters("RHS120x80x6.3", 120, 80, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS120x80x8": __RHSProfileParameters("RHS120x80x8", 120, 80, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS120x80x10": __RHSProfileParameters("RHS120x80x10", 120, 80, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS140x80x4": __RHSProfileParameters("RHS140x80x4", 140, 80, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS140x80x5": __RHSProfileParameters("RHS140x80x5", 140, 80, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS140x80x6_3": __RHSProfileParameters("RHS140x80x6.3", 140, 80, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS140x80x8": __RHSProfileParameters("RHS140x80x8", 140, 80, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS140x80x10": __RHSProfileParameters("RHS140x80x10", 140, 80, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS150x100x4": __RHSProfileParameters("RHS150x100x4", 150, 100, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS150x100x5": __RHSProfileParameters("RHS150x100x5", 150, 100, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS150x100x6_3": __RHSProfileParameters("RHS150x100x6.3", 150, 100, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS150x100x8": __RHSProfileParameters("RHS150x100x8", 150, 100, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS150x100x10": __RHSProfileParameters("RHS150x100x10", 150, 100, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS150x100x12_5": __RHSProfileParameters("RHS150x100x12.5", 150, 100, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS160x80x4": __RHSProfileParameters("RHS160x80x4", 160, 80, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS160x80x5": __RHSProfileParameters("RHS160x80x5", 160, 80, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS160x80x6_3": __RHSProfileParameters("RHS160x80x6.3", 160, 80, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS160x80x8": __RHSProfileParameters("RHS160x80x8", 160, 80, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS160x80x10": __RHSProfileParameters("RHS160x80x10", 160, 80, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS160x80x12_5": __RHSProfileParameters("RHS160x80x12.5", 160, 80, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS180x100x4": __RHSProfileParameters("RHS180x100x4", 180, 100, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS180x100x5": __RHSProfileParameters("RHS180x100x5", 180, 100, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS180x100x6_3": __RHSProfileParameters("RHS180x100x6.3", 180, 100, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS180x100x8": __RHSProfileParameters("RHS180x100x8", 180, 100, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS180x100x10": __RHSProfileParameters("RHS180x100x10", 180, 100, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS180x100x12_5": __RHSProfileParameters("RHS180x100x12.5", 180, 100, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS200x100x4": __RHSProfileParameters("RHS200x100x4", 200, 100, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "RHS200x100x5": __RHSProfileParameters("RHS200x100x5", 200, 100, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "RHS200x100x6_3": __RHSProfileParameters("RHS200x100x6.3", 200, 100, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS200x100x8": __RHSProfileParameters("RHS200x100x8", 200, 100, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS200x100x10": __RHSProfileParameters("RHS200x100x10", 200, 100, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS200x100x12_5": __RHSProfileParameters("RHS200x100x12.5", 200, 100, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS200x100x16": __RHSProfileParameters("RHS200x100x16", 200, 100, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "RHS200x120x6_3": __RHSProfileParameters("RHS200x120x6.3", 200, 120, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS200x120x8": __RHSProfileParameters("RHS200x120x8", 200, 120, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS200x120x10": __RHSProfileParameters("RHS200x120x10", 200, 120, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS200x120x12_5": __RHSProfileParameters("RHS200x120x12.5", 200, 120, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS250x150x6_3": __RHSProfileParameters("RHS250x150x6.3", 250, 150, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS250x150x8": __RHSProfileParameters("RHS250x150x8", 250, 150, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS250x150x10": __RHSProfileParameters("RHS250x150x10", 250, 150, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS250x150x12_5": __RHSProfileParameters("RHS250x150x12.5", 250, 150, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS250x150x14_2": __RHSProfileParameters("RHS250x150x14.2", 250, 150, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "RHS250x150x16": __RHSProfileParameters("RHS250x150x16", 250, 150, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "RHS260x180x6_3": __RHSProfileParameters("RHS260x180x6.3", 260, 180, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS260x180x8": __RHSProfileParameters("RHS260x180x8", 260, 180, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS260x180x10": __RHSProfileParameters("RHS260x180x10", 260, 180, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS260x180x12_5": __RHSProfileParameters("RHS260x180x12.5", 260, 180, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS260x180x14_2": __RHSProfileParameters("RHS260x180x14.2", 260, 180, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "RHS260x180x16": __RHSProfileParameters("RHS260x180x16", 260, 180, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "RHS300x200x6_3": __RHSProfileParameters("RHS300x200x6.3", 300, 200, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS300x200x8": __RHSProfileParameters("RHS300x200x8", 300, 200, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS300x200x10": __RHSProfileParameters("RHS300x200x10", 300, 200, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS300x200x12_5": __RHSProfileParameters("RHS300x200x12.5", 300, 200, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS300x200x14_2": __RHSProfileParameters("RHS300x200x14.2", 300, 200, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "RHS300x200x16": __RHSProfileParameters("RHS300x200x16", 300, 200, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "RHS350x250x6_3": __RHSProfileParameters("RHS350x250x6.3", 350, 250, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "RHS350x250x8": __RHSProfileParameters("RHS350x250x8", 350, 250, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS350x250x10": __RHSProfileParameters("RHS350x250x10", 350, 250, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS350x250x12_5": __RHSProfileParameters("RHS350x250x12.5", 350, 250, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS350x250x14_2": __RHSProfileParameters("RHS350x250x14.2", 350, 250, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "RHS350x250x16": __RHSProfileParameters("RHS350x250x16", 350, 250, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "RHS400x200x8": __RHSProfileParameters("RHS400x200x8", 400, 200, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS400x200x10": __RHSProfileParameters("RHS400x200x10", 400, 200, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS400x200x12_5": __RHSProfileParameters("RHS400x200x12.5", 400, 200, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS400x200x14_2": __RHSProfileParameters("RHS400x200x14.2", 400, 200, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "RHS400x200x16": __RHSProfileParameters("RHS400x200x16", 400, 200, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "RHS450x250x8": __RHSProfileParameters("RHS450x250x8", 450, 250, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "RHS450x250x10": __RHSProfileParameters("RHS450x250x10", 450, 250, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS450x250x12_5": __RHSProfileParameters("RHS450x250x12.5", 450, 250, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS450x250x14_2": __RHSProfileParameters("RHS450x250x14.2", 450, 250, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "RHS450x250x16": __RHSProfileParameters("RHS450x250x16", 450, 250, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "RHS500x300x10": __RHSProfileParameters("RHS500x300x10", 500, 300, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "RHS500x300x12_5": __RHSProfileParameters("RHS500x300x12.5", 500, 300, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "RHS500x300x14_2": __RHSProfileParameters("RHS500x300x14.2", 500, 300, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "RHS500x300x16": __RHSProfileParameters("RHS500x300x16", 500, 300, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "RHS500x300x20": __RHSProfileParameters("RHS500x300x20", 500, 300, 20, 20, 20, 20, 30, 30, 30, 30, 20, 20, 20, 20),
}


class RHS(metaclass=StandardProfileMeta):
    """Geometrical representation of RHS steel profiles.

    This class provides access to standard RHS profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a RHSProfile instance.

    Note: the corners of SHS profiles are not of constant thickness but are thicker,
    this feature has not been implemented yet in Blueprints.
    The corners are conservatively approximated by assuming a constant radius following the outside perimeter.

    Usage example
    -------------
        >>> profile = RHS.RHS100x50x4
        >>> print(isinstance(profile, RHSProfile))  # True
        >>>
        >>> # To iterate over all available RHS profiles:
        >>> for profile in RHS:
        >>>     print(isinstance(profile, RHSProfile))  # True
    """

    _factory = RHSProfile
    """Factory class for creating standard RHS profiles."""
    _database = RHS_PROFILES_DATABASE
    """Database of standard RHS profile parameters."""
