"""Formula 8.126 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import operator
from collections.abc import Callable

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot126CheckPartiallyLoadedAreaResistance(ComparisonFormula):
    r"""Class representing formula 8.126 for the verification of the design resistance of a partially loaded
    area.
    """

    label = "8.126"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, f_cd: MPA, a_c1: MM2, a_c0: MM2, nu_part: DIMENSIONLESS) -> None:
        r"""Verify the design resistance of a partially loaded area.

        FprEN 1992-1-1:2023 (E) art 8.6 (2) - Formula (8.126)

        Parameters
        ----------
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        a_c1 : MM2
            [$A_{c1}$] Contributing concrete area according to Formula (8.129), see
            Form8Dot129ContributingConcreteArea [$mm^2$].
        a_c0 : MM2
            [$A_{c0}$] Loaded area according to Formula (8.127) or (8.128), see
            Form8Dot127ConcentricallyLoadedArea or Form8Dot128EccentricallyLoadedArea [$mm^2$].
        nu_part : DIMENSIONLESS
            [$\nu_{part}$] Confinement factor. A value of 3,0 may be adopted unless larger resistance can be
            justified based on refined analysis including tensile stresses due to load or restraint,
            where relevant [$-$].
        """
        super().__init__()
        self.f_cd = f_cd
        self.a_c1 = a_c1
        self.a_c0 = a_c0
        self.nu_part = nu_part

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(f_cd: MPA, a_c1: MM2, a_c0: MM2, *_args, **_kwargs) -> float:
        """Evaluates the design resistance, for more information see the __init__ method."""
        raise_if_negative(f_cd=f_cd, a_c1=a_c1)
        raise_if_less_or_equal_to_zero(a_c0=a_c0)

        return float(f_cd * np.sqrt(a_c1 / a_c0))

    @staticmethod
    def _evaluate_rhs(f_cd: MPA, nu_part: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the limit on the design resistance, for more information see the __init__ method."""
        raise_if_negative(f_cd=f_cd, nu_part=nu_part)

        return float(nu_part * f_cd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.126."""
        _equation: str = r"\sigma_{Rdu} = f_{cd} \cdot \sqrt{\frac{A_{c1}}{A_{c0}}} \leq \nu_{part} \cdot f_{cd}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\sigma_{Rdu}": f"{self.lhs:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
                r"A_{c1}": f"{self.a_c1:.{n}f}",
                r"A_{c0}": f"{self.a_c0:.{n}f}",
                r"\nu_{part}": f"{self.nu_part:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\sigma_{Rdu}": rf"{self.lhs:.{n}f} \ MPa",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
                r"A_{c1}": rf"{self.a_c1:.{n}f} \ mm^2",
                r"A_{c0}": rf"{self.a_c0:.{n}f} \ mm^2",
                r"\nu_{part}": f"{self.nu_part:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )
