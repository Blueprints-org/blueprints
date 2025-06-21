"""Formula 7.7n from EN 1992-1-1:2004: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot7nMaxBarDiameterTension(Formula):
    r"""Class representing formula 7.7n for the calculation of [$⌀_s$]."""

    label = "7.7n"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        diam_s_star: MM,
        f_ct_eff: MPA,
        h_cr: MM,
        h: MM,
        d: MM,
    ) -> None:
        r"""[$⌀_s$] Calculation of the maximum bar diameter for tension [$mm$].

        EN 1992-1-1:2004 art.7.3.3(2) - Formula (7.7n)

        Parameters
        ----------
        diam_s_star : MM
            [$⌀^*_s$] Maximum bar size given in the Table 7.2N [$mm$].
        f_ct_eff : MPA
            [$f_{ct,eff}$] Mean value of the tensile strength of the concrete effective at the time
            when the cracks may first be expected to occur [$MPa$].
        h_cr : MM
            [$h_{cr}$] Depth of the tensile zone immediately prior to cracking, considering the characteristic values
            of prestress and axial forces under the quasi-permanent combination of actions [$mm$].
        h : MM
            [$h$] Overall depth of the section [$mm$].
        d : MM
            [$d$] Effective depth to the centroid of the outer layer of reinforcement [$mm$].
        """
        super().__init__()
        self.diam_s_star = diam_s_star
        self.f_ct_eff = f_ct_eff
        self.h_cr = h_cr
        self.h = h
        self.d = d

    @staticmethod
    def _evaluate(
        diam_s_star: MM,
        f_ct_eff: MPA,
        h_cr: MM,
        h: MM,
        d: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(diam_s_star=diam_s_star, f_ct_eff=f_ct_eff, h_cr=h_cr, h=h, d=d)
        denominator: MM = 2 * (h - d)
        raise_if_less_or_equal_to_zero(denominator=denominator)

        return diam_s_star * (f_ct_eff / 2.9) * (h_cr) / (8 * (h - d))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.7n."""
        _equation: str = r"⌀^*_s \cdot \left(\frac{f_{ct,eff}}{2.9}\right) \cdot \left(\frac{h_{cr}}{8 \cdot ( h - d)}\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"⌀^*_s": f"{self.diam_s_star:.{n}f}",
                r"f_{ct,eff}": f"{self.f_ct_eff:.{n}f}",
                r"h_{cr}": f"{self.h_cr:.{n}f}",
                r" h": f" {self.h:.{n}f}",
                r" d": f" {self.d:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"⌀_s",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm",
        )
