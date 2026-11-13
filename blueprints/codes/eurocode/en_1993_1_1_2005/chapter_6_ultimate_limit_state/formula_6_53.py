"""Formula 6.53 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot53NonDimensionalSlendernessTorsionalBucklingClass4(Formula):
    r"""Class representing formula 6.53 for the calculation of the non-dimensional slenderness for torsional or
    torsional-flexural buckling of a member with a Class 4 cross-section.
    """

    label = "6.53"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a_eff: MM2,
        f_y: MPA,
        n_cr: N,
    ) -> None:
        r"""[$\overline{\lambda}_T$] Non-dimensional slenderness for torsional or torsional-flexural buckling,
        for Class 4 cross-sections [-].

        EN 1993-1-1:2005 art.6.3.1.4(2) - Formula (6.53)

        Parameters
        ----------
        a_eff : MM2
            [$A_{eff}$] Effective area of the cross-section [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength [$MPa$].
        n_cr : N
            [$N_{cr}$] Elastic critical force, where [$N_{cr} = N_{cr,TF}$] but [$N_{cr} < N_{cr,T}$]. [$N_{cr,TF}$] is the
            elastic torsional-flexural buckling force and [$N_{cr,T}$] is the elastic torsional buckling force [$N$].
        """
        super().__init__()
        self.a_eff = a_eff
        self.f_y = f_y
        self.n_cr = n_cr

    @staticmethod
    def _evaluate(
        a_eff: MM2,
        f_y: MPA,
        n_cr: N,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_eff=a_eff, f_y=f_y)
        raise_if_less_or_equal_to_zero(n_cr=n_cr)

        return np.sqrt(a_eff * f_y / n_cr)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.53."""
        _equation: str = r"\sqrt{\frac{A_{eff} \cdot f_y}{N_{cr}}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_{eff}": f"{self.a_eff:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"N_{cr}": f"{self.n_cr:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A_{eff}": rf"{self.a_eff:.{n}f} \ mm^2",
                r"f_y": rf"{self.f_y:.{n}f} \ MPa",
                r"N_{cr}": rf"{self.n_cr:.{n}f} \ N",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\overline{\lambda}_T",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
