"""Formula 8.8N from NEN-EN 1992-1-1+C2:2011: Chapter 8 - Detailing of reinforcement and prestressing tendons."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS, KN, MM, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot8nAnchorageCapacityWeldedTransverseBar(Formula):
    """Class representing the formula 8.8N for the calculation of the anchorage capacity of welded transverse bar, welded on the inside of the main
    bar.
    """

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        l_td: MM,
        diameter_t: MM,
        sigma_td: MPA,
        f_wd: KN,
    ) -> None:
        """[:math:`F_{btd}`] Anchorage capacity of welded transverse bar, welded on the inside of the main bar [:math:`kN`].

            Note: Value may be found in National Annex.

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - formula (8.8N)

        Parameters
        ----------
        l_td: MM
            [:math:`l_{td}`] Design length of transverse bar [:math:`mm`].

            :math:`= 1.16 ⋅ ø_{t} ⋅ (f_{yd}/σ_{td})^{0.5} ≤ l_{t}`

            Use your own implementation of this formula or use the SubForm8Dot8nDesignLengthOfTransverseBar class.
        diameter_t: MM
            [:math:`ø_{t}`] Diameter of transverse bar [:math:`mm`].
        sigma_td: MPA
            [:math:`σ_{td}`] Concrete stress [:math:`MPa`].

            :math:`=(f_{ctd}+σ_{cm})/y ≤ 3⋅f_{cd}`

            Use your own implementation of this formula or use the SubForm8Dot8nConcreteStress class.
        f_wd: KN
            [:math:`F_{wd}`] Design shear strength of weld (specified as a factor times :math:`A_{s}⋅f_{yd}`; say :math:`0.5⋅A_{s}⋅f_{yd}` where
            :math:`A_{s}` is the cross-section of the anchored bar and fyd is its design yield strength)  [kN].
        """
        super().__init__()
        self.l_td = l_td
        self.diameter_t = diameter_t
        self.sigma_td = sigma_td
        self.f_wd = f_wd

    @staticmethod
    def _evaluate(
        l_td: MM,
        diameter_t: MM,
        sigma_td: MPA,
        f_wd: KN,
    ) -> KN:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            l_td=l_td,
            diameter_t=diameter_t,
            sigma_td=sigma_td,
            f_wd=f_wd,
        )
        return min(l_td * diameter_t * sigma_td * N_TO_KN, f_wd)


class SubForm8Dot8nDesignLengthOfTransverseBar(Formula):
    """Class representing sub-formula for formula 8.8N, which calculates the design length of the transverse bar."""

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        diameter_t: MM,
        f_yd: MPA,
        sigma_td: MPA,
        l_t: MM,
    ) -> None:
        """[:math:`l_{td}`] Design length of transverse bar [:math:`mm`].

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - :math:`l_{td}`

        Parameters
        ----------
        diameter_t: MM
            [:math:`ø_{t}`] Diameter of transverse bar [:math:`mm`].
        f_yd: MPA
            [:math:`f_{yd}`] Design yield strength of bar [:math:`MPa`].
        sigma_td: MPA
            [:math:`σ_{td}`] Concrete stress [:math:`MPa`].

            :math:`=(f_{ctd}+σ_{cm})/y ≤ 3⋅f_{cd}`

            Use your own implementation of this formula or use the SubForm8Dot8nConcreteStress class.
        l_t: MM
            [:math:`l_{t}`] Length of transverse bar, but not more than the spacing of bars to be anchored [:math:`mm`].
        """
        super().__init__()
        self.diameter_t = diameter_t
        self.f_yd = f_yd
        self.sigma_td = sigma_td
        self.l_t = l_t

    @staticmethod
    def _evaluate(
        diameter_t: MM,
        f_yd: MPA,
        sigma_td: MPA,
        l_t: MM,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            diameter_t=diameter_t,
            f_yd=f_yd,
            l_t=l_t,
        )
        raise_if_less_or_equal_to_zero(sigma_td=sigma_td)
        return min(1.16 * diameter_t * (f_yd / sigma_td) ** 0.5, l_t)


class SubForm8Dot8nConcreteStress(Formula):
    """Class representing sub-formula for formula 8.8N, which calculates the concrete stress."""

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ctd: MPA,
        sigma_cm: MPA,
        y_function: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        """[:math:`σ_{td}`] Concrete stress [:math:`MPa`].

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - σtd

        Parameters
        ----------
        f_ctd: MPA
            [:math:`f_{ctd}`] Design tensile strength of concrete [:math:`MPa`].
        sigma_cm: MPA
            [:math:`σ_{cm}`] Compression in the concrete perpendicular to both bars (mean value) [:math:`MPa`].
        y_function: DIMENSIONLESS
            [y] A function [-]

            :math:`= 0.015 + 0.14 ⋅ exp(-0.18⋅x)`

            Use your own implementation of this formula or use the SubForm8Dot8nFunctionY class.
        f_cd: MPA
            [:math:`f_{cd}`] Design value compressive strength of concrete [:math:`MPa`].
        """
        super().__init__()
        self.f_ctd = f_ctd
        self.sigma_cm = sigma_cm
        self.y_function = y_function
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        f_ctd: MPA,
        sigma_cm: MPA,
        y_function: DIMENSIONLESS,
        f_cd: MPA,
    ) -> MPA:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            f_ctd=f_ctd,
            sigma_cm=sigma_cm,
            f_cd=f_cd,
        )
        raise_if_less_or_equal_to_zero(y_function=y_function)
        return min((f_ctd + sigma_cm) / y_function, 3 * f_cd)


class SubForm8Dot8nFunctionY(Formula):
    """Class representing sub-formula for formula 8.8N, which calculates the function y."""

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        x_function: DIMENSIONLESS,
    ) -> None:
        """[y] A function [-].

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - y

        Parameters
        ----------
        x_function: DIMENSIONLESS
            [x] A function accounting for the geometry [-]

            :math:`= 2⋅(c/ø_{t}) + 1`

            Use your own implementation of this formula or use the SubForm8Dot8nFunctionX class.
        """
        super().__init__()
        self.x_function = x_function

    @staticmethod
    def _evaluate(
        x_function: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(x_function=x_function)
        return 0.015 + 0.14 * np.exp(-0.18 * x_function)


class SubForm8Dot8nFunctionX(Formula):
    """Class representing sub-formula for formula 8.8N, which calculates the function x."""

    label = "8.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        cover: MM,
        diameter_t: MM,
    ) -> None:
        """[x] A function accounting for the geometry [-].

        NEN-EN 1992-1-1+C2:2011 art.8.6(2) - x

        Parameters
        ----------
        cover: MM
            [c] Concrete cover perpendicular to both bars [:math:`mm`].
        diameter_t: MM
            [:math:`ø_{t}`] Diameter of transverse bar [:math:`mm`].
        """
        super().__init__()
        self.cover = cover
        self.diameter_t = diameter_t

    @staticmethod
    def _evaluate(
        cover: MM,
        diameter_t: MM,
    ) -> DIMENSIONLESS:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(cover=cover)
        raise_if_less_or_equal_to_zero(diameter_t=diameter_t)
        return 2 * (cover / diameter_t) + 1
