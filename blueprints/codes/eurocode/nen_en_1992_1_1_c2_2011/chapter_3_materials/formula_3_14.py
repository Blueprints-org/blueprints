"""Formula 3.14 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA


class Form3Dot14StressStrainForShortTermLoading(Formula):
    """Class representing formula 3.14, which calculates the compressive stress-strength ratio."""

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
            Use your own implementation of this formula or use the SubForm3Dot14K class.
        eta : float
            [η] Strain - peak-strain ratio [-].
            = εc / εc1
            Use your own implementation of this formula or use the SubForm3Dot14Eta class.

        Returns
        -------
        None
        """
        super().__init__()
        self.k = k
        self.eta = eta

    @staticmethod
    def _evaluate(
        k: float,
        eta: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if k < 0:
            raise ValueError(f"Invalid k: {k}. k cannot be negative")
        if eta < 0:
            raise ValueError(f"Invalid eta: {eta}. eta cannot be negative")
        return (k * eta - eta**2) / (1 + (k - 2) * eta)


class SubForm3Dot14Eta(Formula):
    """Class representing sub-formula 1 for formula 3.14, which calculates eta."""

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
        """Evaluates the formula, for more information see the __init__ method."""
        return epsilon_c / epsilon_c1


class SubForm3Dot14K(Formula):
    """Class representing sub-formula 2 for formula 3.14, which calculates k."""

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
        """Evaluates the formula, for more information see the __init__ method."""
        if e_cm < 0:
            raise ValueError(f"Invalid e_cm: {e_cm}. e_cm cannot be negative")
        if f_cm <= 0:
            raise ValueError(f"Invalid f_cm: {f_cm}. f_cm cannot be negative or zero")
        return 1.05 * e_cm * abs(epsilon_c1) / f_cm
