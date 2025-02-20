"""Formula 5.27 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form5Dot27EffectiveDesignModulusElasticity(Formula):
    """Class representing formula 5.27 for the calculation of the effective design modulus of elasticity, [$E_{cd,eff}$]."""

    label = "5.27"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, e_cd: MPA, phi_ef: DIMENSIONLESS) -> None:
        r"""[$E_{cd,eff}$] Effective design modulus of elasticity.

        NEN-EN 1992-1-1+C2:2011 art.5.8.6(3) - Formula (5.27)

        Parameters
        ----------
        e_cd : MPA
            [$E_{cd}$] is the design modulus of elasticity of concrete according to 5.8.6 (3).
        phi_ef : DIMENSIONLESS
            [$\phi_{ef}$] is the effective creep coefficient; same value as for columns may be used.
        """
        super().__init__()
        self.e_cd = e_cd
        self.phi_ef = phi_ef

    @staticmethod
    def _evaluate(e_cd: MPA, phi_ef: DIMENSIONLESS) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(e_cd=e_cd, phi_ef=phi_ef)
        return e_cd / (1 + phi_ef)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.27."""
        return LatexFormula(
            return_symbol=r"E_{cd,eff}",
            result=f"{self:.3f}",
            equation=r"\frac{E_{cd}}{1 + \phi_{ef}}",
            numeric_equation=rf"\frac{{{self.e_cd:.3f}}}{{1 + {self.phi_ef:.3f}}}",
            comparison_operator_label="=",
        )
