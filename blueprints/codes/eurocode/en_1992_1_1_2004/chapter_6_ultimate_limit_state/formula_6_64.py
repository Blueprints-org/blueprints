"""Formula 6.64 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot64BondFactor(Formula):
    r"""Class representing formula 6.64 for the calculation of [$\eta$]."""

    label = "6.64"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        a_s: MM2,
        a_p: MM2,
        xi: DIMENSIONLESS,
        d_s: MM,
        d_p: MM,
    ) -> None:
        r"""[$\eta$] Calculation of [$\eta$].

        EN 1992-1-1:2004 art.6.8.2(2) - Formula (6.64)

        Parameters
        ----------
        a_s : MM2
            [$A_s$] Area of reinforcing steel [$mm^2$].
        a_p : MM2
            [$A_P$] Area of prestressing tendon or tendons [$mm^2$].
        xi : DIMENSIONLESS
            [$\xi$] ratio of bond strength between bonded tendons and ribbed steel in concrete. The value is subject to the
            relevant European Technical Approval. In the absence of this the values given in Table 6.2 may be used. [-].
        d_s : MM
            [$⌀_s$] Largest diameter of reinforcement [$mm$].
        d_p : MM
            [$⌀_P$] Diameter or equivalent diameter of prestressing steel [$mm$].
            $⌀_P = 1.6 \cdot \sqrt{A_P}$ for bundles
            $⌀_P = 1.75 \cdot ⌀_wire}$ for single 7 wire strands where $⌀_wire$ is the wire diameter
            $⌀_P = 1.20 \cdot ⌀_wire}$ for single 3 wire strands where $⌀_wire$ is the wire diameter
        """
        super().__init__()
        self.a_s = a_s
        self.a_p = a_p
        self.xi = xi
        self.d_s = d_s
        self.d_p = d_p

    @staticmethod
    def _evaluate(
        a_s: MM2,
        a_p: MM2,
        xi: DIMENSIONLESS,
        d_s: MM,
        d_p: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_s=a_s, a_p=a_p, xi=xi, d_s=d_s)
        raise_if_less_or_equal_to_zero(d_p=d_p)

        return (a_s + a_p) / (a_s + a_p * np.sqrt(xi * d_s / d_p))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.64."""
        _equation: str = r"\frac{A_s + A_P}{A_s + A_P \cdot \sqrt{\xi \cdot ⌀_s / ⌀_P}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_s": f"{self.a_s:.{n}f}",
                r"A_P": f"{self.a_p:.{n}f}",
                r"\xi": f"{self.xi:.{n}f}",
                r"⌀_s": f"{self.d_s:.{n}f}",
                r"⌀_P": f"{self.d_p:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\eta",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
