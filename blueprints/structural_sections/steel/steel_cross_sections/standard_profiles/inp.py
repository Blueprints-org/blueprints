"""INP Steel Profiles."""
# ruff: noqa: RUF012

from enum import Enum


class INPProfile(Enum):
    """Enumeration of INP steel profiles with dimensions and properties."""

    INP_80 = {"name": "INP80", "h": 80, "b": 42, "t_w": 3.9, "t_f": 5.9, "radius": 0}
    INP_100 = {"name": "INP100", "h": 100, "b": 50, "t_w": 4.5, "t_f": 6.8, "radius": 0}
    INP_120 = {"name": "INP120", "h": 120, "b": 58, "t_w": 5.1, "t_f": 7.7, "radius": 0}
    INP_140 = {"name": "INP140", "h": 140, "b": 66, "t_w": 5.7, "t_f": 8.6, "radius": 0}
    INP_160 = {"name": "INP160", "h": 160, "b": 74, "t_w": 6.3, "t_f": 9.5, "radius": 0}
    INP_180 = {"name": "INP180", "h": 180, "b": 82, "t_w": 6.9, "t_f": 10.4, "radius": 0}
    INP_200 = {"name": "INP200", "h": 200, "b": 90, "t_w": 7.5, "t_f": 11.3, "radius": 0}
    INP_220 = {"name": "INP220", "h": 220, "b": 98, "t_w": 8.1, "t_f": 12.2, "radius": 0}
    INP_240 = {"name": "INP240", "h": 240, "b": 106, "t_w": 8.7, "t_f": 13.1, "radius": 0}
    INP_260 = {"name": "INP260", "h": 260, "b": 113, "t_w": 9.4, "t_f": 14.1, "radius": 0}
    INP_280 = {"name": "INP280", "h": 280, "b": 119, "t_w": 10.1, "t_f": 15.2, "radius": 0}
    INP_300 = {"name": "INP300", "h": 300, "b": 125, "t_w": 10.8, "t_f": 16.2, "radius": 0}
    INP_320 = {"name": "INP320", "h": 320, "b": 131, "t_w": 11.5, "t_f": 17.3, "radius": 0}
    INP_340 = {"name": "INP340", "h": 340, "b": 137, "t_w": 12.2, "t_f": 18.3, "radius": 0}
    INP_360 = {"name": "INP360", "h": 360, "b": 143, "t_w": 13, "t_f": 19.5, "radius": 0}
    INP_380 = {"name": "INP380", "h": 380, "b": 149, "t_w": 13.7, "t_f": 20.5, "radius": 0}
    INP_400 = {"name": "INP400", "h": 400, "b": 155, "t_w": 14.4, "t_f": 21.6, "radius": 0}
