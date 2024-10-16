"""Contains formula 2.22 from CUR 228."""

from blueprints.codes.cur.cur_228 import CUR_228
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN_M3, KPA, M


class Form2Dot22ModulusHorizontalSubgrade(Formula):
    """Representation of equation 2.22 CUR 228."""

    source_document = CUR_228
    label = "2.22"

    def __init__(self, r: M, e_p: KPA, alpha: float) -> None:
        """Calculates the modulus of horizontal subgrade reaction (k_h) using Menard stiffness for r < 0.3 m.

        Parameters
        ----------
        r: M
            The radius of a foundation pile [m]:
            r >= 0.3 m
        e_p: KPA
            Elastic modulus of Ménard [kPa]:
            e_p ≈ beta * q_c
                beta: float
                    Dependent on soil type [-]:
                q_c: KPA
                    Cone resistance [kPa]
        alpha: float
            Factor dependent on soil type [-]:
        """
        super().__init__()
        self.r = r
        self.e_p = e_p
        self.alpha = alpha

    @staticmethod
    def _evaluate(r: M, e_p: KPA, alpha: float) -> KN_M3:
        """Return the Menard stiffness k_h when r < 0.3 m [kN/m3]."""
        if r < 0.3:
            return e_p / 2 / r / ((4 * 2.65**alpha + 3 * alpha) / 18)
        msg = "Radius is equal to- or larger than 0.3m, use: Eq2Dot21ModulusHorizontalSubgrade"
        raise ValueError(msg)

    def latex(self, n_decimals: int = 2) -> LatexFormula:
        """Latex representation of the full equation including result.

        Parameters
        ----------
        n_decimals: int
            Number of decimals to round the result to

        Returns
        -------
        LatexFormula
            Latex representation of the equation

        """
        n = n_decimals
        return LatexFormula(
            return_symbol=r"k_{h}",
            result=f"{self:.{n}f} kN/m3",
            equation=r"\frac{2 \cdot R}{E_{p}} \cdot \frac{4 \cdot 2.65^{\alpha} + 3 \alpha}{18}",
            numeric_equation=rf"\frac{{2 \cdot {self.r :.{n}f}}}{{{self.e_p :.{n}f}}} \cdot \frac{{4 \cdot 2.65^{{{self.alpha :.{n}f}}} + 3 \cdot "
            rf"{self.alpha :.{n}f}}}{{18}}",
            unit="kN/m^3",
        )
