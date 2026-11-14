"""AU profile geometry data extracted from DXF files.

Each module in this package contains coordinate data for one AU profile,
with smooth curves interpolated from DXF bulge values.
"""

from .au14 import AU14_GEOMETRY
from .au16 import AU16_GEOMETRY
from .au18 import AU18_GEOMETRY
from .au20 import AU20_GEOMETRY
from .au23 import AU23_GEOMETRY
from .au25 import AU25_GEOMETRY

__all__ = [
    "AU14_GEOMETRY",
    "AU16_GEOMETRY",
    "AU18_GEOMETRY",
    "AU20_GEOMETRY",
    "AU23_GEOMETRY",
    "AU25_GEOMETRY",
]
