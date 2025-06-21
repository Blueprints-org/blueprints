"""Formula 6.35 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot35CheckAxialForceZ(Formula):
    r"""Class representing formula 6.35 for checking axial force about the z-z axis."""

    label = "6.35"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        n_ed: N,
        h_w: MM,
        t_w: MM,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""For doubly symmetrical I- and H-sections, allowance need not be made for the
        effect of the axial force on the plastic resistance moment about the z-z axis when
        6.35 is satisfied.

        EN 1993-1-1:2005 art.6.2.9(4) - Formula (6.35)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design axial force [$N$].
        h_w : MM
            [$h_w$] Web height [$mm$].
        t_w : MM
            [$t_{w}$] Web thickness [$mm$].
        f_y : MPA
            [$f_{y}$] Yield strength [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor [-].
        """
        super().__init__()
        self.n_ed = n_ed
        self.h_w = h_w
        self.t_w = t_w
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @staticmethod
    def _evaluate(
        n_ed: N,
        h_w: MM,
        t_w: MM,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(h_w=h_w, t_w=t_w, f_y=f_y, gamma_m0=gamma_m0)
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0)

        return n_ed <= (h_w * t_w * f_y) / gamma_m0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.35."""
        _equation: str = r"N_{Ed} \leq \frac{h_{w} \cdot t_{w} \cdot f_{y}}{\gamma_{M0}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"h_{w}": f"{self.h_w:.{n}f}",
                r"t_{w}": f"{self.t_w:.{n}f}",
                r"f_{y}": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"h_{w}": rf"{self.h_w:.{n}f} \ mm",
                r"t_{w}": rf"{self.t_w:.{n}f} \ mm",
                r"f_{y}": rf"{self.f_y:.{n}f} \ MPa",
                r"\gamma_{M0}": rf"{self.gamma_m0:.{n}f}",
            },
            True,
        )
        return LatexFormula(
            return_symbol="CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="\\to",
            unit="",
        )
