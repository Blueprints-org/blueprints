"""Formula 8.13 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot13ConfinementStressMultipleConfinement(Formula):
    r"""Class representing formula 8.13 for the calculation of the confinement stress for members in
    compression with multiple confinement reinforcement.
    """

    label = "8.13"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        sum_a_s_confx: MM2,
        b_csy: MM,
        sum_a_s_confy: MM2,
        b_csx: MM,
        f_yd: MPA,
        s: MM,
    ) -> None:
        r"""[$\sigma_{c2d}$] Confinement stress for members in compression with multiple confinement
        reinforcement, see Figure 8.3 c) and d) [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.1.4(3) - Formula (8.13)

        Parameters
        ----------
        sum_a_s_confx : MM2
            [$\Sigma A_{s,confx}$] Sum of the cross-sectional areas of the legs of confinement reinforcement in
            the [$x$] direction [$mm^2$].
        b_csy : MM
            [$b_{csy}$] Width of the confinement core in the [$y$] direction, to the centrelines of the
            confinement reinforcement, see Figure 8.3 [$mm$].
        sum_a_s_confy : MM2
            [$\Sigma A_{s,confy}$] Sum of the cross-sectional areas of the legs of confinement reinforcement in
            the [$y$] direction [$mm^2$].
        b_csx : MM
            [$b_{csx}$] Width of the confinement core in the [$x$] direction, to the centrelines of the
            confinement reinforcement, see Figure 8.3 [$mm$].
        f_yd : MPA
            [$f_{yd}$] Design value of the yield strength of the reinforcement [$MPa$].
        s : MM
            [$s$] Spacing of confinement reinforcement [$mm$].
        """
        super().__init__()
        self.sum_a_s_confx = sum_a_s_confx
        self.b_csy = b_csy
        self.sum_a_s_confy = sum_a_s_confy
        self.b_csx = b_csx
        self.f_yd = f_yd
        self.s = s

    @staticmethod
    def _evaluate(
        sum_a_s_confx: MM2,
        b_csy: MM,
        sum_a_s_confy: MM2,
        b_csx: MM,
        f_yd: MPA,
        s: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sum_a_s_confx=sum_a_s_confx, sum_a_s_confy=sum_a_s_confy, f_yd=f_yd)
        raise_if_less_or_equal_to_zero(b_csy=b_csy, b_csx=b_csx, s=s)

        return min(sum_a_s_confx / b_csy, sum_a_s_confy / b_csx) * f_yd / s

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.13."""
        _equation: str = r"\min\left(\frac{\Sigma A_{s,confx}}{b_{csy}}, \frac{\Sigma A_{s,confy}}{b_{csx}}\right) \cdot \frac{f_{yd}}{s}"
        # The lone symbol s is anchored as "{s}" (its own fraction denominator) to avoid matching the "s" that
        # is part of b_csx and b_csy.
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\Sigma A_{s,confx}": f"{self.sum_a_s_confx:.{n}f}",
                r"b_{csy}": f"{self.b_csy:.{n}f}",
                r"\Sigma A_{s,confy}": f"{self.sum_a_s_confy:.{n}f}",
                r"b_{csx}": f"{self.b_csx:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
                r"{s}": "{" + f"{self.s:.{n}f}" + "}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\Sigma A_{s,confx}": rf"{self.sum_a_s_confx:.{n}f} \ mm^2",
                r"b_{csy}": rf"{self.b_csy:.{n}f} \ mm",
                r"\Sigma A_{s,confy}": rf"{self.sum_a_s_confy:.{n}f} \ mm^2",
                r"b_{csx}": rf"{self.b_csx:.{n}f} \ mm",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
                r"{s}": "{" + rf"{self.s:.{n}f} \ mm" + "}",
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
