"""Formula 5.3a from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.validations import raise_if_negative


class Form5Dot3aTransverseForceUnbracedMembers(Formula):
    """Class representing formula 5.3a for the calculation of the transverse force for unbraced members, :math:`H_{i}`.

    See Figure 5.1 a1.
    """

    label = "5.3a"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        theta_i: DIMENSIONLESS,
        n_axial_force: KN,
    ) -> None:
        """[:math:`H_{i}`] Transverse force for unbraced members [:math:`kN`].

        NEN-EN 1992-1-1+C2:2011 art.5.2(7) - Formula (5.3a)

        Parameters
        ----------
        theta_i : DIMENSIONLESS
            [:math:`Θ_{i}`] Eccentricity, initial inclination imperfections [-].

            Use your own implementation of this value or use the :class:`Form5Dot1Imperfections` class.
        n_axial_force : KN
            [:math:`N`] Axial force [:math:`kN`].

            Positive values for compression, tension is not allowed.

        Notes
        -----
        Eccentricity is suitable for statically determinate members, whereas transverse load can be used for
        both determinate and indeterminate members. The force :math:`H_{i}` may be substituted by some other equivalent
        transverse action.
        """
        super().__init__()
        self.theta_i = theta_i
        self.n_axial_force = n_axial_force

    @staticmethod
    def _evaluate(
        theta_i: DIMENSIONLESS,
        n_axial_force: KN,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(theta_i=theta_i, n_axial_force=n_axial_force)
        return theta_i * n_axial_force
