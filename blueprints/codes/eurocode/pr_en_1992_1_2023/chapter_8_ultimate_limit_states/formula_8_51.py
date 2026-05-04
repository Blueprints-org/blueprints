"""Formula 8.51 from prEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""


from blueprints.codes.eurocode.pr_en_1992_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot51TensileChordForceDueToShear(Formula):
    r"""Class representing formula 8.51 for the calculation of the tensile cord force due to shear."""

    label = "8.51"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
            self,
            m_ed: NMM,
            z: MM,
            n_vd: N,
            n_ed: N,
    ) -> None:
        r"""[$F_{td}$] Calculation of tensile chord force due to shear[$N$].

        prEN 1992-1-1:2023 art.8.2.3 (8) - Formula (8.51)

        Parameters
        ----------
        m_ed : NMM
            [$M_{Ed}$] Design bending moment [$Nmm$].
        z : MM
            [$z$] Internal lever arm [$mm$].
        n_vd : N
            [$N_{Vd}$] Additional tensile axial force due to shear [$N$].
        n_ed : N
            [$N_{Ed}$] Design axial force [$N$].
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

        return m_ed / z + (n_vd + n_ed) / 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.51."""
        _equation: str = r"\frac{M_{Ed}}{z} + \frac{N_{Vd} + N_{Ed}}{2}"
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
                r"M_{Ed}": rf"{self.m_ed:.3f} \ Nmm",
                r"z": rf"{self.z:.3f} \ mm",
                r"N_{Vd}": rf"{self.n_vd:.3f} \ N",
                r"N_{Ed}": rf"{self.n_ed:.3f} \ N",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"F_{td}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )
