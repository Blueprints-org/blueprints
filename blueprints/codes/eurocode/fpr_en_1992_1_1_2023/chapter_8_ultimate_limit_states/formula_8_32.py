"""Formula 8.32 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot32DesignShearStressResistanceWithNormalForce(Formula):
    """Class representing formula 8.32 for the calculation of the design value of the shear stress resistance
    of members without shear reinforcement, considering the effect of compressive normal forces.
    """

    label = "8.32"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        tau_rdc_0: MPA,
        k_1: DIMENSIONLESS,
        sigma_cp: MPA,
        tau_rdc_min: MPA,
        tau_rdc_max: MPA,
    ) -> None:
        r"""[$\tau_{Rd,c}$] Design value of the shear stress resistance, considering the effect of compressive
        normal forces [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (5) - Formula (8.32)

        The standard offers this as an alternative to Formula (8.27) in combination with Formula (8.31). It is
        printed as a single expression enclosed by a lower and an upper bound, which is implemented as a
        maximum against [$\tau_{Rdc,min}$] followed by a minimum against [$\tau_{Rdc,max}$]. That order only
        matters for the degenerate input where the lower bound exceeds the upper one, in which case the
        upper bound wins. The standard assumes this cannot happen and prints no rule for it, so it is
        defined here rather than rejected.

        Parameters
        ----------
        tau_rdc_0 : MPA
            [$\tau_{Rdc,0}$] Design value of the shear stress resistance without the effect of compressive
            normal forces according to Formula (8.33), see Form8Dot33ShearStressResistanceWithoutAxialForce [$MPa$].
        k_1 : DIMENSIONLESS
            [$k_1$] Factor according to Formula (8.34), see Form8Dot34FactorK1, unless the National Annex gives
            another value. It is not required to be positive and is not guarded here: Formula (8.34) prints only
            an upper bound, and its eccentricity [$e_p$] is defined as positive towards the tensile side, so a
            tendon eccentric towards the compression side gives a negative [$e_p$] and can drive [$k_1$] below
            zero [$-$].
        sigma_cp : MPA
            [$\sigma_{cp}$] Normal stress, defined by the standard as [$N_{Ed} / A_c$] with [$A_c$] the area of
            the concrete cross-section. **Compression is negative.** The standard does not say so anywhere near
            this formula, but the printed minus sign settles it: compression has to raise the shear stress
            resistance, and with a positive [$k_1$] the term [$- k_1 \cdot \sigma_{cp}$] only does that for a
            negative [$\sigma_{cp}$]. It also follows from [$N_{Ed}$] itself, which this clause treats as
            positive in tension, as Formula (8.31) does.

            Note that the sign of this term flipped between the two generations of the code. EN 1992-1-1:2004
            prints [$+ k_1 \cdot \sigma_{cp}$] with compression positive, so a value carried over from a
            calculation to that code has the wrong sign here [$MPa$].
        tau_rdc_min : MPA
            [$\tau_{Rdc,min}$] Minimum shear stress resistance according to Formula (8.20), see
            Form8Dot20MinimumShearStressResistance [$MPa$].
        tau_rdc_max : MPA
            [$\tau_{Rdc,max}$] Maximum shear stress resistance according to Formula (8.35), see
            Form8Dot35MaximumShearStressResistance [$MPa$].
        """
        super().__init__()
        self.tau_rdc_0 = tau_rdc_0
        self.k_1 = k_1
        self.sigma_cp = sigma_cp
        self.tau_rdc_min = tau_rdc_min
        self.tau_rdc_max = tau_rdc_max

    @staticmethod
    def _evaluate(
        tau_rdc_0: MPA,
        k_1: DIMENSIONLESS,
        sigma_cp: MPA,
        tau_rdc_min: MPA,
        tau_rdc_max: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(tau_rdc_0=tau_rdc_0, tau_rdc_min=tau_rdc_min, tau_rdc_max=tau_rdc_max)

        # The two bounds come from different formulas, (8.20) and (8.35), and nothing ties them together.
        # (8.20) does not depend on the reinforcement ratio while (8.35) does, so for a lightly reinforced
        # member the maximum can fall below the minimum and the printed chain has no solution at all. Clamping
        # anyway would return one of the two bounds and quietly break the relation this formula prints, so the
        # combination is refused instead. The standard says nothing about it; this is a decision taken here.
        if tau_rdc_min > tau_rdc_max:
            raise ValueError(
                f"The minimum shear stress resistance of {tau_rdc_min} MPa exceeds the maximum of {tau_rdc_max} MPa, "
                f"so no value can satisfy Formula (8.32). Check the inputs of Formulas (8.20) and (8.35)."
            )

        return min(max(tau_rdc_0 - k_1 * sigma_cp, tau_rdc_min), tau_rdc_max)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.32."""
        _equation: str = r"\min\left(\max\left(\tau_{Rdc,0} - k_1 \cdot \sigma_{cp}, \tau_{Rdc,min}\right), \tau_{Rdc,max}\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Rdc,0}": f"{self.tau_rdc_0:.{n}f}",
                r"k_1": f"{self.k_1:.{n}f}",
                r"\sigma_{cp}": r"\left(" + f"{self.sigma_cp:.{n}f}" + r"\right)",
                r"\tau_{Rdc,min}": f"{self.tau_rdc_min:.{n}f}",
                r"\tau_{Rdc,max}": f"{self.tau_rdc_max:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Rdc,0}": rf"{self.tau_rdc_0:.{n}f} \ MPa",
                r"k_1": f"{self.k_1:.{n}f}",
                r"\sigma_{cp}": r"\left(" + rf"{self.sigma_cp:.{n}f} \ MPa" + r"\right)",
                r"\tau_{Rdc,min}": rf"{self.tau_rdc_min:.{n}f} \ MPa",
                r"\tau_{Rdc,max}": rf"{self.tau_rdc_max:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        # The value of the expression before the two bounds are applied. The line above already shows the
        # arithmetic, so what this adds is whether a bound was active: it differs from the result exactly then.
        _intermediate: str = f"{self.tau_rdc_0 - self.k_1 * self.sigma_cp:.{n}f}"

        return LatexFormula(
            return_symbol=r"\tau_{Rd,c}",
            result=f"{self:.{n}f}",
            intermediate_result=_intermediate,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
