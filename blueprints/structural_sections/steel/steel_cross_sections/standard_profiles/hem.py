"""HEM Steel Profiles."""
# ruff: noqa: RUF012

from enum import Enum


class HEMProfile(Enum):
    """Enumeration of HEM steel profiles with dimensions."""

    HEM_100 = {"name": "HEM100", "h": 120, "b": 106, "t_w": 12, "t_f": 20, "radius": 0}
    HEM_120 = {"name": "HEM120", "h": 140, "b": 126, "t_w": 12.5, "t_f": 21, "radius": 0}
    HEM_140 = {"name": "HEM140", "h": 160, "b": 146, "t_w": 13, "t_f": 22, "radius": 0}
    HEM_160 = {"name": "HEM160", "h": 180, "b": 166, "t_w": 14, "t_f": 23, "radius": 0}
    HEM_180 = {"name": "HEM180", "h": 200, "b": 186, "t_w": 14.5, "t_f": 24, "radius": 0}
    HEM_200 = {"name": "HEM200", "h": 220, "b": 206, "t_w": 15, "t_f": 25, "radius": 0}
    HEM_220 = {"name": "HEM220", "h": 240, "b": 226, "t_w": 15.5, "t_f": 26, "radius": 0}
    HEM_240 = {"name": "HEM240", "h": 270, "b": 248, "t_w": 18, "t_f": 32, "radius": 0}
    HEM_260 = {"name": "HEM260", "h": 290, "b": 268, "t_w": 18, "t_f": 32.5, "radius": 0}
    HEM_280 = {"name": "HEM280", "h": 310, "b": 288, "t_w": 18.5, "t_f": 33, "radius": 0}
    HEM_300 = {"name": "HEM300", "h": 340, "b": 310, "t_w": 21, "t_f": 39, "radius": 0}
    HEM_320 = {"name": "HEM320", "h": 359, "b": 309, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_340 = {"name": "HEM340", "h": 377, "b": 309, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_360 = {"name": "HEM360", "h": 395, "b": 308, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_400 = {"name": "HEM400", "h": 432, "b": 307, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_450 = {"name": "HEM450", "h": 478, "b": 307, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_500 = {"name": "HEM500", "h": 524, "b": 306, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_550 = {"name": "HEM550", "h": 572, "b": 306, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_600 = {"name": "HEM600", "h": 620, "b": 305, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_650 = {"name": "HEM650", "h": 668, "b": 305, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_700 = {"name": "HEM700", "h": 716, "b": 304, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_800 = {"name": "HEM800", "h": 814, "b": 303, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_900 = {"name": "HEM900", "h": 910, "b": 302, "t_w": 21, "t_f": 40, "radius": 0}
    HEM_1000 = {"name": "HEM1000", "h": 1008, "b": 302, "t_w": 21, "t_f": 40, "radius": 0}
