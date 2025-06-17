"""HEA Steel Profiles."""

from enum import Enum

from blueprints.type_alias import MM


class HEA(Enum):
    """Geometrical representation of HEA steel profiles."""

    HEA100 = ("HEA100", 96, 100, 5, 8, 12)
    HEA120 = ("HEA120", 114, 120, 5, 8, 12)
    HEA140 = ("HEA140", 133, 140, 5.5, 8.5, 12)
    HEA160 = ("HEA160", 152, 160, 6, 9, 15)
    HEA180 = ("HEA180", 171, 180, 6, 9.5, 15)
    HEA200 = ("HEA200", 190, 200, 6.5, 10, 18)
    HEA220 = ("HEA220", 210, 220, 7, 11, 18)
    HEA240 = ("HEA240", 230, 240, 7.5, 12, 21)
    HEA260 = ("HEA260", 250, 260, 7.5, 12.5, 24)
    HEA280 = ("HEA280", 270, 280, 8, 13, 24)
    HEA300 = ("HEA300", 290, 300, 8.5, 14, 27)
    HEA320 = ("HEA320", 310, 300, 9, 15.5, 27)
    HEA340 = ("HEA340", 330, 300, 9.5, 16.5, 27)
    HEA360 = ("HEA360", 350, 300, 10, 17.5, 27)
    HEA400 = ("HEA400", 390, 300, 11, 19, 27)
    HEA450 = ("HEA450", 440, 300, 11.5, 21, 27)
    HEA500 = ("HEA500", 490, 300, 12, 23, 27)
    HEA550 = ("HEA550", 540, 300, 12.5, 24, 27)
    HEA600 = ("HEA600", 590, 300, 13, 25, 27)
    HEA650 = ("HEA650", 640, 300, 13.5, 26, 27)
    HEA700 = ("HEA700", 690, 300, 14.5, 27, 27)
    HEA800 = ("HEA800", 790, 300, 15, 28, 30)
    HEA900 = ("HEA900", 890, 300, 16, 30, 30)
    HEA1000 = ("HEA1000", 990, 300, 16.5, 31, 30)

    def __init__(self, alias: str, h: MM, b: MM, t_w: MM, t_f: MM, radius: MM) -> None:
        """Initialize HEA profile.

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
        self.web_height = h - 2 * t_f - 2 * radius
        self.top_radius = radius
        self.bottom_radius = radius
