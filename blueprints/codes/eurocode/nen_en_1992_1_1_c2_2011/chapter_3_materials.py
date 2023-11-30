"""Module including all formulas from chapter 3 - Materials of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA


class Form3Dot1EstimationConcreteCompressiveStrength(Formula):
    """Class representing formula 3.1 for the estimation of the concrete compressive strength, fcm(t),  after t days
    with an average temperature of 20 degrees Celsius [MPa]."""

    label = "3.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        beta_cc_t: float,
        f_cm: MPA,
    ) -> None:
        """[fcm(t)] The estimated concrete compressive strength [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(6) - Formula (3.1)

        Parameters
        ----------
        beta_cc_t : float
            [βcc(t)] Coefficient dependent of the age of concrete [-].
        f_cm : MPA
            [fcm] Average concrete compressive strength on day 28 based on table 3.1 [MPa].
        """
        super().__init__()
        self.beta_cc_t = beta_cc_t
        self.f_cm = f_cm

    @staticmethod
    def _evaluate(
        beta_cc_t: float,
        f_cm: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method"""
        if beta_cc_t < 0:
            raise ValueError(f"Negative beta_cc_t: {beta_cc_t}. beta_cc_t cannot be negative")
        if f_cm < 0:
            raise ValueError(f"Negative f_cm: {f_cm}. f_cm cannot be negative")
        return beta_cc_t * f_cm


class Form3Dot2CoefficientDependentOfConcreteAge(Formula):
    """Class representing formula 3.2 for the coefficient βcc(t) which is dependent of the age of concrete [-]."""

    label = "3.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        s: float,
        t: int,
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
        t : int
            [t] Age of concrete in days [days].
        """
        super().__init__()
        self.s = s
        self.t = t

    @staticmethod
    def _evaluate(
        s: float,
        t: int,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if s < 0:
            raise ValueError(f"Invalid s: {s}. s cannot be negative")
        if t <= 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative or zero")
        return np.exp(s * (1 - (28 / t) ** (1 / 2)))


class SubForm3Dot2CoefficientTypeOfCementS(Formula):
    """Class representing sub-formula for formula 3.2, which calculates the coefficient s which is dependent on the cement class"""

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
        """Evaluates the formula, for more information see the __init__ method"""
        match cement_class.lower():
            case "r":
                return 0.20
            case "n":
                return 0.25
            case "s":
                return 0.38
            case _:
                raise ValueError(f"Invalid cement class: {cement_class}. Options: R, N or S")


class Form3Dot15DesignValueCompressiveStrength(Formula):
    """Class representing formula 3.15 for the calculation of the concrete compressive strength design value."""

    label = "3.15"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_cc: float,
        f_ck: MPA,
        gamma_c: float,
    ) -> None:
        """[fcd] Design value concrete compressive strength [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.6(1) - Formula (3.15)

        Parameters
        ----------
        alpha_cc : float
            [αcc] Coefficient taking long term effects on compressive strength into account and unfavorable effect due to positioning loading [-]
            Normally between 0.8 and 1, see national appendix. Recommended value: 1.0
        f_ck : MPA
            [fck] Characteristic compressive strength [MPa].
        gamma_c : float
            [γc] Partial safety factor concrete, see 2.4.2.4 [-]
        """
        super().__init__()
        self.alpha_cc = alpha_cc
        self.f_ck = f_ck
        self.gamma_c = gamma_c

    @staticmethod
    def _evaluate(
        alpha_cc: float,
        f_ck: MPA,
        gamma_c: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if alpha_cc < 0:
            raise ValueError(f"Invalid alpha_cc: {alpha_cc}. alpha_cc cannot be negative")
        if f_ck < 0:
            raise ValueError(f"Invalid f_ck: {f_ck}. f_ck cannot be negative")
        if gamma_c <= 0:
            raise ValueError(f"Invalid gamma_c: {gamma_c}. gamma_c cannot be negative or zero")
        return alpha_cc * f_ck / gamma_c


class Form3Dot16DesignValueTensileStrength(Formula):
    """Class representing formula 3.16 for the calculation of the concrete tensile strength design value."""

    label = "3.16"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_ct: float,
        f_ctk_0_05: MPA,
        gamma_c: float,
    ) -> None:
        """[fcd] Design value concrete tensile strength [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.6(2) - Formula (3.16)

        Parameters
        ----------
        alpha_ct : float
            [αct] Coefficient taking long term effects on tensile strength into account and unfavorable effect due to positioning loading [-]
            See national appendix. Recommended value: 1.0
        f_ctk_0_05 : MPA
            [fctk,0,05] Characteristic tensile strength 5% [MPa].
        gamma_c : float
            [γc] Partial safety factor concrete, see 2.4.2.4 [-]
        """
        super().__init__()
        self.alpha_ct = alpha_ct
        self.f_ctk_0_05 = f_ctk_0_05
        self.gamma_c = gamma_c

    @staticmethod
    def _evaluate(
        alpha_ct: float,
        f_ctk_0_05: MPA,
        gamma_c: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if alpha_ct < 0:
            raise ValueError(f"Invalid alpha_ct: {alpha_ct}. alpha_ct cannot be negative")
        if f_ctk_0_05 < 0:
            raise ValueError(f"Invalid f_ctk_0_05: {f_ctk_0_05}. f_ctk_0_05 cannot be negative")
        if gamma_c <= 0:
            raise ValueError(f"Invalid gamma_c: {gamma_c}. gamma_c cannot be negative or zero")
        return alpha_ct * f_ctk_0_05 / gamma_c
