"""Formula NB.NB.12 from NEN-EN 1993-1-1:2006: Chapter NB.NB - Parameter S."""

import numpy as np

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006 import NEN_EN_1993_1_1_2006_A1_2014_NB_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM4, MM6, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class FormNBDotNB12ParameterS(Formula):
    r"""Class representing formula NB.NB.12 for the calculation of [$S$]."""

    label = "NB.NB.12"
    source_document = NEN_EN_1993_1_1_2006_A1_2014_NB_2016

    def __init__(
        self,
        e: MPA,
        i_w: MM6,
        g: MPA,
        i_t: MM4,
    ) -> None:
        r"""[$S$] Calculation of parameter S [$mm$].

        NEN-EN 1993-1-1:2006 art.NB.NB.4.3(2) - Formula (NB.NB.12)

        Parameters
        ----------
        e : MPA
            [$E$] Elasticity modulus [$MPa$].
        i_w : MM6
            [$I_w$] Warping constant [$mm^6$].
        g : MPA
            [$G$] Shear modulus [$MPa$].
        i_t : MM4
            [$I_t$] Torsional moment of inertia [$mm^4$].
        """
        super().__init__()
        self.e = e
        self.i_w = i_w
        self.g = g
        self.i_t = i_t

    @staticmethod
    def _evaluate(
        e: MPA,
        i_w: MM6,
        g: MPA,
        i_t: MM4,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(g=g, i_t=i_t)
        raise_if_negative(e=e, i_w=i_w)

        return np.sqrt((e * i_w) / (g * i_t))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula NB.NB.12."""
        _equation: str = r"\sqrt{\frac{E \cdot I_w}{G \cdot I_t}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"E": f"{self.e:.{n}f}",
                r"I_w": f"{self.i_w:.{n}f}",
                r"G": f"{self.g:.{n}f}",
                r"I_t": f"{self.i_t:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"E": rf"{self.e:.{n}f} \ MPa",
                r"I_w": rf"{self.i_w:.{n}f} \ mm^6",
                r"G": rf"{self.g:.{n}f} \ MPa",
                r"I_t": rf"{self.i_t:.{n}f} \ mm^4",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"S",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
