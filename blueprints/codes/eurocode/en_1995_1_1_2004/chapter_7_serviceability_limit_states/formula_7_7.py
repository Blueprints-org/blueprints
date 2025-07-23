"""Formula 7.7 from EN 1995-1-1:2004."""

from blueprints.codes.eurocode.en_1995_1_1_2004 import EN_1995_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, HZ, NM2_M, M
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form7Dot7NumberOfFOVibrations(Formula):
    r"""Class representing formula 7.7 for the calculations of the number of first-order vibrations with a natural frequency less than 40Hz."""

    label = "7.7"
    source_document = EN_1995_1_1_2004
    # frequency limit to check
    f_40 = 40

    def __init__(self, f_1: HZ, b: M, length: M, ei_l: NM2_M, ei_b: NM2_M) -> None:
        r"""[$n_{40}$] The number of first-order vibrations with a natural frequency less than 40Hz [$-$].

        EN 1995-1-1:2004 art 7.3.3(5) - Formula (7.7)

        Parameters
        ----------
        f_1 : HZ
            [$f_{1}$] Natural frequency of rectangular floor, laid freely on all four sides [$Hz$].
        length : M
            [$l$] Span of the floor [$m$].
        b : M
            [$b$] Width of the floor [$m$].
        ei_l : NM2_M
            [$(EI)_{l}$] Equivalent bending stiffness of the floor around the axis perpendicular to the longitudinal axis of the beam [$Nm^{2}/m$].
        ei_b : NM2_M
            [$(EI)_{l}$] Equivalent bending stiffness of the floor around the axis parallel to the longitudinal axis of the beam, with $EI_{b} < EI_{l}$ [$Nm^{2}/m$].

        Returns
        -------
        None
        """  # noqa: E501
        super().__init__()
        self.f_1 = f_1
        self.length = length
        self.b = b
        self.ei_l = ei_l
        self.ei_b = ei_b

    @staticmethod
    def _evaluate(f_1: HZ, b: M, length: M, ei_l: NM2_M, ei_b: NM2_M) -> DIMENSIONLESS:
        """Evaluate the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(f_1=f_1, b=b, length=length, ei_l=ei_l, ei_b=ei_b)
        if f_1 > Form7Dot7NumberOfFOVibrations.f_40:
            raise ValueError(f"Value of $f_1$ ({f_1:.3f}) exceeds the allowed limit of {Form7Dot7NumberOfFOVibrations.f_40}.")
        if not ei_b < ei_l:
            raise ValueError(rf"$EI_l$ ({ei_l:.2f}) must be bigger than $EI_b$ ({ei_b:.2f}).")
        return (((40 / f_1) ** 2 - 1) * (b / length) ** 4 * ei_l / ei_b) ** 0.25

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 7.7."""
        eq_for: str = (
            r"\left\{\left ( \left (\frac{40}{f_1} \right )^2 -1 \right)\left ( \frac{b}{l } \right )^4 \frac{(EI)_l}{(EI)_b}\right\}^{0.25}"
        )
        repl_symb = {
            "(EI)_l": f"{self.ei_l:.{n}f}",
            "(EI)_b": f"{self.ei_b:.{n}f}",
            "f_1": f"{self.f_1:.{n}f}",
            "l ": f"{self.length:.{n}f}",
            "b": f"{self.b:.{n}f}",
        }
        return LatexFormula(
            return_symbol=r"n_{40}",
            result=f"{self:.{n}f}",
            equation=eq_for,
            numeric_equation=latex_replace_symbols(eq_for, repl_symb),
        )
