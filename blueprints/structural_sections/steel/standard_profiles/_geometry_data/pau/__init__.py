"""PAU profile geometry data extracted from DXF files.

Each module in this package contains coordinate data for one PAU profile,
with smooth curves interpolated from DXF bulge values.
"""

from .pau2240 import PAU2240_GEOMETRY
from .pau2250 import PAU2250_GEOMETRY
from .pau2260 import PAU2260_GEOMETRY
from .pau2440 import PAU2440_GEOMETRY
from .pau2450 import PAU2450_GEOMETRY
from .pau2460 import PAU2460_GEOMETRY
from .pau2770 import PAU2770_GEOMETRY
from .pau2780 import PAU2780_GEOMETRY

__all__ = [
    "PAU2240_GEOMETRY",
    "PAU2250_GEOMETRY",
    "PAU2260_GEOMETRY",
    "PAU2440_GEOMETRY",
    "PAU2450_GEOMETRY",
    "PAU2460_GEOMETRY",
    "PAU2770_GEOMETRY",
    "PAU2780_GEOMETRY",
]
