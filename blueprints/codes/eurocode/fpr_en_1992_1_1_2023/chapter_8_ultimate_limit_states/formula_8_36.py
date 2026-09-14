"""Formula 8.36 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot36EffectiveDepthPrestressedMembers(Formula):
    """Class representing formula 8.36 for the calculation of the effective depth of prestressed members
    with bonded tendons.
    """

    label = "8.36"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, d_s: MM, a_s: MM2, d_p: MM, a_p: MM2) -> None:
        r"""[$d$] Effective depth of prestressed members with bonded tendons [$mm$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (6) - Formula (8.36)

        The area of prestressed reinforcement [$A_p$] may be omitted if including it reduces the shear
        resistance through the reduced effective depth, provided the longitudinal tension reinforcement
        [$A_s$] is sufficient to carry [$M_{Ed}$] and [$N_{Ed}$] taking into account the effect of
        prestressing. Passing [$A_p = 0$] returns [$d_s$], which is that omission.

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
        """
        super().__init__()
        self.d_s = d_s
        self.a_s = a_s
        self.d_p = d_p
        self.a_p = a_p

    @staticmethod
    def _evaluate(d_s: MM, a_s: MM2, d_p: MM, a_p: MM2) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d_s=d_s, a_s=a_s, d_p=d_p, a_p=a_p)

        denominator = d_s * a_s + d_p * a_p
        raise_if_less_or_equal_to_zero(denominator=denominator)

        return (d_s**2 * a_s + d_p**2 * a_p) / denominator

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.36."""
        _equation: str = r"\frac{\left(d_s\right)^2 \cdot A_s + \left(d_p\right)^2 \cdot A_p}{d_s \cdot A_s + d_p \cdot A_p}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_s": f"{self.d_s:.{n}f}",
                r"A_s": f"{self.a_s:.{n}f}",
                r"d_p": f"{self.d_p:.{n}f}",
                r"A_p": f"{self.a_p:.{n}f}",
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
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"d",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
