"""Contains formula 2.21 from CUR 228."""

from blueprints.codes.cur.cur_228 import CUR_228, R_0
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN_M3, KPA, M
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form2Dot21ModulusHorizontalSubgrade(Formula):
    """Representation of equation 2.21 CUR 228."""

    source_document = CUR_228
    label = "2.21"
    n_decimals: int = 2

    def __init__(self, r: M, e_p: KPA, alpha: DIMENSIONLESS) -> None:
        """Calculates the modulus of horizontal subgrade reaction (k_h) using Menard stiffness for r >= 0.3 m.

        Parameters
        ----------
        r: M
            The radius of a foundation pile [m]:
            r >= 0.3 m
        e_p: KPA
            Elastic modulus of Ménard [kPa]:
            e_p ≈ beta * q_c
            beta: DIMENSIONLESS
                Dependent on soil type [-]: (table 2.1)
            q_c: KPA
                Cone resistance [kPa]
        alpha: DIMENSIONLESS
            Factor dependent on soil type [-]: (table 2.1)
        """
        super().__init__()
        self.r = float(r)
        self.e_p = float(e_p)
        self.alpha = float(alpha)

    @staticmethod
    def _evaluate(r: M, e_p: KPA, alpha: DIMENSIONLESS) -> KN_M3:
        """Evaluates the formula, for more information see the __init__ method."""
        r_0 = R_0
        raise_if_negative(e_p=e_p)
        raise_if_less_or_equal_to_zero(r=r, alpha=alpha)

        if r >= r_0:
            return 3 * e_p / (1.3 * r_0 * (2.65 * r / r_0) ** alpha + alpha * r)
        msg = "Radius is smaller than 0.3m, use: Eq2Dot21ModulusHorizontalSubgrade"
        raise ValueError(msg)

    def latex(self, n: int = 3) -> LatexFormula:
        """Latex representation of the full equation including result.

        Parameters
        ----------
        n: int
            Number of decimals to round the result to

        Returns
        -------
        LatexFormula
            Latex representation of the equation

        """
        n = self.n_decimals

        return LatexFormula(
            return_symbol="k_{h}",
            equation=r"\frac{1}{3 \cdot E_{p}} \cdot "
            r"\left[1.3 \cdot R_{0} "
            r"\left( 2.65 \frac{R}{R_0}\right)^\alpha"
            r" + \alpha \cdot  R \right]",
            numeric_equation=rf"\frac{{1}}{{3 \cdot {self.e_p:.{n}}}} \cdot"
            rf"\left[1.3 \cdot {R_0:.{n}} "
            rf"\left( 2.65 \cdot \frac{{{self.r:.{n}}}}{{{R_0:.{n}}}}\right)^{{{self.alpha:.{n}f}}}"
            rf"+ {self.alpha:.{n}} \cdot {self.r:.{n}}\right]",
            result=f"{self:.{n}f}",
            unit="kN/m^3",
        )
