"""Formula 8.77 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(Formula):
    r"""Class representing formula 8.77 for the design shear stress resistance at an interface where yielding of the
    reinforcement crossing it is not ensured.

    It applies where the required reinforcement crossing the interface cannot be assumed to yield because of
    insufficient anchorage, for example in structural toppings. Where yielding is ensured, Formula (8.76) applies
    according to 8.2.6(3) and (5).

    The printed line carries an upper bound, so the result is the smaller of the expression and that bound. The
    "where" list defines [$\mu_v$] and [$\sigma_n$] as in 8.2.6(5), so the two rules that paragraph states for
    [$\sigma_n$] apply here as well: a compressive stress is not taken larger than [$0.60 \cdot f_{cd}$], and for a
    tensile stress the term [$\mu_v \cdot \sigma_n$] is taken as zero. Compression is positive.

    As in Formula (8.76), the cap on [$\sigma_n$] cannot govern the result for any [$\mu_v$] of Table 8.2, where the
    smallest value is 0,5: with [$\sigma_n$] at its cap that term alone reaches [$0.30 \cdot f_{cd}$], which already
    exceeds the whole upper bound of [$0.25 \cdot f_{cd}$]. The cap is implemented because the standard states it.

    The remaining rules of 8.2.6(7) act on the coefficients rather than on this expression, so they are applied by
    the caller when choosing the inputs: [$k_{dowel} = 0$] when an intersecting bar sits closer than [$10\phi$] to an
    edge in the direction of the acting shear force; [$c_{v2} = \mu_v = k_v = 0$] for interface reinforcement at 90
    degrees with an embedment length of at least [$8\phi$] but anchored for a stress lower than [$0.5 \cdot f_{yd}$];
    and [$c_{v2}$] increased by a factor 1,2 for horizontal shear transfer in slab members with cast-in-place
    structural toppings and rough or very rough interfaces.

    Footnote a of Table 8.2 belongs to that same group: it sets [$c_{v2} = 0$] when the interface carries tensile
    stresses caused by an external axial force in perpendicular direction, which is the very condition that makes
    [$\sigma_n$] negative here. This class does not apply it, since [$c_{v2}$] is an input and overriding a supplied
    value would be silent; a caller passing a negative [$\sigma_n$] is expected to have read that footnote when
    picking the coefficient. Table 8.2 also prints no coefficients at all for a keyed interface, so this formula
    has no tabulated inputs for keyed joints.

    No lower bound is applied to the result, because the standard prints none, even though a caller can drive the
    expression negative by combining a zero coefficient with the tension case.
    """

    label = "8.77"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        c_v2: DIMENSIONLESS,
        f_ck: MPA,
        gamma_c: DIMENSIONLESS,
        mu_v: DIMENSIONLESS,
        sigma_n: MPA,
        k_v: DIMENSIONLESS,
        rho_i: DIMENSIONLESS,
        f_yd: MPA,
        k_dowel: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        r"""[$\tau_{Rdi}$] Design shear stress resistance at the interface without ensured yielding [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.2.6(7) - Formula (8.77)

        Parameters
        ----------
        c_v2 : DIMENSIONLESS
            [$c_{v2}$] Factor which depends on the roughness of the interface, see Table 8.2 and art. 8.2.6(6).
            Note that the standard refers to Table 8.1 here, while Table 8.1 gives effectiveness factors for
            confinement and it is Table 8.2 that lists this coefficient under the heading of Formula (8.77) [$-$].
        f_ck : MPA
            [$f_{ck}$] Lowest compressive strength of the concretes at the interface [$MPa$].
        gamma_c : DIMENSIONLESS
            [$\gamma_C$] Partial factor for concrete [$-$].
        mu_v : DIMENSIONLESS
            [$\mu_v$] Factor which depends on the roughness of the interface, see Table 8.2 and art. 8.2.6(6) [$-$].
        sigma_n : MPA
            [$\sigma_n$] Compressive stress over the interface area [$A_i$] caused by the minimum external axial
            force across the interface that acts simultaneously with the shear force, as defined in art. 8.2.6(5).
            Compression is positive here: a positive value is capped at [$0.60 \cdot f_{cd}$], and a negative value
            is a tensile stress, for which the term [$\mu_v \cdot \sigma_n$] is taken as 0 [$MPa$].
        k_v : DIMENSIONLESS
            [$k_v$] Factor which depends on the roughness of the interface, see Table 8.2 and art. 8.2.6(6) [$-$].
        rho_i : DIMENSIONLESS
            [$\rho_i$] Ratio [$A_{si} / A_i$] of the bonded reinforcement crossing the interface, as defined in
            art. 8.2.6(5) [$-$].
        f_yd : MPA
            [$f_{yd}$] Design value of the yield strength of the reinforcement crossing the interface [$MPa$].
        k_dowel : DIMENSIONLESS
            [$k_{dowel}$] Factor for dowel action which depends on the roughness of the interface, see Table 8.2
            and art. 8.2.6(6). It is to be taken as 0 when an intersecting reinforcing bar sits closer than
            [$10\phi$] to an edge in the direction of the acting shear force [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.c_v2 = c_v2
        self.f_ck = f_ck
        self.gamma_c = gamma_c
        self.mu_v = mu_v
        self.sigma_n = sigma_n
        self.k_v = k_v
        self.rho_i = rho_i
        self.f_yd = f_yd
        self.k_dowel = k_dowel
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        c_v2: DIMENSIONLESS,
        f_ck: MPA,
        gamma_c: DIMENSIONLESS,
        mu_v: DIMENSIONLESS,
        sigma_n: MPA,
        k_v: DIMENSIONLESS,
        rho_i: DIMENSIONLESS,
        f_yd: MPA,
        k_dowel: DIMENSIONLESS,
        f_cd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        # sigma_n is deliberately not guarded: a negative value is the tensile stress that art. 8.2.6(5) allows
        # for and neutralises below. The four roughness coefficients may legitimately be zero, since 8.2.6(7)
        # itself prescribes zero values for them in two of its cases.
        raise_if_negative(c_v2=c_v2, f_ck=f_ck, mu_v=mu_v, k_v=k_v, rho_i=rho_i, f_yd=f_yd, k_dowel=k_dowel, f_cd=f_cd)
        raise_if_less_or_equal_to_zero(gamma_c=gamma_c)

        sigma_n_effective = min(max(sigma_n, 0), 0.60 * f_cd)
        resistance = c_v2 * np.sqrt(f_ck) / gamma_c + mu_v * sigma_n_effective + k_v * rho_i * f_yd * mu_v + k_dowel * rho_i * np.sqrt(f_yd * f_cd)

        return min(resistance, 0.25 * f_cd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.77."""
        _equation: str = (
            r"\min\left(c_{v2} \cdot \frac{\sqrt{f_{ck}}}{\gamma_C} + \mu_v \cdot "
            r"\min\left(\max\left(\sigma_n, 0\right), 0.60 \cdot f_{cd}\right) + "
            r"k_v \cdot \rho_i \cdot f_{yd} \cdot \mu_v + "
            r"k_{dowel} \cdot \rho_i \cdot \sqrt{f_{yd} \cdot f_{cd}}, 0.25 \cdot f_{cd}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"c_{v2}": f"{self.c_v2:.{n}f}",
                r"f_{ck}": f"{self.f_ck:.{n}f}",
                r"\gamma_C": f"{self.gamma_c:.{n}f}",
                r"\mu_v": f"{self.mu_v:.{n}f}",
                r"\sigma_n": f"{self.sigma_n:.{n}f}",
                r"k_{dowel}": f"{self.k_dowel:.{n}f}",
                r"k_v": f"{self.k_v:.{n}f}",
                r"\rho_i": f"{self.rho_i:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                # The roughness coefficients, the partial factor and the reinforcement ratio are dimensionless.
                r"c_{v2}": f"{self.c_v2:.{n}f}",
                r"f_{ck}": rf"{self.f_ck:.{n}f} \ MPa",
                r"\gamma_C": f"{self.gamma_c:.{n}f}",
                r"\mu_v": f"{self.mu_v:.{n}f}",
                r"\sigma_n": rf"{self.sigma_n:.{n}f} \ MPa",
                r"k_{dowel}": f"{self.k_dowel:.{n}f}",
                r"k_v": f"{self.k_v:.{n}f}",
                r"\rho_i": f"{self.rho_i:.{n}f}",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rdi}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
