"""Formula 8.20 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot20MinimumShearStressResistance(Formula):
    """Class representing formula 8.20 for the calculation of the minimum shear stress resistance."""

    label = "8.20"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, gamma_v: DIMENSIONLESS, f_ck: MPA, f_yd: MPA, d_dg: MM, d: MM) -> None:
        r"""[$\tau_{Rdc,min}$] Minimum shear stress resistance [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.1 (4) - Formula (8.20)

        Parameters
        ----------
        gamma_v : DIMENSIONLESS
            [$\gamma_V$] Partial factor for shear design according to Table 4.3 (NDP) or Tables A.1 (NDP)
            and A.2 (NDP) [$-$].
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        f_yd : MPA
            [$f_{yd}$] Design value of the yield strength which has been used to design the flexural
            reinforcement. In case of prestressed members without ordinary reinforcement it may be replaced by
            [$f_{pd} - \sigma_{pm,\infty}$], where [$\sigma_{pm,\infty}$] is the prestress in the tendons after
            losses [$MPa$].
        d_dg : MM
            [$d_{dg}$] Size parameter describing the failure zone roughness, which depends on the concrete type
            and its aggregate properties. The standard gives it as [$16 + D_{lower} \leq 40$] for concrete with
            [$f_{ck} \leq 60$] MPa, and as [$16 + D_{lower} \cdot \left(60/f_{ck}\right)^2 \leq 40$] for concrete
            with [$f_{ck} > 60$] MPa, both in millimetres. [$D_{lower}$] is the smallest value of the upper sieve
            size [$D$] in an aggregate for the coarsest fraction of aggregates in the concrete permitted by the
            specification of concrete according to EN 206; where [$D_{max}$] is known it may replace
            [$D_{lower}$], see the NOTE 2 to 8.2.1(4) [$mm$].
        d : MM
            [$d$] Effective depth of the flexural reinforcement. For prestressed members see 8.2.2(6) [$mm$].
        """
        super().__init__()
        self.gamma_v = gamma_v
        self.f_ck = f_ck
        self.f_yd = f_yd
        self.d_dg = d_dg
        self.d = d

    @staticmethod
    def _evaluate(gamma_v: DIMENSIONLESS, f_ck: MPA, f_yd: MPA, d_dg: MM, d: MM) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ck=f_ck, d_dg=d_dg)
        raise_if_less_or_equal_to_zero(gamma_v=gamma_v, f_yd=f_yd, d=d)

        return (11 / gamma_v) * np.sqrt((f_ck / f_yd) * (d_dg / d))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.20."""
        _equation: str = r"\frac{11}{\gamma_V} \cdot \sqrt{\frac{f_{ck}}{f_{yd}} \cdot \frac{d_{dg}}{d}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\gamma_V": f"{self.gamma_v:.{n}f}",
                r"f_{ck}": f"{self.f_ck:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
                r"d_{dg}": f"{self.d_dg:.{n}f}",
                r"{d}": "{" + f"{self.d:.{n}f}" + "}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\gamma_V": f"{self.gamma_v:.{n}f}",
                r"f_{ck}": rf"{self.f_ck:.{n}f} \ MPa",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
                r"d_{dg}": rf"{self.d_dg:.{n}f} \ mm",
                r"{d}": "{" + rf"{self.d:.{n}f} \ mm" + "}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rdc,min}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
