"""HEA Steel Profiles."""
# ruff: noqa: RUF012

from enum import Enum


class HEAProfile(Enum):
    """Enumeration of HEA steel profiles with dimensions and properties."""

    HEA_100 = {"name": "HEA100", "h": 96, "b": 100, "t_w": 5, "t_f": 8, "radius": 0}
    HEA_120 = {"name": "HEA120", "h": 114, "b": 120, "t_w": 5, "t_f": 8, "radius": 0}
    HEA_140 = {"name": "HEA140", "h": 133, "b": 140, "t_w": 5.5, "t_f": 8.5, "radius": 0}
    HEA_160 = {"name": "HEA160", "h": 152, "b": 160, "t_w": 6, "t_f": 9, "radius": 0}
    HEA_180 = {"name": "HEA180", "h": 171, "b": 180, "t_w": 6, "t_f": 9.5, "radius": 0}
    HEA_200 = {"name": "HEA200", "h": 190, "b": 200, "t_w": 6.5, "t_f": 10, "radius": 0}
    HEA_220 = {"name": "HEA220", "h": 210, "b": 220, "t_w": 7, "t_f": 11, "radius": 0}
    HEA_240 = {"name": "HEA240", "h": 230, "b": 240, "t_w": 7.5, "t_f": 12, "radius": 0}
    HEA_260 = {"name": "HEA260", "h": 250, "b": 260, "t_w": 7.5, "t_f": 12.5, "radius": 0}
    HEA_280 = {"name": "HEA280", "h": 270, "b": 280, "t_w": 8, "t_f": 13, "radius": 0}
    HEA_300 = {"name": "HEA300", "h": 290, "b": 300, "t_w": 8.5, "t_f": 14, "radius": 0}
    HEA_320 = {"name": "HEA320", "h": 310, "b": 300, "t_w": 9, "t_f": 15.5, "radius": 0}
    HEA_340 = {"name": "HEA340", "h": 330, "b": 300, "t_w": 9.5, "t_f": 16.5, "radius": 0}
    HEA_360 = {"name": "HEA360", "h": 350, "b": 300, "t_w": 10, "t_f": 17.5, "radius": 0}
    HEA_400 = {"name": "HEA400", "h": 390, "b": 300, "t_w": 11, "t_f": 19, "radius": 0}
    HEA_450 = {"name": "HEA450", "h": 440, "b": 300, "t_w": 11.5, "t_f": 21, "radius": 0}
    HEA_500 = {"name": "HEA500", "h": 490, "b": 300, "t_w": 12, "t_f": 23, "radius": 0}
    HEA_550 = {"name": "HEA550", "h": 540, "b": 300, "t_w": 12.5, "t_f": 24, "radius": 0}
    HEA_600 = {"name": "HEA600", "h": 590, "b": 300, "t_w": 13, "t_f": 25, "radius": 0}
    HEA_650 = {"name": "HEA650", "h": 640, "b": 300, "t_w": 13.5, "t_f": 26, "radius": 0}
    HEA_700 = {"name": "HEA700", "h": 690, "b": 300, "t_w": 14.5, "t_f": 27, "radius": 0}
    HEA_800 = {"name": "HEA800", "h": 790, "b": 300, "t_w": 15, "t_f": 28, "radius": 0}
    HEA_900 = {"name": "HEA900", "h": 890, "b": 300, "t_w": 16, "t_f": 30, "radius": 0}
    HEA_1000 = {"name": "HEA1000", "h": 990, "b": 300, "t_w": 16.5, "t_f": 31, "radius": 0}
