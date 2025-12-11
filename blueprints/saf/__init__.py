"""Implementation of SAF (Structural Analysis Format) on Blueprints.

 https://www.saf.guide/en/stable/

 We try to keep our implementation up to date with the latest SAF but will make our own choices if needed.

**This is not a full implementation of SAF, but rather a focused one for our use cases.**
"""

from blueprints.saf.results.result_internal_force_1d import (
    ResultFor,
    ResultInternalForce1D,
    ResultOn,
)
from blueprints.saf.results.result_internal_force_2d_edge import (
    ResultInternalForce2DEdge,
    ResultOn2DEdge,
)

__all__ = [
    "ResultFor",
    "ResultInternalForce1D",
    "ResultInternalForce2DEdge",
    "ResultOn",
    "ResultOn2DEdge",
]
