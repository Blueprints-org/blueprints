"""Formula 8.16 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot16BasicTransmissionLength(Formula):
    """Class representing formula 8.16 for the calculation of the basic transmission length :math:`l_{pt}`."""

    label = "8.16"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_1: DIMENSIONLESS,
        alpha_2: DIMENSIONLESS,
        diameter: MM,
        sigma_pm0: MPA,
        f_bpt: MPA,
    ) -> None:
        """[:math:`l_{pt}`] Basic value of the transmission length [:math:`mm`].

        NEN-EN 1992-1-1+C2:2011 art.8.10.2.2(2) - Formula (8.16)

        Parameters
        ----------
        alpha_1 : DIMENSIONLESS
            [:math:`α_{1}`] Coefficient taking account of the type of release [-].

            = 1.0 for gradual release;

            = 1.25 for sudden release.

            Use your own implementation for this value or use :class:`SubForm8Dot16Alpha1` class.
        alpha_2 : DIMENSIONLESS
            [:math:`α_{2}`] Coefficient taking account of the type of prestressing steel [-].

            = 0.25 for tendons with circular cross-section;

            = 0.19 for 3 and 7-wire strands.

            Use your own implementation for this value or use :class:`SubForm8Dot16Alpha2` class.
        diameter : MM
            [:math:`Ø`] Nominal diameter of the tendon [:math:`mm`].
        sigma_pm0 : MPA
            [:math:`σ_{pm0}`] Tendon stress at time of release [:math:`MPa`].
        f_bpt : MPA
            [:math:`f_{bpt}`] Constant bond stress at which prestress is assumed to be transferred to the concrete [:math:`MPa`]

            Use your own implementation for this value or use :class:`Form8Dot15PrestressTransferStress` class.
        """
        super().__init__()
        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2
        self.diameter = diameter
        self.sigma_pm0 = sigma_pm0
        self.f_bpt = f_bpt

    @staticmethod
    def _evaluate(
        alpha_1: DIMENSIONLESS,
        alpha_2: DIMENSIONLESS,
        diameter: MM,
        sigma_pm0: MPA,
        f_bpt: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            diameter=diameter,
            sigma_pm0=sigma_pm0,
        )
        raise_if_less_or_equal_to_zero(f_bpt=f_bpt)
        return alpha_1 * alpha_2 * diameter * sigma_pm0 / f_bpt


class SubForm8Dot16Alpha1(Formula):
    """Class representing sub-formula 8.16 for the calculation of the coefficient :math:`α_{1}`."""

    label = "8.16"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, release_type: str) -> None:
        """[:math:`α_{1}`] Coefficient taking account of the type of release [-].

        NEN-EN 1992-1-1+C2:2011 art.8.10.2.2(2) - Formula (8.16)

        Parameters
        ----------
        release_type : str
            Type of release, either "gradual" or "sudden".
        """
        super().__init__()
        self.release_type = release_type

    @staticmethod
    def _evaluate(release_type: str) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        match release_type.lower():
            case "gradual":
                return 1.0
            case "sudden":
                return 1.25
            case _:
                raise ValueError(f"Invalid release type: {release_type}. Valid values are 'gradual' or 'sudden'.")


class SubForm8Dot16Alpha2(Formula):
    """Class representing sub-formula 8.16 for the calculation of the coefficient :math:`α_{2}`."""

    label = "8.16"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        type_of_wire: str,
    ) -> None:
        """[:math:`α_{2}`] Coefficient that takes into account the type of wires in the cross-section [-].

        NEN-EN 1992-1-1+C2:2011 art.8.10.2.2(2) - Formula (8.16)

        Parameters
        ----------
        type_of_wire : str
            Type of wire.

            = 'circular' for circular cross-sections;

            = '3_7_wire_strands' for 3 and 7-wire strands;
        """
        super().__init__()
        self.type_of_wire = type_of_wire

    @staticmethod
    def _evaluate(type_of_wire: str) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        match type_of_wire.lower():
            case "circular":
                return 0.25
            case "3_7_wire_strands":
                return 0.19
            case _:
                raise ValueError(f"Invalid type of wire: {type_of_wire}. Valid values are 'circular' or '3_7_wire_strands'.")
