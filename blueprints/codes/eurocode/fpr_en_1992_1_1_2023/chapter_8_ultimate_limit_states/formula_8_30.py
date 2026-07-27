"""Formula 8.30 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot30EffectiveShearSpan(Formula):
    """Class representing formula 8.30 for the calculation of the effective shear span with respect to
    the control section, for reinforced concrete members.
    """

    label = "8.30"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, m_ed: NMM, v_ed: N, d: MM) -> None:
        r"""[$a_{cs}$] Effective shear span with respect to the control section [$mm$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (3) - Formula (8.30)

        The standard prints this as a ratio in absolute value bars, bounded from below by [$d$], which is
        implemented as the maximum of the two. Because of the absolute value, the signs of [$M_{Ed}$] and
        [$V_{Ed}$] do not affect the result, so both may be passed signed.

        Parameters
        ----------
        m_ed : NMM
            [$M_{Ed}$] Design bending moment at the control section, including the effects of prestressing
            according to 8.2.1(8) [$Nmm$].
        v_ed : N
            [$V_{Ed}$] Design shear force at the control section, including the effects of prestressing
            according to 8.2.1(8) [$N$].
        d : MM
            [$d$] Effective depth [$mm$].
        """
        super().__init__()
        self.m_ed = m_ed
        self.v_ed = v_ed
        self.d = d

    @staticmethod
    def _evaluate(m_ed: NMM, v_ed: N, d: MM) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        # The guard is on the magnitude, so a negative shear force passes and only zero is refused. Naming
        # the keyword after the magnitude keeps the error from claiming that a negative value is illegal.
        # Refusing a shear force of zero is a reading of the standard, since it is a denominator. Refusing an
        # effective depth of zero is an addition made here: the standard prints no such condition.
        raise_if_less_or_equal_to_zero(abs_v_ed=abs(v_ed), d=d)

        return max(abs(m_ed / v_ed), d)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.30."""
        _equation: str = r"\max\left(\left|\frac{M_{Ed}}{V_{Ed}}\right|, d\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"M_{Ed}": f"{self.m_ed:.{n}f}",
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
                r", d": f", {self.d:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"M_{Ed}": rf"{self.m_ed:.{n}f} \ Nmm",
                r"V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                r", d": rf", {self.d:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"a_{cs}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
