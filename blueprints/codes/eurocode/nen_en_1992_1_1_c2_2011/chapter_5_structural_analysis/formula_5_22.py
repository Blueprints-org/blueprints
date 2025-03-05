"""Formula 5.22 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot22FactorKs(Formula):
    """Class representing the factor K_s that represents the factor for contribution of reinforcement to the resistance."""

    label = "5.22"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, rho: DIMENSIONLESS) -> None:
        r"""[$K_s$] Factor K_s = 1.

        NEN-EN 1992-1-1+C2:2011 art.5.8.7.2(2) - Formula (5.22)

        Parameters
        ----------
        rho : DIMENSIONLESS
            [$\rho$] Geometric reinforcement ratio, As/Ac. Must be >= 0.002.
        """
        super().__init__()
        self.rho = rho

    @staticmethod
    def _evaluate(rho: DIMENSIONLESS) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if rho < 0.002:
            raise ValueError(f"Invalid rho: {rho}. rho cannot be less than 0.002")
        return 1.0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.22 K_s."""
        return LatexFormula(
            return_symbol=r"K_s",
            result=f"{self._evaluate(self.rho):.3f}",
            equation=r"1",
            numeric_equation="1",
            comparison_operator_label="=",
        )


class Form5Dot22FactorKc(Formula):
    """Class representing the factor K_c representing the factor for effects of cracking, creep, etc."""

    label = "5.22"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, k1: DIMENSIONLESS, k2: DIMENSIONLESS, phi_ef: DIMENSIONLESS, rho: float) -> None:
        r"""[$K_c$] Factor K_c = k_1 * k_2 / (1 + \phi_{ef}).

        NEN-EN 1992-1-1+C2:2011 art.5.8.7.2(2) - Formula (5.22)

        Parameters
        ----------
        k1 : DIMENSIONLESS
            [$k_1$] Factor which depends on concrete strength class, Expression (5.23).
        k2 : DIMENSIONLESS
            [$k_2$] Factor which depends on axial force and slenderness, Expression (5.24).
        phi_ef : DIMENSIONLESS
            [$\phi_{ef}$] Effective creep ratio, see 5.8.4.
        rho : DIMENSIONLESS
            [$\rho$] Geometric reinforcement ratio, As/Ac. Must be >= 0.002.
        """
        super().__init__()
        self.k1 = k1
        self.k2 = k2
        self.phi_ef = phi_ef
        self.rho = rho

    @staticmethod
    def _evaluate(k1: DIMENSIONLESS, k2: DIMENSIONLESS, phi_ef: DIMENSIONLESS, rho: float) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        if rho < 0.002:
            raise ValueError(f"Invalid rho: {rho}. rho cannot be less than 0.002")
        raise_if_less_or_equal_to_zero(phi_ef=phi_ef)
        raise_if_negative(k1=k1, k2=k2)
        return k1 * k2 / (1 + phi_ef)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.22 K_c."""
        return LatexFormula(
            return_symbol=r"K_c",
            result=f"{self:.3f}",
            equation=r"\frac{k_1 \cdot k_2}{1 + \phi_{ef}}",
            numeric_equation=rf"\frac{{{self.k1:.3f} \cdot {self.k2:.3f}}}{{1 + {self.phi_ef:.3f}}}",
            comparison_operator_label="=",
        )
