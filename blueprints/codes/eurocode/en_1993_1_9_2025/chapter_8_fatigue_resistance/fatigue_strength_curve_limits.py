"""Fatigue strength curve limits from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)."""

from dataclasses import dataclass, field

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength import Form8FatigueStrength
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_value import Form8FatigueStrengthCurveValue
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


@dataclass(frozen=True)
class FatigueStrengthCurveLimits:
    r"""Characteristic fatigue strength limits of a standard fatigue strength curve (EN 1993-1-9:2025, Figures 8.1 - 8.4).

    Given a detail category [$\Delta\sigma_C$] and a selected curve, this exposes the constant amplitude fatigue
    limit [$\Delta\sigma_D$] and the cut-off limit [$\Delta\sigma_L$] directly, and acts as the single entry point
    to evaluate the fatigue strength [$\Delta\sigma_R$] at any number of cycles via :meth:`fatigue_strength`.

    Parameters
    ----------
    delta_sigma_c : MPA
        [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
        For shear curves this is the shear detail category [$\Delta\tau_C$].
    curve : FatigueStrengthCurve
        The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4).

    Methods
    -------
    delta_sigma_d : MPA
        Returns the constant amplitude fatigue limit [$\Delta\sigma_D$] at [$N_D$].
    delta_sigma_l : MPA | None
        Returns the cut-off limit [$\Delta\sigma_L$] at [$N_L$], or ``None`` for the shear curve, which has no
        separate cut-off branch.
    fatigue_strength : Form8FatigueStrength
        Returns the fatigue strength [$\Delta\sigma_R$] at a given number of cycles.
    """

    delta_sigma_c: MPA
    curve: FatigueStrengthCurve
    label: str = field(init=False, default="Figures 8.1-8.4 (fatigue strength curve limits)")
    source_document: str = field(init=False, default=EN_1993_1_9_2025)

    def __post_init__(self) -> None:
        """Validates the detail category."""
        raise_if_negative(delta_sigma_c=self.delta_sigma_c)

    @property
    def delta_sigma_d(self) -> MPA:
        r"""[$\Delta\sigma_D$] Constant amplitude fatigue limit at [$N_D$] [$MPa$]."""
        return Form8FatigueStrengthCurveValue(
            delta_sigma_ref=self.delta_sigma_c,
            n_ref=self.curve.n_c,
            n_target=self.curve.n_d,
            m=self.curve.m1,
            point="D",
        )

    @property
    def delta_sigma_l(self) -> MPA | None:
        r"""[$\Delta\sigma_L$] Cut-off limit at [$N_L$] [$MPa$], or ``None`` for the shear curve (no separate cut-off branch)."""
        if self.curve.m2 is None or self.curve.n_l is None:
            return None
        return Form8FatigueStrengthCurveValue(
            delta_sigma_ref=self.delta_sigma_d,
            n_ref=self.curve.n_d,
            n_target=self.curve.n_l,
            m=self.curve.m2,
            point="L",
        )

    def fatigue_strength(self, n_cycles: DIMENSIONLESS) -> Form8FatigueStrength:
        r"""[$\Delta\sigma_R$] Fatigue strength at ``n_cycles`` on this curve [$MPa$].

        Parameters
        ----------
        n_cycles : DIMENSIONLESS
            [$N$] Number of cycles at which the fatigue strength is evaluated [$-$].

        Returns
        -------
        Form8FatigueStrength
            The fatigue strength evaluator (a ``float`` carrying the value and a ``latex`` representation).
        """
        return Form8FatigueStrength(delta_sigma_c=self.delta_sigma_c, curve=self.curve, n_cycles=n_cycles)
