"""HEB Steel Profiles."""

from enum import Enum

from blueprints.type_alias import MM


class HEB(Enum):
    """Geometrical representation of HEB steel profiles."""

    HEB100 = ("HEB100", 100, 100, 6, 10, 12)
    HEB120 = ("HEB120", 120, 120, 6.5, 11, 12)
    HEB140 = ("HEB140", 140, 140, 7, 12, 12)
    HEB160 = ("HEB160", 160, 160, 8, 13, 15)
    HEB180 = ("HEB180", 180, 180, 8.5, 14, 15)
    HEB200 = ("HEB200", 200, 200, 9, 15, 18)
    HEB220 = ("HEB220", 220, 220, 9.5, 16, 18)
    HEB240 = ("HEB240", 240, 240, 10, 17, 21)
    HEB260 = ("HEB260", 260, 260, 10, 17.5, 24)
    HEB280 = ("HEB280", 280, 280, 10.5, 18, 24)
    HEB300 = ("HEB300", 300, 300, 11, 19, 27)
    HEB320 = ("HEB320", 320, 300, 11.5, 20.5, 27)
    HEB340 = ("HEB340", 340, 300, 12, 21.5, 27)
    HEB360 = ("HEB360", 360, 300, 12.5, 22.5, 27)
    HEB400 = ("HEB400", 400, 300, 13.5, 24, 27)
    HEB450 = ("HEB450", 450, 300, 14, 26, 27)
    HEB500 = ("HEB500", 500, 300, 14.5, 28, 27)
    HEB550 = ("HEB550", 550, 300, 15, 29, 27)
    HEB600 = ("HEB600", 600, 300, 15.5, 30, 27)
    HEB650 = ("HEB650", 650, 300, 16, 31, 27)
    HEB700 = ("HEB700", 700, 300, 17, 32, 27)
    HEB800 = ("HEB800", 800, 300, 17.5, 33, 30)
    HEB900 = ("HEB900", 900, 300, 18.5, 35, 30)
    HEB1000 = ("HEB1000", 1000, 300, 19, 36, 30)

    def __init__(self, alias: str, h: MM, b: MM, t_w: MM, t_f: MM, radius: MM) -> None:
        """Initialize HEB profile.

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
