"""Formula 8.128 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2
from blueprints.validations import raise_if_negative


class Form8Dot128EccentricallyLoadedArea(Formula):
    r"""Class representing formula 8.128 for the calculation of an eccentrically loaded area."""

    label = "8.128"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        a_0: MM,
        e_a: MM,
        b_0: MM,
        e_b: MM,
    ) -> None:
        r"""[$A_{c0,red}$] Eccentrically loaded area [$mm^2$].

        FprEN 1992-1-1:2023 (E) art. 8.6(2) - Formula (8.128)

        [$a_{0,red}$] and [$b_{0,red}$] follow from [$a_{0,red} = a_0 - 2 \cdot e_a$] and
        [$b_{0,red} = b_0 - 2 \cdot e_b$], see Figure 8.33 a).

        Parameters
        ----------
        a_0 : MM
            [$a_0$] Length of the loaded area in the direction perpendicular to the closest edge of the load
            introduction block, see Figure 8.32 [$mm$].
        e_a : MM
            [$e_a$] Eccentricity of the applied load to the center of [$A_{c0}$], parallel to [$a_0$] [$mm$].
        b_0 : MM
            [$b_0$] Width of the loaded area, see Figure 8.32 [$mm$].
        e_b : MM
            [$e_b$] Eccentricity of the applied load to the center of [$A_{c0}$], parallel to [$b_0$] [$mm$].
        """
        super().__init__()
        self.a_0 = a_0
        self.e_a = e_a
        self.b_0 = b_0
        self.e_b = e_b

    @staticmethod
    def _evaluate(
        a_0: MM,
        e_a: MM,
        b_0: MM,
        e_b: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_0=a_0, b_0=b_0)

        a_0_red = a_0 - 2 * e_a
        b_0_red = b_0 - 2 * e_b
        return a_0_red * b_0_red

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.128."""
        _equation: str = r"\left(a_0 - 2 \cdot e_a\right) \cdot \left(b_0 - 2 \cdot e_b\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_0": f"{self.a_0:.{n}f}",
                r"e_a": f"{self.e_a:.{n}f}",
                r"b_0": f"{self.b_0:.{n}f}",
                r"e_b": f"{self.e_b:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_0": rf"{self.a_0:.{n}f} \ mm",
                r"e_a": rf"{self.e_a:.{n}f} \ mm",
                r"b_0": rf"{self.b_0:.{n}f} \ mm",
                r"e_b": rf"{self.e_b:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"A_{c0,red}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm^2",
        )
