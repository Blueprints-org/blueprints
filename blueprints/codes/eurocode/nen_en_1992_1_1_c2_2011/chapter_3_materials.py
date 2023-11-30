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


class Form3Dot17CompressiveStressConcrete(Formula):
    """Class representing formula 3.17 for the calculation of compressive stress in concrete using stress-strain diagram of figure 3.3."""

    label = "3.17"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_cd: MPA,
        epsilon_c: float,
        epsilon_c2: float,
        n: float,
    ) -> None:
        """[σc] Compressive stress in concrete using stress-strain diagram of figure 3.3 [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.7(1) - Formula (3.17)

        Parameters
        ----------
        f_cd : MPA
            [fcd] Design value compressive strength concrete [MPa]
        epsilon_c : float
            [εc] Strain in concrete [-].
        epsilon_c2 : float
            [εc2] Strain in concrete when reaching maximum strength following table 3.1 [-]
        n : float
            Exponent following table 3.1
        """
        super().__init__()
        self.f_cd = f_cd
        self.epsilon_c = epsilon_c
        self.epsilon_c2 = epsilon_c2
        self.n = n

    @staticmethod
    def _evaluate(
        f_cd: MPA,
        epsilon_c: float,
        epsilon_c2: float,
        n: float,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method"""
        if f_cd < 0:
            raise ValueError(f"Invalid f_cd: {f_cd}. f_cd cannot be negative")
        if epsilon_c < 0:
            raise ValueError(f"Invalid epsilon_c: {epsilon_c}. epsilon_c cannot be negative")
        if epsilon_c > epsilon_c2:
            raise ValueError(f"epsilon_c: {epsilon_c} > epsilon_c2: {epsilon_c2}. Try using Form3Dot18CompressiveStressConcrete class.")
        return f_cd * (1 - (1 - (epsilon_c / epsilon_c2)) ** n)


class Form3Dot18CompressiveStressConcrete(Formula):
    """Class representing formula 3.18 for the calculation of compressive stress in concrete using stress-strain diagram of figure 3.3."""

    label = "3.18"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_cd: MPA,
    ) -> None:
        """[σc] Compressive stress in concrete using stress-strain diagram of figure 3.3 [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.7(1) - Formula (3.18)

        Parameters
        ----------
        f_cd : MPA
            [fcd] Design value compressive strength concrete [MPa]
        """
        super().__init__()
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        f_cd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method"""
        if f_cd < 0:
            raise ValueError(f"Invalid f_cd: {f_cd}. f_cd cannot be negative")
        return f_cd


class Form3Dot19And20EffectivePressureZoneHeight(Formula):
    """Class representing formula 3.19 and 3.20 for the calculation of the lambda factor for the effective pressure zone height."""

    label = "3.19-20"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        """[λ] Factor effective pressure zone height [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.7(3) - Formula (3.19) and (3.20)

        Parameters
        ----------
        f_ck : MPA
            [fck] Characteristic compressive strength concrete [MPa]
        """
        super().__init__()
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        f_ck: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if f_ck <= 50:
            return 0.8
        if f_ck <= 90:
            return 0.8 - (f_ck - 50) / 400
        raise ValueError(f"Invalid f_ck: {f_ck}. Maximum of f_ck is 90 MPa")


class Form3Dot21And22EffectiveStrength(Formula):
    """Class representing formula 3.21 and 3.22 for the calculation of the eta factor for the effective strength."""

    label = "3.21-22"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        """[η] Factor effective strength [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.7(3) - Formula (3.21) and (3.22)

        Parameters
        ----------
        f_ck : MPA
            [fck] Characteristic compressive strength concrete [MPa]
        """
        super().__init__()
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        f_ck: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if f_ck <= 50:
            return 1.0
        if f_ck <= 90:
            return 1.0 - (f_ck - 50) / 200
        raise ValueError(f"Invalid f_ck: {f_ck}. Maximum of f_ck is 90 MPa")
