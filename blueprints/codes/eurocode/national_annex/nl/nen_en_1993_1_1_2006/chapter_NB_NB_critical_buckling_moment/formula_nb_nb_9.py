"""Formula NB.NB.9 from NEN-EN 1993-1-1:2006: Chapter NB.NB - Parameter alpha."""

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006 import NEN_EN_1993_1_1_2006_A1_2014_NB_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class FormNBDotNB9Alpha(Formula):
    r"""Class representing formula NB.NB.9 for the calculation of [$\alpha$]."""

    label = "NB.NB.9"
    source_document = NEN_EN_1993_1_1_2006_A1_2014_NB_2016

    def __init__(
            self,
            h: MM,
            t_f: MM,
            t_w: MM,
            b: MM,
            l_g: MM,
    ) -> None:
        r"""[$\alpha$] Parameter dependent on beam dimensions [-].

        NEN-EN 1993-1-1:2006 art.NB.NB.4.2(2) - Formula (NB.NB.9)

        Parameters
        ----------
        h : MM
            [$h$] Height of a beam [$mm$].
        t_f : MM
            [$t_f$] Thickness of the flange (t is t in case of a tube profile) [$mm$].
        t_w : MM
            [$t_w$] Thickness of the web (t_w is 2t in case of a tube profile) [$mm$].
        b : MM
            [$b$] Width of the beam [$mm$].
        l_g : MM
            [$L_g$] Length of the beam between supports [$mm$].
        """
        super().__init__()
        self.h = h
        self.t_f = t_f
        self.t_w = t_w
        self.b = b
        self.l_g = l_g

    @staticmethod
    def _evaluate(
            h: MM,
            t_f: MM,
            t_w: MM,
            b: MM,
            l_g: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(t_w=t_w, b=b, l_g=l_g)
        raise_if_negative(h=h, t_f=t_f)

        return max(575, (h * t_f * 1e12) / (t_w ** 3 * b * l_g ** 2))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula NB.NB.9."""
        _equation: str = r"\max\left(575, \frac{h \cdot t_f \cdot 10^{12}}{t_w^3 \cdot b \cdot L_g^2}\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"h ": f"{self.h:.{n}f} ",
                r"t_f": f"{self.t_f:.{n}f}",
                r"t_w": f"{self.t_w:.{n}f}",
                r"b": f"{self.b:.{n}f}",
                r"L_g": f"{self.l_g:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"h ": rf"{self.h:.{n}f} \ mm ",
                r"t_f": rf"{self.t_f:.{n}f} \ mm",
                r"t_w": rf"{self.t_w:.{n}f} \ mm",
                r"b": rf"{self.b:.{n}f} \ mm",
                r"L_g": rf"{self.l_g:.{n}f} \ mm",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"\alpha",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
