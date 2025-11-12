"""Formula 3.7 from EN 1992-1-1:2004: Chapter 3 - Materials."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form3Dot7NonLinearCreepCoefficient(Formula):
    """Class representing formula 3.7 for the calculation of the non-linear creep coefficient."""

    label = "3.7"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        phi_inf_t0: DIMENSIONLESS,
        k_sigma: DIMENSIONLESS,
    ) -> None:
        r"""[$\varphi_{nl}(\infty,t_0)$] The non-linear creep coefficient [$-$].

        EN 1992-1-1:2004 art.3.1.4(4) - Formula (3.7)

        Parameters
        ----------
        phi_inf_t0 : DIMENSIONLESS
            [$\varphi(\infty, t_0)$] Creep coefficient if high accuracy is not required use figure 3.1 and/or use appendix B [$-$].
        k_sigma : DIMENSIONLESS
            [$k_{\sigma}$] Stress-strength ratio [$\sigma_c / f_{ck}(t_0)$] [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.phi_inf_t0 = phi_inf_t0
        self.k_sigma = k_sigma

    @staticmethod
    def _evaluate(
        phi_inf_t0: DIMENSIONLESS,
        k_sigma: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(phi_inf_t0=phi_inf_t0, k_sigma=k_sigma)
        return phi_inf_t0 * np.exp(1.5 * (k_sigma - 0.45))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 3.7."""
        return LatexFormula(
            return_symbol=r"\varphi_{nl}(\infty, t_0)",
            result=f"{self:.{n}f}",
            equation=r"\varphi(\infty, t_0) \cdot \exp( 1.5 ( k_{\sigma} - 0.45))",
            numeric_equation=rf"{self.phi_inf_t0:.{n}f} \cdot \exp( 1.5 ( {self.k_sigma:.{n}f} - 0.45))",
            comparison_operator_label="=",
        )
