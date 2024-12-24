"""Formula 5.13N from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KNM, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot13NLimitSlenderness(Formula):
    r"""Class representing formula 5.13N for the calculation of the slenderness limit, :math:`\lambda_{lim}`."""

    label = "5.13N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a: DIMENSIONLESS,
        b: DIMENSIONLESS,
        c: DIMENSIONLESS,
        n: DIMENSIONLESS,
    ) -> None:
        r"""[:math:`\lambda_{lim}`] Slenderness limit [:math:`-`].

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.1(1) - Formula (5.13N)

        Parameters
        ----------
        a : DIMENSIONLESS
            [:math:`A`] Dimensionless factor for effective creep ratio.
        b : DIMENSIONLESS
            [:math:`B`] Dimensionless factor for mechanical reinforcement ratio.
        c : DIMENSIONLESS
            [:math:`C`] Dimensionless factor for moment ratio.
        n : DIMENSIONLESS
            [:math:`n`] Dimensionless factor for relative normal force.
        """
        super().__init__()
        self.a = a
        self.b = b
        self.c = c
        self.n = n

    @staticmethod
    def _evaluate(
        a: float,
        b: float,
        c: float,
        n: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            a=a,
            b=b,
            c=c,
        )
        raise_if_less_or_equal_to_zero(n=n)

        return 20 * a * b * c / (n**0.5)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13N."""
        return LatexFormula(
            return_symbol=r"\lambda_{lim}",
            result=f"{self:.3f}",
            equation=r"20 \cdot A \cdot B \cdot C / \sqrt{n}",
            numeric_equation=rf"20 \cdot {self.a:.3f} \cdot {self.b:.3f} \cdot {self.c:.3f} / \sqrt{{{self.n:.3f}}}",
            comparison_operator_label="=",
            unit="-",
        )


class Form5Dot13NSub1FactorForEffectiveCreepRatio(Formula):
    r"""Class representing formula 5.13Nsub1 for the calculation of the effective creep ratio, :math:`A`."""

    label = "5.13Nsub1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        phi_ef: DIMENSIONLESS,
    ) -> None:
        r"""[:math:`A`] factor for effective creep ratio [:math:`-`].

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.1(1) - Formula (5.13Nsub1)

        Parameters
        ----------
        phi_ef : DIMENSIONLESS
            [:math:`\phi_{ef}`] Effective creep ratio.
        """
        super().__init__()
        self.phi_ef = phi_ef

    @staticmethod
    def _evaluate(
        phi_ef: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            phi_ef=phi_ef,
        )

        return 1 / (1 + 0.2 * phi_ef)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13Nsub1."""
        return LatexFormula(
            return_symbol=r"A",
            result=f"{self:.3f}",
            equation=r"1 / (1 + 0.2 \cdot \phi_{ef})",
            numeric_equation=rf"1 / (1 + 0.2 \cdot {self.phi_ef:.3f})",
            comparison_operator_label="=",
            unit="-",
        )


class Form5Dot13NSub2FactorForMechanicalReinforcementRatio(Formula):
    r"""Class representing formula 5.13Nsub2 for the calculation of the factor for the
    mechanical reinforcement ratio, :math:`B`.
    """

    label = "5.13Nsub2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_s: MM2,
        f_yd: MPA,
        a_c: MM2,
        f_cd: MPA,
    ) -> None:
        r"""[:math:`B`] factor for mechanical reinforcement ratio [:math:`-`].

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.1(2) - Formula (5.13Nsub2)

        Parameters
        ----------
        a_s : MM2
            [:math:`A_s`] Area of reinforcement [:math:`mm^2`].
        f_yd : MPA
            [:math:`f_{yd}`] Design yield strength of reinforcement [:math:`MPa`].
        a_c : MM2
            [:math:`A_c`] Area of concrete [:math=`mm^2`].
        f_cd : MPA
            [:math=`f_{cd}`] Design compressive strength of concrete [:math=`MPa`].
        """
        super().__init__()
        self.a_s = a_s
        self.f_yd = f_yd
        self.a_c = a_c
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        a_s: MM2,
        f_yd: MPA,
        a_c: MM2,
        f_cd: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_s=a_s, f_yd=f_yd)
        raise_if_less_or_equal_to_zero(a_c=a_c, f_cd=f_cd)

        return (1 + 2 * (a_s * f_yd) / (a_c * f_cd)) ** 0.5

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13Nsub2."""
        return LatexFormula(
            return_symbol=r"B",
            result=f"{self:.3f}",
            equation=r"\sqrt{1 + 2 \cdot \frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}}}",
            numeric_equation=rf"\sqrt{{1 + 2 \cdot \frac{{{self.a_s:.3f} \cdot {self.f_yd:.3f}}}{{{self.a_c:.3f} " rf"\cdot {self.f_cd:.3f}}}}}",
            comparison_operator_label="=",
            unit="-",
        )


class Form5Dot13NSub3FactorForMomentRatio(Formula):
    r"""Class representing formula 5.13Nsub3 for the calculation of the factor for moment ratio, :math:`C`."""

    label = "5.13Nsub3"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        m_01: KNM,
        m_02: KNM,
    ) -> None:
        r"""[:math:`C`] factor for moment ratio [:math=`-`].

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.1(3) - Formula (5.13Nsub3)

        Parameters
        ----------
        m_01 : KNM
            [:math=`M_{01}`] Bending moment at end 1 (the absolute smaller value) [:math=`kNm`].
        m_02 : KNM
            [:math=`M_{02}`] Bending moment at end 2 (the absolute larger value) [:math=`kNm`].
        """
        super().__init__()
        self.m_01 = m_01
        self.m_02 = m_02

    @staticmethod
    def _evaluate(
        m_01: KNM,
        m_02: KNM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(m_01=m_01, m_02=m_02)

        if m_01 > m_02:
            raise ValueError("m_01 should be less than or equal to m_02")

        # the formula is not defined for m_02 == 0, but the spirit of the formula is to return 1.7
        if m_02 == 0:
            return 1.7

        return 1.7 - (m_01 / m_02)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13Nsub3."""
        return LatexFormula(
            return_symbol=r"C",
            result=f"{self:.3f}",
            equation=r"1.7 - \frac{M_{01}}{M_{02}}",
            numeric_equation=rf"1.7 - \frac{{{self.m_01:.3f}}}{{{self.m_02:.3f}}}",
            comparison_operator_label="=",
            unit="-",
        )
