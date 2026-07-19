"""Formula 5.2 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 5 - Structural analysis."""

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, N
from blueprints.validations import LessOrEqualToZeroError, raise_if_less_or_equal_to_zero, raise_if_mismatch_sign


class Form5Dot2ElasticCriticalBucklingFactor(Formula):
    r"""Class representing formula 5.2 for the calculation of [$\alpha_{cr}$]."""

    label = "5.2"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        h_ed: N,
        v_ed: N,
        h: MM,
        delta_h_ed: MM,
    ) -> None:
        r"""[$\alpha_{cr}$] Calculation of the elastic critical buckling factor for a building storey.

        NEN-EN 1993-1-1+C2+A1:2016 art.5.2.1(4)B - Formula (5.2)

        Parameters
        ----------
        h_ed : N
            [$H_{Ed}$] Total design horizontal reaction at the storey base [$N$].
        v_ed : N
            [$V_{Ed}$] Total design vertical load on the structure at the storey base [$N$].
        h : MM
            [$h$] Storey height [$mm$].
        delta_h_ed : MM
            [$\delta_{H,Ed}$] Horizontal displacement at the top of the storey relative to the bottom [$mm$].
        """
        super().__init__()
        self.h_ed = h_ed
        self.v_ed = v_ed
        self.h = h
        self.delta_h_ed = delta_h_ed

    @staticmethod
    def _evaluate(
        h_ed: N,
        v_ed: N,
        h: MM,
        delta_h_ed: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_mismatch_sign(h_ed=h_ed, v_ed=v_ed)
        raise_if_less_or_equal_to_zero(h=h, delta_h_ed=delta_h_ed)

        if v_ed == 0.0:
            raise LessOrEqualToZeroError(value_name="v_ed", value=v_ed)

        return (h_ed / v_ed) * (h / delta_h_ed)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.2."""
        _equation: str = r"\frac{H_{Ed}}{V_{Ed}} \cdot \frac{h}{\delta_{H,Ed}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"H_{Ed}": f"{self.h_ed:.{n}f}",
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
                r"h": f"{self.h:.{n}f}",
                r"\delta_{H,Ed}": f"{self.delta_h_ed:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"H_{Ed}": rf"{self.h_ed:.{n}f} \ N",
                r"V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                r"h": rf"{self.h:.{n}f} \ mm",
                r"\delta_{H,Ed}": rf"{self.delta_h_ed:.{n}f} \ mm",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"\alpha_{cr}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="",
        )
