"""LNP Steel Profiles."""

from enum import Enum

from blueprints.type_alias import MM


class LNP(Enum):
    r"""Geometrical representation of LNP steel profiles.

       ↓-- Web thickness
      ┌──\ <-- Toe radius
      │  │
      │  │
      │  │
      │  │
    > │   \ <-- Root radius
    | │    \_____
    | │          \ <-- Base thickness
    | └───────────┘
    |     ^ Width
    Height

    The horizontal leg is at the top, the vertical leg descends from the left.
    """

    LNP_40x40x4 = ("LNP 40x40x4", 40, 40, 4, 6, 3)
    LNP_40x40x5 = ("LNP 40x40x5", 40, 40, 5, 6, 3)
    LNP_45x45x5 = ("LNP 45x45x5", 45, 45, 5, 7, 3.5)
    LNP_50x50x5 = ("LNP 50x50x5", 50, 50, 5, 7, 3.5)
    LNP_50x50x6 = ("LNP 50x50x6", 50, 50, 6, 7, 3.5)
    LNP_50x50x8 = ("LNP 50x50x8", 50, 50, 8, 7, 3.5)
    LNP_50x30x4 = ("LNP 50x30x4", 50, 30, 4, 5, 2.5)
    LNP_50x30x5 = ("LNP 50x30x5", 50, 30, 5, 5, 2.5)
    LNP_55x55x6 = ("LNP 55x55x6", 55, 55, 6, 8, 4)
    LNP_60x60x6 = ("LNP 60x60x6", 60, 60, 6, 8, 4)
    LNP_60x60x8 = ("LNP 60x60x8", 60, 60, 8, 8, 4)
    LNP_60x60x10 = ("LNP 60x60x10", 60, 60, 10, 8, 4)
    LNP_60x30x5 = ("LNP 60x30x5", 60, 30, 5, 5, 2.5)
    LNP_60x30x7 = ("LNP 60x30x7", 60, 30, 7, 5, 2.5)
    LNP_60x40x5 = ("LNP 60x40x5", 60, 40, 5, 6, 3)
    LNP_60x40x6 = ("LNP 60x40x6", 60, 40, 6, 6, 3)
    LNP_60x40x7 = ("LNP 60x40x7", 60, 40, 7, 6, 3)
    LNP_65x65x7 = ("LNP 65x65x7", 65, 65, 7, 9, 4.5)
    LNP_70x70x7 = ("LNP 70x70x7", 70, 70, 7, 9, 4.5)
    LNP_70x70x9 = ("LNP 70x70x9", 70, 70, 9, 9, 4.5)
    LNP_70x50x6 = ("LNP 70x50x6", 70, 50, 6, 7, 3.5)
    LNP_75x75x8 = ("LNP 75x75x8", 75, 75, 8, 9, 4.5)
    LNP_75x50x6 = ("LNP 75x50x6", 75, 50, 6, 7, 3.5)
    LNP_75x50x7 = ("LNP 75x50x7", 75, 50, 7, 7, 3.5)
    LNP_80x80x8 = ("LNP 80x80x8", 80, 80, 8, 10, 5)
    LNP_80x80x10 = ("LNP 80x80x10", 80, 80, 10, 10, 5)
    LNP_80x80x12 = ("LNP 80x80x12", 80, 80, 12, 10, 5)
    LNP_80x40x6 = ("LNP 80x40x6", 80, 40, 6, 7, 3.5)
    LNP_80x40x8 = ("LNP 80x40x8", 80, 40, 8, 7, 3.5)
    LNP_90x90x9 = ("LNP 90x90x9", 90, 90, 9, 11, 5.5)
    LNP_90x60x6 = ("LNP 90x60x6", 90, 60, 6, 7, 3.5)
    LNP_90x60x8 = ("LNP 90x60x8", 90, 60, 8, 7, 3.5)
    LNP_100x100x10 = ("LNP 100x100x10", 100, 100, 10, 12, 6)
    LNP_100x100x12 = ("LNP 100x100x12", 100, 100, 12, 12, 6)
    LNP_100x100x14 = ("LNP 100x100x14", 100, 100, 14, 12, 6)
    LNP_100x50x6 = ("LNP 100x50x6", 100, 50, 6, 8, 4)
    LNP_100x50x8 = ("LNP 100x50x8", 100, 50, 8, 8, 4)
    LNP_100x50x10 = ("LNP 100x50x10", 100, 50, 10, 8, 4)
    LNP_100x65x7 = ("LNP 100x65x7", 100, 65, 7, 10, 5)
    LNP_100x65x9 = ("LNP 100x65x9", 100, 65, 9, 10, 5)
    LNP_100x65x11 = ("LNP 100x65x11", 100, 65, 11, 10, 5)
    LNP_100x75x9 = ("LNP 100x75x9", 100, 75, 9, 10, 5)
    LNP_110x110x10 = ("LNP 110x110x10", 110, 110, 10, 12, 6)
    LNP_120x120x10 = ("LNP 120x120x10", 120, 120, 10, 13, 6.5)
    LNP_120x120x12 = ("LNP 120x120x12", 120, 120, 12, 13, 6.5)
    LNP_120x120x15 = ("LNP 120x120x15", 120, 120, 15, 13, 6.5)
    LNP_120x80x8 = ("LNP 120x80x8", 120, 80, 8, 11, 5.5)
    LNP_120x80x10 = ("LNP 120x80x10", 120, 80, 10, 11, 5.5)
    LNP_120x80x12 = ("LNP 120x80x12", 120, 80, 12, 11, 5.5)
    LNP_130x130x12 = ("LNP 130x130x12", 130, 130, 12, 14, 7)
    LNP_130x65x8 = ("LNP 130x65x8", 130, 65, 8, 11, 5.5)
    LNP_130x65x10 = ("LNP 130x65x10", 130, 65, 10, 11, 5.5)
    LNP_130x65x12 = ("LNP 130x65x12", 130, 65, 12, 11, 5.5)
    LNP_140x140x13 = ("LNP 140x140x13", 140, 140, 13, 15, 7.5)
    LNP_140x140x15 = ("LNP 140x140x15", 140, 140, 15, 15, 7.5)
    LNP_150x150x14 = ("LNP 150x150x14", 150, 150, 14, 16, 8)
    LNP_150x150x16 = ("LNP 150x150x16", 150, 150, 16, 16, 8)
    LNP_150x75x9 = ("LNP 150x75x9", 150, 75, 9, 12, 6)
    LNP_150x75x11 = ("LNP 150x75x11", 150, 75, 11, 10.5, 5.5)
    LNP_150x100x10 = ("LNP 150x100x10", 150, 100, 10, 12, 6)
    LNP_150x100x12 = ("LNP 150x100x12", 150, 100, 12, 12, 6)
    LNP_150x100x14 = ("LNP 150x100x14", 150, 100, 14, 13, 6.5)
    LNP_160x160x15 = ("LNP 160x160x15", 160, 160, 15, 17, 8.5)
    LNP_160x160x17 = ("LNP 160x160x17", 160, 160, 17, 17, 8.5)
    LNP_160x160x20 = ("LNP 160x160x20", 160, 160, 20, 17, 8.5)
    LNP_160x80x10 = ("LNP 160x80x10", 160, 80, 10, 13, 6.5)
    LNP_160x80x12 = ("LNP 160x80x12", 160, 80, 12, 13, 6.5)
    LNP_160x80x14 = ("LNP 160x80x14", 160, 80, 14, 13, 6.5)
    LNP_180x180x16 = ("LNP 180x180x16", 180, 180, 16, 18, 9)
    LNP_180x180x18 = ("LNP 180x180x18", 180, 180, 18, 18, 9)
    LNP_180x180x20 = ("LNP 180x180x20", 180, 180, 20, 18, 9)
    LNP_200x200x16 = ("LNP 200x200x16", 200, 200, 16, 18, 9)
    LNP_200x200x18 = ("LNP 200x200x18", 200, 200, 18, 18, 9)
    LNP_200x200x20 = ("LNP 200x200x20", 200, 200, 20, 18, 9)
    LNP_200x200x22 = ("LNP 200x200x22", 200, 200, 22, 18, 9)
    LNP_200x200x24 = ("LNP 200x200x24", 200, 200, 24, 18, 9)
    LNP_200x200x26 = ("LNP 200x200x26", 200, 200, 26, 18, 9)
    LNP_200x100x10 = ("LNP 200x100x10", 200, 100, 10, 15, 7.5)
    LNP_200x100x12 = ("LNP 200x100x12", 200, 100, 12, 15, 7.5)
    LNP_200x100x14 = ("LNP 200x100x14", 200, 100, 14, 15, 7.5)
    LNP_200x100x16 = ("LNP 200x100x16", 200, 100, 16, 15, 7.5)

    def __init__(self, alias: str, h: MM, b: MM, t: MM, root_radius: MM, toe_radius: MM) -> None:
        """Initialize LNP profile.

        This method sets the profile's alias, dimensions, and radii.

        Parameters
        ----------
        alias: str
            Profile alias.
        h: MM
            Total height of the profile.
        b: MM
            Total width of the profile.
        t: MM
            Thickness of the profile.
        root_radius: MM
            Radius at the root of the profile.
        toe_radius: MM
            Radius at the toe of the profile.
        """
        self.alias = alias
        self.height = h
        self.width = b
        self.base_thickness = t
        self.web_thickness = t
        self.root_radius = root_radius
        self.back_radius = 0
        self.toe_radius = toe_radius
