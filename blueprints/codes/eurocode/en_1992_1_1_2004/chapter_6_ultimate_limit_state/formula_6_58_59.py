"""Formula 6.58 and 6.59 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot58And59TensileForce(Formula):
    r"""Class representing formula 6.58 and 6.59 for the calculation of the tensile force [$T$]."""

    label = "6.58/6.59"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f: N,
        a: MM,
        b: MM,
        capital_h: MM,
    ) -> None:
        r"""[$T$] Tensile force [$N$].

        EN 1992-1-1:2004 art.6.5.3(3) - Formula (6.58 and 6.59)

        Parameters
        ----------
        f : N
            [$F$] Applied force [$N$].
        a : MM
            [$a$] Width of the concentrated force [$mm$].
        b : MM
            [$b$] Width of the locally widened section [$mm$].
        capital_h : MM
            [$H$] Height of the widened section. Also used to calculate h: $h=H/2$ [$mm$].
        """
        super().__init__()
        self.f = f
        self.a = a
        self.b = b
        self.capital_h = capital_h

    @staticmethod
    def _evaluate(
        f: N,
        a: MM,
        b: MM,
        capital_h: MM,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f=f, a=a)
        raise_if_less_or_equal_to_zero(b=b, capital_h=capital_h)

        # calculate h from capital_h with Figure 6.25b
        h = capital_h / 2
        if b <= capital_h / 2:
            return 1 / 4 * (b - a) / b * f
        return 1 / 4 * (1 - 0.7 * a / h) * f

    def latex(self, n: int = 3) -> LatexFormula:
        r"""Returns LatexFormula object for formula 6.58/6.59."""
        _equation: str = (
            r"\begin{cases} \frac{1}{4} \cdot \frac{ b - a}{ b} \cdot F & \text{if } b \leq "
            r"\frac{H}{2} \\ \frac{1}{4} \cdot \left(1 - 0.7 \cdot \frac{ a}{\frac{H}{2}}\right) "
            r"\cdot F & \text{if } b > \frac{H}{2} \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "F": f"{self.f:.{n}f}",
                " a": f" {self.a:.{n}f}",
                " b": f" {self.b:.{n}f}",
                "H": f"{self.capital_h:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"T",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
