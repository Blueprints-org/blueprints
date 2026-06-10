"""Fatigue strength curve limits from EN 1993-1-9:2005: Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)."""

from blueprints.codes.eurocode.en_1993_1_9_2005 import EN_1993_1_9_2005
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve_value import Form7FatigueStrengthCurveValue
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_negative


class Form7ConstantAmplitudeFatigueLimit(Formula):
    r"""Class representing the constant amplitude fatigue limit [$\Delta\sigma_D$] at [$N_D$] cycles.

    The constant amplitude fatigue limit is given in EN 1993-1-9:2005, 7.1(2) (see Figure 7.1) by scaling the detail
    category [$\Delta\sigma_C$] along the first branch (slope [$m = 3$]):
    [$\Delta\sigma_D = \left( 2 / 5 \right)^{1/3} \Delta\sigma_C = 0.737 \: \Delta\sigma_C$].

    Only the direct stress curve (Figure 7.1) has a constant amplitude fatigue limit. The shear curve (Figure 7.2)
    has a single slope running straight to its cut-off limit [$\Delta\tau_L$], so this formula is not defined for it
    (see :attr:`FatigueStrengthCurve.has_constant_amplitude_fatigue_limit`).
    """

    label = "Figures 7.1-7.2 (constant amplitude fatigue limit)"
    source_document = EN_1993_1_9_2005

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$\Delta\sigma_D$] Constant amplitude fatigue limit at [$N_D$] cycles [$MPa$].

        EN 1993-1-9:2005 - Chapter 7 - Fatigue strength (7.1(2), Figure 7.1)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from. Must have a constant amplitude fatigue limit;
            the shear curve (Figure 7.2) is not allowed.

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_c: MPA = delta_sigma_c
        self.curve: FatigueStrengthCurve = curve

    @staticmethod
    def _curve_value(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> Form7FatigueStrengthCurveValue:
        r"""Underlying power-law evaluation of [$\Delta\sigma_D$] from the detail category, reused for the value and its LaTeX."""
        if curve.n_d is None:
            raise ValueError(
                f"Curve {curve.name} has no constant amplitude fatigue limit (single-slope shear curve); "
                "the curve runs straight to its cut-off limit."
            )
        return Form7FatigueStrengthCurveValue(
            delta_sigma_ref=delta_sigma_c,
            n_ref=curve.n_c,
            n_target=curve.n_d,
            m=curve.m1,
            point="D",
            stress_type=curve.stress_type,
        )

    @staticmethod
    def _evaluate(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_c=delta_sigma_c)
        return float(Form7ConstantAmplitudeFatigueLimit._curve_value(delta_sigma_c, curve))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the constant amplitude fatigue limit."""
        return self._curve_value(self.delta_sigma_c, self.curve).latex(n=n)


class Form7CutOffLimit(Formula):
    r"""Class representing the cut-off limit [$\Delta\sigma_L$] (or [$\Delta\tau_L$]) at [$N_L$] cycles.

    For the direct stress curve (Figure 7.1) the cut-off limit is given in EN 1993-1-9:2005, 7.1(3) by scaling the
    constant amplitude fatigue limit [$\Delta\sigma_D$] along the second branch (slope [$m = 5$]):
    [$\Delta\sigma_L = \left( 5 / 100 \right)^{1/5} \Delta\sigma_D = 0.549 \: \Delta\sigma_D$].

    For the shear curve (Figure 7.2) the cut-off limit is given in 7.1(2) by scaling the detail category
    [$\Delta\tau_C$] along the single slope ([$m = 5$]):
    [$\Delta\tau_L = \left( 2 / 100 \right)^{1/5} \Delta\tau_C = 0.457 \: \Delta\tau_C$].
    """

    label = "Figures 7.1-7.2 (cut-off limit)"
    source_document = EN_1993_1_9_2005

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$\Delta\sigma_L$] Cut-off limit at [$N_L$] cycles [$MPa$].

        EN 1993-1-9:2005 - Chapter 7 - Fatigue strength (7.1(2) and 7.1(3), Figures 7.1 - 7.2)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For the shear curve this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 7.1 - 7.2).

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_c: MPA = delta_sigma_c
        self.curve: FatigueStrengthCurve = curve

    @staticmethod
    def _curve_value(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> Form7FatigueStrengthCurveValue:
        r"""Underlying power-law evaluation of [$\Delta\sigma_L$], reused for the value and its LaTeX.

        For the direct stress curve the cut-off limit follows from the constant amplitude fatigue limit along the
        second branch; for the single-slope shear curve it follows straight from the detail category.
        """
        if curve.n_d is not None and curve.m2 is not None:
            delta_sigma_d = float(Form7ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=curve))
            return Form7FatigueStrengthCurveValue(
                delta_sigma_ref=delta_sigma_d,
                n_ref=curve.n_d,
                n_target=curve.n_l,
                m=curve.m2,
                point="L",
                stress_type=curve.stress_type,
            )
        return Form7FatigueStrengthCurveValue(
            delta_sigma_ref=delta_sigma_c,
            n_ref=curve.n_c,
            n_target=curve.n_l,
            m=curve.m1,
            point="L",
            stress_type=curve.stress_type,
        )

    @staticmethod
    def _evaluate(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_c=delta_sigma_c)
        return float(Form7CutOffLimit._curve_value(delta_sigma_c, curve))

    def latex(self, n: int = 3) -> LatexFormula:
        r"""Returns LatexFormula object for the cut-off limit ([$\Delta\tau$] symbol for the shear curve)."""
        return self._curve_value(self.delta_sigma_c, self.curve).latex(n=n)
