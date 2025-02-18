"""Formula 9.14 from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailing and specific rules."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, MM
from blueprints.validations import raise_if_negative


class Form9Dot14SplittingForceColumnOnRock(Formula):
    """Class representing the formula 9.14 for the calculation of the splitting force on a column footing on rock."""

    label = "9.14"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c: MM,
        h: MM,
        n_ed: KN,
    ) -> None:
        r"""[$F_s$] Splitting force on a column footing on rock [$kN$].

        NEN-EN 1992-1-1+C2:2011 art.9.8.4(2) - Formula (9.14)

        Parameters
        ----------
        c: MM
            [$c$] Width over which [$N_{Ed}$] is applied [$mm$].
        h: MM
            [$h$] Lesser of [$b$] and [$H$] from figure 9.14 [$mm$].
        n_ed: KN
            [$N_{Ed}$] Design value of the applied axial force [$kN$].
        """
        super().__init__()
        self.c = c
        self.h = h
        self.n_ed = n_ed

    @staticmethod
    def _evaluate(
        c: MM,
        h: MM,
        n_ed: KN,
    ) -> KN:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(c=c, h=h, n_ed=n_ed)
        return 0.25 * (1 - (c / h)) * n_ed

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 9.14."""
        return LatexFormula(
            return_symbol=r"F_s",
            result=f"{self:.2f}",
            equation=r"0.25 \cdot ( 1 - c / h ) \cdot N_{Ed}",
            numeric_equation=rf"0.25 \cdot ( 1 - {self.c:.2f} / {self.h:.2f} ) \cdot {self.n_ed:.2f}",
            comparison_operator_label="=",
        )
