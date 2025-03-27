"""HEB Steel Profiles."""
# ruff: noqa: RUF012

from enum import Enum


class HEBProfile(Enum):
    """Enumeration of HEB steel profiles with dimensions."""

    HEB_100 = {"name": "HEB100", "h": 100, "b": 100, "t_w": 6, "t_f": 10, "radius": 12}
    HEB_120 = {"name": "HEB120", "h": 120, "b": 120, "t_w": 6.5, "t_f": 11, "radius": 12}
    HEB_140 = {"name": "HEB140", "h": 140, "b": 140, "t_w": 7, "t_f": 12, "radius": 12}
    HEB_160 = {"name": "HEB160", "h": 160, "b": 160, "t_w": 8, "t_f": 13, "radius": 15}
    HEB_180 = {"name": "HEB180", "h": 180, "b": 180, "t_w": 8.5, "t_f": 14, "radius": 15}
    HEB_200 = {"name": "HEB200", "h": 200, "b": 200, "t_w": 9, "t_f": 15, "radius": 18}
    HEB_220 = {"name": "HEB220", "h": 220, "b": 220, "t_w": 9.5, "t_f": 16, "radius": 18}
    HEB_240 = {"name": "HEB240", "h": 240, "b": 240, "t_w": 10, "t_f": 17, "radius": 21}
    HEB_260 = {"name": "HEB260", "h": 260, "b": 260, "t_w": 10, "t_f": 17.5, "radius": 24}
    HEB_280 = {"name": "HEB280", "h": 280, "b": 280, "t_w": 10.5, "t_f": 18, "radius": 24}
    HEB_300 = {"name": "HEB300", "h": 300, "b": 300, "t_w": 11, "t_f": 19, "radius": 27}
    HEB_320 = {"name": "HEB320", "h": 320, "b": 300, "t_w": 11.5, "t_f": 20.5, "radius": 27}
    HEB_340 = {"name": "HEB340", "h": 340, "b": 300, "t_w": 12, "t_f": 21.5, "radius": 27}
    HEB_360 = {"name": "HEB360", "h": 360, "b": 300, "t_w": 12.5, "t_f": 22.5, "radius": 27}
    HEB_400 = {"name": "HEB400", "h": 400, "b": 300, "t_w": 13.5, "t_f": 24, "radius": 27}
    HEB_450 = {"name": "HEB450", "h": 450, "b": 300, "t_w": 14, "t_f": 26, "radius": 27}
    HEB_500 = {"name": "HEB500", "h": 500, "b": 300, "t_w": 14.5, "t_f": 28, "radius": 27}
    HEB_550 = {"name": "HEB550", "h": 550, "b": 300, "t_w": 15, "t_f": 29, "radius": 27}
    HEB_600 = {"name": "HEB600", "h": 600, "b": 300, "t_w": 15.5, "t_f": 30, "radius": 27}
    HEB_650 = {"name": "HEB650", "h": 650, "b": 300, "t_w": 16, "t_f": 31, "radius": 27}
    HEB_700 = {"name": "HEB700", "h": 700, "b": 300, "t_w": 17, "t_f": 32, "radius": 27}
    HEB_800 = {"name": "HEB800", "h": 800, "b": 300, "t_w": 17.5, "t_f": 33, "radius": 30}
    HEB_900 = {"name": "HEB900", "h": 900, "b": 300, "t_w": 18.5, "t_f": 35, "radius": 30}
    HEB_1000 = {"name": "HEB1000", "h": 1000, "b": 300, "t_w": 19, "t_f": 36, "radius": 30}
