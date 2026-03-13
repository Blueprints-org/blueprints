"""Formula 7.6 from EN 1995-1-1:2004."""

from blueprints.codes.eurocode.en_1995_1_1_2004 import EN_1995_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import HZ, KG_M2, M_NS2, M
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form7Dot6VelocityResponse(Formula):
    r"""Class representing formula 7.6 for the calculation of velocity response [$v$] of a unit impulse load."""

    label = "7.6"
    source_document = EN_1995_1_1_2004

    def __init__(self, n_40: HZ, m: KG_M2, length: M, b: M) -> None:
        r"""[$v$] The velocity response of a unit impulse load, in [$m/(Ns^2)$].

        EN 1995-1-1:2004 art 7.3.3(5) - Formula (7.6)

        Parameters
        ----------
        n_40 : HZ
            [$n_{40}$] Number of first-order vibrations with a natural frequency less than 40 Hz [$Hz$].
        m : KG_M2
            [$m$] Mass per unit area [$kg/m^{2}$].
        length : M
            [$l$] Span of the floor [$m$].
        b : M
            [$b$] Width of the floor [$m$].

        Returns
        -------
        None
        """
        super().__init__()
        self.n_40 = n_40
        self.m = m
        self.length = length
        self.b = b

    @staticmethod
    def _evaluate(n_40: HZ, m: KG_M2, length: M, b: M) -> M_NS2:
        """Evaluate the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_40=n_40, m=m, length=length, b=b)
        return 4 * (0.4 + 0.6 * n_40) / (m * b * length + 200)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 7.6."""
        eq_form: str = r"\frac{4 \cdot (0.4 + 0.6 \cdot n_{40})}{m \cdot b \cdot l + 200}"
        repl_symb = {"n_{40}": f"{self.n_40:.{n}f}", "m": f"{self.m:.{n}f}", "l": f"{self.length:.{n}f}", "b": f"{self.b:.{n}f}"}
        return LatexFormula(
            return_symbol=r"v",
            result=f"{self:.{n + 1}f}",
            equation=eq_form,
            numeric_equation=latex_replace_symbols(eq_form, repl_symb),
            comparison_operator_label="=",
        )
