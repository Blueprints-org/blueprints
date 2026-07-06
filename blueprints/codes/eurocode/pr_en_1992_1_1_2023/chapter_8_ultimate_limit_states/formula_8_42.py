"""Formula 8.42 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, MPA
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot42ShearStressResistanceReinforcement(Formula):
    r"""Class representing formula 8.42 for the shear stress resistance perpendicular to the longitudinal
    member axis in case of yielding of the shear reinforcement.

    prEN 1992-1-1:2023 art. 8.2.3 (5) - Formula (8.42)

    Formula
    -------
    [$\tau_{Rd,sy} = \rho_w \cdot f_{ywd} \cdot \cot \theta$]

    Parameters
    ----------
    rho_w : DIMENSIONLESS
        [$\rho_w$] Shear reinforcement ratio (dimensionless). Defined in formula (8.42).
    f_ywd : MPA
        [$f_{ywd}$] Design yield strength of the shear reinforcement ($MPa$).
    theta : DEG
        [$\theta$] Angle of the inclination angle of the compression strut [$degrees$].
    """

    label = "8.42"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
        theta: DEG,
    ) -> None:
        super().__init__()
        self.rho_w = rho_w
        self.f_ywd = f_ywd
        self.theta = theta

    @staticmethod
    def _evaluate(rho_w: DIMENSIONLESS, f_ywd: MPA, theta: DEG) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(rho_w=rho_w, f_ywd=f_ywd)
        raise_if_less_or_equal_to_zero(theta=theta)
        return rho_w * f_ywd * cot(theta)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.42."""
        _equation: str = r"\rho_w \cdot f_{ywd} \cdot \cot \left( \theta \right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
                r"\theta": f"{self.theta:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\rho_w": rf"{self.rho_w:.{n}f}",
                r"f_{ywd}": rf"{self.f_ywd:.{n}f} \ MPa",
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
            },
            unique_symbol_check=True,
        )
        intermediate_result = rf"{self.rho_w:.{n}f} \cdot {self.f_ywd:.{n}f} \cdot {cot(self.theta):.{n}f}"

        return LatexFormula(
            return_symbol=r"\tau_{Rd,sy}",
            result=f"{self:.{n}f}",
            intermediate_result=intermediate_result,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
