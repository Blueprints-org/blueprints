"""Formula 5.26 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot26FactorKs(Formula):
    """Class representing the factor K_s that represents the factor for contribution of reinforcement to the resistance."""

    label = "5.26"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, rho: float) -> None:
        r"""[$K_s$] Factor $K_s = 0$.

        NEN-EN 1992-1-1+C2:2011 art.5.8.7.2(2) - Formula (5.26)

        Parameters
        ----------
        rho : float
            [$\rho$] Geometric reinforcement ratio, As/Ac. Must be >= 0.01.
        """
        super().__init__()
        self.rho = rho

    @staticmethod
    def _evaluate(rho: float) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if rho <= 0.01:
            raise ValueError(f"Invalid rho: {rho}. rho cannot be less than 0.01")
        return 0.0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.26 K_s."""
        return LatexFormula(
            return_symbol=r"K_s",
            result=f"{self._evaluate(self.rho):.3f}",
            equation=r"0",
            numeric_equation="0",
            comparison_operator_label="=",
        )


class Form5Dot26FactorKc(Formula):
    """Class representing the factor K_c representing the factor for effects of cracking, creep, etc."""

    label = "5.26"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, phi_ef: DIMENSIONLESS, rho: float) -> None:
        r"""[$K_c$] Factor $K_c = \frac{0.3}{1 + 0.5 \cdot \phi_{ef}}$.

        NEN-EN 1992-1-1+C2:2011 art.5.8.7.2(2) - Formula (5.26)

        Parameters
        ----------
        phi_ef : DIMENSIONLESS
            [$\phi_{ef}$] Effective creep ratio, see 5.8.4.
        rho : float
            [$\rho$] Geometric reinforcement ratio, As/Ac. Must be > 0.01.
        """
        super().__init__()
        self.phi_ef = phi_ef
        self.rho = rho

    @staticmethod
    def _evaluate(phi_ef: DIMENSIONLESS, rho: float) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        if rho <= 0.01:
            raise ValueError(f"Invalid rho: {rho}. rho must be greater than 0.01")
        raise_if_less_or_equal_to_zero(phi_ef=phi_ef)
        return 0.3 / (1 + 0.5 * phi_ef)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.26 K_c."""
        return LatexFormula(
            return_symbol=r"K_c",
            result=f"{self:.3f}",
            equation=r"\frac{0.3}{1 + 0.5 \cdot \phi_{ef}}",
            numeric_equation=rf"\frac{{{0.3}}}{{1 + 0.5 \cdot {self.phi_ef:.3f}}}",
            comparison_operator_label="=",
        )
