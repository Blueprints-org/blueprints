"""GU profile geometry data extracted from DXF files.

Each module in this package contains coordinate data for one GU profile,
with smooth curves interpolated from DXF bulge values.
"""

from .gu6 import GU6_GEOMETRY
from .gu7 import GU7_GEOMETRY
from .gu8 import GU8_GEOMETRY
from .gu10 import GU10_GEOMETRY
from .gu11 import GU11_GEOMETRY
from .gu12 import GU12_GEOMETRY
from .gu13 import GU13_GEOMETRY
from .gu14 import GU14_GEOMETRY
from .gu15 import GU15_GEOMETRY
from .gu16 import GU16_GEOMETRY
from .gu18 import GU18_GEOMETRY
from .gu18_400 import GU18_400_GEOMETRY
from .gu20 import GU20_GEOMETRY
from .gu21 import GU21_GEOMETRY
from .gu22 import GU22_GEOMETRY
from .gu23 import GU23_GEOMETRY
from .gu27 import GU27_GEOMETRY
from .gu28 import GU28_GEOMETRY
from .gu30 import GU30_GEOMETRY
from .gu31 import GU31_GEOMETRY
from .gu32 import GU32_GEOMETRY
from .gu33 import GU33_GEOMETRY

__all__ = [
    "GU6_GEOMETRY",
    "GU7_GEOMETRY",
    "GU8_GEOMETRY",
    "GU10_GEOMETRY",
    "GU11_GEOMETRY",
    "GU12_GEOMETRY",
    "GU13_GEOMETRY",
    "GU14_GEOMETRY",
    "GU15_GEOMETRY",
    "GU16_GEOMETRY",
    "GU18_400_GEOMETRY",
    "GU18_GEOMETRY",
    "GU20_GEOMETRY",
    "GU21_GEOMETRY",
    "GU22_GEOMETRY",
    "GU23_GEOMETRY",
    "GU27_GEOMETRY",
    "GU28_GEOMETRY",
    "GU30_GEOMETRY",
    "GU31_GEOMETRY",
    "GU32_GEOMETRY",
    "GU33_GEOMETRY",
]
