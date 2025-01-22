"""Formula 5.13N from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

import math
from typing import Optional

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot13NSlendernessCriterion(Formula):
    """Class representing formula 5.13N for the calculation of slenderness criterion for individual elements."""

    label = "5.13N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, phi_eff: float, omega: DIMENSIONLESS, rm: DIMENSIONLESS, n: DIMENSIONLESS) -> None:
        r"""[:math:`\lambda_{lim}`] Slenderness limit for individual elements.

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.1(1) - Formula (5.13N)

        Parameters
        ----------
        phi_eff : float
            Effective creep coefficient.
        omega : SubFormOmegaMechanicalReinforcementRatio
            Mechanical reinforcement ratio.
        rm : SubFormRmMomentRatio
            Moment ratio.
        n : SubFormNRelativeNormalForce
            Relative normal force.
        """
        super().__init__()
        self.phi_eff = phi_eff
        self.omega = omega
        self.rm = rm
        self.n = n

    @staticmethod
    def calculate_a(phi_eff: Optional[float]) -> float:
        """Calculate A based on phi_eff."""
        if phi_eff is None:
            return 0.7
        return 1 / (1 + 0.2 * phi_eff)

    @staticmethod
    def calculate_b(omega: Optional[float]) -> float:
        """Calculate B based on omega."""
        if omega is None:
            return 1.1
        return omega

    @staticmethod
    def calculate_c(rm: Optional[float]) -> float:
        """Calculate C based on rm."""
        if rm is None:
            return 0.7
        return 1.7 - rm

    @staticmethod
    def _evaluate(phi_eff: DIMENSIONLESS, omega: DIMENSIONLESS, rm: DIMENSIONLESS, n: DIMENSIONLESS) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(phi_eff=phi_eff, omega=omega, rm=rm, n=n)
        raise_if_less_or_equal_to_zero(n=n)

        a = Form5Dot13NSlendernessCriterion.calculate_a(phi_eff)
        b = Form5Dot13NSlendernessCriterion.calculate_b(omega)
        c = Form5Dot13NSlendernessCriterion.calculate_c(rm)

        return 20 * a * b * c / math.sqrt(n)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13N."""
        a = self.calculate_a(self.phi_eff)
        b = self.calculate_b(self.omega)
        c = self.calculate_c(self.rm)

        return LatexFormula(
            return_symbol=r"\lambda_{lim}",
            result=f"{self:.3f}",
            equation=r"20 \cdot A \cdot B \cdot C / \sqrt{n}",
            numeric_equation=rf"20 \cdot {a} \cdot {b} \cdot {c} / \sqrt{{{self.n}}}",
            comparison_operator_label="=",
        )


class SubForm5Dot13NOmegaMechanicalReinforcementRatio(Formula):
    """Class representing sub-formula for the calculation of the mechanical reinforcement ratio (ω)."""

    label = "5.13N_ω"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, a_s: MM2, fyd: MPA, a_c: MM2, fcd: MPA) -> None:
        r"""[:math:`\omega`] Mechanical reinforcement ratio.

        Parameters
        ----------
        a_s : MM2
            Total area of the cross-section of the longitudinal reinforcement [:math:`mm^2`].
        fyd : MPA
            Design yield strength of the reinforcement [:math:`MPa`].
        a_c : MM2
            Area of concrete cross-section [:math:`mm^2`].
        fcd : MPA
            Design compressive strength of concrete [:math:`MPa`].
        """
        super().__init__()
        self.a_s = a_s
        self.fyd = fyd
        self.a_c = a_c
        self.fcd = fcd

    @staticmethod
    def _evaluate(a_s: MM2, fyd: MPA, a_c: MM2, fcd: MPA) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_s=a_s, fyd=fyd, a_c=a_c, fcd=fcd)
        raise_if_less_or_equal_to_zero(ratio=a_c * fcd)

        return (a_s * fyd) / (a_c * fcd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for the sub-formula ω."""
        return LatexFormula(
            return_symbol=r"\omega",
            result=f"{self:.3f}",
            equation=r"\frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}}",
            numeric_equation=rf"\frac{{{self.a_s} \cdot {self.fyd}}}{{{self.a_c} \cdot {self.fcd}}}",
            comparison_operator_label="=",
        )


class SubForm5Dot13NRelativeNormalForce(Formula):
    """Class representing sub-formula for the calculation of the relative normal force (n)."""

    label = "5.13N_n"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, n_ed: KN, a_c: MM2, fcd: MPA) -> None:
        """[:math:`n`] Relative normal force.

        Parameters
        ----------
        n_ed : KN
            Design value of axial force [:math:`kN`].
        a_c : MM2
            Area of concrete cross-section [:math:`mm^2`].
        fcd : MPA
            Design compressive strength of concrete [:math:`MPa`].
        """
        super().__init__()
        self.n_ed = n_ed
        self.a_c = a_c
        self.fcd = fcd

    @staticmethod
    def _evaluate(n_ed: KN, a_c: MM2, fcd: MPA) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(n_ed=n_ed, a_c=a_c, fcd=fcd)

        return n_ed / (a_c * fcd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for the sub-formula n."""
        return LatexFormula(
            return_symbol=r"n",
            result=f"{self:.3f}",
            equation=r"\frac{N_{Ed}}{A_c \cdot f_{cd}}",
            numeric_equation=rf"\frac{{{self.n_ed}}}{{{self.a_c} \cdot {self.fcd}}}",
            comparison_operator_label="=",
        )


class SubForm5Dot13NRmMomentRatio(Formula):
    """Class representing sub-formula for the calculation of the moment ratio (rm)."""

    label = "rm"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, m_01: float, m_02: float) -> None:
        """[:math:`rm`] Moment ratio.

        Parameters
        ----------
        m_01 : float
            First-order end moment [:math:`kNm`].
        m_02 : float
            Second-order end moment [:math:`kNm`].
        """
        super().__init__()
        self.m_01 = m_01
        self.m_02 = m_02

    @staticmethod
    def _evaluate(m_01: float, m_02: float) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(m_01=m_01, m_02=m_02)

        return m_01 / m_02

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for the sub-formula rm."""
        return LatexFormula(
            return_symbol=r"rm",
            result=f"{self:.3f}",
            equation=r"\frac{M_{01}}{M_{02}}",
            numeric_equation=rf"\frac{{{self.m_01}}}{{{self.m_02}}}",
            comparison_operator_label="=",
        )
