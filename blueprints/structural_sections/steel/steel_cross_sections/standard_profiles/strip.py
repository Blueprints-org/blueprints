"""Standard Steel Strips."""

from enum import Enum

from blueprints.type_alias import MM


class StripStandardProfileClass(Enum):
    """Enumeration of standard steel strips."""

    STRIP_160x5 = ("160x5", 160, 5)
    STRIP_160x6 = ("160x6", 160, 6)
    STRIP_160x8 = ("160x8", 160, 8)
    STRIP_160x10 = ("160x10", 160, 10)
    STRIP_160x12 = ("160x12", 160, 12)
    STRIP_160x15 = ("160x15", 160, 15)
    STRIP_160x20 = ("160x20", 160, 20)
    STRIP_160x25 = ("160x25", 160, 25)
    STRIP_160x30 = ("160x30", 160, 30)
    STRIP_165x5 = ("165x5", 165, 5)
    STRIP_165x6 = ("165x6", 165, 6)
    STRIP_165x8 = ("165x8", 165, 8)
    STRIP_165x10 = ("165x10", 165, 10)
    STRIP_165x12 = ("165x12", 165, 12)
    STRIP_165x15 = ("165x15", 165, 15)
    STRIP_165x20 = ("165x20", 165, 20)
    STRIP_165x25 = ("165x25", 165, 25)
    STRIP_165x30 = ("165x30", 165, 30)
    STRIP_170x5 = ("170x5", 170, 5)
    STRIP_170x6 = ("170x6", 170, 6)
    STRIP_170x8 = ("170x8", 170, 8)
    STRIP_170x10 = ("170x10", 170, 10)
    STRIP_170x12 = ("170x12", 170, 12)
    STRIP_170x15 = ("170x15", 170, 15)
    STRIP_170x20 = ("170x20", 170, 20)
    STRIP_180x5 = ("180x5", 180, 5)
    STRIP_180x6 = ("180x6", 180, 6)
    STRIP_180x8 = ("180x8", 180, 8)
    STRIP_180x10 = ("180x10", 180, 10)
    STRIP_180x12 = ("180x12", 180, 12)
    STRIP_180x15 = ("180x15", 180, 15)
    STRIP_180x20 = ("180x20", 180, 20)
    STRIP_180x25 = ("180x25", 180, 25)
    STRIP_180x30 = ("180x30", 180, 30)
    STRIP_180x40 = ("180x40", 180, 40)
    STRIP_180x50 = ("180x50", 180, 50)
    STRIP_200x5 = ("200x5", 200, 5)
    STRIP_200x6 = ("200x6", 200, 6)
    STRIP_200x8 = ("200x8", 200, 8)
    STRIP_200x10 = ("200x10", 200, 10)
    STRIP_200x12 = ("200x12", 200, 12)
    STRIP_200x15 = ("200x15", 200, 15)
    STRIP_200x20 = ("200x20", 200, 20)
    STRIP_200x25 = ("200x25", 200, 25)
    STRIP_200x30 = ("200x30", 200, 30)
    STRIP_200x40 = ("200x40", 200, 40)
    STRIP_200x50 = ("200x50", 200, 50)
    STRIP_220x6 = ("220x6", 220, 6)
    STRIP_220x8 = ("220x8", 220, 8)
    STRIP_220x10 = ("220x10", 220, 10)
    STRIP_220x12 = ("220x12", 220, 12)
    STRIP_220x15 = ("220x15", 220, 15)
    STRIP_220x20 = ("220x20", 220, 20)
    STRIP_220x25 = ("220x25", 220, 25)
    STRIP_220x30 = ("220x30", 220, 30)
    STRIP_230x6 = ("230x6", 230, 6)
    STRIP_230x8 = ("230x8", 230, 8)
    STRIP_230x10 = ("230x10", 230, 10)
    STRIP_230x12 = ("230x12", 230, 12)
    STRIP_230x15 = ("230x15", 230, 15)
    STRIP_230x20 = ("230x20", 230, 20)
    STRIP_230x25 = ("230x25", 230, 25)

    def __init__(self, code: str, width: MM, height: MM) -> None:
        """Initialize standard steel strip profile.
        Args:
            code (str): Profile code.
            width (MM): Width of the strip.
            height (MM): Height of the strip.
        """
        self.code = code
        self.width = width
        self.height = height
