"""Formula 8.25 from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM3, MM4, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot25ShearStress(Formula):
    r"""Class representing formula 8.25 for the calculation of [$\tau_{Ed}$]."""

    label = "8.25"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        v_ed: N,
        s: MM3,
        i: MM4,
        t: MM,
    ) -> None:
        r"""[$\tau_{Ed}$] Calculation of the design elastic shear stress [$MPa$].

        EN 1993-1-1:2025 art.8.2.6(4) - Formula (8.25)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design value of the shear force [$N$].
        s : MM3
            [$S$] First moment of area about the centroidal axis of that portion of the cross-section between
            the point at which the shear is required and the boundary of the cross-section [$mm^3$].
        i : MM4
            [$I$] Second moment of area of the whole cross section [$mm^4$].
        t : MM
            [$t$] Thickness at the examined point [$mm$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.s = s
        self.i = i
        self.t = t

    @staticmethod
    def _evaluate(
        v_ed: N,
        s: MM3,
        i: MM4,
        t: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed=v_ed, s=s)
        raise_if_less_or_equal_to_zero(i=i, t=t)

        return (v_ed * s) / (i * t)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.25."""
        _equation: str = r"\frac{V_{Ed} \cdot S}{I \cdot t}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
                r"S": f"{self.s:.{n}f}",
                r"I": f"{self.i:.{n}f}",
                r" t": f" {self.t:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
