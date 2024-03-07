"""Formula 3.4 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DAYS, MPA


class Form3Dot4DevelopmentTensileStrength(Formula):
    """Class representing formula 3.4 for an initial estimation of the tensile strength, fctm(t), after t days."""

    label = "3.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        beta_cc_t: float,
        alpha: float,
        f_ctm: MPA,
    ) -> None:
        """[fctm(t)] The initial estimation of the tensile strength after t days [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(9) - Formula (3.4)

        Parameters
        ----------
        beta_cc_t : float
            [βcc(t)] Coefficient dependent of the age of concrete [-].
        alpha : float
            [α] Factor dependent of the age of concrete [-]
            alpha = 1 for t < 28 days
            alpha = 2/3 for t >= 28 days
            Use your own implementation of this value or use the SubForm3Dot4CoefficientAgeConcreteAlpha class.
        f_ctm : MPA
            [fctm] Tensile strength from table 3.1 [MPa].

        Returns
        -------
        None
        """
        super().__init__()
        self.beta_cc_t = beta_cc_t
        self.alpha = alpha
        self.f_ctm = f_ctm

    @staticmethod
    def _evaluate(
        beta_cc_t: float,
        alpha: float,
        f_ctm: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        if beta_cc_t < 0:
            raise ValueError(f"Negative beta_cc_t: {beta_cc_t}. beta_cc_t cannot be negative")
        if f_ctm < 0:
            raise ValueError(f"Negative f_ctm: {f_ctm}. f_ctm cannot be negative")
        if alpha < 0:
            raise ValueError(f"Negative alpha: {alpha}. alpha cannot be negative")
        return beta_cc_t**alpha * f_ctm


class SubForm3Dot4CoefficientAgeConcreteAlpha(Formula):
    """Class representing sub-formula for formula 3.4 for the coefficient 'α' which is dependent of the age of concrete."""

    label = "3.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        t: DAYS,
    ) -> None:
        """[α] Factor dependent of the age of concrete [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(9) - α

        Parameters
        ----------
        t : DAYS
            [t] Age of concrete in days [days].
        """
        super().__init__()
        self.t = t

    @staticmethod
    def _evaluate(
        t: DAYS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if t <= 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative or zero")
        if t < 28:
            return 1.0
        return 2 / 3
