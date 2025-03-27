"""HEM Steel Profiles."""

from enum import Enum

from blueprints.type_alias import MM


class HEMProfile(Enum):
    """Enumeration of HEM steel profiles with dimensions."""

    HEM_100 = ("HEM100", 120, 106, 12, 20, 12)
    HEM_120 = ("HEM120", 140, 126, 12.5, 21, 12)
    HEM_140 = ("HEM140", 160, 146, 13, 22, 12)
    HEM_160 = ("HEM160", 180, 166, 14, 23, 15)
    HEM_180 = ("HEM180", 200, 186, 14.5, 24, 15)
    HEM_200 = ("HEM200", 220, 206, 15, 25, 18)
    HEM_220 = ("HEM220", 240, 226, 15.5, 26, 18)
    HEM_240 = ("HEM240", 270, 248, 18, 32, 21)
    HEM_260 = ("HEM260", 290, 268, 18, 32.5, 24)
    HEM_280 = ("HEM280", 310, 288, 18.5, 33, 24)
    HEM_300 = ("HEM300", 340, 310, 21, 39, 27)
    HEM_320 = ("HEM320", 359, 309, 21, 40, 27)
    HEM_340 = ("HEM340", 377, 309, 21, 40, 27)
    HEM_360 = ("HEM360", 395, 308, 21, 40, 27)
    HEM_400 = ("HEM400", 432, 307, 21, 40, 27)
    HEM_450 = ("HEM450", 478, 307, 21, 40, 27)
    HEM_500 = ("HEM500", 524, 306, 21, 40, 27)
    HEM_550 = ("HEM550", 572, 306, 21, 40, 27)
    HEM_600 = ("HEM600", 620, 305, 21, 40, 27)
    HEM_650 = ("HEM650", 668, 305, 21, 40, 27)
    HEM_700 = ("HEM700", 716, 304, 21, 40, 27)
    HEM_800 = ("HEM800", 814, 303, 21, 40, 30)
    HEM_900 = ("HEM900", 910, 302, 21, 40, 30)
    HEM_1000 = ("HEM1000", 1008, 302, 21, 40, 30)

    def __init__(self, code: str, h: MM, b: MM, t_w: MM, t_f: MM, radius: MM) -> None:
        """Initialize HEM profile.
        Args:
            code (str): Profile code.
            h (MM): Total height.
            b (MM): Total width.
            t_w (MM): Web thickness.
            t_f (MM): Flange thickness.
            radius (MM): Radius.
        """
        self.code = code
        self.h = h
        self.b = b
        self.t_w = t_w
        self.t_f = t_f
        self.radius = radius
