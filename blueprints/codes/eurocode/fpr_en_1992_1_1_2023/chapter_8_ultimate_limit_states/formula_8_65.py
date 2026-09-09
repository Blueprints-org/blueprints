"""Formula 8.65 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot65LongitudinalShearStressFlangeWebJunction(Formula):
    """Class representing formula 8.65 for the calculation of the longitudinal shear stress at the junction
    between one side of a flange and the web.
    """

    label = "8.65"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, delta_f_d: N, h_f: MM, delta_x: MM) -> None:
        r"""[$\tau_{Ed}$] Longitudinal shear stress at the junction between one side of a flange and the
        web [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.5 (1) - Formula (8.65)

        The standard limits the length under consideration: the maximum value that may be assumed for
        [$\Delta x$] is half the distance between the section where the moment is 0 and the section where it is
        maximum, and where point loads are applied it should not exceed the distance between point loads. Those
        are conditions on how the caller chooses the length, not bounds on the result, so they are not enforced
        here.

        Parameters
        ----------
        delta_f_d : N
            [$\Delta F_d$] Change of the axial force in the flange over the length [$\Delta x$], see
            Figure 8.13 [$N$].
        h_f : MM
            [$h_f$] Thickness of the flange at the junctions [$mm$].
        delta_x : MM
            [$\Delta x$] Length under consideration, see Figure 8.13 [$mm$].
        """
        super().__init__()
        self.delta_f_d = delta_f_d
        self.h_f = h_f
        self.delta_x = delta_x

    @staticmethod
    def _evaluate(delta_f_d: N, h_f: MM, delta_x: MM) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        # The standard prints no sign requirement on the change of the axial force and no absolute value
        # bars, so rejecting a negative one is a decision taken here and not a reading of the standard. It is
        # preferred over passing the sign through, because a negative shear stress would satisfy the check of
        # Formula (8.66) for a load case that is just as onerous as its mirror image. Taking the magnitude
        # instead would also close that path, but it would silently accept either sign convention.
        raise_if_negative(delta_f_d=delta_f_d)
        raise_if_less_or_equal_to_zero(h_f=h_f, delta_x=delta_x)

        return delta_f_d / (h_f * delta_x)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.65."""
        _equation: str = r"\frac{\Delta F_d}{h_f \cdot \Delta x}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\Delta F_d": f"{self.delta_f_d:.{n}f}",
                r"h_f": f"{self.h_f:.{n}f}",
                r"\Delta x": f"{self.delta_x:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\Delta F_d": rf"{self.delta_f_d:.{n}f} \ N",
                r"h_f": rf"{self.h_f:.{n}f} \ mm",
                r"\Delta x": rf"{self.delta_x:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
