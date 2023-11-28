"""This package represents the formulas in NEN-EN 1992-1-1+C2:2011 - Chapter 3."""
import numpy as np

from blueprints.codes.formula import Formula

# pylint: disable=arguments-differ


class Form3Dot1EstimationConcreteCompressiveStrength(Formula):
    """Class representing formula 3.1 for the estimation of the concrete compressive strength, f_cm(t),  after t days
    with an average temperature of 20 degrees Celsius [MPa]."""

    label = "3.1"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, beta_cc_t: float, f_cm: float) -> None:
        """Calculates fcm(t), the estimated concrete compressive strength [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2

        Parameters
        ----------
        beta_cc_t: float
            [beta_cc(t)] coefficient dependent of the age of concrete [-].
        f_cm: float
            [fcm] average concrete compressive strength on day 28 based on table 3.1 [MPa].
        """
        super().__init__()
        self.beta_cc_t = beta_cc_t
        self.f_cm = f_cm

    @staticmethod
    def _evaluate(beta_cc_t: float, f_cm: float) -> float:
        """For more detailed documentation see the class docstring."""
        return beta_cc_t * f_cm


class Form3Dot2CoefficientDependentOfConcreteAge(Formula):
    """Class representing formula 3.2 for the coefficient which is dependent of the age of concrete, beta_cc(t) [-]."""

    label = "3.2"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, s: float, t: int) -> None:
        """Calculates beta_cc(t) coefficient which is dependent of the age of concrete in days [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2

        Parameters
        ----------
        s: float
            [s] coefficient dependent on the kind of cement [-].
        t: int
            [t] age of concrete in days [days].
        """
        super().__init__()
        self.s = s
        self.t = t

    @staticmethod
    def _evaluate(s: float, t: int) -> float:
        """For more detailed documentation see the class docstring."""
        return np.exp(s * (1 - (28 / t) ** (1 / 2)))


class Form3Dot3AxialTensileStrengthFromTensileSplittingStrength(Formula):
    """Class representing formula 3.3 for the approximated axial tensile strength, fct, determined by tensile splitting strength [MPa]."""

    label = "3.3"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, f_ct_sp: float) -> None:
        """Calculates fct, the approximated axial tensile strength when tensile strength is determined as coefficient
        which is dependent of the age of concrete [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2

        Parameters
        ----------
        f_ct_sp: float
            [fct,sp] tensile splitting strength [MPa].
        """
        super().__init__()
        self.f_ct_sp = f_ct_sp

    @staticmethod
    def _evaluate(f_ct_sp: float) -> float:
        """For more detailed documentation see the class docstring."""
        return 0.9 * f_ct_sp


class Form3Dot4DevelopmentTensileStrength(Formula):
    """Class representing formula 3.4 for an initial estimation of the tensile strength, fctm(t), after t days [MPa]."""

    label = "3.4"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, beta_cc_t: float, alpha: float, f_ctm: float) -> None:
        """Calculates fctm(t), the initial estimation of the tensile strength after t days [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2

        Parameters
        ----------
        beta_cc_t: float
            [beta_cc(t)] coefficient dependent of the age of concrete [-].
        alpha: float
            [alpha] factor dependent of the age of concrete [-]
            alpha = 1 for t < 28 days
            alpha = 2/3 for t >= 28 days
        f_ctm: float
            [fctm] Tensile strength from table 3.1 [MPa]
        """
        super().__init__()
        self.beta_cc_t = beta_cc_t
        self.alpha = alpha
        self.f_ctm = f_ctm

    @staticmethod
    def _evaluate(beta_cc_t: float, alpha: float, f_ctm: float) -> float:
        """For more detailed documentation see the class docstring."""
        if alpha in (1, 2 / 3):
            return beta_cc_t**alpha * f_ctm
        raise ValueError("Wrong value for alpha: alpha = 1 for t < 28 days, alpha = 2/3 for t >= 28 days")
