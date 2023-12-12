"""Formula 8.8N from NEN-EN 1992-1-1+C2:2011: Chapter 8 - Detailing of reinforcement and prestressing tendons."""
# pylint: disable=arguments-differ

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS, KN, MM, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot8NAnchorageCapacityWeldedTransverseBar(Formula):
    """Class representing the formula 8.8N for the calculation of the anchorage capacity of welded transverse bar, welded on the inside of the main
    bar"""

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        l_td: MM,
        phi_t: MM,
        sigma_td: MPA,
        f_wd: KN,
    ) -> None:
        """[Fbtd] Anchorage capacity of welded transverse bar, welded on the inside of the main bar [kN].
            Note: Value may be found in National Annex.

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - formula (8.8N)

        Parameters
        ----------
        l_td: MM
            [ltd] Design length of transverse bar [mm].
            = 1.16 * phit (fyd/σtd)^0.5 <= lt
            Use your own implementation of this formula or use the SubForm8Dot8NDesignLengthOfTransverseBar class.
        phi_t: MM
            [Φt] Diameter of transverse bar [mm].
        sigma_td: MPA
            [σtd] Concrete stress [MPa].
            = (fctd+σcm)/y <= 3*fcd
            Use your own implementation of this formula or use the SubForm8Dot8NConcreteStress class.
        f_wd: KN
            [Fwd] Design shear strength of weld (specified as a factor times As*fyd; say 0.5*As*fyd where As is the cross-section of the anchored bar
            and fyd is its design yield strength)  [kN].
        """
        super().__init__()
        self.l_td = l_td
        self.phi_t = phi_t
        self.sigma_td = sigma_td
        self.f_wd = f_wd

    @staticmethod
    def _evaluate(
        l_td: MM,
        phi_t: MM,
        sigma_td: MPA,
        f_wd: KN,
    ) -> KN:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            l_td=l_td,
            phi_t=phi_t,
            sigma_td=sigma_td,
            f_wd=f_wd,
        )
        return min(l_td * phi_t * sigma_td * N_TO_KN, f_wd)


class SubForm8Dot8NDesignLengthOfTransverseBar(Formula):
    """Class representing sub-formula for formula 8.8N, which calculates the design length of the transverse bar"""

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        phi_t: MM,
        f_yd: MPA,
        sigma_td: MPA,
        l_t: MM,
    ) -> None:
        """[ltd] Design length of transverse bar [mm].

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - ltd

        Parameters
        ----------
        phi_t: MM
            [Φt] Diameter of transverse bar [mm].
        f_yd: MPA
            [fyd] Design yield strength of bar [MPa].
        sigma_td: MPA
            [σtd] Concrete stress [MPa].
            = (fctd+σcm)/y <= 3*fcd
            Use your own implementation of this formula or use the SubForm8Dot8NConcreteStress class.
        l_t: MM
            [lt] Length of transverse bar, but not more than the spacing of bars to be anchored [mm].
        """
        super().__init__()
        self.phi_t = phi_t
        self.f_yd = f_yd
        self.sigma_td = sigma_td
        self.l_t = l_t

    @staticmethod
    def _evaluate(
        phi_t: MM,
        f_yd: MPA,
        sigma_td: MPA,
        l_t: MM,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            phi_t=phi_t,
            f_yd=f_yd,
            l_t=l_t,
        )
        raise_if_less_or_equal_to_zero(sigma_td=sigma_td)
        return min(1.16 * phi_t * (f_yd / sigma_td) ** 0.5, l_t)


class SubForm8Dot8NConcreteStress(Formula):
    """Class representing sub-formula for formula 8.8N, which calculates the concrete stress"""

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ctd: MPA,
        sigma_cm: MPA,
        y: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        """[σtd] Concrete stress [MPa].

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - σtd

        Parameters
        ----------
        f_ctd: MPA
            [fctd] Design tensile strength of concrete [MPa].
        sigma_cm: MPA
            [σcm] Compression in the concrete perpendicular to both bars (mean value) [MPa].
        y: DIMENSIONLESS
            [y] A function [-]
            = 0.015 + 0.14 * exp(-0.18*x)
            Use your own implementation of this formula or use the SubForm8Dot8NFunctionY class.
        f_cd: MPA
            [fcd] Design value compressive strength of concrete [MPa].
        """
        super().__init__()
        self.f_ctd = f_ctd
        self.sigma_cm = sigma_cm
        self.y = y
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        f_ctd: MPA,
        sigma_cm: MPA,
        y: DIMENSIONLESS,
        f_cd: MPA,
    ) -> MPA:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            f_ctd=f_ctd,
            sigma_cm=sigma_cm,
            f_cd=f_cd,
        )
        raise_if_less_or_equal_to_zero(y=y)
        return min((f_ctd + sigma_cm) / y, 3 * f_cd)


class SubForm8Dot8NFunctionY(Formula):
    """Class representing sub-formula for formula 8.8N, which calculates the function y"""

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        x: DIMENSIONLESS,
    ) -> None:
        """[y] A function [-]

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - y

        Parameters
        ----------
        x: DIMENSIONLESS
            [x] A function accounting for the geometry [-]
            = 2 * (c/phit) + 1
            Use your own implementation of this formula or use the SubForm8Dot8NFunctionX class.
        """
        super().__init__()
        self.x = x

    @staticmethod
    def _evaluate(
        x: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(x=x)
        return 0.015 + 0.14 * np.exp(-0.18 * x)


class SubForm8Dot8NFunctionX(Formula):
    """Class representing sub-formula for formula 8.8N, which calculates the function x"""

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c: MM,
        phi_t: MM,
    ) -> None:
        """[x] A function accounting for the geometry [-]

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - x

        Parameters
        ----------
        c: MM
            [c] Concrete cover perpendicular to both bars [mm].
        phi_t: MM
            [Φt] Diameter of transverse bar [mm].
        """
        super().__init__()
        self.c = c
        self.phi_t = phi_t

    @staticmethod
    def _evaluate(
        c: MM,
        phi_t: MM,
    ) -> DIMENSIONLESS:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(c=c)
        raise_if_less_or_equal_to_zero(phi_t=phi_t)
        return 2 * (c / phi_t) + 1
