"""This package represents the Eurocode NEN-EN 1992-1-1+C2:2011 code - Chapter 9 - formula (9.10)."""
# pylint: disable=arguments-differ

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MM


class Form9Dot10MaximumSpacingBentUpBars(Formula):
    """Class representing the formula 9.10 for the calculation of the maximum longitudinal spacing of bent up bars for slabs"""

    label = "9.10"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, d: MM) -> None:
        """[smax] Maximum longitudinal spacing of bent up bars for slabs [mm].

        NEN-EN 1992-1-1+C2:2011 art.9.3.2(4) - Formula (9.10)

        Parameters
        ----------
        d: MM
            [d] Effective height of the cross-section [mm].
        """
        super().__init__()
        self.d = d

    @staticmethod
    def _evaluate(d: MM) -> MM:
        """For more detailed documentation see the class docstring."""
        if d < 0:
            raise ValueError(f"Negative d: {d}. d cannot be negative")
        return d
