"""Formula 8.52 from prEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot52CompressiveChordForceDueToShear(Formula):
    r"""Class representing formula 8.52 for the calculation of the compressive chord force due to shear."""

    label = "8.52"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        m_ed: NMM,
        z: MM,
        n_vd: N,
        n_ed: N,
    ) -> None:
        r"""[$F_{cd}$] Calculation of the compressive chord force due to shear [$N$].

        prEN 1992-1-1:2023 art 8.2.3 (8) - Formula (8.52)

        Parameters
        ----------
        m_ed : NMM
            [$M_{Ed}$] Design moment at the section [$Nmm$].
        z : MM
            [$z$] Lever arm [$mm$].
        n_vd : N
            [$N_{Vd}$] Additional tensile axial force due to shear [$N$].
        n_ed : N
            [$N_{Ed}$] Axial force in the section [$N$].
        """
        super().__init__()
        self.m_ed = m_ed
        self.z = z
        self.n_vd = n_vd
        self.n_ed = n_ed

    @staticmethod
    def _evaluate(
        m_ed: NMM,
        z: MM,
        n_vd: N,
        n_ed: N,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(z=z)
        raise_if_negative(m_ed=m_ed, n_vd=n_vd, n_ed=n_ed)

        return m_ed / z - (n_vd + n_ed) / 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.52."""
        _equation: str = r"\frac{M_{Ed}}{z} - \frac{N_{Vd} + N_{Ed}}{2}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"M_{Ed}": f"{self.m_ed:.{n}f}",
                r"z": f"{self.z:.{n}f}",
                r"N_{Vd}": f"{self.n_vd:.{n}f}",
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"M_{Ed}": rf"{self.m_ed:.{n}f} \ Nmm",
                r"z": rf"{self.z:.{n}f} \ mm",
                r"N_{Vd}": rf"{self.n_vd:.{n}f} \ N",
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"F_{cd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )
