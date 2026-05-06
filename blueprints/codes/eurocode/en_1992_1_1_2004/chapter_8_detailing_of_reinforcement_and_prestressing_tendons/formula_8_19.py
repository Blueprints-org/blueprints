"""Formula 8.19 from EN 1992-1-1:2004: Chapter 8 - Detailing of Reinforcement and Prestressing Tendons."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot19DispersionLength(Formula):
    """Class representing formula 8.19 for the calculation of dispersion length [$l_{disp}$]."""

    label = "8.19"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        l_pt: M,
        d: M,
    ) -> None:
        r"""[$l_{disp}$] Dispersion length for prestressing tendons [$m$].

        EN 1992-1-1:2004 art.8.10.2.2(4) - Formula (8.19)

        Parameters
        ----------
        l_pt : M
            [$l_{disp}$] Length of prestressing tendon [$m$].
        d : M
            [$d$] Diameter of the tendon [$m$].
        """
        super().__init__()
        self.l_pt = l_pt
        self.d = d

    @staticmethod
    def _evaluate(
        l_pt: DIMENSIONLESS,
        d: M,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(l_pt=l_pt, d=d)
        return (l_pt**2 + d**2) ** 0.5

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.19."""
        _equation: str = r"\sqrt{l_{pt}^2 + d^2}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"l_{pt}": f"{self.l_pt:.{n}f}",
                r"d": f"{self.d:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"l_{pt}": rf"({self.l_pt:.{n}f} \ m)",
                r"d": rf"({self.d:.{n}f} \ m)",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"l_{disp}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="m",
        )

