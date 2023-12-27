"""Formula 8.2 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_negative


class Form8Dot2UltimateBondStress(Formula):
    """Class representing formula 8.2 for the calculation of the design value of the ultimate bond stress for ribbed bars."""

    label = "8.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        eta_1: DIMENSIONLESS,
        eta_2: DIMENSIONLESS,
        f_ctd: MPA,
    ) -> None:
        """[fbd] The design value of the ultimate bond stress for ribbed bars [-].

        NEN-EN 1992-1-1+C2:2011 art.8.4.2(2) - Formula (8.2)

        Parameters
        ----------
        eta_1 : DIMENSIONLESS
            [η1] coefficient related to the quality of the bond condition and the position of the bar during concreting (see Figure 8.2) [-].
            = 1 when ‘good’ conditions are obtained;
            = 0.7 other cases and for bars in structural elements built with slip-forms, unless it can be shown that ‘good’ bond conditions exist;
            Use your own implementation of this formula or use the SubForm8Dot2CoefficientQualityOfBond class.
        eta_2 : DIMENSIONLESS
            [η2] A factor related to the bar diameter [-].
            = 1 for bars with a diameter ≤ 32 mm;
            = (132 - Ø) / 100 for bars with a diameter > 32 mm.
            Use your own implementation of this value or use the SubForm8Dot2CoefficientBarDiameter class.
        f_ctd : MPA
            [fctd] Design tensile strength of concrete according to art.3.1.6(2) [MPa].
            Due to the increasing brittleness of higher strength concrete, fctk,0,05 should be limited here to the value for C60/75, unless it can be
            verified that the average bond strength increases above this limit.
        """
        super().__init__()
        self.eta_1 = eta_1
        self.eta_2 = eta_2
        self.f_ctd = f_ctd

    @staticmethod
    def _evaluate(
        eta_1: DIMENSIONLESS,
        eta_2: DIMENSIONLESS,
        f_ctd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(eta_1=eta_1, eta_2=eta_2, f_ctd=f_ctd)
        return 2.25 * eta_1 * eta_2 * f_ctd


class SubForm8Dot2CoefficientQualityOfBond(Formula):
    """Class representing sub-formula for formula 8.2, which calculates the coefficient 'η1' which is dependent on the quality of the bond."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "8.2"

    def __init__(self, bond_quality: str) -> None:
        """[η1] Coefficient that depends on the type of cement [-].

        NEN-EN 1992-1-1+C2:2011 art.8.4.2(2) - η1

        Parameters
        ----------
        bond_quality : str
            Quality of the bond.
                = 'good' for a good bond condition.;
                = 'other' for other cases and for bars in structural elements built with slip-forms, unless it can be shown that ‘good’ bond
                conditions exist.;
        """
        super().__init__()
        self.bond_quality = bond_quality

    @staticmethod
    def _evaluate(bond_quality: str) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        match bond_quality.lower():
            case "good":
                return 1
            case "other":
                return 0.7
            case _:
                raise ValueError(f"Invalid bond quality: {bond_quality}. Options: 'good' or 'other'")


class SubForm8Dot2CoefficientBarDiameter(Formula):
    """Class representing sub-formula for formula 8.2, which calculates the coefficient 'η2' which is dependent on the bar diameter."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "8.2"

    def __init__(self, diameter: MM) -> None:
        """[η2] Coefficient that depends on the bar diameter [-].

        NEN-EN 1992-1-1+C2:2011 art.8.4.2(2) - η2

        Parameters
        ----------
        diameter : MM
            [Ø] Diameter of the bar [mm].
        """
        super().__init__()
        self.diameter = diameter

    @staticmethod
    def _evaluate(diameter: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(diameter=diameter)
        if diameter <= 32:
            return 1
        return (132 - diameter) / 100
