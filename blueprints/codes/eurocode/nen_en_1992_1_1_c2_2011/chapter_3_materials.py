"""This package represents the Eurocode NEN-EN 1992-1-1+C2:2011 code - Chapter 3."""
import numpy as np

from blueprints.codes.formula import Formula


class Form3Dot1ApproximationConcreteCompressiveStrength(Formula):
    """Class representing the formula 3.1 for the approximation of the concrete compressive strength after t days
    with an average temperature of 20 degrees C [MPa]."""

    label = "3.1"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, beta_cc_t: float, f_cm: float) -> None:
        """Calculates the approximation of the concrete compressive strength [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1

        Parameters
        ----------
        beta_cc_t: float
            Coefficient dependent of the age of concrete [-].
        f_cm: float
            Average concrete compressive strength on day 28 based on table 3.1 [MPa].

        Returns
        -------
        f_cm_t: float
            Average concrete compressive strength at age t days
        """
        super().__init__()
        self.beta_cc_t = beta_cc_t
        self.f_cm = f_cm

    @staticmethod
    def _evaluate(beta_cc_t: float, f_cm: float) -> float:
        """For more detailed documentation see the class docstring."""
        return beta_cc_t * f_cm


class Form3Dot2CoefficientDependentOfConcreteAge(Formula):
    """Class representing the formula 3.2 for the coefficient which is dependent of the age of concrete [-]."""

    label = "3.2"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, s: float, t: int) -> None:
        """Calculates the coefficient which is dependent of the age of concrete [-].

        NEN-EN 1992-1-1+C2:2011 art.3.2

        Parameters
        ----------
        s: float
            Coefficient dependent on the kind of cement [-].
        t: int
            Age of concrete in days [days].

        Returns
        -------
        beta_cc_t: float
            Coefficient which is dependent of the age of concrete [-].
        """
        super().__init__()
        self.s = s
        self.t = t

    @staticmethod
    def _evaluate(s: float, t: float) -> float:
        """For more detailed documentation see the class docstring."""
        return np.exp(s * (1 - (28 / t) ** 1 / 2))
