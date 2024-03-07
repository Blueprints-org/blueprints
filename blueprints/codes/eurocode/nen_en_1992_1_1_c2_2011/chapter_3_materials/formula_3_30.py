"""Formula 3.30 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import HOURS, PERCENTAGE


class Form3Dot30RatioLossOfPreStressClass3(Formula):
    """Class representing formula 3.30 for the calculation of the ratio between loss of pre-stress and initial pre-stress of class 3."""

    label = "3.30"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        rho_1000: PERCENTAGE,
        mu: float,
        t: HOURS,
    ) -> None:
        """[Δσpr / σpi] Ratio between loss of pre-stress and initial pre-stress for class 3. [-].

        NEN-EN 1992-1-1+C2:2011 art.3.3.2(7) - Formula (3.30)

        Parameters
        ----------
        rho_1000 : PERCENTAGE
            [ρ1000] Value of relaxation loss at 1000h after prestressing at an average temperature of 20 degrees Celsius [%]
        mu : float
            [μ] Ratio between initial pre-stress and characteristic tensile strength [-]
            = σpi / fpk
            Use your own implementation of this formula or use sub_formula_3_28_39_30 class SubForm3Dot282930Mu.
        t : HOURS
            [t] Time after prestressing [hours]

        Returns
        -------
        None
        """
        super().__init__()
        self.rho_1000 = rho_1000
        self.mu = mu
        self.t = t

    @staticmethod
    def _evaluate(
        rho_1000: PERCENTAGE,
        mu: float,
        t: HOURS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if rho_1000 < 0:
            raise ValueError(f"Invalid rho_1000: {rho_1000}. rho_1000 cannot be negative")
        if t < 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative")
        return 1.98 * rho_1000 * np.exp(8 * mu) * (t / 1000) ** (0.75 * (1 - mu)) * 10**-5
