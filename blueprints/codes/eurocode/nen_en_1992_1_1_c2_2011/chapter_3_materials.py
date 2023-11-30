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


class Form3Dot11AutogeneShrinkage(Formula):
    """Class representing formula 3.11, which calculates the autogene shrinkage"""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.11"

    def __init__(
        self,
        beta_as_t: float,
        epsilon_ca_inf: float,
    ) -> None:
        """[εca(t)] Autogene shrinkage [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.11)

        Parameters
        ----------
        beta_as_t : float
            [βas(t)] Coefficient dependent on time in days for autogene shrinkage [-].
            = 1 - exp(-0.2 * t^0.5)
            Use your own implementation of this formula or use the Form3Dot13CoefficientTimeAutogeneShrinkage class
        epsilon_ca_inf : float
            [εca] Autogene shrinkage at infinity [-].
            = 2.5 * (fck - 10) E-6
            Use your own implementation of this formula or use the Form3Dot12AutogeneShrinkageInfinity class.
        """
        super().__init__()
        self.beta_as_t = beta_as_t
        self.epsilon_ca_inf = epsilon_ca_inf

    @staticmethod
    def _evaluate(
        beta_as_t: float,
        epsilon_ca_inf: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if beta_as_t < 0:
            raise ValueError(f"Invalid beta_as_t: {beta_as_t}. beta_as_t cannot be negative")
        return beta_as_t * epsilon_ca_inf


class Form3Dot12AutogeneShrinkageInfinity(Formula):
    """Class representing formula 3.12, which calculates the autogene shrinkage at infinity"""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.12"

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        """[εca(∞)] Autogene shrinkage at infinity [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.12)

        Parameters
        ----------
        f_ck : MPA
            [fck] Compressive strength concrete [MPa].
        """
        super().__init__()
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        f_ck: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if f_ck < 0:
            raise ValueError(f"Invalid f_ck: {f_ck}. f_ck cannot be negative")
        return 2.5 * (f_ck - 10) * 10**-6


class Form3Dot13CoefficientTimeAutogeneShrinkage(Formula):
    """Class representing formula 3.13, which calculates the coefficient dependent on time for the autogene shrinkage"""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.13"

    def __init__(
        self,
        t: float,
    ) -> None:
        """[βas(t)] Coefficient dependent on time in days for autogene shrinkage [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.13)

        Parameters
        ----------
        t : float
            [t] Time in days [-].
        """
        super().__init__()
        self.t = t

    @staticmethod
    def _evaluate(
        t: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if t < 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative")
        return 1 - np.exp(-0.2 * t**0.5)


class Form3Dot14StressStrainForShortTermLoading(Formula):
    """Class representing formula 3.14, which calculates the compressive stress-strength ratio"""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.14"

    def __init__(
        self,
        k: float,
        eta: float,
    ) -> None:
        """[σc / fcm] Compressive stress-strength ratio [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.5(1) - Formula (3.14)

        Parameters
        ----------
        k : float
            [k] [-].
            = 1.05 * Ecm * |εc1| / fcm
            Use your own implementation of this formula or use the Sub2Form3Dot14K class.
        eta : float
            [η] Strain - peak-strain ratio [-].
            = εc / εc1
            Use your own implementation of this formula or use the Sub1Form3Dot14Eta class.
        """
        super().__init__()
        self.k = k
        self.eta = eta

    @staticmethod
    def _evaluate(
        k: float,
        eta: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if k < 0:
            raise ValueError(f"Invalid k: {k}. k cannot be negative")
        if eta < 0:
            raise ValueError(f"Invalid eta: {eta}. eta cannot be negative")
        return (k * eta - eta**2) / (1 + (k - 2) * eta)


class Sub1Form3Dot14Eta(Formula):
    """Class representing sub-formula 1 for formula 3.14, which calculates eta"""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.14"

    def __init__(
        self,
        epsilon_c: float,
        epsilon_c1: float,
    ) -> None:
        """[η] Strain - peak-strain ratio [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.5(1) - η

        Parameters
        ----------
        epsilon_c : float
            [εc] Strain concrete [-].
        epsilon_c1 : float
            [εc1] Strain concrete at peak-stress following table 3.1 [-].
        """
        super().__init__()
        self.epsilon_c = epsilon_c
        self.epsilon_c1 = epsilon_c1

    @staticmethod
    def _evaluate(
        epsilon_c: float,
        epsilon_c1: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        return epsilon_c / epsilon_c1


class Sub2Form3Dot14K(Formula):
    """Class representing sub-formula 2 for formula 3.14, which calculates k"""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.14"

    def __init__(self, e_cm: MPA, epsilon_c1: float, f_cm: MPA) -> None:
        """[k] [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.5(1) - k

        Parameters
        ----------
        e_cm : MPA
            [Ecm] Elastic modulus concrete [MPa].
        epsilon_c1 : float
            [εc1] Strain concrete at peak-stress following table 3.1 [-].
        f_cm : MPA
            [fcm] Compressive strength concrete [MPa].
        """
        super().__init__()
        self.e_cm = e_cm
        self.epsilon_c1 = epsilon_c1
        self.f_cm = f_cm

    @staticmethod
    def _evaluate(
        e_cm: MPA,
        epsilon_c1: float,
        f_cm: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if e_cm < 0:
            raise ValueError(f"Invalid e_cm: {e_cm}. e_cm cannot be negative")
        if f_cm <= 0:
            raise ValueError(f"Invalid f_cm: {f_cm}. f_cm cannot be negative or zero")
        return 1.05 * e_cm * abs(epsilon_c1) / f_cm
