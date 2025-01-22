"""Formula 5.38a from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_5_2008 import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, KN, KNM, MM2, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot13SimplifiedBucklingCheck(Formula):
    """Class representing formula 5.13 for combined axial force and bending moment check."""

    label = "5.13"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        n_ed: KN,
        m_ed: KNM,
        a: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        gamma_m1: DIMENSIONLESS,
        chi: DIMENSIONLESS,
        m_c_rd: KNM,
    ) -> None:
        r"""
        Simplified buckling check.

        Provided that the boundary conditions are supplied by elements (anchor, earth support, capping beam, etc.)
        that give positional restraint corresponding to the non-sway buckling mode, this check may be used:

        Parameters
        ----------
        n_ed : KN
            [$kN$] Design axial force [$kN$].
        m_ed : KNM
            [$kNm$] Design bending moment [$kNm$].
        a : MM2
            [$mm^2$] Cross-sectional area [$mm^2$].
        f_y : MPA
            [$MPa$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_M0$] Partial factor according to 5.1.1 (4) [-].
        gamma_m1 : DIMENSIONLESS
            [$\gamma_M1$] Partial factor according to 5.1.1 (4) [-].
        chi : DIMENSIONLESS
            [$\chi$] Buckling coefficient from 6.3.1.2 of EN 1993-1-1 [-].
        m_c_rd : KNM
            [$kNm$] Design moment resistance of the cross-section [$kNm$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.m_ed = m_ed
        self.a = a
        self.f_y = f_y
        self.gamma_m0 = gamma_m0
        self.gamma_m1 = gamma_m1
        self.chi = chi
        self.m_c_rd = m_c_rd

    @staticmethod
    def _evaluate(
        n_ed: KN,
        m_ed: KNM,
        a: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        gamma_m1: DIMENSIONLESS,
        chi: DIMENSIONLESS,
        m_c_rd: KNM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            n_ed=n_ed,
            m_ed=m_ed,
        )
        raise_if_less_or_equal_to_zero(
            a=a,
            f_y=f_y,
            chi=chi,
            m_c_rd=m_c_rd,
            gamma_m0=gamma_m0,
            gamma_m1=gamma_m1,
        )
        n_pl_rd: KN = a * f_y / gamma_m0 * N_TO_KN
        return (n_ed / (chi * n_pl_rd * (gamma_m0 / gamma_m1)) + 1.15 * m_ed / (m_c_rd * (gamma_m0 / gamma_m1))) <= 1.0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.13."""
        _equation: str = (
            r"\frac{N_{Ed}}{\chi \cdot N_{pl,Rd} \cdot \left( \frac{\gamma_{M0}}{\gamma_{M1}} \right)} + "
            r"1.15 \cdot \frac{M_{Ed}}{M_{c,Rd} \cdot \left( \frac{\gamma_{M0}}{\gamma_{M1}} \right)} \leq 1.0"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "N_{Ed}": f"{self.n_ed:.3f}",
                "M_{Ed}": f"{self.m_ed:.3f}",
                "N_{pl,Rd}": f"{self.a * self.f_y / self.gamma_m0:.3f}",
                "M_{c,Rd}": f"{self.m_c_rd:.3f}",
                "gamma_{M0}": f"{self.gamma_m0:.3f}",
                "gamma_{M1}": f"{self.gamma_m1:.3f}",
                "chi": f"{self.chi:.3f}",
            },
            True,  # set to False when a single variable appears more than once in equation
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
