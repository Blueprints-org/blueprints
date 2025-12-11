"""SAF Results objects package."""

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
