"""Formula 6.20 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM3, MM4, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot20TauEd(Formula):
    r"""Class representing formula 6.20 for the calculation of [$\tau_{Ed}$]."""

    label = "6.20"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        v_ed: N,
        s: MM3,
        i: MM4,
        t: MM,
    ) -> None:
        r"""[$\tau_{Ed}$] Calculation of the design elastic shear stress [$MPa$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.6(4) - Formula (6.20)

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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.20."""
        _equation: str = r"\frac{V_{Ed} \cdot S}{I \cdot t}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"V_{Ed}": f"{self.v_ed:.3f}",
                r"S": f"{self.s:.3f}",
                r"I": f"{self.i:.3f}",
                r" t": f" {self.t:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Ed}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
