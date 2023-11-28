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


class Form3Dot5ApproximationVarianceElasticModulusOverTime(Formula):
    """Class representing formula 3.5 for the approximation of the elastic modulus, Ecm(t) at day t."""

    label = "3.5"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, f_cm_t: float, f_cm: float, e_cm: float) -> None:
        """Calculates Ecm(t), the approximated elastic modulus at day t [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.3

        Parameters
        ----------
        f_cm_t: float
            [fcm(t)] compressive strength concrete at t days [MPa].
        f_cm: float
            [fcm] average concrete compressive strength on day 28 based on table 3.1 [MPa].
        e_cm: float
            [Ecm] average elastic modulus on day 28 [MPa]
        """
        super().__init__()
        self.f_cm_t = f_cm_t
        self.f_cm = f_cm
        self.e_cm = e_cm

    @staticmethod
    def _evaluate(f_cm_t: float, f_cm: float, e_cm: float) -> float:
        """For more detailed documentation see the class docstring."""
        return (f_cm_t / f_cm) ** 0.3 * e_cm


class Form3Dot6CreepDeformationOfConcrete(Formula):
    """Class representing formula 3.6 for the calculation of creep deformation of concrete."""

    label = "3.6"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, phi_inf_t0: float, sigma_c: float, e_c: float) -> None:
        """Calculates epsilon_cc(inf,t0), the creep deformation of concrete [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4

        Parameters
        ----------
        phi_inf_t0: float
            [phi(inf,t0)] creep coefficient if high accuracy is not required use figure 3.1 and/or use appendix B [-].
        sigma_c: float
            [sigma_c] concrete compressive stress [MPa].
        e_c: float
            [Ec] tangent modulus = 1.05 * Ecm [MPa].
        """
        super().__init__()
        self.phi_inf_t0 = phi_inf_t0
        self.sigma_c = sigma_c
        self.e_c = e_c

    @staticmethod
    def _evaluate(phi_inf_t0: float, sigma_c: float, e_c: float) -> float:
        """For more detailed documentation see the class docstring."""
        return phi_inf_t0 * sigma_c / e_c


class Form3Dot7NonLinearCreepCoefficient(Formula):
    """Class representing formula 3.7 for the calculation of the non-linear creep coefficient."""

    label = "3.7"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, phi_inf_t0: float, k_sigma: float) -> None:
        """Calculates phi_nl(inf,t0), the non-linear creep coefficient [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4

        Parameters
        ----------
        phi_inf_t0: float
            [phi(inf,t0)] creep coefficient if high accuracy is not required use figure 3.1 and/or use appendix B [-].
        k_sigma: float
            [k_sigma] stress-strength ratio (sigma_c / f_ck(t0)) [-].
        """
        super().__init__()
        self.phi_inf_t0 = phi_inf_t0
        self.k_sigma = k_sigma

    @staticmethod
    def _evaluate(phi_inf_t0: float, k_sigma: float) -> float:
        """For more detailed documentation see the class docstring."""
        return phi_inf_t0 * np.exp(1.5 * (k_sigma - 0.45))


class Form3Dot8TotalShrinkage(Formula):
    """Class representing formula 3.8 for the calculation of the total shrinkage."""

    label = "3.8"
    source_document = "NEN-EN 1992-1-1+C2:2011"

    def __init__(self, epsilon_cd: float, epsilon_ca: float) -> None:
        """Calculates epsilon_cs, the total shrinkage [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4

        Parameters
        ----------
        epsilon_cd: float
            [epsilon_cd] drying shrinkage [-].
        epsilon_ca: float
            [epsilon_ca] autogene shrinkage [-].
        """
        super().__init__()
        self.epsilon_cd = epsilon_cd
        self.epsilon_ca = epsilon_ca

    @staticmethod
    def _evaluate(epsilon_cd: float, epsilon_ca: float) -> float:
        """For more detailed documentation see the class docstring."""
        return epsilon_cd + epsilon_ca
