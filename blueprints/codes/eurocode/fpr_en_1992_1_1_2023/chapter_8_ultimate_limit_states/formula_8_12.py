"""Formula 8.12 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot12ConfinementStressRectangularSingleConfinement(Formula):
    r"""Class representing formula 8.12 for the calculation of the confinement stress for rectangular members
    in compression with single confinement reinforcement.
    """

    label = "8.12"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        a_s_conf: MM2,
        f_yd: MPA,
        b_csx: MM,
        b_csy: MM,
        s: MM,
    ) -> None:
        r"""[$\sigma_{c2d}$] Confinement stress for rectangular members in compression with single confinement
        reinforcement, with [$b_{csx}$] and [$b_{csy}$] according to Figure 8.3 c) [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.1.4(3) - Formula (8.12)

        Parameters
        ----------
        a_s_conf : MM2
            [$A_{s,conf}$] Cross-sectional area of one leg of confinement reinforcement [$mm^2$].
        f_yd : MPA
            [$f_{yd}$] Design value of the yield strength of the reinforcement [$MPa$].
        b_csx : MM
            [$b_{csx}$] Width of the confinement core in the [$x$] direction, to the centrelines of the
            confinement reinforcement, see Figure 8.3 [$mm$].
        b_csy : MM
            [$b_{csy}$] Width of the confinement core in the [$y$] direction, to the centrelines of the
            confinement reinforcement, see Figure 8.3 [$mm$].
        s : MM
            [$s$] Spacing of confinement reinforcement [$mm$].
        """
        super().__init__()
        self.a_s_conf = a_s_conf
        self.f_yd = f_yd
        self.b_csx = b_csx
        self.b_csy = b_csy
        self.s = s

    @staticmethod
    def _evaluate(
        a_s_conf: MM2,
        f_yd: MPA,
        b_csx: MM,
        b_csy: MM,
        s: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_s_conf=a_s_conf, f_yd=f_yd)
        raise_if_less_or_equal_to_zero(b_csx=b_csx, b_csy=b_csy, s=s)

        return 2 * a_s_conf * f_yd / (max(b_csx, b_csy) * s)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.12."""
        _equation: str = r"\frac{2 \cdot A_{s,conf} \cdot f_{yd}}{\max\left(b_{csx}, b_{csy}\right) \cdot s}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_{s,conf}": f"{self.a_s_conf:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
                r"b_{csx}": f"{self.b_csx:.{n}f}",
                r"b_{csy}": f"{self.b_csy:.{n}f}",
                r"\cdot s}": rf"\cdot {self.s:.{n}f}" + "}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_{s,conf}": rf"{self.a_s_conf:.{n}f} \ mm^2",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
                r"b_{csx}": rf"{self.b_csx:.{n}f} \ mm",
                r"b_{csy}": rf"{self.b_csy:.{n}f} \ mm",
                r"\cdot s}": rf"\cdot {self.s:.{n}f} \ mm" + "}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{c2d}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
