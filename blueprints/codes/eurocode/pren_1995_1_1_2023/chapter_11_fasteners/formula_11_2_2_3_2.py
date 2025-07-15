"""Formula 11.2.2.3-2 from prEN 1995-1-1:2023."""

from blueprints.codes.eurocode.pren_1995_1_1_2023 import PREN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, KN, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form11Dot2Dot2Dot3Dash2WithdrawalStrengthDensityDependent(Formula):
    r"""
    Class representing formula 11.2.2.3-2 for the calculation of withdrawal strength dependent on density.
    
    This formula calculates the withdrawal strength of fasteners based on timber density.
    """

    label = "11.2.2.3-2"
    source_document = PREN_1995_1_1_2023

    def __init__(self, rho_k: float, d: MM) -> None:
        r"""
        [f_{w,k}] Withdrawal strength dependent on timber density.

        prEN 1995-1-1:2023 art 11.2.2.3 - Formula (11.2.2.3-2)

        Parameters
        ----------
        rho_k : float
            [$\rho_k$] Characteristic density of timber [$kg/m^3$].
        d : MM
            [$d$] Diameter of the fastener [$mm$].

        Returns
        -------
        None
        """
        super().__init__()
        self.rho_k = rho_k
        self.d = d

    @staticmethod
    def _evaluate(rho_k: float, d: MM) -> MPA:
        """Evaluate the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(rho_k=rho_k, d=d)
        
        # Withdrawal strength: f_w,k = 20 * (rho_k / 350)^0.8 * d^(-0.2)
        return 20 * (rho_k / 350) ** 0.8 * d ** (-0.2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 11.2.2.3-2."""
        eq_for: str = r"20 \cdot \left(\frac{\rho_k}{350}\right)^{0.8} \cdot d^{-0.2}"
        repl_symb = {
            r"\rho_k": f"{self.rho_k:.{n}f}",
            r"d^{-0.2}": f"{self.d:.{n}f}^{{-0.2}}",
        }
        return LatexFormula(
            return_symbol=r"f_{w,k}",
            result=f"{self:.{n}f}",
            equation=eq_for,
            numeric_equation=latex_replace_symbols(eq_for, repl_symb),
            unit="MPa",
        )