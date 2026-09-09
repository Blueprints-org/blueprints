"""Formula 8.122 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM2, MPA, N
from blueprints.validations import raise_if_negative


class Form8Dot122CheckTieResistance(ComparisonFormula):
    r"""Class representing formula 8.122 for the verification of the resistance of a tie.

    8.5.3(1) introduces this as "The resistance of a tie [$F_{Rd}$] shall fulfil the following condition",
    so the relation is a verification that passes or fails and not a value to be clamped.
    """

    label = "8.122"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, f_td: N, a_s: MM2, f_yd: MPA, a_p: MM2, f_pd: MPA) -> None:
        r"""Verify the design tensile force in a tie against its resistance.

        FprEN 1992-1-1:2023 (E) art 8.5.3 (1) - Formula (8.122)

        Parameters
        ----------
        f_td : N
            [$F_{td}$] Design value of the tensile force in the tie [$N$].
        a_s : MM2
            [$A_s$] Cross-sectional area of the reinforcement of the tie [$mm^2$].
        f_yd : MPA
            [$f_{yd}$] Design value of the yield strength of the reinforcement [$MPa$].
        a_p : MM2
            [$A_p$] Cross-sectional area of the prestressed reinforcement of the tie [$mm^2$].
        f_pd : MPA
            [$f_{pd}$] Design value of the strength of the prestressed reinforcement. If prestressed
            reinforcement is considered as an external action, [$f_{pd}$] should be replaced by
            [$f_{pd} - \sigma_{pd}$] according to 7.6.5(1) [$MPa$].
        """
        super().__init__()
        self.f_td = f_td
        self.a_s = a_s
        self.f_yd = f_yd
        self.a_p = a_p
        self.f_pd = f_pd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(f_td: N, *_args, **_kwargs) -> float:
        """Evaluates the design tensile force, for more information see the __init__ method."""
        raise_if_negative(f_td=f_td)

        return float(f_td)

    @staticmethod
    def _evaluate_rhs(a_s: MM2, f_yd: MPA, a_p: MM2, f_pd: MPA, *_args, **_kwargs) -> float:
        """Evaluates the resistance of the tie, for more information see the __init__ method."""
        raise_if_negative(a_s=a_s, f_yd=f_yd, a_p=a_p, f_pd=f_pd)

        return float(a_s * f_yd + a_p * f_pd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.122."""
        _equation: str = r"F_{td} \leq A_s \cdot f_{yd} + A_p \cdot f_{pd}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_{td}": f"{self.f_td:.{n}f}",
                r"A_s": f"{self.a_s:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
                r"A_p": f"{self.a_p:.{n}f}",
                r"f_{pd}": f"{self.f_pd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_{td}": rf"{self.f_td:.{n}f} \ N",
                r"A_s": rf"{self.a_s:.{n}f} \ mm^2",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
                r"A_p": rf"{self.a_p:.{n}f} \ mm^2",
                r"f_{pd}": rf"{self.f_pd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )
