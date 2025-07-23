"""Formula 11.2.2.3-3 from prEN 1995-1-1:2023."""

from blueprints.codes.eurocode.pren_1995_1_1_2023 import PREN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, KN, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form11Dot2Dot2Dot3Dash3DesignWithdrawalResistance(Formula):
    r"""
    Class representing formula 11.2.2.3-3 for the calculation of design withdrawal resistance.
    
    This formula calculates the design withdrawal resistance considering partial factors.
    """

    label = "11.2.2.3-3"
    source_document = PREN_1995_1_1_2023

    def __init__(self, f_w_rk: KN, k_mod: DIMENSIONLESS, gamma_m: DIMENSIONLESS) -> None:
        r"""
        [F_{w,Rd}] Design withdrawal resistance.

        prEN 1995-1-1:2023 art 11.2.2.3 - Formula (11.2.2.3-3)

        Parameters
        ----------
        f_w_rk : KN
            [$F_{w,Rk}$] Characteristic withdrawal resistance [$kN$].
        k_mod : DIMENSIONLESS
            [$k_{mod}$] Modification factor for load duration and moisture content [-].
        gamma_m : DIMENSIONLESS
            [$\gamma_M$] Partial factor for material properties [-].

        Returns
        -------
        None
        """
        super().__init__()
        self.f_w_rk = f_w_rk
        self.k_mod = k_mod
        self.gamma_m = gamma_m

    @staticmethod
    def _evaluate(f_w_rk: KN, k_mod: DIMENSIONLESS, gamma_m: DIMENSIONLESS) -> KN:
        """Evaluate the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(f_w_rk=f_w_rk, k_mod=k_mod, gamma_m=gamma_m)
        
        # Design withdrawal resistance: F_w,Rd = (k_mod * F_w,Rk) / gamma_M
        return (k_mod * f_w_rk) / gamma_m

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 11.2.2.3-3."""
        eq_for: str = r"\frac{k_{mod} \cdot F_{w,Rk}}{\gamma_M}"
        repl_symb = {
            r"k_{mod}": f"{self.k_mod:.{n}f}",
            r"F_{w,Rk}": f"{self.f_w_rk:.{n}f}",
            r"\gamma_M": f"{self.gamma_m:.{n}f}",
        }
        return LatexFormula(
            return_symbol=r"F_{w,Rd}",
            result=f"{self:.{n}f}",
            equation=eq_for,
            numeric_equation=latex_replace_symbols(eq_for, repl_symb),
            unit="kN",
        )