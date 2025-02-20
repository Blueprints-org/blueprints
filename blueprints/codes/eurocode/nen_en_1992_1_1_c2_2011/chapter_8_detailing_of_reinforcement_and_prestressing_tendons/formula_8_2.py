"""Formula 8.2 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
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
        r"""[$f_{bd}$] The design value of the ultimate bond stress for ribbed bars [$-$].

        NEN-EN 1992-1-1+C2:2011 art.8.4.2(2) - Formula (8.2)

        Parameters
        ----------
        eta_1 : DIMENSIONLESS
            [$η_1$] coefficient related to the quality of the bond condition and the position of the bar during concreting (see Figure 8.2) [$-$].
            = [$1$] when ‘good’ conditions are obtained;
            = [$1$] other cases and for bars in structural elements built with slip-forms, unless it can be shown that ‘good’ bond conditions
            exist;
            Use your own implementation of this formula or use the SubForm8Dot2CoefficientQualityOfBond class.
        eta_2 : DIMENSIONLESS
            [$η_2$] A factor related to the bar diameter [$-$].
            = [$1$] for bars with a diameter ≤ [$32 \text{mm}$];
            = [$(132 - Ø) / 100$] for bars with a diameter > [$32 \text{mm}$].
            Use your own implementation of this value or use the SubForm8Dot2CoefficientBarDiameter class.
        f_ctd : MPA
            [$f_{ctd}$] Design tensile strength of concrete according to art.3.1.6(2) [$MPa$].
            Due to the increasing brittleness of higher strength concrete, [$f_{ctk,0,05}$] should be limited here to the value for C60/75, unless
            it can be verified that the average bond strength increases above this limit.
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

    def latex(self) -> LatexFormula:
        """Returns a representation of the formula in LaTeX format."""
        return LatexFormula(
            return_symbol=r"f_{bd}",
            result=f"{self:.2f}",
            equation=r"2.25 \cdot \eta_1 \cdot \eta_2 \cdot f_{ctd}",
            numeric_equation=rf"2.25 \cdot {self.eta_1:.2f} \cdot {self.eta_2:.2f} \cdot {self.f_ctd:.2f}",
            comparison_operator_label="=",
        )


class SubForm8Dot2CoefficientQualityOfBond(Formula):
    """Class representing sub-formula for formula 8.2, which calculates the coefficient 'η1' which is dependent on the quality of the bond."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "8.2"

    def __init__(self, bond_quality: str) -> None:
        r"""[$η_1$] Coefficient that depends on the type of cement [$-$].

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
        r"""[$η_2$] Coefficient that depends on the bar diameter [$-$].

        NEN-EN 1992-1-1+C2:2011 art.8.4.2(2) - [$η_2$]

        Parameters
        ----------
        diameter : MM
            [$Ø$] Diameter of the bar [$mm$].
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

    def latex(self) -> LatexFormula:
        """Returns a LatexFormula object for this formula."""
        numerical_equation = "1.00" if self.diameter <= 32 else f"(132 - {self.diameter}) / 100"

        return LatexFormula(
            return_symbol=r"\eta_2",
            result=f"{self:.2f}",
            equation=r"\begin{matrix} 1.0 & \text{for }Ø ≤ 32 \\ (132 - Ø) / 100 & \text{for }Ø > 32  \end{matrix}",
            numeric_equation=numerical_equation,
            comparison_operator_label="=",
        )
