"""Formula 7.1 from EN 1992-1-1:2004: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot1MinReinforcingSteel(Formula):
    r"""Class representing formula 7.1 for the calculation of [$A_{s,min}$]."""

    label = "7.1"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        k_c: DIMENSIONLESS,
        k: DIMENSIONLESS,
        f_ct_eff: MPA,
        a_ct: MM2,
        sigma_s: MPA,
    ) -> None:
        r"""[$A_{s,min}$] Calculation of minimum area of reinforcing steel within the tensile zone.

        EN 1992-1-1:2004 art.7.3.2(2) - Formula (7.1)

        Parameters
        ----------
        k_c : DIMENSIONLESS
            [$k_c$] Coefficient which takes account of the stress distribution within the section immediately
            prior to cracking and of the change of the lever arm. For pure tension use 1.0, else use equation 7.2 or 7.3 [$-$].
        k : DIMENSIONLESS
            [$k$] Coefficient which allows for the effect of non-uniform self-equilibrating stresses, which lead to a
            reduction of restraint forces [$-$].
        f_ct_eff : MPA
            [$f_{ct,eff}$] Mean value of the tensile strength of the concrete effective at the time when the cracks may
            first be expected to occur [$MPa$].
        a_ct : MM2
            [$A_{ct}$] Area of concrete within the tensile zone [$mm^2$].
        sigma_s : MPA
            [$\sigma_s$] Absolute value of the maximum stress permitted in the reinforcement immediately after formation
            of the crack [$MPa$].
        """
        super().__init__()
        self.k_c = k_c
        self.k = k
        self.f_ct_eff = f_ct_eff
        self.a_ct = a_ct
        self.sigma_s = sigma_s

    @staticmethod
    def _evaluate(
        k_c: DIMENSIONLESS,
        k: DIMENSIONLESS,
        f_ct_eff: MPA,
        a_ct: MM2,
        sigma_s: MPA,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(k_c=k_c, k=k, f_ct_eff=f_ct_eff, a_ct=a_ct)
        raise_if_less_or_equal_to_zero(sigma_s=sigma_s)

        return (k_c * k * f_ct_eff * a_ct) / sigma_s

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.1."""
        _equation: str = r"\frac{k_c \cdot k \cdot f_{ct,eff} \cdot A_{ct}}{\sigma_s}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"k_c": f"{self.k_c:.{n}f}",
                r"k": f"{self.k:.{n}f}",
                r"f_{ct,eff}": f"{self.f_ct_eff:.{n}f}",
                r"A_{ct}": f"{self.a_ct:.{n}f}",
                r"\sigma_s": f"{self.sigma_s:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_{s,min}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )
