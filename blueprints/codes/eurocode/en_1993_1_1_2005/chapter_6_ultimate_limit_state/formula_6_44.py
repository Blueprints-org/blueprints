"""Formula 6.44 from EN 1993-1-1:2005: Chapter 6 - Ultimate limit state."""

import operator
from collections.abc import Callable
from typing import Any

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MM3, MPA, NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form6Dot44CombinedCompressionBendingClass4CrossSections(ComparisonFormula):
    r"""Class representing formula 6.44 for Class 4 cross-sections."""

    label = "6.44"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        n_ed: N,
        a_eff: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        m_y_ed: NMM,
        e_ny: MM,
        w_eff_y_min: MM3,
        m_z_ed: NMM,
        e_nz: MM,
        w_eff_z_min: MM3,
    ) -> None:
        r"""Combined compression and bending check for Class 4 cross-sections.
        The combined utilization from axial force and bending moments should not exceed unity.

        EN 1993-1-1:2005 art. 6.2.9.3 (2) - Formula (6.44)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design value of the axial force [$N$].
        a_eff : MM2
            [$A_{eff}$] Effective area of the cross-section when subjected to uniform compression [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for resistance of cross-sections [-].
        m_y_ed : NMM
            [$M_{y,Ed}$] Design value of the bending moment about the y-axis [$Nmm$].
        e_ny : MM
            [$e_{Ny}$] Shift of the centroidal y-axis when the cross-section is subjected to compression only [$mm$].
        w_eff_y_min : MM3
            [$W_{eff,y,min}$] Effective section modulus (corresponding to the fibre with the maximum elastic stress) about the y-axis [$mm^3$].
        m_z_ed : NMM
            [$M_{z,Ed}$] Design value of the bending moment about the z-axis [$Nmm$].
        e_nz : MM
            [$e_{Nz}$] Shift of the centroidal z-axis when the cross-section is subjected to compression only [$mm$].
        w_eff_z_min : MM3
            [$W_{eff,z,min}$] Effective section modulus (corresponding to the fibre with the maximum elastic stress) about the z-axis [$mm^3$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.a_eff = a_eff
        self.f_y = f_y
        self.gamma_m0 = gamma_m0
        self.m_y_ed = m_y_ed
        self.e_ny = e_ny
        self.w_eff_y_min = w_eff_y_min
        self.m_z_ed = m_z_ed
        self.e_nz = e_nz
        self.w_eff_z_min = w_eff_z_min

    @classmethod
    def _comparison_operator(cls) -> Callable[[Any, Any], bool]:
        """Returns the comparison operator for this formula.
        LHS should be less than or equal to RHS.
        """
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        n_ed: N,
        a_eff: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        m_y_ed: NMM,
        e_ny: MM,
        w_eff_y_min: MM3,
        m_z_ed: NMM,
        e_nz: MM,
        w_eff_z_min: MM3,
    ) -> float:
        """Evaluates the left-hand side of the comparison. see __init__ for details."""
        raise_if_less_or_equal_to_zero(a_eff=a_eff, gamma_m0=gamma_m0, w_eff_y_min=w_eff_y_min, w_eff_z_min=w_eff_z_min, f_y=f_y)

        # Calculate resistance terms
        n_rd = a_eff * f_y / gamma_m0
        m_y_rd = w_eff_y_min * f_y / gamma_m0
        m_z_rd = w_eff_z_min * f_y / gamma_m0

        # Calculate combined utilization
        return n_ed / n_rd + (m_y_ed + n_ed * e_ny) / m_y_rd + (m_z_ed + n_ed * e_nz) / m_z_rd

    @staticmethod
    def _evaluate_rhs(*_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the comparison. see __init__ for details."""
        return 1.0


    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.44."""
        _equation: str = (
            r"\frac{N_{Ed}}{A_{eff} \cdot f_y / \gamma_{M0}} + "
            r"\frac{M_{y,Ed} + N_{Ed} \cdot e_{Ny}}{W_{eff,y,min} \cdot f_y / \gamma_{M0}} + "
            r"\frac{M_{z,Ed} + N_{Ed} \cdot e_{Nz}}{W_{eff,z,min} \cdot f_y / \gamma_{M0}} \leq 1"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"A_{eff}": f"{self.a_eff:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
                r"M_{y,Ed}": f"{self.m_y_ed:.{n}f}",
                r"e_{Ny}": f"{self.e_ny:.{n}f}",
                r"W_{eff,y,min}": f"{self.w_eff_y_min:.{n}f}",
                r"M_{z,Ed}": f"{self.m_z_ed:.{n}f}",
                r"e_{Nz}": f"{self.e_nz:.{n}f}",
                r"W_{eff,z,min}": f"{self.w_eff_z_min:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"A_{eff}": rf"{self.a_eff:.{n}f} \ mm^2",
                r"f_y": rf"{self.f_y:.{n}f} \ MPa",
                r"\gamma_{M0}": rf"{self.gamma_m0:.{n}f}",
                r"M_{y,Ed}": rf"{self.m_y_ed:.{n}f} \ Nmm",
                r"e_{Ny}": rf"{self.e_ny:.{n}f} \ mm",
                r"W_{eff,y,min}": rf"{self.w_eff_y_min:.{n}f} \ mm^3",
                r"M_{z,Ed}": rf"{self.m_z_ed:.{n}f} \ Nmm",
                r"e_{Nz}": rf"{self.e_nz:.{n}f} \ mm",
                r"W_{eff,z,min}": rf"{self.w_eff_z_min:.{n}f} \ mm^3",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if bool(self) else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )
