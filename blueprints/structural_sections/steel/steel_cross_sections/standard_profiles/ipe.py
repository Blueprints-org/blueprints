"""IPE Steel Profiles."""

from enum import Enum

from blueprints.type_alias import MM


class IPE(Enum):
    """Geometrical representation of IPE steel profiles."""

    IPE80 = ("IPE80", 80, 46, 3.8, 5.2, 5)
    IPE100 = ("IPE100", 100, 55, 4.1, 5.7, 7)
    IPE120 = ("IPE120", 120, 64, 4.4, 6.3, 7)
    IPE140 = ("IPE140", 140, 73, 4.7, 6.9, 7)
    IPE160 = ("IPE160", 160, 82, 5.0, 7.4, 9)
    IPE180 = ("IPE180", 180, 91, 5.3, 8.0, 9)
    IPE200 = ("IPE200", 200, 100, 5.6, 8.5, 12)
    IPE220 = ("IPE220", 220, 110, 5.9, 9.2, 12)
    IPE240 = ("IPE240", 240, 120, 6.2, 9.8, 15)
    IPE270 = ("IPE270", 270, 135, 6.6, 10.2, 15)
    IPE300 = ("IPE300", 300, 150, 7.1, 10.7, 15)
    IPE330 = ("IPE330", 330, 160, 7.5, 11.5, 18)
    IPE360 = ("IPE360", 360, 170, 8.0, 12.7, 18)
    IPE400 = ("IPE400", 400, 180, 8.6, 13.5, 21)
    IPE450 = ("IPE450", 450, 190, 9.4, 14.6, 21)
    IPE500 = ("IPE500", 500, 200, 10.2, 16.0, 21)
    IPE550 = ("IPE550", 550, 210, 11.1, 17.2, 24)
    IPE600 = ("IPE600", 600, 220, 12.0, 19.0, 24)

    def __init__(self, alias: str, h: MM, b: MM, t_w: MM, t_f: MM, radius: MM) -> None:
        """Initialize IPE profile.

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
