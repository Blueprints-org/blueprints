"""Formula 8.53 from prEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.pr_en_1992_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N, DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot53TensileChordLimitForIntermediateSupportOrConcentratedLoads(Formula):
    r"""Class representing formula 8.53 for the calculation of the tensile chord limit in case of direct intermediate support or in the region of concentraded loads."""

    label = "8.53"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
            self,
            m_ed_max: N,
            z: MM,
            n_ed: N,
    ) -> None:
        r"""[$F_{td,max}$] Calculation of the chord force [$N$] in case of direct intermediate support or concentrated loads.

        prEN 1992-1-2023 art.8.5(8) - Formula (8.53)

        Parameters
        ----------
        m_ed_max : N
            [$M_{Ed,max}$] Maximum design moment along the member [$Nmm$].
        z : MM
            [$z$] Internal lever arm [$mm$].
        n_ed : N
            [$N_{Ed}$] Design value of normal force in the section [$N$].
        """
        super().__init__()
        self.m_ed_max = m_ed_max
        self.z = z
        self.n_ed = n_ed

    @staticmethod
    def _evaluate(
            m_ed_max: N,
            z: MM,
            n_ed: N,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(z=z)
        raise_if_negative(m_ed_max=m_ed_max, n_ed=n_ed)

        return m_ed_max / z + n_ed / 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.53."""
        _equation: str = r"\frac{M_{Ed,max}}{z} + \frac{N_{Ed}}{2}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"M_{Ed,max}": f"{self.m_ed_max:.{n}f}",
                r"z": f"{self.z:.{n}f}",
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"M_{Ed,max}": rf"{self.m_ed_max:.3f} \ Nmm",
                r"z": rf"{self.z:.3f} \ mm",
                r"N_{Ed}": rf"{self.n_ed:.3f} \ N",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"F_{td,max}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )
