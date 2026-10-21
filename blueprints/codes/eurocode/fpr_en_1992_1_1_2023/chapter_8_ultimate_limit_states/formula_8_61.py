"""Formula 8.61 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, N
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot61AdditionalTensileForceInclinedShearReinforcement(Formula):
    """Class representing formula 8.61 for the calculation of the additional tensile axial force due to shear in
    members with inclined shear reinforcement.

    This replaces Formula (8.50) for such members.
    """

    label = "8.61"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, v_ed: N, theta: DEG, alpha_w: DEG) -> None:
        r"""[$N_{Vd}$] Additional tensile axial force due to shear [$V_{Ed}$] [$N$].

        FprEN 1992-1-1:2023 (E) art 8.2.3 (13) - Formula (8.61)

        The standard takes the magnitude of the shear force, so the sign of [$V_{Ed}$] does not reach the
        result. The result itself does carry a sign: it turns negative where the shear reinforcement is
        inclined more steeply than the compression field, that is where [$\cot\alpha_w > \cot\theta$]. The
        standard prints no bound on it, so that value is returned unchanged.

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design shear force at the control section. Only its magnitude is used [$N$].
        theta : DEG
            [$\theta$] Inclination of the compression field in the web, selected within the range of Formula
            (8.58), see Form8Dot58CheckCotangentInclinedShearReinforcement [$degrees$].
        alpha_w : DEG
            [$\alpha_w$] Inclination of the shear reinforcement, measured positive as shown in Figure 8.11 b).
            The standard gives this clause for [$45 \leq \alpha_w < 90$] degrees, which is a condition of
            application and is not enforced. Angles above 90 degrees are rejected, since the standard says
            they should be avoided [$degrees$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.theta = theta
        self.alpha_w = alpha_w

    @staticmethod
    def _evaluate(v_ed: N, theta: DEG, alpha_w: DEG) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(theta=theta, alpha_w=alpha_w)

        return abs(v_ed) * (cot(theta) - cot(alpha_w))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.61."""
        _equation: str = r"\left|V_{Ed}\right| \cdot \left(\cot(\theta) - \cot(\alpha_w)\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
                r"\theta": f"{self.theta:.{n}f}",
                r"\alpha_w": f"{self.alpha_w:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
                r"\alpha_w": rf"{self.alpha_w:.{n}f} ^\circ",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"N_{Vd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )
