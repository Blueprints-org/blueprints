"""Formula 7.16a/b from NEN-EN 1992-1-1+C2:2011: Chapter 7 - Serviceability limit state."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot16abSpanDepthRatio(Formula):
    r"""Class representing formula 7.16a/b for the calculation of the limit span/depth ratio."""

    label = "7.16a/b"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        capital_k: DIMENSIONLESS,
        f_ck: MPA,
        rho: DIMENSIONLESS,
        rho_0: DIMENSIONLESS,
        rho_prime: DIMENSIONLESS,
    ) -> None:
        r"""[$\frac{l}{d}$] Limit span/depth ratio [-].

        NEN-EN 1992-1-1+C2:2011 art.7.4.2(2) - Formula (7.16a and 7.16b)

        Parameters
        ----------
        capital_k : DIMENSIONLESS
            [$K$] Factor to take into account the different structural systems [-].
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        rho : DIMENSIONLESS
            [$\rho$] Required tension reinforcement ratio at mid-span to resist the moment
            due to the design loads (at support for cantilevers) [-].
        rho_0 : DIMENSIONLESS
            [$\rho_0$] Reference reinforcement ratio [$\sqrt{f_{ck}} \cdot 10^{-3}$] [-].
        rho_prime : DIMENSIONLESS
            [$\rho'$] Required compression reinforcement ratio at mid-span to resist the moment
            due to design loads (at support for cantilevers) [-].
        """
        super().__init__()
        self.capital_k = capital_k
        self.f_ck = f_ck
        self.rho = rho
        self.rho_0 = rho_0
        self.rho_prime = rho_prime

    @staticmethod
    def _evaluate(
        capital_k: DIMENSIONLESS,
        f_ck: MPA,
        rho: DIMENSIONLESS,
        rho_0: DIMENSIONLESS,
        rho_prime: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(capital_k=capital_k, f_ck=f_ck, rho=rho, rho_0=rho_0, rho_prime=rho_prime)
        raise_if_less_or_equal_to_zero(rho=rho)

        if rho <= rho_0:
            l_over_d = capital_k * (11 + 1.5 * np.sqrt(f_ck) * rho_0 / rho + 3.2 * np.sqrt(f_ck) * (rho_0 / rho - 1) ** 1.5)
        else:
            l_over_d = capital_k * (11 + 1.5 * np.sqrt(f_ck) * rho_0 / (rho - rho_prime) + 1 / 12 * np.sqrt(f_ck) * np.sqrt(rho_prime / rho_0))

        return l_over_d

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 7.16a/b."""
        _equation: str = (
            r"\begin{cases} K \cdot \left(11 + 1.5 \cdot \sqrt{f_{ck}} \cdot \frac{\rho_0}{\rho} + "
            r"3.2 \cdot \sqrt{f_{ck}} \cdot \left(\frac{\rho_0}{\rho} - 1\right)^{3/2}\right) & \text{if } \rho \leq \rho_0 \\ "
            r"K \cdot \left(11 + 1.5 \cdot \sqrt{f_{ck}} \cdot \frac{\rho_0}{\rho - \rho'} + "
            r"\frac{1}{12} \cdot \sqrt{f_{ck}} \cdot \sqrt{\frac{\rho'}{\rho_0}}\right) & \text{if } \rho > \rho_0 \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"K": f"{self.capital_k:.3f}",
                r"f_{ck}": f"{self.f_ck:.3f}",
                r"\rho_0": f"{self.rho_0:.4f}",
                r"\rho'": f"{self.rho_prime:.4f}",
                r"\rho": f"{self.rho:.4f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\frac{l}{d}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
