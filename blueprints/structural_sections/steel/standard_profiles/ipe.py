"""IPE Steel Profiles."""

from enum import Enum
from typing import Self

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.type_alias import MM
from blueprints.utils.abc_enum_meta import ABCEnumMeta


class IPE(IProfile, Enum, metaclass=ABCEnumMeta):
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

    def __new__(cls, name: str, h: MM, b: MM, t_w: MM, t_f: MM, radius: MM) -> Self:
        """Create a new IPE profile enum member.

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

        Returns
        -------
        Self
            The newly created IPE profile enum member.
        """
        obj = object.__new__(cls)
        obj._value_ = (name, h, b, t_w, t_f, radius)

        # Initialize IProfile fields
        object.__setattr__(obj, "name", name)
        object.__setattr__(obj, "top_flange_width", b)
        object.__setattr__(obj, "top_flange_thickness", t_f)
        object.__setattr__(obj, "bottom_flange_width", b)
        object.__setattr__(obj, "bottom_flange_thickness", t_f)
        object.__setattr__(obj, "total_height", h)
        object.__setattr__(obj, "web_thickness", t_w)
        object.__setattr__(obj, "top_radius", radius)
        object.__setattr__(obj, "bottom_radius", radius)

        # Compute derived fields
        IProfile.__post_init__(obj)

        return obj

    def __init__(self, name: str, h: MM, b: MM, t_w: MM, t_f: MM, radius: MM) -> None:
        """Initialize the IPE profile enum member.

        Note
        ----
        This method is intentionally left blank because all initialization is handled in __new__.

        Parameters
        ----------
        name: str
            Profile name.
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
