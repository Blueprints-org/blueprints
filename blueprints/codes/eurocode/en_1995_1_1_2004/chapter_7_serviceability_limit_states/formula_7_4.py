"""Formula 7.4 from EN 1995-1-1:2004."""

from blueprints.codes.eurocode.en_1995_1_1_2004 import EN_1995_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, HZ, M_NS2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot4VelocityResponseLimit(Formula):
    r"""Class representing formula 7.4 for the calculation of the upper limit of the velocity response of a unit impulse load."""

    label = "7.4"
    source_document = EN_1995_1_1_2004

    # Constants for validation
    b_50 = 50
    b_150 = 150

    def __init__(self, b: DIMENSIONLESS, f_1: HZ, ksi: DIMENSIONLESS) -> None:
        r"""[v_{limit}] Upper limit of the velocity response of a unit impulse load, in [$m/(Ns^2)$].

        EN 1995-1-1:2004 art 7.3.3(2) - Formula (7.4)

        Parameters
        ----------
        f_1 : HZ
            [$f_{1}$] Natural frequency of rectangular floor, laid freely on all four sides [$Hz$].
        b : DIMENSIONLESS
            [$b$] Dimensionless factor, taken as 120 in the Dutch National Annex [$-$].
        ksi : DIMENSIONLESS
            [$\xi$] Modal damping factor [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.f_1 = f_1
        self.ksi = ksi
        self.b = b

    @staticmethod
    def _evaluate(b: DIMENSIONLESS, f_1: HZ, ksi: DIMENSIONLESS) -> M_NS2:
        """Evaluate the formula, for more information see the __init__ method."""
        if b < Form7Dot4VelocityResponseLimit.b_50 or b > Form7Dot4VelocityResponseLimit.b_150:
            raise ValueError(
                "b must be at least 50 and no less than 150 (For the Netherlands b must be exactly 120 according to Dutch National Annex)."
            )
        raise_if_less_or_equal_to_zero(f_1=f_1)
        raise_if_negative(ksi=ksi)
        return b ** (f_1 * ksi - 1)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.4."""
        eq_for: str = r"b^{(f_1 \cdot \xi - 1)}"
        repl_symb = {
            "b": f"{self.b:.{n}f}",
            "f_1": f"{self.f_1:.{n}f}",
            r"\xi": f"{self.ksi:.{n}f}",
        }
        return LatexFormula(
            return_symbol=r"v_{lim}",
            result=f"{self:.{n}f}",
            equation=eq_for,
            numeric_equation=latex_replace_symbols(eq_for, repl_symb),
        )
