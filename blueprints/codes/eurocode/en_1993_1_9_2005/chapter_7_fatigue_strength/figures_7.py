"""Fatigue strength curves from EN 1993-1-9:2005: Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)."""

from dataclasses import dataclass
from enum import Enum
from typing import Literal

from blueprints.codes.eurocode.en_1993_1_9_2005 import EN_1993_1_9_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative

# Number of cycles at the detail category reference point, shared by both fatigue strength curves [-].
N_C: DIMENSIONLESS = 2e6


class StressType(Enum):
    """Type of nominal stress range a fatigue strength curve applies to."""

    DIRECT = "direct stress"
    SHEAR = "shear stress"

    @property
    def symbol(self) -> str:
        r"""The stress symbol as it is rendered: [$\Delta\tau$] for shear, [$\Delta\sigma$] for direct stress."""
        return r"\Delta\tau" if self is StressType.SHEAR else r"\Delta\sigma"


class FatigueStrengthCurve(Enum):
    r"""Standard characteristic fatigue strength curves of EN 1993-1-9:2005, Figures 7.1 - 7.2.

    Each member bundles the fixed geometry of one curve: the slope [$m$] of the first branch, the
    number of cycles [$N_D$] at the constant amplitude fatigue limit (when one exists), the slope
    [$m$] of the second branch (when one exists) and the number of cycles [$N_L$] at the cut-off
    limit. The detail category reference point [$N_C$] is shared by both curves (see [$N_C$]).

    Every member is defined as a tuple ``(stress_type, description, m1, n_d, m2, n_l)``. For shear
    (Figure 7.2) there is a single slope running straight to the cut-off limit [$\Delta\tau_L$] at
    [$N_L$], so there is no constant amplitude fatigue limit and ``n_d`` and ``m2`` are ``None``.
    """

    FIG_7_1 = (StressType.DIRECT, "Direct stress ranges (Figure 7.1)", 3.0, 5e6, 5.0, 1e8)
    FIG_7_2 = (StressType.SHEAR, "Shear stress ranges (Figure 7.2)", 5.0, None, None, 1e8)

    def __init__(
        self,
        stress_type: StressType,
        description: str,
        m1: DIMENSIONLESS,
        n_d: DIMENSIONLESS | None,
        m2: DIMENSIONLESS | None,
        n_l: DIMENSIONLESS,
    ) -> None:
        self.stress_type = stress_type
        self.description = description
        self.m1 = m1
        self.n_d = n_d
        self.m2 = m2
        self.n_l = n_l

    @property
    def n_c(self) -> DIMENSIONLESS:
        """[$N_C$] Number of cycles at the detail category reference point [-]."""
        return N_C

    @property
    def has_constant_amplitude_fatigue_limit(self) -> bool:
        r"""Whether the curve has a constant amplitude fatigue limit [$\Delta\sigma_D$] at [$N_D$] cycles.

        ``False`` for the shear curve (Figure 7.2), which has a single slope running straight to its
        cut-off limit [$\Delta\tau_L$] at [$N_L$].
        """
        return self.n_d is not None


class Fig7ConstantAmplitudeFatigueLimit(Formula):
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
    def _evaluate(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(delta_sigma_c=delta_sigma_c)
        return _fatigue_limit_branch(delta_sigma_c, curve).value

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the constant amplitude fatigue limit."""
        return _stress_range_latex(
            branch=_fatigue_limit_branch(self.delta_sigma_c, self.curve),
            symbol=self.curve.stress_type.symbol,
            out_subscript="D",
            result=float(self),
            n=n,
        )


class Fig7CutOffLimit(Formula):
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
    def _evaluate(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(delta_sigma_c=delta_sigma_c)
        return _cut_off_branch(delta_sigma_c, curve).value

    def latex(self, n: int = 3) -> LatexFormula:
        r"""Returns LatexFormula object for the cut-off limit ([$\Delta\tau$] symbol for the shear curve)."""
        return _stress_range_latex(
            branch=_cut_off_branch(self.delta_sigma_c, self.curve),
            symbol=self.curve.stress_type.symbol,
            out_subscript="L",
            result=float(self),
            n=n,
        )


class Fig7NominalStressRange(Formula):
    r"""Class representing the nominal stress range [$\Delta\sigma_R$] (or [$\Delta\tau_R$]) a detail resists at a given number of cycles.

    This is the characteristic fatigue strength read off one of the standard fatigue strength curves of
    EN 1993-1-9:2005 (Figures 7.1 - 7.2, selected through ``curve``) at [$N$] cycles, scaled to the detail
    category [$\Delta\sigma_C$]. It answers which stress range a detail may carry for [$N$] cycles, and is the
    inverse of :class:`Fig7NumberOfCycles`. For direct stress (Figure 7.1) the extended curve of 7.1(3) is
    piecewise:

    - first branch (slope [$m = 3$]) for [$N \leq N_D$]: [$\Delta\sigma_R = \Delta\sigma_C \left( N_C / N \right)^{1 / m}$],
    - second branch (slope [$m = 5$]) for [$N_D < N \leq N_L$]: [$\Delta\sigma_R = \Delta\sigma_D \left( N_D / N \right)^{1 / m}$],
    - constant cut-off for [$N > N_L$]: [$\Delta\sigma_R = \Delta\sigma_L$].

    For shear (Figure 7.2, 7.1(2)) there is a single slope ([$m = 5$]) up to the cut-off limit [$\Delta\tau_L$] at
    [$N_L$], beyond which the strength is constant at [$\Delta\tau_L$].

    Note: the second branch of the direct stress curve belongs to the extended fatigue strength curves of 7.1(3),
    intended for stress spectra with ranges above and below the constant amplitude fatigue limit; under purely
    constant amplitude loading (7.1(2)) ranges below [$\Delta\sigma_D$] cause no fatigue damage. Also, only the curve
    relation itself is evaluated; no low-cycle bound (the curves are defined from about [$10^4$] cycles) and no static
    upper stress limit are enforced, so for [$N < N_C$] the first branch is extrapolated and returns
    [$\Delta\sigma_R > \Delta\sigma_C$].
    """

    label = "Figures 7.1-7.2 (nominal stress range)"
    source_document = EN_1993_1_9_2005

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve, n_cycles: DIMENSIONLESS) -> None:
        r"""[$\Delta\sigma_R$] Nominal stress range at [$N$] cycles on a standard fatigue strength curve [$MPa$].

        EN 1993-1-9:2005 - Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For the shear curve this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 7.1 - 7.2), fixing the slopes and the
            reference cycle numbers [$N_C$], [$N_D$], [$N_L$].
        n_cycles : DIMENSIONLESS
            [$N$] Number of cycles at which the nominal stress range is read [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_c: MPA = delta_sigma_c
        self.curve: FatigueStrengthCurve = curve
        self.n_cycles: DIMENSIONLESS = n_cycles

    @staticmethod
    def _evaluate(delta_sigma_c: MPA, curve: FatigueStrengthCurve, n_cycles: DIMENSIONLESS) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(delta_sigma_c=delta_sigma_c, n_cycles=n_cycles)
        return _branch_at_cycles(delta_sigma_c, curve, n_cycles).value

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the nominal stress range at the requested number of cycles."""
        return _stress_range_latex(
            branch=_branch_at_cycles(self.delta_sigma_c, self.curve, self.n_cycles),
            symbol=self.curve.stress_type.symbol,
            out_subscript="R",
            result=float(self),
            n=n,
        )


class Fig7NumberOfCycles(Formula):
    r"""Class representing the number of cycles to failure [$N_R$] for an applied stress range on a standard fatigue strength curve.

    This is the inverse of :class:`Fig7NominalStressRange`: given a constant-amplitude applied stress range
    [$\Delta\sigma_R$] (or [$\Delta\tau_R$]) and a detail category [$\Delta\sigma_C$], it returns the number of
    cycles [$N_R$] at which [$\Delta\sigma_R$] meets the characteristic fatigue strength curve (EN 1993-1-9:2005,
    Figures 7.1 - 7.2). It provides the denominator [$N_R$] of the partial damage [$n / N_R$] of a Palmgren-Miner
    accumulation (see Annex A). For direct stress (Figure 7.1) the extended curve of 7.1(3) is piecewise:

    - first branch (slope [$m = 3$]), [$\Delta\sigma_R \geq \Delta\sigma_D$]: [$N_R = N_C (\Delta\sigma_C / \Delta\sigma_R)^{m}$],
    - second branch (slope [$m = 5$]), [$\Delta\sigma_L \leq \Delta\sigma_R < \Delta\sigma_D$]: [$N_R = N_D (\Delta\sigma_D / \Delta\sigma_R)^{m}$],
    - below the cut-off limit, [$\Delta\sigma_R < \Delta\sigma_L$]: infinite life [$N_R = \infty$] (no fatigue damage).

    For shear (Figure 7.2) there is a single branch (slope [$m = 5$]) down to the cut-off limit [$\Delta\tau_L$], so
    any [$\Delta\tau_R < \Delta\tau_L$] gives infinite life.

    Note: the second branch of the direct stress curve belongs to the extended fatigue strength curves of 7.1(3),
    intended for stress spectra with ranges above and below the constant amplitude fatigue limit; under purely
    constant amplitude loading (7.1(2)) any [$\Delta\sigma_R < \Delta\sigma_D$] causes no fatigue damage.
    """

    label = "Figures 7.1-7.2 (number of cycles)"
    source_document = EN_1993_1_9_2005

    def __init__(self, delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$N_R$] Number of cycles to failure for an applied stress range on a standard fatigue strength curve [$-$].

        EN 1993-1-9:2005 - Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)

        Parameters
        ----------
        delta_sigma_r : MPA
            [$\Delta\sigma_R$] Applied constant-amplitude stress range to find the number of cycles for [$MPa$].
            For the shear curve this is the applied shear stress range [$\Delta\tau_R$].
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For the shear curve this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 7.1 - 7.2), fixing the slopes and the
            reference cycle numbers [$N_C$], [$N_D$], [$N_L$].

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_r: MPA = delta_sigma_r
        self.delta_sigma_c: MPA = delta_sigma_c
        self.curve: FatigueStrengthCurve = curve

    @staticmethod
    def _evaluate(delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_r=delta_sigma_r)
        raise_if_less_or_equal_to_zero(delta_sigma_c=delta_sigma_c)

        return _governing_branch(delta_sigma_r, delta_sigma_c, curve).value

    @property
    def detailed_result(self) -> dict:
        r"""Reference anchor of the governing branch, so callers can label [$N_R$] without re-deriving the branch.

        Returns
        -------
        dict
            ``reference_point`` ("C", "D" or "L"), the governing reference strength ``delta_sigma_ref`` [$MPa$]
            ([$\Delta\sigma_C$], [$\Delta\sigma_D$] or [$\Delta\sigma_L$]), its cycle number ``n_ref`` [$-$], the
            governing slope ``m`` [$-$] (``None`` below the cut-off) and the number of cycles ``n_r`` [$-$].
        """
        branch = _governing_branch(self.delta_sigma_r, self.delta_sigma_c, self.curve)
        return {
            "reference_point": branch.reference_point,
            "delta_sigma_ref": branch.delta_sigma_ref,
            "n_ref": branch.n_ref,
            "m": branch.m,
            "n_r": float(self),
        }

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the number of cycles at the applied stress range."""
        return _cycles_latex(
            branch=_governing_branch(self.delta_sigma_r, self.delta_sigma_c, self.curve),
            symbol=self.curve.stress_type.symbol,
            result=float(self),
            n=n,
        )


@dataclass(frozen=True)
class _StressRangeBranch:
    r"""A constant-slope branch of a fatigue strength curve, read from its anchor point towards a target cycle number.

    The anchor is a corner point of the curve, ([$N_C$], [$\Delta\sigma_C$]) or ([$N_D$], [$\Delta\sigma_D$]).
    ``target_symbol`` is how the target cycle number is written in the rendered equation: ``"N"`` for a free
    number of cycles, ``"N_{D}"`` or ``"N_{L}"`` for a corner of the curve.
    """

    reference_point: Literal["C", "D"]
    delta_sigma_ref: MPA
    n_ref: DIMENSIONLESS
    m: DIMENSIONLESS
    target_symbol: str
    target_n: DIMENSIONLESS

    @property
    def value(self) -> MPA:
        r"""[$\Delta\sigma_{ref} \left( N_{ref} / N_{target} \right)^{1 / m}$] Stress range at the target of this branch [$MPa$]."""
        return self.delta_sigma_ref * (self.n_ref / self.target_n) ** (1 / self.m)


@dataclass(frozen=True)
class _CyclesBranch:
    """A constant-slope branch of a fatigue strength curve, inverted to give the cycles at an applied stress range.

    Below the cut-off limit L the curve has no power-law relation, which is carried as ``m = None``.
    """

    reference_point: Literal["C", "D", "L"]
    delta_sigma_ref: MPA
    n_ref: DIMENSIONLESS
    m: DIMENSIONLESS | None
    delta_sigma_r: MPA

    @property
    def value(self) -> DIMENSIONLESS:
        r"""[$N_{ref} \left( \Delta\sigma_{ref} / \Delta\sigma_R \right)^{m}$] Number of cycles on this branch [$-$], infinite below the cut-off."""
        if self.m is None:
            return float("inf")
        return self.n_ref * (self.delta_sigma_ref / self.delta_sigma_r) ** self.m


def _fatigue_limit_branch(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> _StressRangeBranch:
    """The first branch, running from the detail category C down to the constant amplitude fatigue limit D.

    Raises
    ------
    ValueError
        If the curve has no constant amplitude fatigue limit (the single-slope shear curve of Figure 7.2).
    """
    if curve.n_d is None:
        raise ValueError(
            f"Curve {curve.name} has no constant amplitude fatigue limit (single-slope shear curve); the curve runs straight to its cut-off limit."
        )
    return _StressRangeBranch(
        reference_point="C",
        delta_sigma_ref=delta_sigma_c,
        n_ref=curve.n_c,
        m=curve.m1,
        target_symbol="N_{D}",
        target_n=curve.n_d,
    )


def _cut_off_branch(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> _StressRangeBranch:
    r"""The last branch, running down to the cut-off limit L at [$N_L$].

    For the direct stress curve this is the second branch, anchored at the constant amplitude fatigue limit D;
    for the single-slope shear curve it is the only branch, anchored at the detail category C.
    """
    if curve.n_d is None or curve.m2 is None:
        return _StressRangeBranch(
            reference_point="C",
            delta_sigma_ref=delta_sigma_c,
            n_ref=curve.n_c,
            m=curve.m1,
            target_symbol="N_{L}",
            target_n=curve.n_l,
        )
    return _StressRangeBranch(
        reference_point="D",
        delta_sigma_ref=_fatigue_limit_branch(delta_sigma_c, curve).value,
        n_ref=curve.n_d,
        m=curve.m2,
        target_symbol="N_{L}",
        target_n=curve.n_l,
    )


def _branch_at_cycles(delta_sigma_c: MPA, curve: FatigueStrengthCurve, n_cycles: DIMENSIONLESS) -> _StressRangeBranch:
    r"""The branch of ``curve`` that governs the nominal stress range at [$N$] cycles.

    Beyond the end of the curve the stress range stays constant, which is expressed by targeting the cut-off
    corner [$N_L$] instead of [$N$].
    """
    first_branch_end = curve.n_d if curve.n_d is not None else curve.n_l
    if n_cycles <= first_branch_end:
        # first branch, slope m1 (also covers N < N_C, where the branch is extrapolated)
        return _StressRangeBranch(
            reference_point="C",
            delta_sigma_ref=delta_sigma_c,
            n_ref=curve.n_c,
            m=curve.m1,
            target_symbol="N",
            target_n=n_cycles,
        )
    if curve.n_d is not None and curve.m2 is not None and n_cycles <= curve.n_l:
        # second branch, slope m2
        return _StressRangeBranch(
            reference_point="D",
            delta_sigma_ref=_fatigue_limit_branch(delta_sigma_c, curve).value,
            n_ref=curve.n_d,
            m=curve.m2,
            target_symbol="N",
            target_n=n_cycles,
        )
    return _cut_off_branch(delta_sigma_c, curve)


def _governing_branch(delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> _CyclesBranch:
    r"""The branch of ``curve`` that governs [$\Delta\sigma_R$].

    The fatigue strength curve is piecewise; the governing branch is the one whose stress range covers
    [$\Delta\sigma_R$]. Below the cut-off limit the life is infinite and there is no power-law relation to
    evaluate, which the returned branch carries as reference point "L" without a slope.
    """
    cut_off = _cut_off_branch(delta_sigma_c, curve)
    if delta_sigma_r < cut_off.value:
        return _CyclesBranch(
            reference_point="L",
            delta_sigma_ref=cut_off.value,
            n_ref=cut_off.target_n,
            m=None,
            delta_sigma_r=delta_sigma_r,
        )

    if curve.n_d is not None and curve.m2 is not None:
        delta_sigma_d = _fatigue_limit_branch(delta_sigma_c, curve).value
        if delta_sigma_r < delta_sigma_d:
            return _CyclesBranch(
                reference_point="D",
                delta_sigma_ref=delta_sigma_d,
                n_ref=curve.n_d,
                m=curve.m2,
                delta_sigma_r=delta_sigma_r,
            )

    return _CyclesBranch(
        reference_point="C",
        delta_sigma_ref=delta_sigma_c,
        n_ref=curve.n_c,
        m=curve.m1,
        delta_sigma_r=delta_sigma_r,
    )


def _stress_range_latex(branch: _StressRangeBranch, symbol: str, out_subscript: str, result: MPA, n: int) -> LatexFormula:
    """Renders a stress range read off ``branch``, labelled with ``out_subscript`` ("D", "L" or "R")."""
    ref = branch.reference_point
    return LatexFormula(
        return_symbol=rf"{symbol}_{{{out_subscript}}}",
        result=f"{result:.{n}f}",
        equation=rf"{symbol}_{{{ref}}} \left( \frac{{N_{{{ref}}}}}{{{branch.target_symbol}}} \right)^{{1 / m}}",
        numeric_equation=(
            rf"{branch.delta_sigma_ref:.{n}f} \left( \frac{{{latex_scientific(branch.n_ref)}}}{{{latex_scientific(branch.target_n)}}} \right)"
            rf"^{{1 / {branch.m:g}}}"
        ),
        comparison_operator_label="=",
        unit="MPa",
    )


def _cycles_latex(branch: _CyclesBranch, symbol: str, result: DIMENSIONLESS, n: int) -> LatexFormula:
    """Renders the number of cycles read off ``branch``; below the cut-off the life is infinite, so there is no fraction to evaluate."""
    if branch.m is None:
        return LatexFormula(return_symbol="N_{R}", result=r"\infty", comparison_operator_label="=")
    ref = branch.reference_point
    return LatexFormula(
        return_symbol="N_{R}",
        result=f"{result:.0f}",
        equation=rf"N_{{{ref}}} \left( \frac{{{symbol}_{{{ref}}}}}{{{symbol}_{{R}}}} \right)^{{m}}",
        numeric_equation=(
            rf"{latex_scientific(branch.n_ref)} \left( \frac{{{branch.delta_sigma_ref:.{n}f}}}{{{branch.delta_sigma_r:.{n}f}}} \right)"
            rf"^{{{branch.m:g}}}"
        ),
        comparison_operator_label="=",
    )
