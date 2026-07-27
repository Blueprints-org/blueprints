"""Formula 8.56 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot56StressInShearReinforcement(Formula):
    """Class representing formula 8.56 for the calculation of the stress in the shear reinforcement that replaces
    the yield strength when the compression field inclination is steeper than 45 degrees.
    """

    label = "8.56"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, e_s: MPA, cot_theta: DIMENSIONLESS, epsilon_x: DIMENSIONLESS, f_ywd: MPA) -> None:
        r"""[$\sigma_{swd}$] Stress in the shear reinforcement [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.3 (12) - Formula (8.56)

        Compression field inclinations with [$\cot\theta < 1$] are allowed if the yield strength [$f_{ywd}$] in
        Formulae (8.55) and (8.57) is replaced by this stress. That is a condition of application, not a bound,
        so it is not enforced here. The standard prints no lower bound on the result either, so a combination
        that gives a negative stress returns that value unchanged.

        Parameters
        ----------
        e_s : MPA
            [$E_s$] Modulus of elasticity of the reinforcing steel [$MPa$].
        cot_theta : DIMENSIONLESS
            [$\cot\theta$] Cotangent of the inclination of the compression field in the web. This formula covers
            the case [$\cot\theta < 1$], which lies outside the range of Formula (8.41) [$-$].
        epsilon_x : DIMENSIONLESS
            [$\varepsilon_x$] Longitudinal strain, which may be calculated according to 8.2.3(7) for a
            cross-section located midway between the support and the load [$-$].
        f_ywd : MPA
            [$f_{ywd}$] Design value of the yield strength of the shear reinforcement, which the stress may not
            exceed [$MPa$].
        """
        super().__init__()
        self.e_s = e_s
        self.cot_theta = cot_theta
        self.epsilon_x = epsilon_x
        self.f_ywd = f_ywd

    @staticmethod
    def _evaluate(e_s: MPA, cot_theta: DIMENSIONLESS, epsilon_x: DIMENSIONLESS, f_ywd: MPA) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(e_s=e_s, cot_theta=cot_theta, epsilon_x=epsilon_x, f_ywd=f_ywd)

        return min(e_s * (cot_theta**2 * (epsilon_x + 0.001) - 0.001), f_ywd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.56."""
        _equation: str = (
            r"\min\left(E_s \cdot \left[\left(\cot(\theta)\right)^2 \cdot "
            r"\left(\varepsilon_x + 0.001\right) - 0.001\right], f_{ywd}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"E_s": f"{self.e_s:.{n}f}",
                r"\cot(\theta)": f"{self.cot_theta:.{n}f}",
                r"\varepsilon_x": f"{self.epsilon_x:.{n}f}",
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"E_s": rf"{self.e_s:.{n}f} \ MPa",
                r"\cot(\theta)": f"{self.cot_theta:.{n}f}",
                r"\varepsilon_x": f"{self.epsilon_x:.{n}f}",
                r"f_{ywd}": rf"{self.f_ywd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{swd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
