"""This package represents the Eurocode NEN-EN 1992-1-1+C2:2011 code - Chapter 4."""
from blueprints.codes.formula import Formula


class Form4Dot1NominalConcreteCover(Formula):
    """Class representing the formula 4.1 for the calculation of the nominal concrete cover [mm]"""

    label = "4.1"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, c_min: float, delta_c_dev: float) -> None:
        """Calculates the nominal concrete cover [mm].

        NEN-EN 1992-1-1+C2:2011 art.4.4.1.1

        Parameters
        ----------
        c_min: float
            Minimum concrete cover based on art. 4.4.1.2 [mm].
        delta_c_dev: float
            Construction tolerance based on art. 4.4.1.3 [mm].

        Returns
        -------
        c_nom: float
            Nominal concrete cover [mm]
        """
        super().__init__()
        self.c_min = c_min
        self.delta_c_dev = delta_c_dev

    @staticmethod
    def _evaluate(c_min: float, delta_c_dev: float) -> float:
        """For more detailed documentation see the class docstring."""
        return c_min + delta_c_dev


class Form4Dot2MinimumConcreteCover(Formula):
    """Class representing the formula 4.2 for the calculation of the minimum concrete cover [mm]."""

    label = "4.2"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, c_min_b: float, c_min_dur: float, delta_c_dur_gamma: float, delta_c_dur_st: float, delta_c_dur_add: float) -> None:
        """Calculates the minimum concrete cover [mm].

        NEN-EN 1992-1-1+C2:2011 art.4.4.1.2

        Parameters
        ----------
        c_min_b: float
            The minimum concrete cover based on the adhesion requirements based on art. 4.4.1.2 (3) [mm].
        c_min_dur: float
            The minimum concrete cover based on environmental conditions based on art. 4.4.1.2 (5) [mm].
        delta_c_dur_gamma: float
            An additional safety requirement based on art. 4.4.1.2 (6) [mm].
        delta_c_dur_st: float
            A reduction of minimum concrete cover when using stainless steel based on art. 4.4.1.2 (7) [mm].
        delta_c_dur_add: float
            A reduction of minimum concrete cover when using additional protection based on art. 4.4.1.2 (8) [mm].

        Returns
        -------
        c_min: float
            Minimum concrete cover [mm].
        """
        super().__init__()
        self.c_min_b = c_min_b
        self.c_min_dur = c_min_dur
        self.delta_c_dur_gamma = delta_c_dur_gamma
        self.delta_c_dur_st = delta_c_dur_st
        self.delta_c_dur_add = delta_c_dur_add

    @staticmethod
    def _evaluate(c_min_b: float, c_min_dur: float, delta_c_dur_gamma: float, delta_c_dur_st: float, delta_c_dur_add: float) -> float:
        """For more detailed documentation see the class docstring."""
        return max(c_min_b, c_min_dur + delta_c_dur_gamma - delta_c_dur_st - delta_c_dur_add, 10)
