"""IPE Steel Profiles."""

from enum import Enum

from blueprints.type_alias import MM


class IPE(Enum):
    """Enumeration of IPE steel profiles with dimensions."""

    IPE_80 = ("IPE80", 80, 46, 3.8, 5.2, 5)
    IPE_100 = ("IPE100", 100, 55, 4.1, 5.7, 7)
    IPE_120 = ("IPE120", 120, 64, 4.4, 6.3, 7)
    IPE_140 = ("IPE140", 140, 73, 4.7, 6.9, 7)
    IPE_160 = ("IPE160", 160, 82, 5.0, 7.4, 9)
    IPE_180 = ("IPE180", 180, 91, 5.3, 8.0, 9)
    IPE_200 = ("IPE200", 200, 100, 5.6, 8.5, 12)
    IPE_220 = ("IPE220", 220, 110, 5.9, 9.2, 12)
    IPE_240 = ("IPE240", 240, 120, 6.2, 9.8, 15)
    IPE_270 = ("IPE270", 270, 135, 6.6, 10.2, 15)
    IPE_300 = ("IPE300", 300, 150, 7.1, 10.7, 15)
    IPE_330 = ("IPE330", 330, 160, 7.5, 11.5, 18)
    IPE_360 = ("IPE360", 360, 170, 8.0, 12.7, 18)
    IPE_400 = ("IPE400", 400, 180, 8.6, 13.5, 21)
    IPE_450 = ("IPE450", 450, 190, 9.4, 14.6, 21)
    IPE_500 = ("IPE500", 500, 200, 10.2, 16.0, 21)
    IPE_550 = ("IPE550", 550, 210, 11.1, 17.2, 24)
    IPE_600 = ("IPE600", 600, 220, 12.0, 19.0, 24)

    def __init__(self, code: str, h: MM, b: MM, t_w: MM, t_f: MM, radius: MM) -> None:
        """Initialize IPE profile.
        Args:
            code (str): Profile code.
            h (MM): Total height.
            b (MM): Total width.
            t_w (MM): Web thickness.
            t_f (MM): Flange thickness.
            radius (MM): Radius.
        """
        self.code = code
        self.top_flange_width = b
        self.top_flange_thickness = t_f
        self.bottom_flange_width = b
        self.bottom_flange_thickness = t_f
        self.total_height = h
        self.web_thickness = t_w
        self.top_radius = radius
        self.bottom_radius = radius
