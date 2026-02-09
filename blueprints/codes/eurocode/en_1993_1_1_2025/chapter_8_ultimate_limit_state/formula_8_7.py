"""Formula 8.7 from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, NMM, N
from blueprints.validations import raise_if_negative


class Form8Dot7AdditionalMoment(Formula):
    r"""Class representing formula 8.7 for the calculation of additional moment [$\Delta M_{Ed}$]."""

    label = "8.7"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        n_ed: N,
        e_n: MM,
    ) -> None:
        r"""[$\Delta M_{Ed}$] Calculation of the additional moment [$Nmm$].

        EN 1993-1-1:2025 art.8.2.2.5(3) - Formula (8.7)
        Where a class 4 cross section is subjected to an axial compression force, the method given in EN 1993-1-5 should be used to
        determine the possible shift [$e_{N}$] of the centroid of the effective area [$A_{eff}$] relative to the centre of gravity
        of the gross cross section and the resulting additional moment according to this formula.

        Note: The sign of the additional moment depends on the effect in the combination of internal forces and moments, see 8.2.9.3(2).

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Axial compression force [$N$].
        e_n : MM
            [$e_{N}$] Shift of the centroid of the effective area relative to the centre of gravity of the gross cross section [$mm$].
            The method given in EN 1993-1-5 should be used to determine the possible shift [$e_{N}$] of the centroid of the effective
            area [$A_{eff$] relative to the centre of gravity of the gross cross section.
        """
        super().__init__()
        self.n_ed = n_ed
        self.e_n = e_n

    @staticmethod
    def _evaluate(
        n_ed: N,
        e_n: MM,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(n_ed=n_ed, e_n=e_n)

        return n_ed * e_n

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.7."""
        _equation: str = r"N_{Ed} \cdot e_{N}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"e_{N}": f"{self.e_n:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\Delta M_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="Nmm",
        )
