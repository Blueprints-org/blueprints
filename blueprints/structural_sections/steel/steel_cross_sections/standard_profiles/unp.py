"""UNP Steel Profiles."""

from enum import Enum

from blueprints.type_alias import MM, RATIO


class UNP(Enum):
    """Enumeration of UNP steel profiles with dimensions and properties."""

    UNP_80 = ("UNP80", 80, 45, 6, 8, 8, 8)
    UNP_100 = ("UNP100", 100, 50, 6, 8.5, 8.5, 8)
    UNP_120 = ("UNP120", 120, 55, 7, 9, 9, 8)
    UNP_140 = ("UNP140", 140, 60, 7, 10, 10, 8)
    UNP_160 = ("UNP160", 160, 65, 7.5, 10.5, 10.5, 8)
    UNP_180 = ("UNP180", 180, 70, 8, 11, 11, 8)
    UNP_200 = ("UNP200", 200, 75, 8.5, 11.5, 11.5, 8)
    UNP_220 = ("UNP220", 220, 80, 9, 12.5, 12.5, 8)
    UNP_240 = ("UNP240", 240, 85, 9.5, 13, 13, 8)
    UNP_260 = ("UNP260", 260, 90, 10, 14, 14, 8)
    UNP_280 = ("UNP280", 280, 95, 10, 15, 15, 8)
    UNP_300 = ("UNP300", 300, 100, 10, 16, 16, 8)
    UNP_320 = ("UNP320", 320, 100, 14, 17.5, 17.5, 5)
    UNP_350 = ("UNP350", 350, 100, 14, 16, 16, 5)
    UNP_380 = ("UNP380", 380, 102, 13.5, 16, 16, 5)
    UNP_400 = ("UNP400", 400, 110, 14, 18, 18, 5)

    def __init__(self, code: str, h: MM, b: MM, t_w: MM, t_f: MM, radius: MM, slope: RATIO) -> None:
        """Initialize UNP profile.
        Args:
            code (str): Profile code.
            h (MM): Total height.
            b (MM): Total width.
            t_w (MM): Web thickness.
            t_f (MM): Flange thickness.
            radius (MM): Radius (always 0 for UNP profiles).
            slope (RATIO): Slope of the flange.
        """
        self.code = code
        self.top_flange_total_width = b
        self.top_flange_thickness = t_f
        self.bottom_flange_total_width = b
        self.bottom_flange_thickness = t_f
        self.total_height = h
        self.web_thickness = t_w
        self.radius = radius
        self.slope = slope
