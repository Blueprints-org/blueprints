"""Formula 5.13N from NEN-EN 1992-1-1 C2:2011: Chapter 5 Structural Analysis."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, KNM, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot13nSlendernessCriterionIsolatedMembers(Formula):
    """Class representing formula 5.13N for the calculation of the slenderness limit where second order effects may be ignored."""

    label = "5.13N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, a: DIMENSIONLESS, b: DIMENSIONLESS, c: DIMENSIONLESS, n_ed: N, a_c: MM2, f_cd: MPA) -> None:
        """[$λ_{lim}$] Calculation of the slenderness limit, where second order effects may be ignored (dimensionless).

        Note:
        The value of [$λ_{lim}$] for use in a Country may be found in its National Annex. The recommended value
        follows from this equation.

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.1 (1) - formula (5.13N)

        Parameters
        ----------
        a : DIMENSIONLESS
            [$A$] calculation value, based on the effective creep ratio. Follows from equation 5.13A. If unknown, A = 0,7.

        b : DIMENSIONLESS
            [$B$] calculation value, based on the mechanical reinforcement ratio. Follows from equation 5.13B. If unknown, B = 1,1.

        c : DIMENSIONLESS
            [$C$] calculation value, based on the moment ratio. Follows from equation 5.13C. If unknown, C = 0,7.

        n_ed : N
            [$N_{Ed}$] is the design value of the axial force [$N$].

        a_c : MM2
            [$A_c$] is the area of concrete section [$mm^2$].

        f_cd :
            [$f_{cd}$] is the design value of concrete compressive strength [$MPa$].
        """
        super().__init__()
        self.a = a
        self.b = b
        self.c = c
        self.n_ed = n_ed
        self.a_c = a_c
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(a: DIMENSIONLESS, b: DIMENSIONLESS, c: DIMENSIONLESS, n_ed: N, a_c: MM2, f_cd: MPA) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b=b, c=c)
        raise_if_less_or_equal_to_zero(a_c=a_c, f_cd=f_cd, n_ed=n_ed)

        n = n_ed / (a_c * f_cd)
        return 20 * a * b * c * np.sqrt(n)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13N."""
        _equation: str = r"20 \cdot A \cdot B \cdot C \cdot \sqrt{\frac{N_{Ed}}{A_c \cdot f_{cd}}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_c": f"{self.a_c:.3f}",
                r"A": f"{self.a:.3f}",
                r"B": f"{self.b:.3f}",
                r"C": f"{self.c:.3f}",
                r"N_{Ed}": f"{self.n_ed:.3f}",
                r"f_{cd}": f"{self.f_cd:.3f}",
            },
            True,
        )

        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A_c": rf"{self.a_c:.3f} \ mm^2",
                r"A": f"{self.a:.3f}",
                r"B": f"{self.b:.3f}",
                r"C": f"{self.c:.3f}",
                r"N_{Ed}": rf"{self.n_ed:.3f} \ N",
                r"f_{cd}": rf"{self.f_cd:.3f} \ MPa",
            },
        )
        return LatexFormula(
            return_symbol=r"\lambda_{lim}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


class Form5Dot13aCreepFactor(Formula):
    r"""Class representing formula 5.13a for [$A$] in formula (5.13N)."""

    label = "5.13a"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        phi_ef: DIMENSIONLESS,
    ) -> None:
        r"""[$A$] Calculation of the factor [$A$] in formula (5.13N).

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.1 (1) - formula (5.13a)

        Parameters
        ----------
        phi_ef : DIMENSIONLESS
            [$\phi_{ef}$] Effective creep ratio; see 5.8.4 (If [$\phi_{ef}$] is not known, A = 0.7)
        """
        super().__init__()
        self.phi_ef = phi_ef

    @staticmethod
    def _evaluate(
        phi_ef: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(phi_ef=phi_ef)

        return 1 / (1 + 0.2 * phi_ef)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13a."""
        _equation: str = r"\frac{1}{(1 + 0.2 \cdot \phi_{ef})}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\phi_{ef}": f"{self.phi_ef:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )


class Form5Dot13bMechanicalReinforcementFactor(Formula):
    r"""Class representing formula 5.13b for [$B$] in formula (5.13N)."""

    label = "5.13b"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_s: MM2,
        f_yd: MPA,
        a_c: MM2,
        f_cd: MPA,
    ) -> None:
        r"""[$B$] Calculation of the factor [$B$] in formula (5.13N).

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.1 (1) - formula (5.13b)

        Parameters
        ----------
        a_s : MM2
            [$A_s$] is the total area of longitudinal reinforcement [$mm^2$].

        f_yd : MPA
            [$f_{yd}$] is the design yield stress of the reinforcement [$MPa$].

        a_c : MM2
            [$A_c$] is the area of concrete section [$mm^2$].

        f_cd : MPA
            [$f_{cd}$] is the design value of concrete compressive strength [$MPa$].
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

        return (a_s * f_yd) / (a_c * f_cd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13b."""
        _equation: str = r"\frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_s": f"{self.a_s:.3f}",
                r"f_{yd}": f"{self.f_yd:.3f}",
                r"A_c": f"{self.a_c:.3f}",
                r"f_{cd}": f"{self.f_cd:.3f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A_s": rf"{self.a_s:.3f} \ mm^2",
                r"f_{yd}": rf"{self.f_yd:.3f} \ MPa",
                r"A_c": rf"{self.a_c:.3f} \ mm^2",
                r"f_{cd}": rf"{self.f_cd:.3f} \ MPa",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"B",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


class Form5Dot13cMomentFactor(Formula):
    r"""Class representing formula 5.13c for [$C$] in formula (5.13N)."""

    label = "5.13c"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        m_01: KNM,
        m_02: KNM,
    ) -> None:
        r"""[$C$] Calculation of the factor [$C$] in formula (5.13N).

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.1 (1) - formula (5.13b)

        Parameters
        ----------
        m_01 : KNM
            [$M_{01}$] is one of the first order end moments [$kNm$].

        m_02 : KNM
            [$M_{02}$] is one of the first order end moments [$kNm$].
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
        raise_if_negative(m_01=m_01)
        raise_if_less_or_equal_to_zero(m_02=m_02)

        return m_01 / m_02

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13b."""
        _equation: str = r"\frac{M_{01}}{M_{02}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"M_{01}": f"{self.m_01:.3f}",
                r"M_{02}": f"{self.m_02:.3f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"M_{01}": rf"{self.m_01:.3f} \ kNm",
                r"M_{02}": rf"{self.m_02:.3f} \ kNm",
            },
        )
        return LatexFormula(
            return_symbol=r"C",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
