"""Formula 7.4 from NEN-EN 1992-1-1+C2:2011: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot4MeanStressConcrete(Formula):
    r"""Class representing formula 7.4 for the calculation of [$\sigma_c$]."""

    label = "7.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        n_ed: N,
        b: MM,
        h: MM,
    ) -> None:
        r"""[$\sigma_c$] Calculation of mean stress of the concrete in the cross-section under consideration [$MPa$].

        NEN-EN 1992-1-1+C2:2011 art.7.3.2(2) - Formula (7.4)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Axial force at the serviceability limit state acting on the part of the
            cross-section under consideration (compressive force positive) [$N$].
        b : MM
            [$b$] Width of the cross-section [$mm$].
        h : MM
            [$h$] Height of the cross-section [$mm$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.b = b
        self.h = h

    @staticmethod
    def _evaluate(
        n_ed: N,
        b: MM,
        h: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(b=b, h=h)
        raise_if_negative(n_ed=n_ed)

        return n_ed / (b * h)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 7.4."""
        _equation: str = r"\frac{N_{Ed}}{b \cdot h}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.3f}",
                r"b": f"{self.b:.3f}",
                r"h": f"{self.h:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_c",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
