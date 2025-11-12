"""Formula 5.13N from EN 1992-1-1:2004: Chapter 5 Structural Analysis."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, KNM, MM2, MPA, N
from blueprints.validations import EqualToZeroError, raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot13nSlendernessCriterionIsolatedMembers(Formula):
    """Class representing formula 5.13N for the calculation of the slenderness limit where second order effects may be ignored."""

    label = "5.13N"
    source_document = EN_1992_1_1_2004

    def __init__(self, a: DIMENSIONLESS, b: DIMENSIONLESS, c: DIMENSIONLESS, n_ed: N, a_c: MM2, f_cd: MPA) -> None:
        """[$λ_{lim}$] Calculation of the slenderness limit, where second order effects may be ignored (dimensionless).

        Note:
        The value of [$λ_{lim}$] for use in a Country may be found in its National Annex. The recommended value
        follows from this equation.

        EN 1992-1-1:2004 art.5.8.3.1 (1) - formula (5.13N)

        Parameters
        ----------
        a : DIMENSIONLESS
            [$A$] calculation value, based on the effective creep ratio [$-$].
            Follows from equation 5.13A. If unknown, A = 0,7.
            Use your own implementation of this value or use the `SubForm5Dot13aCreepRatio` class.
        b : DIMENSIONLESS
            [$B$] calculation value, based on the mechanical reinforcement ratio [$-$].
            Follows from equation 5.13B. If unknown, B = 1,1.
            Use your own implementation of this value or use the `SubForm5Dot13bMechanicalReinforcementFactor` class.
        c : DIMENSIONLESS
            [$C$] calculation value, based on the moment ratio [$-$].
            Follows from equation 5.13C. If unknown, C = 0,7.
            Use your own implementation of this value or use the `SubForm5Dot13cMomentRatio` class.
        n_ed : N
            [$N_{Ed}$] is the design value of the axial force [$N$].
        a_c : MM2
            [$A_c$] is the area of the concrete section [$mm^2$].
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
        return (20 * a * b * c) / np.sqrt(n)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13N."""
        _equation: str = r"\frac{20 \cdot A \cdot B \cdot C}{\sqrt{N_{Ed} \cdot A_c \cdot f_{cd}}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_c": f"{self.a_c:.{n}f}",
                r"A": f"{self.a:.{n}f}",
                r"B": f"{self.b:.{n}f}",
                r"C": f"{self.c:.{n}f}",
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            True,
        )

        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A_c": rf"{self.a_c:.{n}f} \ mm^2",
                r"A": f"{self.a:.{n}f}",
                r"B": f"{self.b:.{n}f}",
                r"C": f"{self.c:.{n}f}",
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
            },
        )
        return LatexFormula(
            return_symbol=r"\lambda_{lim}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


class SubForm5Dot13aCreepRatio(Formula):
    r"""Class representing sub-formula for [$A$] in formula (5.13N)."""

    label = "5.13"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        phi_ef: DIMENSIONLESS,
    ) -> None:
        r"""[$A$] Calculation of the factor [$A$] in formula (5.13N).

        EN 1992-1-1:2004 art.5.8.3.1 (1) - formula (5.13N)

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

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13a."""
        _equation: str = r"\frac{1}{(1 + 0.2 \cdot \phi_{ef})}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\phi_{ef}": f"{self.phi_ef:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )


class SubForm5Dot13bMechanicalReinforcementFactor(Formula):
    r"""Class representing sub-formula for [$B$] in formula (5.13N)."""

    label = "5.13"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        a_s: MM2,
        f_yd: MPA,
        a_c: MM2,
        f_cd: MPA,
    ) -> None:
        r"""[$B$] Calculation of the factor [$B$] in formula (5.13N).

        EN 1992-1-1:2004 art.5.8.3.1 (1) - formula (5.13N)

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

        mechanical_reinforcement_ratio = (a_s * f_yd) / (a_c * f_cd)
        return np.sqrt(1 + 2 * mechanical_reinforcement_ratio)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13b."""
        _equation: str = r"\sqrt{1 + 2 \cdot \frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_s": f"{self.a_s:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
                r"A_c": f"{self.a_c:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A_s": rf"{self.a_s:.{n}f} \ mm^2",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
                r"A_c": rf"{self.a_c:.{n}f} \ mm^2",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"B",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


class SubForm5Dot13cMomentRatio(Formula):
    r"""Class representing sub-formula for [$C$] in formula (5.13N)."""

    label = "5.13c"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        m_01: KNM,
        m_02: KNM,
    ) -> None:
        r"""[$C$] Calculation of the factor [$C$] in formula (5.13N).

        EN 1992-1-1:2004 art.5.8.3.1 (1) - formula (5.13)

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
        if m_02 == 0.0:
            raise EqualToZeroError(value_name="m_02", value=m_02)

        if not abs(m_02) >= abs(m_01):
            raise ValueError("The absolute value of M_02 must be equal to or larger than the absolute value of M_01.")

        return 1.7 - (m_01 / m_02)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13b."""
        _equation: str = r"1.7 - \frac{M_{01}}{M_{02}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"M_{01}": f"{self.m_01:.{n}f}",
                r"M_{02}": f"{self.m_02:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"M_{01}": rf"{self.m_01:.{n}f} \ kNm",
                r"M_{02}": rf"{self.m_02:.{n}f} \ kNm",
            },
        )
        return LatexFormula(
            return_symbol=r"C",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
