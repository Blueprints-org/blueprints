"""AZ profile geometry data extracted from DXF files.

Each module in this package contains coordinate data for one AZ profile,
with smooth curves interpolated from DXF bulge values.
"""

from .az12_700 import AZ12_700_GEOMETRY
from .az12_770 import AZ12_770_GEOMETRY
from .az13_700 import AZ13_700_GEOMETRY
from .az13_700_10_10 import AZ13_700_10_10_GEOMETRY
from .az13_770 import AZ13_770_GEOMETRY
from .az14_700 import AZ14_700_GEOMETRY
from .az14_770 import AZ14_770_GEOMETRY
from .az14_770_10_10 import AZ14_770_10_10_GEOMETRY
from .az17_700 import AZ17_700_GEOMETRY
from .az18 import AZ18_GEOMETRY
from .az18_10_10 import AZ18_10_10_GEOMETRY
from .az18_700 import AZ18_700_GEOMETRY
from .az18_800 import AZ18_800_GEOMETRY
from .az19_700 import AZ19_700_GEOMETRY
from .az20_700 import AZ20_700_GEOMETRY
from .az22_800 import AZ22_800_GEOMETRY
from .az24_700 import AZ24_700_GEOMETRY
from .az25_800 import AZ25_800_GEOMETRY
from .az26 import AZ26_GEOMETRY
from .az26_700 import AZ26_700_GEOMETRY
from .az27_800 import AZ27_800_GEOMETRY
from .az28_700 import AZ28_700_GEOMETRY
from .az28_750 import AZ28_750_GEOMETRY
from .az30_750 import AZ30_750_GEOMETRY
from .az32_750 import AZ32_750_GEOMETRY
from .az36_700n import AZ36_700N_GEOMETRY
from .az38_700n import AZ38_700N_GEOMETRY
from .az40_700n import AZ40_700N_GEOMETRY
from .az42_700n import AZ42_700N_GEOMETRY
from .az44_700n import AZ44_700N_GEOMETRY
from .az46_700n import AZ46_700N_GEOMETRY
from .az48_700 import AZ48_700_GEOMETRY
from .az50_700 import AZ50_700_GEOMETRY
from .az52_700 import AZ52_700_GEOMETRY

__all__ = [
    "AZ12_700_GEOMETRY",
    "AZ12_770_GEOMETRY",
    "AZ13_700_10_10_GEOMETRY",
    "AZ13_700_GEOMETRY",
    "AZ13_770_GEOMETRY",
    "AZ14_700_GEOMETRY",
    "AZ14_770_10_10_GEOMETRY",
    "AZ14_770_GEOMETRY",
    "AZ17_700_GEOMETRY",
    "AZ18_10_10_GEOMETRY",
    "AZ18_700_GEOMETRY",
    "AZ18_800_GEOMETRY",
    "AZ18_GEOMETRY",
    "AZ19_700_GEOMETRY",
    "AZ20_700_GEOMETRY",
    "AZ22_800_GEOMETRY",
    "AZ24_700_GEOMETRY",
    "AZ25_800_GEOMETRY",
    "AZ26_700_GEOMETRY",
    "AZ26_GEOMETRY",
    "AZ27_800_GEOMETRY",
    "AZ28_700_GEOMETRY",
    "AZ28_750_GEOMETRY",
    "AZ30_750_GEOMETRY",
    "AZ32_750_GEOMETRY",
    "AZ36_700N_GEOMETRY",
    "AZ38_700N_GEOMETRY",
    "AZ40_700N_GEOMETRY",
    "AZ42_700N_GEOMETRY",
    "AZ44_700N_GEOMETRY",
    "AZ46_700N_GEOMETRY",
    "AZ48_700_GEOMETRY",
    "AZ50_700_GEOMETRY",
    "AZ52_700_GEOMETRY",
]
