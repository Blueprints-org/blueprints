"""Formula 8.5, 8.6, 8.7 and 8.8 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM


class Form8Dot5To8DesignMomentsForOrthogonalReinforcement(Formula):
    r"""Class representing formulas 8.5, 8.6, 8.7 and 8.8 for the calculation of the design moments an
    orthogonally reinforced solid slab element with bending and torsional moments shall be designed for.
    """

    label = "8.5/8.6/8.7/8.8"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        m_edx: NMM,
        m_edy: NMM,
        m_edxy: NMM,
        is_x_direction: bool,
        is_primed: bool,
    ) -> None:
        r"""[$m_{Rdx}$], [$m_{Rdy}$], [$m_{Rdx}'$] or [$m_{Rdy}'$] Design moment for the reinforcement in local
        axis [$x$] or [$y$], on the unprimed or primed face [$Nmm$].

        FprEN 1992-1-1:2023 (E) art. 8.1.3(1) - Formula (8.5), (8.6), (8.7) and (8.8)

        Applies to orthogonally reinforced solid slab elements with bending and torsional moments where
        [$\left|m_{Edxy}\right| \leq 0{,}07 \cdot d^2 \cdot f_{cd}$]; that condition of application is not
        enforced here. [$x$] and [$y$] are local axes parallel to the reinforcement.

        Parameters
        ----------
        m_edx : NMM
            [$m_{Edx}$] Design bending moment about the local [$x$] axis. Only used when [$is\_x\_direction$]
            is True [$Nmm$].
        m_edy : NMM
            [$m_{Edy}$] Design bending moment about the local [$y$] axis. Only used when [$is\_x\_direction$]
            is False [$Nmm$].
        m_edxy : NMM
            [$m_{Edxy}$] Design torsional moment. Only its magnitude is used, so it may be passed
            signed [$Nmm$].
        is_x_direction : bool
            True to compute the design moment for the local [$x$] direction ([$m_{Rdx}$] or [$m_{Rdx}'$]),
            False for the local [$y$] direction ([$m_{Rdy}$] or [$m_{Rdy}'$]).
        is_primed : bool
            True to compute the design moment on the primed face ([$m_{Rdx}'$] or [$m_{Rdy}'$]), False for
            the unprimed face ([$m_{Rdx}$] or [$m_{Rdy}$]).
        """
        super().__init__()
        self.m_edx = m_edx
        self.m_edy = m_edy
        self.m_edxy = m_edxy
        self.is_x_direction = is_x_direction
        self.is_primed = is_primed

    @staticmethod
    def _evaluate(
        m_edx: NMM,
        m_edy: NMM,
        m_edxy: NMM,
        is_x_direction: bool,
        is_primed: bool,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        m_ed = m_edx if is_x_direction else m_edy
        sign = -1 if is_primed else 1
        return sign * m_ed + abs(m_edxy)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 8.5, 8.6, 8.7 and 8.8."""
        m_ed_symbol = r"m_{Edx}" if self.is_x_direction else r"m_{Edy}"
        return_symbol = ("m_{Rdx}" if self.is_x_direction else "m_{Rdy}") + ("'" if self.is_primed else "")
        sign_symbol = "-" if self.is_primed else ""
        m_ed = self.m_edx if self.is_x_direction else self.m_edy

        _equation: str = rf"{sign_symbol}{m_ed_symbol} + \left|m_{{Edxy}}\right|"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                m_ed_symbol: f"{m_ed:.{n}f}",
                r"m_{Edxy}": f"{self.m_edxy:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                m_ed_symbol: rf"{m_ed:.{n}f} \ Nmm",
                r"m_{Edxy}": rf"{self.m_edxy:.{n}f} \ Nmm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=return_symbol,
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )
