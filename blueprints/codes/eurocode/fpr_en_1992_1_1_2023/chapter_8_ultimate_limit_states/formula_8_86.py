"""Formula 8.86 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable, Sequence

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_lists_differ_in_length, raise_if_negative


class Form8Dot86CheckInteractionInternalForces(ComparisonFormula):
    r"""Class representing formula 8.86 for the simplified and conservative verification of a cross-section
    subjected to a combination of internal forces.

    Each term of the sum is the ratio of one individual design action to the corresponding individual design
    resistance of the cross-section, for example the design torsional moment over the pure design torsional
    resistance of 8.3.4, or the design shear stress over the shear stress resistance. The pair of a term therefore
    carries the unit of the internal force it belongs to, and the terms of the sum need not share that unit, which
    is why the actions and the resistances are plain floats here instead of one of the unit type aliases.

    ``unity_check`` is the sum itself, since the right-hand side of the criterion is 1,0.

    Paragraph 8.3.6(2) allows the ratios for shear actions and for the corresponding bending moments to be left out
    of the same sum, under the condition stated there, and to be verified as two separate combinations instead.
    Which internal forces enter one instance of this check is therefore a decision of the caller, made by choosing
    what to pass in.
    """

    label = "8.86"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, s_ed: Sequence[float], s_rd: Sequence[float]) -> None:
        r"""Check whether the sum of the ratios of the individual design actions to their corresponding individual
        design resistances does not exceed 1,0.

        FprEN 1992-1-1:2023 (E) art. 8.3.6(1) - Formula (8.86)

        Parameters
        ----------
        s_ed : Sequence[float]
            [$S_{Ed}$] Individual design actions of the cross-section, one per internal force considered, in the
            same order as their resistances. Pass magnitudes: a term of this sum is a utilisation, so a negative
            value would relieve the criterion instead of loading it [$unit of the internal force considered$].
        s_rd : Sequence[float]
            [$S_{Rd}$] Corresponding individual design resistances of the cross-section, one per internal force
            considered (e.g. design torsional moment and pure design torsional resistance (refer to 8.3.4),
            design bending moment and pure design bending moment resistance and design shear stress and shear
            stress resistance) [$unit of the internal force considered$].
        """
        super().__init__()
        self.s_ed = tuple(s_ed)
        self.s_rd = tuple(s_rd)

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(s_ed: Sequence[float], s_rd: Sequence[float], *_args, **_kwargs) -> float:
        """Evaluates the sum of the ratios, for more information see the __init__ method."""
        raise_if_lists_differ_in_length(s_ed=s_ed, s_rd=s_rd)
        if not s_ed:
            raise ValueError("At least one internal force must be considered, so s_ed and s_rd cannot be empty.")
        raise_if_negative(min_s_ed=min(s_ed))
        raise_if_less_or_equal_to_zero(min_s_rd=min(s_rd))

        return float(sum(action / resistance for action, resistance in zip(s_ed, s_rd)))

    @staticmethod
    def _evaluate_rhs(*_args, **_kwargs) -> float:
        """Evaluates the limit of the linear criterion, for more information see the __init__ method."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.86."""
        _equation: str = r"\sum \left( \frac{S_{Ed}}{S_{Rd}} \right)_{i} \leq 1.0"
        _terms: str = " + ".join(rf"\frac{{{action:.{n}f}}}{{{resistance:.{n}f}}}" for action, resistance in zip(self.s_ed, self.s_rd))
        _numeric_equation: str = rf"{_terms} \leq 1.0"
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label=r"\to",
            unit="",
        )
