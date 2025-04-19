"""UNP Steel Profiles."""

from enum import Enum

from blueprints.type_alias import MM, PERCENTAGE


class UNP(Enum):
    """Geometrical representation of UNP steel profiles."""

    UNP80 = ("UNP80", 80, 45, 6, 8, 8, 4, 8)
    UNP100 = ("UNP100", 100, 50, 6, 8.5, 8.5, 4.5, 8)
    UNP120 = ("UNP120", 120, 55, 7, 9, 9, 4.5, 8)
    UNP140 = ("UNP140", 140, 60, 7, 10, 10, 5, 8)
    UNP160 = ("UNP160", 160, 65, 7.5, 10.5, 10.5, 5.5, 8)
    UNP180 = ("UNP180", 180, 70, 8, 11, 11, 5.5, 8)
    UNP200 = ("UNP200", 200, 75, 8.5, 11.5, 11.5, 6, 8)
    UNP220 = ("UNP220", 220, 80, 9, 12.5, 12.5, 6.5, 8)
    UNP240 = ("UNP240", 240, 85, 9.5, 13, 13, 6.5, 8)
    UNP260 = ("UNP260", 260, 90, 10, 14, 14, 7, 8)
    UNP280 = ("UNP280", 280, 95, 10, 15, 15, 7.5, 8)
    UNP300 = ("UNP300", 300, 100, 10, 16, 16, 8, 8)
    UNP320 = ("UNP320", 320, 100, 14, 17.5, 17.5, 8.75, 5)
    UNP350 = ("UNP350", 350, 100, 14, 16, 16, 8, 5)
    UNP380 = ("UNP380", 380, 102, 13.5, 16, 16, 8, 5)
    UNP400 = ("UNP400", 400, 110, 14, 18, 18, 9, 5)

    def __init__(self, alias: str, h: MM, b: MM, t_w: MM, t_f: MM, r1: MM, r2: MM, slope: PERCENTAGE) -> None:
        """Initialize UNP profile.
        Args:
            alias (str): Profile alias.
            h (MM): Total height.
            b (MM): Total width.
            t_w (MM): Web thickness.
            t_f (MM): Flange thickness.
            r1 (MM): Root fillet radius.
            r2 (MM): Toe radius.
            slope (RATIO): Slope of the flange.
        """
        self.alias = alias
        self.top_flange_total_width = b
        self.top_flange_thickness = t_f
        self.bottom_flange_total_width = b
        self.bottom_flange_thickness = t_f
        self.total_height = h
        self.web_thickness = t_w
        self.root_fillet_radius = r1
        self.toe_radius = r2
        self.slope = slope
