"""Formula 3.2 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DAYS, DIMENSIONLESS


class Form3Dot2CoefficientDependentOfConcreteAge(Formula):
    r"""Class representing formula 3.2 for the coefficient [$\beta_{cc}(t)$] which is dependent of the age of concrete."""

    label = "3.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        s: DIMENSIONLESS,
        t: DAYS,
    ) -> None:
        r"""[$\beta_{cc}(t)$] Coefficient which is dependent of the age of concrete in days [$-$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(6) - Formula (3.2)

        Parameters
        ----------
        s : DIMENSIONLESS
            [$s$] Coefficient dependent on the kind of cement [$-$].
            = 0.20 for cement of strength classes CEM 42.5 R, CEM 52.5 N, and CEM 52.5 R (class R);
            = 0.25 for cement of strength classes CEM 32.5 R, CEM 42.5 N (class N);
            = 0.38 for cement of strength class CEM 32.5 N (class S).
            Use your own implementation of this formula or use the SubForm3Dot2CoefficientTypeOfCementS class.
        t : DAYS
            [$t$] Age of concrete in days [$\text{days}$].

        Returns
        -------
        None
        """
        super().__init__()
        self.s = s
        self.t = t

    @staticmethod
    def _evaluate(
        s: DIMENSIONLESS,
        t: DAYS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        if s < 0:
            raise ValueError(f"Invalid s: {s}. s cannot be negative")
        if t <= 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative or zero")
        return np.exp(s * (1 - (28 / t) ** (1 / 2)))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.2."""
        return LatexFormula(
            return_symbol=r"\beta_{cc}(t)",
            result=f"{self:.3f}",
            equation=r"\exp \left( s \cdot \left( 1 - \left( \frac{28}{t} \right) ^{1/2} \right) \right)",
            numeric_equation=rf"\exp \left( {self.s:.3f} \cdot \left( 1 - \left( \frac{{28}}{{{self.t:.2f}}} \right) ^{{1/2}} \right) \right)",
            comparison_operator_label="=",
        )


class SubForm3Dot2CoefficientTypeOfCementS(Formula):
    r"""Class representing sub-formula for formula 3.2, which calculates the coefficient [$s$] which is dependent on the cement class."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.2"

    def __init__(
        self,
        cement_class: str,
    ) -> None:
        r"""[$s$] Coefficient that depends on the type of cement [$-$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(6) - s

        Parameters
        ----------
        cement_class : str
            [$cement\_class$] Class of the cement.
                = 'R' for cement of strength classes CEM 42.5 R, CEM 52.5 N, and CEM 52.5 R (class R);
                = 'N' for cement of strength classes CEM 32.5 R, CEM 42.5 N (class N);
                = 'S' for cement of strength class CEM 32.5 N (class S).

        """
        super().__init__()
        self.cement_class = cement_class

    @staticmethod
    def _evaluate(
        cement_class: str,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        match cement_class.lower():
            case "r":
                return 0.20
            case "n":
                return 0.25
            case "s":
                return 0.38
            case _:
                raise ValueError(f"Invalid cement class: {cement_class}. Options: 'R', 'N' or 'S'")

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.2s."""
        return LatexFormula(
            return_symbol=r"s",
            result=f"{self:.3f}",
            equation=r"\text{cement class}",
            numeric_equation=rf"{self.cement_class}",
            comparison_operator_label=r"\rightarrow",
        )
