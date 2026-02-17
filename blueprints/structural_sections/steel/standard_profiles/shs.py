"""SHS Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.rhs_profile import RHSProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __SHSProfileParameters(NamedTuple):
    """Parameters for defining a SHS profile."""

    name: str
    """Name of the SHS profile."""
    total_height: MM
    """Total height of the SHS profile."""
    total_width: MM
    """Total width of the SHS profile."""
    left_wall_thickness: MM
    """Thickness of the left wall of the SHS profile."""
    right_wall_thickness: MM
    """Thickness of the right wall of the SHS profile."""
    top_wall_thickness: MM
    """Thickness of the top wall of the SHS profile."""
    bottom_wall_thickness: MM
    """Thickness of the bottom wall of the SHS profile."""
    top_right_outer_radius: MM
    """Outer radius of the top right corner of the SHS profile."""
    top_left_outer_radius: MM
    """Outer radius of the top left corner of the SHS profile."""
    bottom_right_outer_radius: MM
    """Outer radius of the bottom right corner of the SHS profile."""
    bottom_left_outer_radius: MM
    """Outer radius of the bottom left corner of the SHS profile."""
    top_right_inner_radius: MM
    """Inner radius of the top right corner of the SHS profile."""
    top_left_inner_radius: MM
    """Inner radius of the top left corner of the SHS profile."""
    bottom_right_inner_radius: MM
    """Inner radius of the bottom right corner of the SHS profile."""
    bottom_left_inner_radius: MM
    """Inner radius of the bottom left corner of the SHS profile."""


SHS_PROFILES_DATABASE = {
    "SHS40x2_6": __SHSProfileParameters("SHS40x2.6", 40, 40, 2.6, 2.6, 2.6, 2.6, 3.9, 3.9, 3.9, 3.9, 2.6, 2.6, 2.6, 2.6),
    "SHS40x3_2": __SHSProfileParameters("SHS40x3.2", 40, 40, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "SHS40x4": __SHSProfileParameters("SHS40x4", 40, 40, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "SHS40x5": __SHSProfileParameters("SHS40x5", 40, 40, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS50x2_6": __SHSProfileParameters("SHS50x2.6", 50, 50, 2.6, 2.6, 2.6, 2.6, 3.9, 3.9, 3.9, 3.9, 2.6, 2.6, 2.6, 2.6),
    "SHS50x3_2": __SHSProfileParameters("SHS50x3.2", 50, 50, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "SHS50x4": __SHSProfileParameters("SHS50x4", 50, 50, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "SHS50x5": __SHSProfileParameters("SHS50x5", 50, 50, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS50x6_3": __SHSProfileParameters("SHS50x6.3", 50, 50, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS60x2_6": __SHSProfileParameters("SHS60x2.6", 60, 60, 2.6, 2.6, 2.6, 2.6, 3.9, 3.9, 3.9, 3.9, 2.6, 2.6, 2.6, 2.6),
    "SHS60x3_2": __SHSProfileParameters("SHS60x3.2", 60, 60, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "SHS60x4": __SHSProfileParameters("SHS60x4", 60, 60, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "SHS60x5": __SHSProfileParameters("SHS60x5", 60, 60, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS60x6_3": __SHSProfileParameters("SHS60x6.3", 60, 60, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS60x8": __SHSProfileParameters("SHS60x8", 60, 60, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS70x3_2": __SHSProfileParameters("SHS70x3.2", 70, 70, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "SHS70x4": __SHSProfileParameters("SHS70x4", 70, 70, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "SHS70x5": __SHSProfileParameters("SHS70x5", 70, 70, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS70x6_3": __SHSProfileParameters("SHS70x6.3", 70, 70, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS70x8": __SHSProfileParameters("SHS70x8", 70, 70, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS80x3_2": __SHSProfileParameters("SHS80x3.2", 80, 80, 3.2, 3.2, 3.2, 3.2, 4.8, 4.8, 4.8, 4.8, 3.2, 3.2, 3.2, 3.2),
    "SHS80x4": __SHSProfileParameters("SHS80x4", 80, 80, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "SHS80x5": __SHSProfileParameters("SHS80x5", 80, 80, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS80x6_3": __SHSProfileParameters("SHS80x6.3", 80, 80, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS80x8": __SHSProfileParameters("SHS80x8", 80, 80, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS90x4": __SHSProfileParameters("SHS90x4", 90, 90, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "SHS90x5": __SHSProfileParameters("SHS90x5", 90, 90, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS90x6_3": __SHSProfileParameters("SHS90x6.3", 90, 90, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS90x8": __SHSProfileParameters("SHS90x8", 90, 90, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS100x4": __SHSProfileParameters("SHS100x4", 100, 100, 4, 4, 4, 4, 6, 6, 6, 6, 4, 4, 4, 4),
    "SHS100x5": __SHSProfileParameters("SHS100x5", 100, 100, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS100x6_3": __SHSProfileParameters("SHS100x6.3", 100, 100, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS100x8": __SHSProfileParameters("SHS100x8", 100, 100, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS100x10": __SHSProfileParameters("SHS100x10", 100, 100, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS120x5": __SHSProfileParameters("SHS120x5", 120, 120, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS120x6_3": __SHSProfileParameters("SHS120x6.3", 120, 120, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS120x8": __SHSProfileParameters("SHS120x8", 120, 120, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS120x10": __SHSProfileParameters("SHS120x10", 120, 120, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS120x12_5": __SHSProfileParameters("SHS120x12.5", 120, 120, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS140x5": __SHSProfileParameters("SHS140x5", 140, 140, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS140x6_3": __SHSProfileParameters("SHS140x6.3", 140, 140, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS140x8": __SHSProfileParameters("SHS140x8", 140, 140, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS140x10": __SHSProfileParameters("SHS140x10", 140, 140, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS140x12_5": __SHSProfileParameters("SHS140x12.5", 140, 140, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS150x5": __SHSProfileParameters("SHS150x5", 150, 150, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS150x6_3": __SHSProfileParameters("SHS150x6.3", 150, 150, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS150x8": __SHSProfileParameters("SHS150x8", 150, 150, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS150x10": __SHSProfileParameters("SHS150x10", 150, 150, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS150x12_5": __SHSProfileParameters("SHS150x12.5", 150, 150, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS150x14_2": __SHSProfileParameters("SHS150x14.2", 150, 150, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS150x16": __SHSProfileParameters("SHS150x16", 150, 150, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS160x5": __SHSProfileParameters("SHS160x5", 160, 160, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS160x6_3": __SHSProfileParameters("SHS160x6.3", 160, 160, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS160x8": __SHSProfileParameters("SHS160x8", 160, 160, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS160x10": __SHSProfileParameters("SHS160x10", 160, 160, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS160x12_5": __SHSProfileParameters("SHS160x12.5", 160, 160, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS160x14_2": __SHSProfileParameters("SHS160x14.2", 160, 160, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS160x16": __SHSProfileParameters("SHS160x16", 160, 160, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS180x5": __SHSProfileParameters("SHS180x5", 180, 180, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS180x6_3": __SHSProfileParameters("SHS180x6.3", 180, 180, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS180x8": __SHSProfileParameters("SHS180x8", 180, 180, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS180x10": __SHSProfileParameters("SHS180x10", 180, 180, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS180x12_5": __SHSProfileParameters("SHS180x12.5", 180, 180, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS180x14_2": __SHSProfileParameters("SHS180x14.2", 180, 180, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS180x16": __SHSProfileParameters("SHS180x16", 180, 180, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS200x5": __SHSProfileParameters("SHS200x5", 200, 200, 5, 5, 5, 5, 7.5, 7.5, 7.5, 7.5, 5, 5, 5, 5),
    "SHS200x6_3": __SHSProfileParameters("SHS200x6.3", 200, 200, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS200x8": __SHSProfileParameters("SHS200x8", 200, 200, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS200x10": __SHSProfileParameters("SHS200x10", 200, 200, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS200x12_5": __SHSProfileParameters("SHS200x12.5", 200, 200, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS200x14_2": __SHSProfileParameters("SHS200x14.2", 200, 200, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS200x16": __SHSProfileParameters("SHS200x16", 200, 200, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS220x6_3": __SHSProfileParameters("SHS220x6.3", 220, 220, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS220x8": __SHSProfileParameters("SHS220x8", 220, 220, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS220x10": __SHSProfileParameters("SHS220x10", 220, 220, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS220x12_5": __SHSProfileParameters("SHS220x12.5", 220, 220, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS220x14_2": __SHSProfileParameters("SHS220x14.2", 220, 220, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS220x16": __SHSProfileParameters("SHS220x16", 220, 220, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS250x6_3": __SHSProfileParameters("SHS250x6.3", 250, 250, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS250x8": __SHSProfileParameters("SHS250x8", 250, 250, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS250x10": __SHSProfileParameters("SHS250x10", 250, 250, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS250x12_5": __SHSProfileParameters("SHS250x12.5", 250, 250, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS250x14_2": __SHSProfileParameters("SHS250x14.2", 250, 250, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS250x16": __SHSProfileParameters("SHS250x16", 250, 250, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS260x6_3": __SHSProfileParameters("SHS260x6.3", 260, 260, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS260x8": __SHSProfileParameters("SHS260x8", 260, 260, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS260x10": __SHSProfileParameters("SHS260x10", 260, 260, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS260x12_5": __SHSProfileParameters("SHS260x12.5", 260, 260, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS260x14_2": __SHSProfileParameters("SHS260x14.2", 260, 260, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS260x16": __SHSProfileParameters("SHS260x16", 260, 260, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS300x6_3": __SHSProfileParameters("SHS300x6.3", 300, 300, 6.3, 6.3, 6.3, 6.3, 9.4, 9.4, 9.4, 9.4, 6.3, 6.3, 6.3, 6.3),
    "SHS300x8": __SHSProfileParameters("SHS300x8", 300, 300, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS300x10": __SHSProfileParameters("SHS300x10", 300, 300, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS300x12_5": __SHSProfileParameters("SHS300x12.5", 300, 300, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS300x14_2": __SHSProfileParameters("SHS300x14.2", 300, 300, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS300x16": __SHSProfileParameters("SHS300x16", 300, 300, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS350x8": __SHSProfileParameters("SHS350x8", 350, 350, 8, 8, 8, 8, 12, 12, 12, 12, 8, 8, 8, 8),
    "SHS350x10": __SHSProfileParameters("SHS350x10", 350, 350, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS350x12_5": __SHSProfileParameters("SHS350x12.5", 350, 350, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS350x14_2": __SHSProfileParameters("SHS350x14.2", 350, 350, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS350x16": __SHSProfileParameters("SHS350x16", 350, 350, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS400x10": __SHSProfileParameters("SHS400x10", 400, 400, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10),
    "SHS400x12_5": __SHSProfileParameters("SHS400x12.5", 400, 400, 12.5, 12.5, 12.5, 12.5, 18.8, 18.8, 18.8, 18.8, 12.5, 12.5, 12.5, 12.5),
    "SHS400x14_2": __SHSProfileParameters("SHS400x14.2", 400, 400, 14.2, 14.2, 14.2, 14.2, 21.3, 21.3, 21.3, 21.3, 14.2, 14.2, 14.2, 14.2),
    "SHS400x16": __SHSProfileParameters("SHS400x16", 400, 400, 16, 16, 16, 16, 24, 24, 24, 24, 16, 16, 16, 16),
    "SHS400x20": __SHSProfileParameters("SHS400x20", 400, 400, 20, 20, 20, 20, 30, 30, 30, 30, 20, 20, 20, 20),
}


class SHS(metaclass=StandardProfileMeta):
    """Geometrical representation of SHS steel profiles.

    This class provides access to standard SHS profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a RHSProfile instance.

    Note: the corners of SHS profiles are not of constant thickness but are thicker,
    this feature has not been implemented yet in Blueprints.
    The corners are conservatively approximated by assuming a constant radius following the outside perimeter.

    Usage example
    -------------
        >>> profile = SHS.SHS100x5
        >>> print(isinstance(profile, RHSProfile))  # True
        >>>
        >>> # To iterate over all available SHS profiles:
        >>> for profile in SHS:
        >>>     print(isinstance(profile, RHSProfile))  # True
    """

    _factory = RHSProfile
    """Factory class for creating standard SHS profiles."""
    _database = SHS_PROFILES_DATABASE
    """Database of standard SHS profile parameters."""
