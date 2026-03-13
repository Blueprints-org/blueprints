"""Formula 5.12 from EN 1993-5:2007: Chapter 5 - Ultimate Limit States."""

import numpy as np

from blueprints.codes.eurocode.en_1993_5_2007 import EN_1993_5_2007
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MM4, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot12ElasticCriticalLoad(Formula):
    r"""Class representing formula 5.12 for the calculation of the elastic critical load, [$N_{cr}$]."""

    label = "5.12"
    source_document = EN_1993_5_2007

    def __init__(
        self,
        e: MPA,
        i: MM4,
        beta_d: DIMENSIONLESS,
        l: MM,  # noqa: E741
    ) -> None:
        r"""[$N_{cr}$] Elastic critical load [$N$].

        EN 1993-5:2007 art.5.2.3 - Formula (5.12)

        Parameters
        ----------
        e : MPA
            [$E$] Modulus of elasticity [$MPa$].
        i : MM4
            [$I$] Moment of inertia [$mm^4$].
        beta_d : DIMENSIONLESS
            [$\beta_D$] Reduction factor, see 6.4 [$-$].
        l : MM
            [$l$] the buckling length, determined according to Figure 5-2 for a free or partially fixed earth
            support or according to Figure 5-3 for a fixed earth support. [$mm$].
        """
        super().__init__()
        self.e = e
        self.i = i
        self.beta_d = beta_d
        self.l = l

    @staticmethod
    def _evaluate(
        e: MPA,
        i: MM4,
        beta_d: DIMENSIONLESS,
        l: MM,  # noqa: E741
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            e=e,
            i=i,
            beta_d=beta_d,
        )
        raise_if_less_or_equal_to_zero(l=l)

        return (e * i * beta_d * (np.pi**2)) / (l**2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.12."""
        return LatexFormula(
            return_symbol=r"N_{cr}",
            result=f"{self:.{n}f}",
            equation=r"\frac{E \cdot I \cdot \beta_D \cdot \pi^2}{l^2}",
            numeric_equation=rf"\frac{{{self.e:.{n}f} \cdot {self.i:.{n}f} \cdot {self.beta_d:.{n}f} \cdot \pi^2}}{{{self.l:.{n}f}^2}}",
            comparison_operator_label="=",
            unit="N",
        )
