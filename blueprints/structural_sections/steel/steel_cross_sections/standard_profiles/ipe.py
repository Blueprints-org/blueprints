"""IPE Steel Profiles."""
# ruff: noqa: RUF012

from enum import Enum


class IPEProfile(Enum):
    """Enumeration of IPE steel profiles with dimensions and properties."""

    IPE_80 = {"name": "IPE80", "h": 80, "b": 46, "t_w": 3.8, "t_f": 5.2, "radius": 5}
    IPE_100 = {"name": "IPE100", "h": 100, "b": 55, "t_w": 4.1, "t_f": 5.7, "radius": 7}
    IPE_120 = {"name": "IPE120", "h": 120, "b": 64, "t_w": 4.4, "t_f": 6.3, "radius": 7}
    IPE_140 = {"name": "IPE140", "h": 140, "b": 73, "t_w": 4.7, "t_f": 6.9, "radius": 7}
    IPE_160 = {"name": "IPE160", "h": 160, "b": 82, "t_w": 5.0, "t_f": 7.4, "radius": 9}
    IPE_180 = {"name": "IPE180", "h": 180, "b": 91, "t_w": 5.3, "t_f": 8.0, "radius": 9}
    IPE_200 = {"name": "IPE200", "h": 200, "b": 100, "t_w": 5.6, "t_f": 8.5, "radius": 12}
    IPE_220 = {"name": "IPE220", "h": 220, "b": 110, "t_w": 5.9, "t_f": 9.2, "radius": 12}
    IPE_240 = {"name": "IPE240", "h": 240, "b": 120, "t_w": 6.2, "t_f": 9.8, "radius": 15}
    IPE_270 = {"name": "IPE270", "h": 270, "b": 135, "t_w": 6.6, "t_f": 10.2, "radius": 15}
    IPE_300 = {"name": "IPE300", "h": 300, "b": 150, "t_w": 7.1, "t_f": 10.7, "radius": 15}
    IPE_330 = {"name": "IPE330", "h": 330, "b": 160, "t_w": 7.5, "t_f": 11.5, "radius": 18}
    IPE_360 = {"name": "IPE360", "h": 360, "b": 170, "t_w": 8.0, "t_f": 12.7, "radius": 18}
    IPE_400 = {"name": "IPE400", "h": 400, "b": 180, "t_w": 8.6, "t_f": 13.5, "radius": 21}
    IPE_450 = {"name": "IPE450", "h": 450, "b": 190, "t_w": 9.4, "t_f": 14.6, "radius": 21}
    IPE_500 = {"name": "IPE500", "h": 500, "b": 200, "t_w": 10.2, "t_f": 16.0, "radius": 21}
    IPE_550 = {"name": "IPE550", "h": 550, "b": 210, "t_w": 11.1, "t_f": 17.2, "radius": 24}
    IPE_600 = {"name": "IPE600", "h": 600, "b": 220, "t_w": 12.0, "t_f": 19.0, "radius": 24}
