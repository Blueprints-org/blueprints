"""Formula 6.4 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, NMM, N
from blueprints.validations import raise_if_negative


class Form6Dot4AxialCompression(Formula):
    r"""Class representing formula 6.4 for the calculation of additional moment [$\Delta M_{Ed}$]."""

    label = "6.4"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        n_ed: N,
        e_n: MM,
    ) -> None:
        r"""[$\Delta M_{Ed}$] Calculation of the additional moment [$Nmm$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.2.5(4) - Formula (6.4)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Axial compression force [$N$].
        e_n : MM
            [$e_{N}$] Shift of the centroid of the effective area relative to the centre of gravity of the gross cross section [$mm$].
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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.4."""
        _equation: str = r"N_{Ed} \cdot e_{N}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.3f}",
                r"e_{N}": f"{self.e_n:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\Delta M_{Ed}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="Nmm",
        )
