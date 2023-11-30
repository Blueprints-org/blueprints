"""Module including all formulas from chapter 3 - Materials of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DAYS, MM, MM2, MPA


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
        """
        super().__init__()
        self.s = s
        self.t = t

    @staticmethod
    def _evaluate(
        s: float,
        t: DAYS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if s < 0:
            raise ValueError(f"Invalid s: {s}. s cannot be negative")
        if t <= 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative or zero")
        return np.exp(s * (1 - (28 / t) ** (1 / 2)))


class SubForm3Dot2CoefficientTypeOfCementS(Formula):
    """Class representing sub-formula for formula 3.2, which calculates the coefficient 's'
    which is dependent on the cement class"""

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


class Form3Dot3AxialTensileStrengthFromTensileSplittingStrength(Formula):
    """Class representing formula 3.3 for the approximated axial tensile strength, fct, determined by
    tensile splitting strength."""

    label = "3.3"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ct_sp: MPA,
    ) -> None:
        """[fct] The approximated axial tensile strength when tensile strength is determined as coefficient
        which is dependent of the age of concrete [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(8) - Formula (3.3)

        Parameters
        ----------
        f_ct_sp : float
            [fct,sp] Tensile strength determined by tensile splitting strength [MPa].
        """
        super().__init__()
        self.f_ct_sp = f_ct_sp

    @staticmethod
    def _evaluate(
        f_ct_sp: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method"""
        if f_ct_sp < 0:
            raise ValueError(f"Negative f_ct_sp: {f_ct_sp}. f_ct_sp cannot be negative")
        return 0.9 * f_ct_sp


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
            [fctm] Tensile strength from table 3.1 [MPa]
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
        """Evaluates the formula, for more information see the __init__ method"""
        if beta_cc_t < 0:
            raise ValueError(f"Negative beta_cc_t: {beta_cc_t}. beta_cc_t cannot be negative")
        if f_ctm < 0:
            raise ValueError(f"Negative f_ctm: {f_ctm}. f_ctm cannot be negative")
        if alpha < 0:
            raise ValueError(f"Negative alpha: {alpha}. alpha cannot be negative")
        return beta_cc_t**alpha * f_ctm


class SubForm3Dot4CoefficientAgeConcreteAlpha(Formula):
    """Class representing sub-formula for formula 3.4 for the coefficient 'α' which
    is dependent of the age of concrete."""

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
        """Evaluates the formula, for more information see the __init__ method"""
        if t <= 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative or zero")
        if t < 28:
            return 1.0
        return 2 / 3


class Form3Dot5ApproximationVarianceElasticModulusOverTime(Formula):
    """Class representing formula 3.5 for the approximation of the elastic modulus, Ecm(t) at day t."""

    label = "3.5"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_cm_t: MPA,
        f_cm: MPA,
        e_cm: MPA,
    ) -> None:
        """[Ecm(t)] The approximated elastic modulus at day t [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.3(3) - Formula (3.5)

        Parameters
        ----------
        f_cm_t : MPA
            [fcm(t)] Compressive strength concrete at t days [MPa].
        f_cm : MPA
            [fcm] Average concrete compressive strength on day 28 based on table 3.1 [MPa].
        e_cm : MPA
            [Ecm] Average elastic modulus on day 28 [MPa]
        """
        super().__init__()
        self.f_cm_t = f_cm_t
        self.f_cm = f_cm
        self.e_cm = e_cm

    @staticmethod
    def _evaluate(
        f_cm_t: MPA,
        f_cm: MPA,
        e_cm: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method"""
        if f_cm_t < 0:
            raise ValueError(f"Negative f_cm_t: {f_cm_t}. f_cm_t cannot be negative")
        if f_cm < 0:
            raise ValueError(f"Negative f_cm: {f_cm}. f_cm cannot be negative")
        if e_cm < 0:
            raise ValueError(f"Negative e_cm: {e_cm}. e_cm cannot be negative")
        return (f_cm_t / f_cm) ** 0.3 * e_cm


class Form3Dot6CreepDeformationOfConcrete(Formula):
    """Class representing formula 3.6 for the calculation of creep deformation of concrete."""

    label = "3.6"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        phi_inf_t0: float,
        sigma_c: MPA,
        e_c: MPA,
    ) -> None:
        """εcc(∞,t0) Creep deformation of concrete at the time t = ∞ for a constant concrete compressive
        stress σc applied at time t0 [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(3) - Formula (3.6)

        Parameters
        ----------
        phi_inf_t0 : float
            [φ(∞, t0)] Creep coefficient if high accuracy is not required use figure 3.1 else use appendix B [-].
        sigma_c : MPA
            [σc] Concrete compressive stress [MPa].
        e_c : MPA
            [Ec] tangent modulus = 1.05 * Ecm. According to art.3.1.4(2) [MPa].
        """
        super().__init__()
        self.phi_inf_t0 = phi_inf_t0
        self.sigma_c = sigma_c
        self.e_c = e_c

    @staticmethod
    def _evaluate(
        phi_inf_t0: float,
        sigma_c: MPA,
        e_c: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if phi_inf_t0 < 0:
            raise ValueError(f"Negative phi_inf_t0: {phi_inf_t0}. phi_inf_t0 cannot be negative")
        if sigma_c < 0:
            raise ValueError(f"Negative sigma_c: {sigma_c}. sigma_c cannot be negative")
        if e_c < 0:
            raise ValueError(f"Negative e_c: {e_c}. e_c cannot be negative")
        return phi_inf_t0 * sigma_c / e_c


class Form3Dot7NonLinearCreepCoefficient(Formula):
    """Class representing formula 3.7 for the calculation of the non-linear creep coefficient."""

    label = "3.7"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        phi_inf_t0: float,
        k_sigma: float,
    ) -> None:
        """[φnl(∞,t0)] The non-linear creep coefficient [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(4) - Formula (3.7)

        Parameters
        ----------
        phi_inf_t0 : float
            [φ(∞, t0)] Creep coefficient if high accuracy is not required use figure 3.1 and/or use appendix B [-].
        k_sigma : float
            [kσ] Stress-strength ratio (σc / fck(t0)) [-].
        """
        super().__init__()
        self.phi_inf_t0 = phi_inf_t0
        self.k_sigma = k_sigma

    @staticmethod
    def _evaluate(
        phi_inf_t0: float,
        k_sigma: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if phi_inf_t0 < 0:
            raise ValueError(f"Negative phi_inf_t0: {phi_inf_t0}. phi_inf_t0 cannot be negative")
        if k_sigma < 0:
            raise ValueError(f"Negative k_sigma: {k_sigma}. k_sigma cannot be negative")
        return phi_inf_t0 * np.exp(1.5 * (k_sigma - 0.45))


class Form3Dot8TotalShrinkage(Formula):
    """Class representing formula 3.8 for the calculation of the total shrinkage."""

    label = "3.8"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        epsilon_cd: float,
        epsilon_ca: float,
    ) -> None:
        """[εcs] The total shrinkage [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.8)

        Parameters
        ----------
        epsilon_cd : float
            [εcd] Drying shrinkage [-].
        epsilon_ca : float
            [εca] Autogene shrinkage [-].
        """
        super().__init__()
        self.epsilon_cd = epsilon_cd
        self.epsilon_ca = epsilon_ca

    @staticmethod
    def _evaluate(
        epsilon_cd: float,
        epsilon_ca: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        return epsilon_cd + epsilon_ca


class Form3Dot9DryingShrinkage(Formula):
    """Class representing formula 3.9 for the calculation of the drying shrinkage."""

    label = "3.9"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        beta_ds_tt_s: float,
        k_h: float,
        epsilon_cd_0: float,
    ) -> None:
        """[εcd(t)] Development of the drying shrinkage [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.9)

        Parameters
        ----------
        beta_ds_tt_s : float
            [βds(t, ts)] Coefficient that depends on the age t (in days) of the concrete for the drying shrinkage [-].
        k_h : float
            [kh] Coefficient depending on the fictional thickness h0 following table 3.3 [-].
            h0 = 100 -> kh = 1.0
            h0 = 200 -> kh = 0.85
            h0 = 300 -> kh = 0.75
            h0 >= 500 -> kh = 0.70
        epsilon_cd_0 : float
            [εcd,0] Nominal unobstructed drying shrinkage, formula in appendix B or use table 3.2 [-]
        """
        super().__init__()
        self.beta_ds_tt_s = beta_ds_tt_s
        self.k_h = k_h
        self.epsilon_cd_0 = epsilon_cd_0

    @staticmethod
    def _evaluate(
        beta_ds_tt_s: float,
        k_h: float,
        epsilon_cd_0: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if beta_ds_tt_s < 0:
            raise ValueError(f"Negative beta_ds_tt_s: {beta_ds_tt_s}. beta_ds_tt_s cannot be negative")
        if k_h < 0:
            raise ValueError(f"Negative k_h: {k_h}. k_h cannot be negative")
        return beta_ds_tt_s * k_h * epsilon_cd_0


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
        """Evaluates the formula, for more information see the __init__ method"""
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
    """Class representing sub-formula for formula 3.10 for the calculation of fictional
    thickness of the cross-section."""

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
        """Evaluates the formula, for more information see the __init__ method"""
        if a_c <= 0:
            raise ValueError(f"Invalid a_c: {a_c}. a_c cannot be negative or zero")
        if u <= 0:
            raise ValueError(f"Invalid u: {u}. u cannot be negative or zero")
        return 2 * a_c / u


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
            [εca(∞)] Autogene shrinkage at infinity [-].
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
        t: DAYS,
    ) -> None:
        """[βas(t)] Coefficient dependent on time in days for autogene shrinkage [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.13)

        Parameters
        ----------
        t : DAYS
            [t] Time in days [days].
        """
        super().__init__()
        self.t = t

    @staticmethod
    def _evaluate(
        t: DAYS,
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
            Use your own implementation of this formula or use the SubForm3Dot14K class.
        eta : float
            [η] Strain - peak-strain ratio [-].
            = εc / εc1
            Use your own implementation of this formula or use the SubForm3Dot14Eta class.
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


class SubForm3Dot14Eta(Formula):
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


class SubForm3Dot14K(Formula):
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
