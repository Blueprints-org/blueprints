"""Formula 8.42 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot42ShearStressResistanceReinforcement(Formula):
    r"""Class representing formula 8.42 for the shear stress resistance perpendicular to the longitudinal
    member axis in case of yielding of the shear reinforcement.

    prEN 1992-1-1:2023 art. 8.2.3 (5) - Formula (8.42)

    Formula
    -------
    $\tau_{Rd,sy} = \rho_w \cdot f_{ywd} \cdot \cot \theta$

    Parameters
    ----------
    rho_w : DIMENSIONLESS
        [$\rho_w$] Shear reinforcement ratio (dimensionless). Defined in formula (8.42).
    f_ywd : MPA
        [$f_{ywd}$] Design yield strength of the shear reinforcement ($MPa$).
    cot_theta : DIMENSIONLESS
        [$\cot \theta$] Cotangent of the inclination angle of the compression strut (dimensionless).
    """

    label = "8.42"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
        cot_theta: DIMENSIONLESS,
    ) -> None:
        super().__init__()
        self.rho_w = rho_w
        self.f_ywd = f_ywd
        self.cot_theta = cot_theta

    @staticmethod
    def _evaluate(rho_w: DIMENSIONLESS, f_ywd: MPA, cot_theta: DIMENSIONLESS) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        # None of the variables are denominators, they must be non-negative (zero allowed)
        raise_if_negative(rho_w=rho_w, f_ywd=f_ywd, cot_theta=cot_theta)
        return rho_w * f_ywd * cot_theta

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.42."""
        _equation: str = r"\rho_w \cdot f_{ywd} \cdot \cot \theta"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
                r"\cot \theta": f"{self.cot_theta:.{n}f}",
            },
            unique_symbol_check=False,
        )

        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\rho_w": rf"{self.rho_w:.{n}f}",
                r"f_{ywd}": rf"{self.f_ywd:.{n}f} \ MPa",
                r"\cot \theta": rf"{self.cot_theta:.{n}f}",
            },
            unique_symbol_check=True,
        )

        return LatexFormula(
            return_symbol=r"\tau_{Rd,sy}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
