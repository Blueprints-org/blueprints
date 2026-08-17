"""Formula 8.37 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot37ReinforcementRatioPrestressedMembers(Formula):
    """Class representing formula 8.37 for the calculation of the reinforcement ratio of prestressed members
    with bonded tendons.
    """

    label = "8.37"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, d_s: MM, a_s: MM2, d_p: MM, a_p: MM2, b_w: MM, d: MM) -> None:
        r"""[$\rho_l$] Reinforcement ratio of prestressed members with bonded tendons [$-$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (6) - Formula (8.37)

        The area of prestressed reinforcement [$A_p$] may be omitted under the conditions given in 8.2.2(6).
        With [$A_p = 0$] and [$d = d_s$] this formula reduces to Formula (8.28).

        Parameters
        ----------
        d_s : MM
            [$d_s$] Effective depth of the longitudinal tension reinforcement [$mm$].
        a_s : MM2
            [$A_s$] Area of the longitudinal tension reinforcement [$mm^2$].
        d_p : MM
            [$d_p$] Effective depth of the prestressed reinforcement [$mm$].
        a_p : MM2
            [$A_p$] Area of the prestressed reinforcement [$mm^2$].
        b_w : MM
            [$b_w$] Width of the cross-section of linear members [$mm$].
        d : MM
            [$d$] Effective depth according to Formula (8.36), see Form8Dot36EffectiveDepthPrestressedMembers [$mm$].
            Within this clause it is not a free value: for the same member it follows from the four
            reinforcement quantities above. Passing anything else yields a ratio that is silently
            inconsistent with the section it claims to describe.
        """
        super().__init__()
        self.d_s = d_s
        self.a_s = a_s
        self.d_p = d_p
        self.a_p = a_p
        self.b_w = b_w
        self.d = d

    @staticmethod
    def _evaluate(d_s: MM, a_s: MM2, d_p: MM, a_p: MM2, b_w: MM, d: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d_s=d_s, a_s=a_s, d_p=d_p, a_p=a_p)
        raise_if_less_or_equal_to_zero(b_w=b_w, d=d)

        return (d_s * a_s + d_p * a_p) / (b_w * d**2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.37."""
        _equation: str = r"\frac{d_s \cdot A_s + d_p \cdot A_p}{b_w \cdot \left(d\right)^2}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_s": f"{self.d_s:.{n}f}",
                r"A_s": f"{self.a_s:.{n}f}",
                r"d_p": f"{self.d_p:.{n}f}",
                r"A_p": f"{self.a_p:.{n}f}",
                r"b_w": f"{self.b_w:.{n}f}",
                r"\left(d\right)": rf"\left({self.d:.{n}f}\right)",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_s": rf"{self.d_s:.{n}f} \ mm",
                r"A_s": rf"{self.a_s:.{n}f} \ mm^2",
                r"d_p": rf"{self.d_p:.{n}f} \ mm",
                r"A_p": rf"{self.a_p:.{n}f} \ mm^2",
                r"b_w": rf"{self.b_w:.{n}f} \ mm",
                r"\left(d\right)": rf"\left({self.d:.{n}f} \ mm\right)",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\rho_l",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
