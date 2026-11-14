"""PAL profile geometry data extracted from DXF files.

Each module in this package contains coordinate data for one PAL profile,
with smooth curves interpolated from DXF bulge values.
"""

from .pal3030 import PAL3030_GEOMETRY
from .pal3040 import PAL3040_GEOMETRY
from .pal3050 import PAL3050_GEOMETRY
from .pal3130 import PAL3130_GEOMETRY
from .pal3140 import PAL3140_GEOMETRY
from .pal3150 import PAL3150_GEOMETRY

__all__ = [
    "PAL3030_GEOMETRY",
    "PAL3040_GEOMETRY",
    "PAL3050_GEOMETRY",
    "PAL3130_GEOMETRY",
    "PAL3140_GEOMETRY",
    "PAL3150_GEOMETRY",
]
