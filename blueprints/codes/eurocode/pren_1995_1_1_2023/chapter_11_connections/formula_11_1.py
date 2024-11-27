"""Formula 11.1 from prEN 1995-1-1: Chapter 11 - Connections."""

from blueprints.codes.eurocode.pren_1995_1_1_2023 import PREN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form11Dot1AxialTensileResistance(Formula):
    """Class representing formula 11.1 for axial tensile resistance of a fastener."""

    label = "11.1"
    source_document = PREN_1995_1_1_2023

    def __init__(
        self,
        k_mod: DIMENSIONLESS,
        gamma_r: DIMENSIONLESS,
        f_pull_k: KN,
        f_w_k: KN,
    ) -> None:
        r"""[:math:`F_{ax,t,d}`] Calculate the design axial tensile resistance of an axially-loaded fastener.

        Parameters
        ----------
        k_mod : DIMENSIONLESS.
            [:math:`k_{mod}`]  Modification factor accounting for the effect of the duration of load and moisture
        gamma_r : DIMENSIONLESS
            [:math:`\\gamma_R`] Partial factor for resistance.
        f_pull_k : KN
            [:math:`F_{pull,k}`] Characteristic head pull-through resistance in [:math:`kN`].
        f_w_k : KN
            [:math:`F_{w,k}`] Characteristic withdrawal resistance in [:math:`kN`].
        """
        super().__init__()
        self.k_mod: float = k_mod
        self.gamma_r: float = gamma_r
        self.f_pull_k: float = f_pull_k
        self.f_w_k: float = f_w_k

    @staticmethod
    def _evaluate(
        k_mod: DIMENSIONLESS,
        gamma_r: DIMENSIONLESS,
        f_pull_k: KN,
        f_w_k: KN,
    ) -> KN:
        """Evaluates the formula for the design axial tensile resistance."""
        raise_if_less_or_equal_to_zero(k_mod=k_mod, gamma_r=gamma_r, f_pull_k=f_pull_k, f_w_k=f_w_k)
        return k_mod / gamma_r * max(f_pull_k, f_w_k)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 11.1."""
        _equation: str = r"\frac{k_{mod}}{\gamma_R} \cdot \max  \left \{ \begin{array}{c}F_{pull,k} \\ F_{w,k} \end{array}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"k_{mod}": f"{self.k_mod:.2f}",
                r"\gamma_R": f"{self.gamma_r:.2f}",
                r"F_{pull,k}": f"{self.f_pull_k:.2f}",
                r"F_{w,k}": f"{self.f_w_k:.2f}",
            },
            True,
        )

        return LatexFormula(
            return_symbol=r"F_{ax,t,d}",
            result=str(self),
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="kN",
        )
