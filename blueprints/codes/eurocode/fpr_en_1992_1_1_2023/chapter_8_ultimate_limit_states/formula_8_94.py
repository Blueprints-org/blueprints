"""Formula 8.94 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot94PunchingShearStressResistance(Formula):
    r"""Class representing formula 8.94 for the calculation of the design punching shear stress resistance of
    slabs without shear reinforcement.

    The standard writes this as an expression bounded from above, which is implemented as a minimum of the two.
    """

    label = "8.94"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        gamma_v: DIMENSIONLESS,
        k_pb: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        d_dg: MM,
        d_v: MM,
    ) -> None:
        r"""[$\tau_{Rd,c}$] Design punching shear stress resistance of slabs without shear reinforcement [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.4.3(1) - Formula (8.94)

        Parameters
        ----------
        gamma_v : DIMENSIONLESS
            [$\gamma_V$] Partial factor for shear design according to Table 4.3 (NDP) or Tables A.1 (NDP)
            and A.2 (NDP) [$-$].
        k_pb : DIMENSIONLESS
            [$k_{pb}$] Punching shear gradient enhancement coefficient according to Formula (8.96), see
            Form8Dot96PunchingShearGradientEnhancementCoefficient [$-$].
        rho_l : DIMENSIONLESS
            [$\rho_l$] Longitudinal reinforcement ratio at the control perimeter according to Formula (8.95),
            see Form8Dot95LongitudinalReinforcementRatioPunchingShear [$-$].
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        d_dg : MM
            [$d_{dg}$] Size parameter describing the failure zone roughness, which depends on the concrete type
            and its aggregate properties. The standard gives it as [$16 + D_{lower} \leq 40$] for concrete with
            [$f_{ck} \leq 60$] MPa, and as [$16 + D_{lower} \cdot \left(60/f_{ck}\right)^2 \leq 40$] for concrete
            with [$f_{ck} > 60$] MPa, both in millimetres. [$D_{lower}$] is the smallest value of the upper sieve
            size [$D$] in an aggregate for the coarsest fraction of aggregates in the concrete permitted by the
            specification of concrete according to EN 206; where [$D_{max}$] is known it may replace
            [$D_{lower}$], see the NOTE 2 to 8.2.1(4) [$mm$].
        d_v : MM
            [$d_v$] Shear-resisting effective depth of the slab according to Formula (8.91) [$mm$].
        """
        super().__init__()
        self.gamma_v = gamma_v
        self.k_pb = k_pb
        self.rho_l = rho_l
        self.f_ck = f_ck
        self.d_dg = d_dg
        self.d_v = d_v

    @staticmethod
    def _evaluate(
        gamma_v: DIMENSIONLESS,
        k_pb: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        d_dg: MM,
        d_v: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(k_pb=k_pb, rho_l=rho_l, f_ck=f_ck, d_dg=d_dg)
        raise_if_less_or_equal_to_zero(gamma_v=gamma_v, d_v=d_v)

        return min(
            (0.6 / gamma_v) * k_pb * (100 * rho_l * f_ck * (d_dg / d_v)) ** (1 / 3),
            (0.5 / gamma_v) * np.sqrt(f_ck),
        )

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.94."""
        _equation: str = (
            r"\min\left(\frac{0.6}{\gamma_V} \cdot k_{pb} \cdot \left(100 \cdot \rho_l \cdot f_{ck} \cdot "
            r"\frac{d_{dg}}{d_v}\right)^{\frac{1}{3}}, \frac{0.5}{\gamma_V} \cdot \sqrt{f_{ck}}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\gamma_V": f"{self.gamma_v:.{n}f}",
                r"k_{pb}": f"{self.k_pb:.{n}f}",
                r"\rho_l": f"{self.rho_l:.{n}f}",
                r"f_{ck}": f"{self.f_ck:.{n}f}",
                r"d_{dg}": f"{self.d_dg:.{n}f}",
                r"d_v": f"{self.d_v:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\gamma_V": f"{self.gamma_v:.{n}f}",
                r"k_{pb}": f"{self.k_pb:.{n}f}",
                r"\rho_l": f"{self.rho_l:.{n}f}",
                r"f_{ck}": rf"{self.f_ck:.{n}f} \ MPa",
                r"d_{dg}": rf"{self.d_dg:.{n}f} \ mm",
                r"d_v": rf"{self.d_v:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rd,c}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
