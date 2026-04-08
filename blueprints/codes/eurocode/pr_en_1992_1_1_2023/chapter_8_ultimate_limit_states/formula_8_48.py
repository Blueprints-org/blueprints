"""Formula 8.48 from prEN 1992-1-1:2023: Chapter 8 - Ultimate Limit States."""

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot48StrainCompressionChordInCompression(Formula):
    r"""Class representing formula 8.48 for the calculation of [$\varepsilon_{xc}$].

    Strain of the compression chord if the flexural compression chord is in compression, where the following may be
    assumed unless more refined methods are used.
    [$\epsilon_{xc} = \frac{-F_{cd}}{A_{cc} \cdot E_{c}}$]
    """

    label = "8.48"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        f_cd: N,
        a_cc: MM2,
        e_c: MPA,
    ) -> None:
        r"""[$\varepsilon_{xc}$] Strain in the compression chord if the flexural compression chord is in compression [$-$].

        prEN 1992-1-1:2023 art.8 - Formula (8.48)

        Parameters
        ----------
        f_cd : N
            [$F_{cd}$] Force in the flexural compression chord [$N$].
        a_cc : MM2
            [$A_{cc}$] Area of the compression chord [$mm^2$].
        e_c : MPA
            [$E_c$] Modulus of elasticity of concrete [$MPa$].
        """
        super().__init__()
        self.f_cd = f_cd
        self.a_cc = a_cc
        self.e_c = e_c

    @staticmethod
    def _evaluate(
        f_cd: N,
        a_cc: MM2,
        e_c: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_cd=f_cd)
        raise_if_less_or_equal_to_zero(a_cc=a_cc, e_c=e_c)

        return -f_cd / (a_cc * e_c)

    def latex(self, n: int = 4) -> LatexFormula:
        """Returns LatexFormula object for formula 8.48."""
        _equation: str = r"\frac{-F_{cd}}{A_{cc} \cdot E_c}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"F_{cd}": f"{self.f_cd:.{n}f}",
                r"A_{cc}": f"{self.a_cc:.{n}f}",
                r"E_c": f"{self.e_c:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"F_{cd}": rf"{self.f_cd:.{n}f} \ N",
                r"A_{cc}": rf"{self.a_cc:.{n}f} \ mm^2",
                r"E_c": rf"{self.e_c:.{n}f} \ MPa",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"\varepsilon_{xc}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
