"""Formula 8.64 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MPA, NMM_MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot64ShearStressResistanceWithTransverseBending(Formula):
    """Class representing formula 8.64 for the calculation of the shear stress resistance reduced by the
    influence of transverse bending.
    """

    label = "8.64"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, tau_rd: MPA, m_ed: NMM_MM, m_rd: NMM_MM) -> None:
        r"""[$\tau_{Rdm}$] Shear stress resistance reduced by the influence of transverse bending [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.4 (2) - Formula (8.64)

        The standard offers this in case of shear reinforcement perpendicular to the longitudinal axis of the
        member and symmetric to the web middle plane, and states that Annex G may be used as an alternative.
        It also allows the interaction to be disregarded altogether where
        [$\tau_{Ed}/\tau_{Rd} < 0,2$] or [$m_{Ed}/m_{Rd} < 0,1$], see 8.2.4(1). Those are conditions of
        application rather than bounds on the result, so none of them is enforced here.

        Parameters
        ----------
        tau_rd : MPA
            [$\tau_{Rd}$] Shear resistance according to the formula in 8.2.3(5), NOTE 1 [$MPa$].
        m_ed : NMM_MM
            [$m_{Ed}$] Transverse bending moment per unit width of the web, see Figure 8.12. The standard
            prints no unit for it; the lower case m marks it as a moment per unit width rather than a sectional
            moment, which is also what makes it commensurable with the shear stress it interacts with. Only its
            ratio to [$m_{Rd}$] enters the formula, so the two only have to be expressed in the same unit, but
            they do have to be the same kind of quantity [$Nmm/mm$].
        m_rd : NMM_MM
            [$m_{Rd}$] Bending resistance without interaction with shear, per unit width of the web. Only the
            ratio of [$m_{Ed}$] to this value enters the formula [$Nmm/mm$].
        """
        super().__init__()
        self.tau_rd = tau_rd
        self.m_ed = m_ed
        self.m_rd = m_rd

    @staticmethod
    def _evaluate(tau_rd: MPA, m_ed: NMM_MM, m_rd: NMM_MM) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(tau_rd=tau_rd, m_ed=m_ed)
        raise_if_less_or_equal_to_zero(m_rd=m_rd)

        # A transverse bending moment above the bending resistance leaves no real square root. The standard
        # prints nothing at all about that case, so rejecting it is a decision taken here and not a reading of
        # the standard. It is preferred over returning zero or a nan, either of which would hide that the
        # bending resistance is already exhausted. Note that m_ed equal to m_rd is inside the formula and
        # returns zero rather than raising.
        radicand = 1 - m_ed / m_rd
        raise_if_negative(one_minus_m_ed_over_m_rd=radicand)

        return tau_rd * np.sqrt(radicand)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.64."""
        _equation: str = r"\tau_{Rd} \cdot \sqrt{1 - \frac{m_{Ed}}{m_{Rd}}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Rd}": f"{self.tau_rd:.{n}f}",
                r"m_{Ed}": f"{self.m_ed:.{n}f}",
                r"m_{Rd}": f"{self.m_rd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Rd}": rf"{self.tau_rd:.{n}f} \ MPa",
                r"m_{Ed}": rf"{self.m_ed:.{n}f} \ Nmm/mm",
                r"m_{Rd}": rf"{self.m_rd:.{n}f} \ Nmm/mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rdm}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
