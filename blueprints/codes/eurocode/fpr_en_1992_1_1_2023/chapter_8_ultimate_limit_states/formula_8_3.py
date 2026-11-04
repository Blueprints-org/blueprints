"""Formula 8.3 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM2, MPA, N
from blueprints.validations import raise_if_negative


class Form8Dot3AxialResistanceWithoutMoment(Formula):
    r"""Class representing formula 8.3 for the calculation of the design value of axial resistance under
    compression without accompanying moments.
    """

    label = "8.3"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        a_c: MM2,
        f_cd: MPA,
        a_s: MM2,
        f_yd: MPA,
    ) -> None:
        r"""[$N_{Rd,0}$] Design value of axial resistance under compression without accompanying moments [$N$].

        FprEN 1992-1-1:2023 (E) art. 8.1.1(8) - Formula (8.3)

        In case of members with confinement reinforcement, [$f_{cd}$] should be replaced by [$f_{cd,c}$]
        according to Formula (8.15).

        Parameters
        ----------
        a_c : MM2
            [$A_c$] Cross-sectional area of the concrete [$mm^2$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        a_s : MM2
            [$A_s$] Cross-sectional area of the reinforcement [$mm^2$].
        f_yd : MPA
            [$f_{yd}$] Design value of the yield strength of the reinforcement [$MPa$].
        """
        super().__init__()
        self.a_c = a_c
        self.f_cd = f_cd
        self.a_s = a_s
        self.f_yd = f_yd

    @staticmethod
    def _evaluate(
        a_c: MM2,
        f_cd: MPA,
        a_s: MM2,
        f_yd: MPA,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_c=a_c, f_cd=f_cd, a_s=a_s, f_yd=f_yd)

        return a_c * f_cd + a_s * f_yd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.3."""
        _equation: str = r"A_c \cdot f_{cd} + A_s \cdot f_{yd}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_c": f"{self.a_c:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
                r"A_s": f"{self.a_s:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_c": rf"{self.a_c:.{n}f} \ mm^2",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
                r"A_s": rf"{self.a_s:.{n}f} \ mm^2",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"N_{Rd,0}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )
