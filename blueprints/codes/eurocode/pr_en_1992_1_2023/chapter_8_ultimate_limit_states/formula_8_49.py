"""Formula 8.49 from prEN 1992-1-2:2023: Chapter 8 - Ultimate Limit States."""

from blueprints.codes.eurocode.pr_en_1992_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot49StrainCompressionChordInTension(Formula):
    r"""Class representing formula 8.49 for the calculation of [$\varepsilon_{xc}$].

    Strain of the compression chord if the flexural compression chord is in tension.
    [$\epsilon_{xc} = \frac{|F_{cd}|}{A_{sc} \cdot E_{s}}$]
    """

    label = "8.49"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        f_cd: N,
        a_sc: MM2,
        e_s: MPA,
    ) -> None:
        r"""[$\varepsilon_{xc}$] Strain in the compression chord if the flexural compression chord is in tension [$-$].

        prEN 1992-1-2:2023 art.8 - Formula (8.49)

        Parameters
        ----------
        f_cd : N
            [$F_{cd}$] Force in the flexural compression chord [$N$].
        a_sc : MM2
            [$A_{sc}$] Area of the compression chord [$mm^2$].
        e_s : MPA
            [$E_s$] Modulus of elasticity of reinforcement steel [$MPa$].
        """
        super().__init__()
        self.f_cd = f_cd
        self.a_sc = a_sc
        self.e_s = e_s

    @staticmethod
    def _evaluate(
        f_cd: N,
        a_sc: MM2,
        e_s: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(a_sc=a_sc, e_s=e_s)

        return abs(f_cd) / (a_sc * e_s)

    def latex(self, n: int = 4) -> LatexFormula:
        """Returns LatexFormula object for formula 8.49."""
        _equation: str = r"\frac{|F_{cd}|}{A_{sc} \cdot E_s}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"|F_{cd}|": f"{abs(self.f_cd):.{n}f}",
                r"A_{sc}": f"{self.a_sc:.{n}f}",
                r"E_s": f"{self.e_s:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"|F_{cd}|": rf"{abs(self.f_cd):.{n}f} \ N",
                r"A_{sc}": rf"{self.a_sc:.{n}f} \ mm^2",
                r"E_s": rf"{self.e_s:.{n}f} \ MPa",
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
