"""Formula 8.1 from NEN-EN 1992-1-1+C2:2011: Chapter 8 Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import KN, MM, MPA
from blueprints.unit_conversion import KN_TO_N
from blueprints.validations import raise_if_negative


class Form8Dot1RequiredMinimumMandrelDiameter(Formula):
    """Class representing formula 8.1 for the calculation of the required minimum mandrel diameter if it needs to be checked to avoid
    concrete failure.
    """

    label = "8.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_bt: KN,
        a_b: MM,
        diameter: MM,
        f_cd: MPA,
    ) -> None:
        """[Øm,min] minimum mandrel diameter if it needs to be checked to avoid concrete failure [MM].

        NEN-EN 1992-1-1+C2:2011 art.8.3(3) - Formula (8.1)

        Parameters
        ----------
        f_bt: KN
            [Fbt] Tensile force from ultimate loads in a bar or group of bars in contact at the start of a bend  [kN].
        a_b: MM
            [ab] Half of the centre-to-centre distance between bars (or groups of bars) perpendicular
            to the plane of the bend for a given bar (or group of bars in contact).
            For a bar or group of bars adjacent to the face of the member, 'ab' should be taken as the cover plus Ø/2 [mm].
        diameter: MM
            [Ø] Diameter of reinforcing bar [mm].
        f_cd: MPA
            [fcd] Design value of concrete compressive stress [MPa].
            Note: The value of fcd should not be taken greater than that for concrete class C55/67.
        """
        super().__init__()
        self.f_bt = f_bt
        self.a_b = a_b
        self.diameter = diameter
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        f_bt: KN,
        a_b: MM,
        diameter: MM,
        f_cd: MPA,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            f_bt=f_bt,
            a_b=a_b,
            diameter=diameter,
            f_cd=f_cd,
        )
        return f_bt * KN_TO_N * ((1 / a_b) + 1 / (2 * diameter)) / f_cd
