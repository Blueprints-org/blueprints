"""Formula 3.2 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DAYS


class Form3Dot2CoefficientDependentOfConcreteAge(Formula):
    """Class representing formula 3.2 for the coefficient βcc(t) which is dependent of the age of concrete."""

    label = "3.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        s: float,
        t: DAYS,
    ) -> None:
        """Calculates beta_cc(t) coefficient which is dependent of the age of concrete in days [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(6) - Formula (3.2)

        Parameters
        ----------
        s : float
            [s] Coefficient dependent on the kind of cement [-].
            = 0.20 for cement of strength classes CEM 42.5 R, CEM 52.5 N, and CEM 52.5 R (class R);
            = 0.25 for cement of strength classes CEM 32.5 R, CEM 42.5 N (class N);
            = 0.38 for cement of strength class CEM 32.5 N (class S).
            Use your own implementation of this formula or use the SubForm3Dot2CoefficientTypeOfCementS class.
        t : DAYS
            [t] Age of concrete in days [days].

        Returns
        -------
        None
        """
        super().__init__()
        self.s = s
        self.t = t

    @staticmethod
    def _evaluate(
        s: float,
        t: DAYS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if s < 0:
            raise ValueError(f"Invalid s: {s}. s cannot be negative")
        if t <= 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative or zero")
        return np.exp(s * (1 - (28 / t) ** (1 / 2)))


class SubForm3Dot2CoefficientTypeOfCementS(Formula):
    """Class representing sub-formula for formula 3.2, which calculates the coefficient 's' which is dependent on the cement class."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.2"

    def __init__(
        self,
        cement_class: str,
    ) -> None:
        """[s] Coefficient that depends on the type of cement [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(6) - s

        Parameters
        ----------
        cement_class : str
            [cement_class] Class of the cement.
                = 'R' for cement of strength classes CEM 42.5 R, CEM 52.5 N, and CEM 52.5 R (class R);
                = 'N' for cement of strength classes CEM 32.5 R, CEM 42.5 N (class N);
                = 'S' for cement of strength class CEM 32.5 N (class S).

        """
        super().__init__()
        self.cement_class = cement_class

    @staticmethod
    def _evaluate(
        cement_class: str,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        match cement_class.lower():
            case "r":
                return 0.20
            case "n":
                return 0.25
            case "s":
                return 0.38
            case _:
                raise ValueError(f"Invalid cement class: {cement_class}. Options: 'R', 'N' or 'S'")
