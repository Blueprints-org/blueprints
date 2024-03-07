"""Formula 3.10 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DAYS, MM, MM2


class Form3Dot10CoefficientAgeConcreteDryingShrinkage(Formula):
    """Class representing formula 3.10 for the calculation of the coefficient for drying shrinkage due to age."""

    label = "3.10"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        t: DAYS,
        t_s: DAYS,
        h_0: MM,
    ) -> None:
        """[βds(t,ts)] Coefficient for drying shrinkage due to age of concrete [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.10)

        Parameters
        ----------
        t : DAYS
            [t] Age in days of the concrete at the considered moment [days].
        t_s : DAYS
            [t] Age in days of the concrete at the start of the drying shrinkage [days].
        h_0 : MM
            [h0] fictional thickness of cross-section [mm].
            = 2 * Ac / u
            Use your own implementation of this formula or use the SubForm3Dot10FictionalCrossSection class.

        Returns
        -------
        None
        """
        super().__init__()
        self.t = t
        self.t_s = t_s
        self.h_0 = h_0

    @staticmethod
    def _evaluate(
        t: DAYS,
        t_s: DAYS,
        h_0: MM,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if t <= 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative or zero")
        if t_s < 0:
            raise ValueError(f"Negative t_s: {t_s}. t_s cannot be negative")
        if t <= t_s:
            raise ValueError("Invalid t and t_s combination. t has to be larger than t_s")
        if h_0 <= 0:
            raise ValueError(f"Invalid h_0: {h_0}. h_0 cannot be negative or zero")
        return (t - t_s) / ((t - t_s) + 0.04 * np.sqrt(h_0**3))


class SubForm3Dot10FictionalCrossSection(Formula):
    """Class representing sub-formula for formula 3.10 for the calculation of fictional thickness of the cross-section."""

    label = "3.10"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_c: MM2,
        u: MM,
    ) -> None:
        """[h0] Fictional thickness of the cross-section [mm].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - h0

        Parameters
        ----------
        a_c : MM2
            [Ac] Area of the cross-section of the concrete [mm²].
        u : MM
            [u] Circumference of part that is subjected to drying [mm].
        """
        super().__init__()
        self.a_c = a_c
        self.u = u

    @staticmethod
    def _evaluate(
        a_c: MM2,
        u: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        if a_c <= 0:
            raise ValueError(f"Invalid a_c: {a_c}. a_c cannot be negative or zero")
        if u <= 0:
            raise ValueError(f"Invalid u: {u}. u cannot be negative or zero")
        return 2 * a_c / u
