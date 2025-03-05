"""Formula 6.78 and 6.79 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, N
from blueprints.validations import raise_if_negative


class Form6Dot78And79FatigueResistance(Formula):
    r"""Class representing formula 6.78 and 6.79 for the calculation of the fatigue resistance."""

    label = "6.78/6.79"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        v_ed_max: N,
        v_ed_min: N,
        v_rd_c: N,
        f_ck: DIMENSIONLESS,
    ) -> None:
        r"""[$\sigma_{Rd,max}$] Fatigue resistance check [$-$].

        NEN-EN 1992-1-1+C2:2011 art.6.8.7(4) - Formula (6.78 and 6.79)

        Parameters
        ----------
        v_ed_max : N
            [$V_{Ed,max}$] Design value of the maximum applied shear force under frequent load combination [$N$].
        v_ed_min : N
            [$V_{Ed,min}$] Design value of the minimum applied shear force under frequent load combination
            in the cross-section where [$V_{Ed,max}$] occurs [$N$].
        v_rd_c : N
            [$V_{Rd,c}$] Design value for shear-resistance according to Expression (6.2.a) [$N$].
        f_ck : DIMENSIONLESS
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.v_ed_max = v_ed_max
        self.v_ed_min = v_ed_min
        self.v_rd_c = v_rd_c
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        v_ed_max: N,
        v_ed_min: N,
        v_rd_c: N,
        f_ck: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ck=f_ck, v_rd_c=v_rd_c)

        abs_v_ed_max = abs(v_ed_max)
        abs_v_ed_min = abs(v_ed_min)
        abs_v_rd_c = abs(v_rd_c)

        # the spirit of the equation in the Eurocode is to differentiate between the two cases, not to throw an error
        v_ed_max_non_zero = 1e-12 if v_ed_max == 0 else v_ed_max

        if v_ed_min / v_ed_max_non_zero >= 0:
            output = abs_v_ed_max / abs_v_rd_c <= min(0.5 + 0.45 * abs_v_ed_min / abs_v_rd_c, 0.9 if f_ck <= 50 else 0.8)
        else:
            output = abs_v_ed_max / abs_v_rd_c <= 0.5 - abs_v_ed_min / abs_v_rd_c

        return output

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.78/6.79."""
        _equation: str = (
            r"\begin{cases} \frac{\left|V_{Ed,max}\right|}{\left|V_{Rd,c}\right|} \leq "
            r"\min\left(0.5 + 0.45 \cdot \frac{\left|V_{Ed,min}\right|}{\left|V_{Rd,c}\right|}, "
            r"\begin{cases} 0.9 & \text{if } f_{ck} \le 50 \\ 0.8 & \text{if } f_{ck} > 50 \end{cases} \right) & \text{if } "
            r"\frac{V_{Ed,min}}{V_{Ed,max}} \geq 0 \\ \frac{\left|V_{Ed,max}\right|}{\left|V_{Rd,c}\right|} \leq 0.5 - "
            r"\frac{\left|V_{Ed,min}\right|}{\left|V_{Rd,c}\right|} & "
            r"\text{if } \frac{V_{Ed,min}}{V_{Ed,max}} < 0 \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "V_{Ed,max}": f"{self.v_ed_max:.3f}",
                "V_{Ed,min}": f"{self.v_ed_min:.3f}",
                "V_{Rd,c}": f"{self.v_rd_c:.3f}",
                "f_{ck}": f"{self.f_ck:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
