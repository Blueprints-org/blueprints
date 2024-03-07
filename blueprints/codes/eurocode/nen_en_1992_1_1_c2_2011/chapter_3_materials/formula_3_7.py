"""Formula 3.7 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula


class Form3Dot7NonLinearCreepCoefficient(Formula):
    """Class representing formula 3.7 for the calculation of the non-linear creep coefficient."""

    label = "3.7"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        phi_inf_t0: float,
        k_sigma: float,
    ) -> None:
        """[φnl(∞,t0)] The non-linear creep coefficient [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(4) - Formula (3.7)

        Parameters
        ----------
        phi_inf_t0 : float
            [φ(∞, t0)] Creep coefficient if high accuracy is not required use figure 3.1 and/or use appendix B [-].
        k_sigma : float
            [kσ] Stress-strength ratio (σc / fck(t0)) [-].

        Returns
        -------
        None
        """
        super().__init__()
        self.phi_inf_t0 = phi_inf_t0
        self.k_sigma = k_sigma

    @staticmethod
    def _evaluate(
        phi_inf_t0: float,
        k_sigma: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if phi_inf_t0 < 0:
            raise ValueError(f"Negative phi_inf_t0: {phi_inf_t0}. phi_inf_t0 cannot be negative")
        if k_sigma < 0:
            raise ValueError(f"Negative k_sigma: {k_sigma}. k_sigma cannot be negative")
        return phi_inf_t0 * np.exp(1.5 * (k_sigma - 0.45))
