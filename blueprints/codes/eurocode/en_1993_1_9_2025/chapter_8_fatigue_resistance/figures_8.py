"""Fatigue strength curves from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)."""

from dataclasses import dataclass
from enum import Enum
from typing import Literal

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative

# Number of cycles at the detail category reference point, shared by every fatigue strength curve [-].
N_C: DIMENSIONLESS = 2e6


class StressType(Enum):
    """Type of nominal stress range a fatigue strength curve applies to."""

    NORMAL = "normal stress"  # [$\Delta\sigma$]
    SHEAR = "shear stress"  # [$\Delta\tau$]


class FatigueStrengthCurve(Enum):
    r"""Standard characteristic fatigue strength curves of EN 1993-1-9:2025, Figures 8.1 - 8.4.

    Each member bundles the fixed geometry of one curve: the slope [$m_1$] of the first branch, the
    number of cycles [$N_D$] at the constant amplitude fatigue limit, and (when a second branch exists)
    the slope [$m_2$] and the number of cycles [$N_L$] at the cut-off limit. The detail category reference
    point [$N_C$] is shared by all curves (see [$N_C$]).

    Every member is defined as a tuple ``(stress_type, description, m1, n_d, m2, n_l)``. For shear
    (Figure 8.4) there is a single slope and no separate cut-off branch, so ``m2`` and ``n_l`` are ``None``.
    """

    FIG_8_1A = (StressType.NORMAL, "Non-welded details, light notch effect (Figure 8.1a)", 5.0, 2e6, 9.0, 1e8)
    FIG_8_1B = (StressType.NORMAL, "Non-welded details, sharp notch effect (Figure 8.1b)", 3.0, 2e6, 5.0, 1e8)
    FIG_8_2A = (StressType.NORMAL, "Welded details, detail category 71 and above (Figure 8.2a)", 3.0, 5e6, 5.0, 1e8)
    FIG_8_2B = (StressType.NORMAL, "Welded details, detail category below 71 (Figure 8.2b)", 3.0, 1e7, 5.0, 1e8)
    FIG_8_3 = (StressType.NORMAL, "Lattice girder joints of hollow sections, Table 10.8 (Figure 8.3)", 5.0, 1e7, 9.0, 1e8)
    FIG_8_4 = (StressType.SHEAR, "Constructional details subject to shear stress (Figure 8.4)", 5.0, 1e8, None, None)

    def __init__(
        self,
        stress_type: StressType,
        description: str,
        m1: DIMENSIONLESS,
        n_d: DIMENSIONLESS,
        m2: DIMENSIONLESS | None,
        n_l: DIMENSIONLESS | None,
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
    def has_cutoff_segment(self) -> bool:
        r"""Whether the curve has a second branch ending at a separate cut-off limit [$\Delta\sigma_L$].

        ``False`` for the shear curve (Figure 8.4), which has a single slope and whose constant amplitude
        fatigue limit [$\Delta\tau_D$] is also its cut-off limit.
        """
        return self.m2 is not None


class Fig8ConstantAmplitudeFatigueLimit(Formula):
    r"""Class representing the constant amplitude fatigue limit [$\Delta\sigma_D$] at [$N_D$] cycles.

    The constant amplitude fatigue limit is read off the standard fatigue strength curve (EN 1993-1-9:2025,
    Figures 8.1 - 8.4) at [$N_D$], by scaling the detail category [$\Delta\sigma_C$] along the first branch
    (slope [$m_1$]): [$\Delta\sigma_D = \Delta\sigma_C \left( N_C / N_D \right)^{1 / m_1}$]. For shear curves
    (Figure 8.4) this is the shear constant amplitude fatigue limit [$\Delta\tau_D$].
    """

    label = "Figures 8.1-8.4 (constant amplitude fatigue limit)"
    source_document = EN_1993_1_9_2025

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$\Delta\sigma_D$] Constant amplitude fatigue limit at [$N_D$] cycles [$MPa$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For shear curves this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4).

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
        r"""Returns LatexFormula object for the constant amplitude fatigue limit ([$\Delta\tau$] symbol for shear curves)."""
        return _stress_range_latex(
            branch=_fatigue_limit_branch(self.delta_sigma_c, self.curve),
            symbol=_stress_symbol(self.curve.stress_type),
            out_subscript="D",
            result=float(self),
            n=n,
        )


class Fig8CutOffLimit(Formula):
    r"""Class representing the cut-off limit [$\Delta\sigma_L$] at [$N_L$] cycles.

    The cut-off limit is read off the standard fatigue strength curve (EN 1993-1-9:2025, Figures 8.1 - 8.4) at
    [$N_L$], by scaling the constant amplitude fatigue limit [$\Delta\sigma_D$] along the second branch
    (slope [$m_2$]): [$\Delta\sigma_L = \Delta\sigma_D \left( N_D / N_L \right)^{1 / m_2}$].

    Only curves with a second branch have a separate cut-off limit. The shear curve (Figure 8.4) has a single
    slope and its constant amplitude fatigue limit [$\Delta\tau_D$] also acts as the cut-off, so this formula is
    not defined for it (see :attr:`FatigueStrengthCurve.has_cutoff_segment`).
    """

    label = "Figures 8.1-8.4 (cut-off limit)"
    source_document = EN_1993_1_9_2025

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$\Delta\sigma_L$] Cut-off limit at [$N_L$] cycles [$MPa$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4). Must have a separate
            cut-off branch; the shear curve (Figure 8.4) is not allowed.

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
        """Returns LatexFormula object for the cut-off limit."""
        return _stress_range_latex(
            branch=_cut_off_branch(self.delta_sigma_c, self.curve),
            symbol=_stress_symbol(self.curve.stress_type),
            out_subscript="L",
            result=float(self),
            n=n,
        )


class Fig8NominalStressRange(Formula):
    r"""Class representing the nominal stress range [$\Delta\sigma_R$] (or [$\Delta\tau_R$]) a detail resists at a given number of cycles.

    This is the characteristic fatigue strength read off one of the standard fatigue strength curves of
    EN 1993-1-9:2025 (Figures 8.1 - 8.4, selected through ``curve``) at [$N$] cycles, scaled to the detail
    category [$\Delta\sigma_C$]. It answers which stress range a detail may carry for [$N$] cycles, and is the
    inverse of :class:`Fig8NumberOfCycles`. The curve is piecewise:

    - first branch (slope [$m_1$]) for [$N \leq N_D$]: [$\Delta\sigma_R = \Delta\sigma_C \left( N_C / N \right)^{1 / m_1}$],
    - second branch (slope [$m_2$]) for [$N_D < N \leq N_L$]: [$\Delta\sigma_R = \Delta\sigma_D \left( N_D / N \right)^{1 / m_2}$],
    - constant cut-off for [$N > N_L$]: [$\Delta\sigma_R = \Delta\sigma_L$].

    For the shear curve (Figure 8.4) there is a single slope and the constant amplitude fatigue limit [$\Delta\tau_D$]
    also acts as the cut-off for [$N > N_D$].

    Note: only the curve relation itself is evaluated; no low-cycle bound (the curves are defined from about
    [$10^4$] cycles) and no static upper stress limit are enforced, so for [$N < N_C$] the first branch is
    extrapolated and returns [$\Delta\sigma_R > \Delta\sigma_C$].
    """

    label = "Figures 8.1-8.4 (nominal stress range)"
    source_document = EN_1993_1_9_2025

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve, n_cycles: DIMENSIONLESS) -> None:
        r"""[$\Delta\sigma_R$] Nominal stress range at [$N$] cycles on a standard fatigue strength curve [$MPa$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For shear curves this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4), fixing the slopes
            [$m_1$], [$m_2$] and the reference cycle numbers [$N_C$], [$N_D$], [$N_L$].
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
            symbol=_stress_symbol(self.curve.stress_type),
            out_subscript="R",
            result=float(self),
            n=n,
        )


class Fig8NumberOfCycles(Formula):
    r"""Class representing the number of cycles to failure [$N_R$] for an applied stress range on a standard fatigue strength curve.

    This is the inverse of :class:`Fig8NominalStressRange`: given a constant-amplitude applied stress range
    [$\Delta\sigma_R$] (or [$\Delta\tau_R$]) and a detail category [$\Delta\sigma_C$], it returns the number of
    cycles [$N_R$] at which [$\Delta\sigma_R$] meets the characteristic fatigue strength curve (EN 1993-1-9:2025,
    Figures 8.1 - 8.4). It provides the denominator [$N_R$] of the partial damage [$n / N_R$] of a Palmgren-Miner
    accumulation. The curve is piecewise:

    - first branch (slope [$m_1$]), [$\Delta\sigma_R \geq \Delta\sigma_D$]: [$N_R = N_C (\Delta\sigma_C / \Delta\sigma_R)^{m_1}$],
    - second branch (slope [$m_2$]), [$\Delta\sigma_L \leq \Delta\sigma_R < \Delta\sigma_D$]: [$N_R = N_D (\Delta\sigma_D / \Delta\sigma_R)^{m_2}$],
    - below the cut-off limit, [$\Delta\sigma_R < \Delta\sigma_L$]: infinite life [$N_R = \infty$] (no fatigue damage).

    For the shear curve (Figure 8.4) there is a single slope and the constant amplitude fatigue limit [$\Delta\tau_D$]
    acts as the cut-off, so any [$\Delta\tau_R < \Delta\tau_D$] gives infinite life.
    """

    label = "Figures 8.1-8.4 (number of cycles)"
    source_document = EN_1993_1_9_2025

    def __init__(self, delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$N_R$] Number of cycles to failure for an applied stress range on a standard fatigue strength curve [$-$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)

        Parameters
        ----------
        delta_sigma_r : MPA
            [$\Delta\sigma_R$] Applied constant-amplitude stress range to find the number of cycles for [$MPa$].
            For shear curves this is the applied shear stress range [$\Delta\tau_R$].
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For shear curves this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4), fixing the slopes
            [$m_1$], [$m_2$] and the reference cycle numbers [$N_C$], [$N_D$], [$N_L$].

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

        branch = _governing_branch(delta_sigma_r, delta_sigma_c, curve)
        if branch is None:
            # below the cut-off limit: infinite life, no damage
            return float("inf")
        return branch.value

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
        if branch is None:
            delta_sigma_ref, n_ref = _cutoff_anchor(self.delta_sigma_c, self.curve)
            return {"reference_point": "L", "delta_sigma_ref": delta_sigma_ref, "n_ref": n_ref, "m": None, "n_r": float(self)}
        return {
            "reference_point": branch.reference_point,
            "delta_sigma_ref": branch.delta_sigma_ref,
            "n_ref": branch.n_ref,
            "m": branch.m,
            "n_r": float(self),
        }

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the number of cycles at the applied stress range."""
        branch = _governing_branch(self.delta_sigma_r, self.delta_sigma_c, self.curve)
        if branch is None:
            # below the cut-off limit: the life is infinite, so there is no fraction to evaluate
            return LatexFormula(return_symbol="N_{R}", result=r"\infty", comparison_operator_label="=")
        return _cycles_latex(branch=branch, symbol=_stress_symbol(self.curve.stress_type), result=float(self), n=n)


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
    slope_subscript: Literal["1", "2"]
    target_symbol: str
    target_n: DIMENSIONLESS

    @property
    def value(self) -> MPA:
        r"""[$\Delta\sigma_{ref} \left( N_{ref} / N_{target} \right)^{1 / m}$] Stress range at the target of this branch [$MPa$]."""
        return self.delta_sigma_ref * (self.n_ref / self.target_n) ** (1 / self.m)


@dataclass(frozen=True)
class _CyclesBranch:
    """A constant-slope branch of a fatigue strength curve, inverted to give the cycles at an applied stress range."""

    reference_point: Literal["C", "D"]
    delta_sigma_ref: MPA
    n_ref: DIMENSIONLESS
    m: DIMENSIONLESS
    slope_subscript: Literal["1", "2"]
    delta_sigma_r: MPA

    @property
    def value(self) -> DIMENSIONLESS:
        r"""[$N_{ref} \left( \Delta\sigma_{ref} / \Delta\sigma_R \right)^{m}$] Number of cycles on this branch [$-$]."""
        return self.n_ref * (self.delta_sigma_ref / self.delta_sigma_r) ** self.m


def _fatigue_limit_branch(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> _StressRangeBranch:
    """The first branch, running from the detail category C down to the constant amplitude fatigue limit D."""
    return _StressRangeBranch(
        reference_point="C",
        delta_sigma_ref=delta_sigma_c,
        n_ref=curve.n_c,
        m=curve.m1,
        slope_subscript="1",
        target_symbol="N_{D}",
        target_n=curve.n_d,
    )


def _cut_off_branch(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> _StressRangeBranch:
    """The second branch, running from the constant amplitude fatigue limit D down to the cut-off limit L.

    Raises
    ------
    ValueError
        If the curve has no second branch (the single-slope shear curve of Figure 8.4).
    """
    if curve.m2 is None or curve.n_l is None:
        raise ValueError(
            f"Curve {curve.name} has no separate cut-off limit (single-slope shear curve); its constant amplitude fatigue limit acts as the cut-off."
        )
    return _StressRangeBranch(
        reference_point="D",
        delta_sigma_ref=_fatigue_limit_branch(delta_sigma_c, curve).value,
        n_ref=curve.n_d,
        m=curve.m2,
        slope_subscript="2",
        target_symbol="N_{L}",
        target_n=curve.n_l,
    )


def _branch_at_cycles(delta_sigma_c: MPA, curve: FatigueStrengthCurve, n_cycles: DIMENSIONLESS) -> _StressRangeBranch:
    r"""The branch of ``curve`` that governs the nominal stress range at [$N$] cycles.

    Beyond the end of the curve the stress range stays constant, which is expressed by targeting the last corner
    ([$N_L$], or [$N_D$] for the single-slope shear curve) instead of [$N$].
    """
    if n_cycles <= curve.n_d:
        # first branch, slope m1 (also covers N < N_C, where the branch is extrapolated)
        return _StressRangeBranch(
            reference_point="C",
            delta_sigma_ref=delta_sigma_c,
            n_ref=curve.n_c,
            m=curve.m1,
            slope_subscript="1",
            target_symbol="N",
            target_n=n_cycles,
        )
    if curve.m2 is None or curve.n_l is None:
        # shear curve: single slope, constant at the fatigue limit beyond N_D
        return _fatigue_limit_branch(delta_sigma_c, curve)
    beyond_cut_off = n_cycles > curve.n_l
    return _StressRangeBranch(
        reference_point="D",
        delta_sigma_ref=_fatigue_limit_branch(delta_sigma_c, curve).value,
        n_ref=curve.n_d,
        m=curve.m2,
        slope_subscript="2",
        target_symbol="N_{L}" if beyond_cut_off else "N",
        target_n=curve.n_l if beyond_cut_off else n_cycles,
    )


def _governing_branch(delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> _CyclesBranch | None:
    r"""The branch of ``curve`` that governs [$\Delta\sigma_R$], or ``None`` below the cut-off.

    The fatigue strength curve is piecewise; the governing branch is the one whose stress range covers
    [$\Delta\sigma_R$]. ``None`` signals the branch below the cut-off limit, where the life is infinite and there
    is no power-law relation to evaluate.
    """
    delta_sigma_d = _fatigue_limit_branch(delta_sigma_c, curve).value
    if delta_sigma_r >= delta_sigma_d:
        # first branch (slope m1), anchored at the detail category point (N_C, Δσ_C)
        return _CyclesBranch(
            reference_point="C",
            delta_sigma_ref=delta_sigma_c,
            n_ref=curve.n_c,
            m=curve.m1,
            slope_subscript="1",
            delta_sigma_r=delta_sigma_r,
        )
    if curve.m2 is not None and curve.n_l is not None and delta_sigma_r >= _cut_off_branch(delta_sigma_c, curve).value:
        # second branch (slope m2), anchored at the constant amplitude fatigue limit point (N_D, Δσ_D)
        return _CyclesBranch(
            reference_point="D",
            delta_sigma_ref=delta_sigma_d,
            n_ref=curve.n_d,
            m=curve.m2,
            slope_subscript="2",
            delta_sigma_r=delta_sigma_r,
        )
    # below the cut-off limit Δσ_L (or below Δτ_D for the single-slope shear curve): infinite life, no damage
    return None


def _cutoff_anchor(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> tuple[MPA, DIMENSIONLESS]:
    r"""Reference strength and cycle number of the cut-off point, below which the life is infinite.

    For curves with a second branch this is the cut-off limit [$(\Delta\sigma_L, N_L)$]; for the single-slope
    shear curve it is the constant amplitude fatigue limit [$(\Delta\tau_D, N_D)$], which also acts as the cut-off.
    """
    branch = _cut_off_branch(delta_sigma_c, curve) if curve.has_cutoff_segment else _fatigue_limit_branch(delta_sigma_c, curve)
    return branch.value, branch.target_n


def _stress_symbol(stress_type: StressType) -> str:
    r"""The rendered stress symbol of a curve: [$\Delta\tau$] for shear, [$\Delta\sigma$] otherwise."""
    return r"\Delta\tau" if stress_type == StressType.SHEAR else r"\Delta\sigma"


def _slope_latex(m: DIMENSIONLESS, n: int) -> str:
    """The slope as it appears in an exponent; the slopes are integers (3, 5, 9), so trailing zeros are stripped."""
    text = f"{m:.{n}f}"
    return text.rstrip("0").rstrip(".") if "." in text else text


def _stress_range_latex(branch: _StressRangeBranch, symbol: str, out_subscript: str, result: MPA, n: int) -> LatexFormula:
    """Renders a stress range read off ``branch``, labelled with ``out_subscript`` ("D", "L" or "R")."""
    ref = branch.reference_point
    return LatexFormula(
        return_symbol=rf"{symbol}_{{{out_subscript}}}",
        result=f"{result:.{n}f}",
        equation=rf"{symbol}_{{{ref}}} \left( \frac{{N_{{{ref}}}}}{{{branch.target_symbol}}} \right)^{{1 / m_{{{branch.slope_subscript}}}}}",
        numeric_equation=(
            rf"{branch.delta_sigma_ref:.{n}f} \left( \frac{{{latex_scientific(branch.n_ref)}}}{{{latex_scientific(branch.target_n)}}} \right)"
            rf"^{{1 / {_slope_latex(branch.m, n)}}}"
        ),
        comparison_operator_label="=",
        unit="MPa",
    )


def _cycles_latex(branch: _CyclesBranch, symbol: str, result: DIMENSIONLESS, n: int) -> LatexFormula:
    """Renders the number of cycles read off ``branch`` for the applied stress range it carries."""
    ref = branch.reference_point
    return LatexFormula(
        return_symbol="N_{R}",
        result=f"{result:.0f}",
        equation=rf"N_{{{ref}}} \left( \frac{{{symbol}_{{{ref}}}}}{{{symbol}_{{R}}}} \right)^{{m_{{{branch.slope_subscript}}}}}",
        numeric_equation=(
            rf"{latex_scientific(branch.n_ref)} \left( \frac{{{branch.delta_sigma_ref:.{n}f}}}{{{branch.delta_sigma_r:.{n}f}}} \right)"
            rf"^{{{_slope_latex(branch.m, n)}}}"
        ),
        comparison_operator_label="=",
    )
