"""Formula 8.2 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot2CheckBiaxialBending(ComparisonFormula):
    r"""Class representing formula 8.2 for the simplified verification of biaxial bending."""

    label = "8.2"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        m_edz: NMM,
        m_rdz_n: NMM,
        m_edy: NMM,
        m_rdy_n: NMM,
        a_n: DIMENSIONLESS,
    ) -> None:
        r"""Verify a cross-section for biaxial bending with a simplified criterion.

        FprEN 1992-1-1:2023 (E) art 8.1.1(8) - Formula (8.2)

        Parameters
        ----------
        m_edz : NMM
            [$M_{Edz}$] Design moment about the z axis, including a 2nd order moment. Only its magnitude is
            used, so it may be passed signed [$Nmm$].
        m_rdz_n : NMM
            [$M_{Rdz,N}$] Moment resistance about the z axis for the given axial compression force [$Nmm$].
        m_edy : NMM
            [$M_{Edy}$] Design moment about the y axis, including a 2nd order moment. Only its magnitude is
            used, so it may be passed signed [$Nmm$].
        m_rdy_n : NMM
            [$M_{Rdy,N}$] Moment resistance about the y axis for the given axial compression force [$Nmm$].
        a_n : DIMENSIONLESS
            [$a_N$] Exponent, taken as 2 for circular and elliptical cross-sections. For rectangular
            cross-sections it follows from [$\left|N_{Ed}\right|/N_{Rd,0}$] according to Formula (8.3), see
            Form8Dot3AxialResistanceWithoutMoment: 1,0 at a ratio of 0,1, 1,5 at 0,7 and 2,0 at 1,0, with
            linear interpolation for intermediate values [$-$].
        """
        super().__init__()
        self.m_edz = m_edz
        self.m_rdz_n = m_rdz_n
        self.m_edy = m_edy
        self.m_rdy_n = m_rdy_n
        self.a_n = a_n

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(m_edz: NMM, m_rdz_n: NMM, m_edy: NMM, m_rdy_n: NMM, a_n: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the biaxial bending ratio, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(m_rdz_n=m_rdz_n, m_rdy_n=m_rdy_n)

        return float((abs(m_edz) / m_rdz_n) ** a_n + (abs(m_edy) / m_rdy_n) ** a_n)

    @staticmethod
    def _evaluate_rhs(*_args, **_kwargs) -> float:
        """Evaluates the limit of the biaxial bending ratio, for more information see the __init__ method."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.2."""
        _equation: str = (
            r"\left(\frac{\left|M_{Edz}\right|}{M_{Rdz,N}}\right)^{a_N} + "
            r"\left(\frac{\left|M_{Edy}\right|}{M_{Rdy,N}}\right)^{a_N} \leq 1.0"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"M_{Edz}": f"{self.m_edz:.{n}f}",
                r"M_{Rdz,N}": f"{self.m_rdz_n:.{n}f}",
                r"M_{Edy}": f"{self.m_edy:.{n}f}",
                r"M_{Rdy,N}": f"{self.m_rdy_n:.{n}f}",
                r"a_N": f"{self.a_n:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"M_{Edz}": rf"{self.m_edz:.{n}f} \ Nmm",
                r"M_{Rdz,N}": rf"{self.m_rdz_n:.{n}f} \ Nmm",
                r"M_{Edy}": rf"{self.m_edy:.{n}f} \ Nmm",
                r"M_{Rdy,N}": rf"{self.m_rdy_n:.{n}f} \ Nmm",
                r"a_N": f"{self.a_n:.{n}f}",
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
