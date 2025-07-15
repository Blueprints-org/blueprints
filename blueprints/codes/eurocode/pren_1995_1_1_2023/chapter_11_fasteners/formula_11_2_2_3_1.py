"""Formula 11.2.2.3-1 from prEN 1995-1-1:2023."""

from blueprints.codes.eurocode.pren_1995_1_1_2023 import PREN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, KN, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form11Dot2Dot2Dot3Dash1WithdrawalCapacityScrew(Formula):
    r"""
    Class representing formula 11.2.2.3-1 for the calculation of withdrawal capacity of screws.
    
    This formula calculates the withdrawal capacity of screws based on the effective head diameter,
    embedment depth, and wood density.
    """

    label = "11.2.2.3-1"
    source_document = PREN_1995_1_1_2023

    def __init__(self, d_head_ef: MM, l_ef: MM, rho_k: float, f_w_k: MPA) -> None:
        r"""
        [F_{w,Rd}] Withdrawal capacity of screws.

        prEN 1995-1-1:2023 art 11.2.2.3 - Formula (11.2.2.3-1)

        Parameters
        ----------
        d_head_ef : MM
            [$d_{head,ef}$] Effective head diameter of the screw [$mm$].
        l_ef : MM
            [$l_{ef}$] Effective embedment depth of the screw [$mm$].
        rho_k : float
            [$\rho_k$] Characteristic density of timber [$kg/m^3$].
        f_w_k : MPA
            [$f_{w,k}$] Characteristic withdrawal strength [$MPa$].

        Returns
        -------
        None
        """
        super().__init__()
        self.d_head_ef = d_head_ef
        self.l_ef = l_ef
        self.rho_k = rho_k
        self.f_w_k = f_w_k

    @staticmethod
    def _evaluate(d_head_ef: MM, l_ef: MM, rho_k: float, f_w_k: MPA) -> KN:
        """Evaluate the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(d_head_ef=d_head_ef, l_ef=l_ef, rho_k=rho_k, f_w_k=f_w_k)
        
        # Withdrawal capacity: F_w,Rd = π * d_head_ef * l_ef * f_w,k
        # Converting from N to kN by dividing by 1000
        return 3.14159 * d_head_ef * l_ef * f_w_k / 1000

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 11.2.2.3-1."""
        eq_for: str = r"\pi \cdot d_{head,ef} \cdot l_{ef} \cdot f_{w,k}"
        repl_symb = {
            r"d_{head,ef}": f"{self.d_head_ef:.{n}f}",
            r"l_{ef}": f"{self.l_ef:.{n}f}",
            r"f_{w,k}": f"{self.f_w_k:.{n}f}",
        }
        return LatexFormula(
            return_symbol=r"F_{w,Rd}",
            result=f"{self:.{n}f}",
            equation=eq_for,
            numeric_equation=latex_replace_symbols(eq_for, repl_symb),
            unit="kN",
        )