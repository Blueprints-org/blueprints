"""Formula 8.106 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot106StrengthReductionCoefficientForShearReinforcement(Formula):
    r"""Class representing formula 8.106 for the calculation of the strength reduction coefficient for the
    contribution of the shear reinforcement.

    The standard writes this as an expression bounded from above by [$0,8$], which is implemented as a
    minimum.
    """

    label = "8.106"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        d_v: MM,
        phi_w: MM,
        d_dg: MM,
        eta_c: DIMENSIONLESS,
        k_pb: DIMENSIONLESS,
    ) -> None:
        r"""[$\eta_s$] Strength reduction coefficient for the contribution of the shear reinforcement [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.4(1) - Formula (8.106)

        Parameters
        ----------
        d_v : MM
            [$d_v$] Shear-resisting effective depth of the slab according to Formula (8.91) [$mm$].
        phi_w : MM
            [$\phi_w$] Diameter of the punching shear reinforcement [$mm$].
        d_dg : MM
            [$d_{dg}$] Size parameter describing the failure zone roughness, which depends on the concrete type
            and its aggregate properties. The standard gives it as [$16 + D_{lower} \leq 40$] for concrete with
            [$f_{ck} \leq 60$] MPa, and as [$16 + D_{lower} \cdot \left(60/f_{ck}\right)^2 \leq 40$] for concrete
            with [$f_{ck} > 60$] MPa, both in millimetres. [$D_{lower}$] is the smallest value of the upper sieve
            size [$D$] in an aggregate for the coarsest fraction of aggregates in the concrete permitted by the
            specification of concrete according to EN 206; where [$D_{max}$] is known it may replace
            [$D_{lower}$], see the NOTE 2 to 8.2.1(4) [$mm$].
        eta_c : DIMENSIONLESS
            [$\eta_c$] Strength reduction coefficient for shear resistance [$\tau_{Rd,c}$] according to
            Formula (8.105), see Form8Dot105StrengthReductionCoefficientForShearResistance [$-$].
        k_pb : DIMENSIONLESS
            [$k_{pb}$] Punching shear gradient enhancement coefficient according to Formula (8.96), see
            Form8Dot96PunchingShearGradientEnhancementCoefficient [$-$].
        """
        super().__init__()
        self.d_v = d_v
        self.phi_w = phi_w
        self.d_dg = d_dg
        self.eta_c = eta_c
        self.k_pb = k_pb

    @staticmethod
    def _evaluate(
        d_v: MM,
        phi_w: MM,
        d_dg: MM,
        eta_c: DIMENSIONLESS,
        k_pb: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d_dg=d_dg)
        raise_if_less_or_equal_to_zero(d_v=d_v, phi_w=phi_w, eta_c=eta_c, k_pb=k_pb)

        return min(
            d_v / (150 * phi_w) + (15 * d_dg / d_v) ** (1 / 2) * (1 / (eta_c * k_pb)) ** (3 / 2),
            0.8,
        )

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.106."""
        _equation: str = (
            r"\min\left(\frac{d_v}{150 \cdot \phi_w} + \left(15 \cdot \frac{d_{dg}}{d_v}\right)^{\frac{1}{2}} \cdot "
            r"\left(\frac{1}{\eta_c \cdot k_{pb}}\right)^{\frac{3}{2}}, 0.8\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\phi_w": f"{self.phi_w:.{n}f}",
                r"d_{dg}": f"{self.d_dg:.{n}f}",
                r"d_v": f"{self.d_v:.{n}f}",
                r"\eta_c": f"{self.eta_c:.{n}f}",
                r"k_{pb}": f"{self.k_pb:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\phi_w": rf"{self.phi_w:.{n}f} \ mm",
                r"d_{dg}": rf"{self.d_dg:.{n}f} \ mm",
                r"d_v": rf"{self.d_v:.{n}f} \ mm",
                r"\eta_c": f"{self.eta_c:.{n}f}",
                r"k_{pb}": f"{self.k_pb:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\eta_s",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
