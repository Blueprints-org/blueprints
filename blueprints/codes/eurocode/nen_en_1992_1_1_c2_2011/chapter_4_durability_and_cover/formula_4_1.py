"""Formula 4.1 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement."""
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MM


class Form4Dot1NominalConcreteCover(Formula):
    """Class representing the formula 4.1 for the calculation of the nominal concrete cover."""

    label = "4.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c_min: MM,
        delta_c_dev: MM,
    ) -> None:
        """[cnom] Calculates the nominal concrete cover [mm].

        NEN-EN 1992-1-1+C2:2011 art.4.4.1.1 (2) - Formula (4.1)

        Parameters
        ----------
        c_min: MM
            [cmin] Minimum concrete cover based on art. 4.4.1.2 [mm].
        delta_c_dev: MM
            [Δcdev] Construction tolerance based on art. 4.4.1.3 [mm].
        """
        super().__init__()
        self.c_min = c_min
        self.delta_c_dev = delta_c_dev

    @staticmethod
    def _evaluate(
        c_min: MM,
        delta_c_dev: MM,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        if c_min < 0:
            raise ValueError(f"Negative c_min: {c_min}. c_min cannot be negative")
        if delta_c_dev < 0:
            raise ValueError(f"Negative delta_c_dev: {delta_c_dev}. delta_c_dev cannot be negative")
        return c_min + delta_c_dev
