"""Formula 8.47 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot47StrainTensionChord(Formula):
    r"""Class representing formula 8.47 for the calculation of [$\epsilon_{xt}$].

    Strain of the tension chord where the following may be assumed unless more refined methods are used.
    [$\epsilon_{xt} = \frac{F_{td}}{A_{st} \cdot E_{s}}$]
    """

    label = "8.47"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        f_td: N,
        a_st: MM2,
        e_s: MPA,
    ) -> None:
        r"""Strain of the tension chord (dimensionless).

        prEN 1992-1-1:2023 art. 8.2.3 (7) - Formula (8.47)

        Parameters
        ----------
        f_td : N
            [$F_{td}$] Design value of the axial force in the tension chord [$N$].
        a_st : MM2
            [$A_{st}$] Area of the longitudinal reinforcement in the tension chord [$mm^2$].
        e_s : MPA
            [$E_s$] Modulus of elasticity of reinforcement steel [$MPa$].
        """
        super().__init__()
        self.f_td = f_td
        self.a_st = a_st
        self.e_s = e_s

    @staticmethod
    def _evaluate(
        f_td: N,
        a_st: MM2,
        e_s: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_td=f_td)
        raise_if_less_or_equal_to_zero(a_st=a_st, e_s=e_s)

        return f_td / (a_st * e_s)

    def latex(self, n: int = 4) -> LatexFormula:
        """Returns LatexFormula object for formula 8.47."""
        _equation: str = r"\frac{F_{td}}{A_{st} \cdot E_s}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"F_{td}": f"{self.f_td:.{n}f}",
                r"A_{st}": f"{self.a_st:.{n}f}",
                r"E_s": f"{self.e_s:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"F_{td}": rf"{self.f_td:.{n}f} \ N",
                r"A_{st}": rf"{self.a_st:.{n}f} \ mm^2",
                r"E_s": rf"{self.e_s:.{n}f} \ MPa",
            },
            True,
        )

        return LatexFormula(
            return_symbol=r"\epsilon_{xt}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="",
        )
