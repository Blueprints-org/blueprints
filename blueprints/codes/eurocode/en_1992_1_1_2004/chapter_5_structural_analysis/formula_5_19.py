"""Formula 5.19 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KNM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot19EffectiveCreepCoefficient(Formula):
    """Class representing formula 5.19 for the calculation of the effective creep coefficient, ϕef."""

    label = "5.19"
    source_document = EN_1992_1_1_2004

    def __init__(self, phi_inf_t0: DIMENSIONLESS, m0_eqp: KNM, m0_ed: KNM) -> None:
        r"""[$\phi_{ef}$] Effective creep coefficient.

        EN 1992-1-1:2004 art.5.8.4(2) - Formula (5.19)

        Parameters
        ----------
        phi_inf_t0 : DIMENSIONLESS
            [$\phi (\infty,t_0)$] is the final value of the creep coefficient according to art. 3.1.4.
        m0_eqp : KNM
            [$M_{0,Eqp}$] is the first-order bending moment in the quasi-permanent load combination (SLS).
        m0_ed : KNM
            [$M_{0,Ed}$] is the first-order bending moment in the ultimate limit state (ULS).
        """
        super().__init__()
        self.phi_inf_t0 = phi_inf_t0
        self.m0_eqp = m0_eqp
        self.m0_ed = m0_ed

    @staticmethod
    def _evaluate(phi_inf_t0: DIMENSIONLESS, m0_eqp: KNM, m0_ed: KNM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(m0_ed=m0_ed)
        return phi_inf_t0 * (m0_eqp / m0_ed)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.19."""
        return LatexFormula(
            return_symbol=r"\phi_{ef}",
            result=f"{self:.{n}f}",
            equation=r"\phi (\infty,t_0) \cdot \frac{M_{0,Eqp}}{M_{0,Ed}}",
            numeric_equation=rf"{self.phi_inf_t0} \cdot \frac{{{self.m0_eqp}}}{{{self.m0_ed}}}",
            comparison_operator_label="=",
        )
