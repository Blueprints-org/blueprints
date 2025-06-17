"""HEM Steel Profiles."""

from enum import Enum

from blueprints.type_alias import MM


class HEM(Enum):
    """Geometrical representation of HEM steel profiles."""

    HEM100 = ("HEM100", 120, 106, 12, 20, 12)
    HEM120 = ("HEM120", 140, 126, 12.5, 21, 12)
    HEM140 = ("HEM140", 160, 146, 13, 22, 12)
    HEM160 = ("HEM160", 180, 166, 14, 23, 15)
    HEM180 = ("HEM180", 200, 186, 14.5, 24, 15)
    HEM200 = ("HEM200", 220, 206, 15, 25, 18)
    HEM220 = ("HEM220", 240, 226, 15.5, 26, 18)
    HEM240 = ("HEM240", 270, 248, 18, 32, 21)
    HEM260 = ("HEM260", 290, 268, 18, 32.5, 24)
    HEM280 = ("HEM280", 310, 288, 18.5, 39, 24)
    HEM300 = ("HEM300", 340, 310, 21, 39, 27)
    HEM320 = ("HEM320", 359, 309, 21, 40, 27)
    HEM340 = ("HEM340", 377, 309, 21, 40, 27)
    HEM360 = ("HEM360", 395, 308, 21, 40, 27)
    HEM400 = ("HEM400", 432, 307, 21, 40, 27)
    HEM450 = ("HEM450", 478, 307, 21, 40, 27)
    HEM500 = ("HEM500", 524, 306, 21, 40, 27)
    HEM550 = ("HEM550", 572, 306, 21, 40, 27)
    HEM600 = ("HEM600", 620, 305, 21, 40, 27)
    HEM650 = ("HEM650", 668, 305, 21, 40, 27)
    HEM700 = ("HEM700", 716, 304, 21, 40, 27)
    HEM800 = ("HEM800", 814, 303, 21, 40, 30)
    HEM900 = ("HEM900", 910, 302, 21, 40, 30)
    HEM1000 = ("HEM1000", 1008, 302, 21, 40, 30)

    def __init__(self, alias: str, h: MM, b: MM, t_w: MM, t_f: MM, radius: MM) -> None:
        """Initialize HEM profile.

        This method sets the profile's alias, dimensions, and radii.

        Parameters
        ----------
        alias: str
            Profile alias.
        h: MM
            Total height of the profile.
        b: MM
            Total width of the profile.
        t_w: MM
            Web thickness of the profile.
        t_f: MM
            Flange thickness of the profile.
        radius: MM
            Radius of the profile.
        """
        self.alias = alias
        self.top_flange_width = b
        self.top_flange_thickness = t_f
        self.bottom_flange_width = b
        self.bottom_flange_thickness = t_f
        self.total_height = h
        self.web_thickness = t_w
        self.top_radius = radius
        self.bottom_radius = radius
