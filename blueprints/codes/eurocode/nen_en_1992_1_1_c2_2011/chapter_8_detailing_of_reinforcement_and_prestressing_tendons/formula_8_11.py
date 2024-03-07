"""Formula 8.11 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_negative


class Form8Dot11MinimumDesignLapLength(Formula):
    """Class representing formula 8.11 for the calculation of the minimum design lap length :math:`l_{0,min}` [:math:`mm`]."""

    label = "8.11"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_6: DIMENSIONLESS,
        l_b_rqd: MM,
        diameter: MM,
    ) -> None:
        """[:math:`l_{0,min}`] Design minimum lap length [:math:`mm`].

        NEN-EN 1992-1-1+C2:2011 art.8.7.3(1) - Formula (8.11)

        Parameters
        ----------
        alpha_6 : DIMENSIONLESS
            [:math:`α_6`] Coefficient for the effect of reinforcement ratio [-].

            :math:`= (ρ_l/25)^{0.5} <= 1.5` with a minimum of 1.0.

            Where: :math:`ρ_l` = reinforcement percentage lapped within :math:`0.65 ⋅ l_0` from the centre of the lap length
            considered (see figure 8.8) [-].

            Use your own implementation for this value or use the :class:`SubForm8Dot10Alpha6` class.
        l_b_rqd: MM
            [:math:`l_{b,rqd}`] Basic required anchorage length, for anchoring the force :math:`A_s ⋅ σ_{sd}` in a straight bar assuming constant
            bond stress (formula 8.3) [:math:`mm`].

            Use your own implementation for this value or use the :class:`Form8Dot3RequiredAnchorageLength` class.
        diameter : MM
            [:math:`Ø`] Diameter of the bar [:math:`mm`].
        """
        super().__init__()
        self.alpha_6 = alpha_6
        self.l_b_rqd = l_b_rqd
        self.diameter = diameter

    @staticmethod
    def _evaluate(
        alpha_6: DIMENSIONLESS,
        l_b_rqd: MM,
        diameter: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            diameter=diameter,
        )
        return max(0.3 * alpha_6 * l_b_rqd, 15 * diameter, 200)
