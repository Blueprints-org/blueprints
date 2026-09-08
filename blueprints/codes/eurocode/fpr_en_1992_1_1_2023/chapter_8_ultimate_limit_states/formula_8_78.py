"""Formula 8.78 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2_MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot78MinimumInterfaceReinforcementAlongEdge(Formula):
    r"""Class representing formula 8.78 for the minimum interface reinforcement per unit length along the edge of a
    composite slab.

    It applies along edges of composite slabs where delamination of the topping cannot be prevented by permanent
    loads, for example from walls.

    The result is an area per unit length, so the lower case [$a_{s,min}$] of the standard rather than an area
    [$A_s$]. With the thickness in millimetres and both strengths in megapascal the result is in [$mm^2/mm$].
    """

    label = "8.78"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        t_min: MM,
        f_ctm: MPA,
        f_yk: MPA,
    ) -> None:
        r"""[$a_{s,min}$] Minimum interface reinforcement per unit length along the edge [$mm^2/mm$].

        FprEN 1992-1-1:2023 (E) art. 8.2.6(9) - Formula (8.78)

        Parameters
        ----------
        t_min : MM
            [$t_{min}$] Smaller value of the thickness of new and old concrete layer [$mm$].
        f_ctm : MPA
            [$f_{ctm}$] Mean tensile strength of respective concrete layer [$MPa$].
        f_yk : MPA
            [$f_{yk}$] Characteristic yield strength of the interface reinforcement. The standard does not list it
            under this formula; it is the characteristic value, not the design value [$f_{yd}$] used in Formulas
            (8.76) and (8.77) [$MPa$].
        """
        super().__init__()
        self.t_min = t_min
        self.f_ctm = f_ctm
        self.f_yk = f_yk

    @staticmethod
    def _evaluate(
        t_min: MM,
        f_ctm: MPA,
        f_yk: MPA,
    ) -> MM2_MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(t_min=t_min, f_ctm=f_ctm)
        raise_if_less_or_equal_to_zero(f_yk=f_yk)

        return t_min * f_ctm / f_yk

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.78."""
        _equation: str = r"\frac{t_{min} \cdot f_{ctm}}{f_{yk}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"t_{min}": f"{self.t_min:.{n}f}",
                r"f_{ctm}": f"{self.f_ctm:.{n}f}",
                r"f_{yk}": f"{self.f_yk:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"t_{min}": rf"{self.t_min:.{n}f} \ mm",
                r"f_{ctm}": rf"{self.f_ctm:.{n}f} \ MPa",
                r"f_{yk}": rf"{self.f_yk:.{n}f} \ MPa",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"a_{s,min}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm^2/mm",
        )
