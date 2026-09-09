"""Formula 8.113 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot113CompressiveStressInStrutOrCompressionField(Formula):
    r"""Class representing formula 8.113 for the calculation of the compressive stress in a strut or in a
    compression field, assumed uniformly distributed over its cross-section.
    """

    label = "8.113"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        f_cd: N,
        b_c: MM,
        t: MM,
    ) -> None:
        r"""[$\sigma_{cd}$] Compressive stress in a strut or in a compression field [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.5.2(2) - Formula (8.113)

        Parameters
        ----------
        f_cd : N
            [$F_{cd}$] Compressive force of the strut [$N$].
        b_c : MM
            [$b_c$] Width of the strut at the considered location [$mm$].
        t : MM
            [$t$] Thickness of the strut, which can be limited by the thickness of the member [$mm$].
        """
        super().__init__()
        self.f_cd = f_cd
        self.b_c = b_c
        self.t = t

    @staticmethod
    def _evaluate(
        f_cd: N,
        b_c: MM,
        t: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(b_c=b_c, t=t)

        return abs(f_cd) / (b_c * t)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.113."""
        _equation: str = r"\frac{\left|F_{cd}\right|}{b_c \cdot t}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_{cd}": f"{self.f_cd:.{n}f}",
                r"b_c": f"{self.b_c:.{n}f}",
                r"\cdot t": rf"\cdot {self.t:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_{cd}": rf"{self.f_cd:.{n}f} \ N",
                r"b_c": rf"{self.b_c:.{n}f} \ mm",
                r"\cdot t": rf"\cdot {self.t:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{cd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
