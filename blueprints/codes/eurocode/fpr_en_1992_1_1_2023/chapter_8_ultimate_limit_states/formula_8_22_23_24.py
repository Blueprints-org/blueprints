"""Formula 8.22, 8.23 and 8.24 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, N_MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot22To24EffectiveDepth(Formula):
    """Class representing formulas 8.22, 8.23 and 8.24 for the calculation of the effective depth of planar members,
    taken as a function of the ratio of the shear forces.
    """

    label = "8.22/8.23/8.24"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, v_ed_x: N_MM, v_ed_y: N_MM, d_x: MM, d_y: MM) -> None:
        r"""[$d$] Effective depth of planar members, as a function of the ratio of the shear forces
        [$v_{Ed,y}/v_{Ed,x}$] [$mm$].

        FprEN 1992-1-1:2023 (E) art 8.2.1 (5) - Formula (8.22), (8.23) and (8.24)

        The boundaries of the ratio are one-sided as printed: a ratio of exactly 0.5 falls under Formula (8.22)
        and a ratio of exactly 2 falls under Formula (8.24). The standard gives no rule for [$v_{Ed,x} = 0$],
        for which the ratio is undefined, so that input is rejected.

        Both shear forces are taken as magnitudes, and the standard does not settle that: it prints no absolute
        value bars and defines no sign convention. Read literally, the ratio is signed, so any pair with
        opposite signs is negative, always satisfies the first condition, and selects [$d_x$] even where
        [$\left|v_{Ed,y}\right|$] dominates. Flipping the positive direction of the y axis would then change
        the effective depth, which cannot be intended.

        The alternative the standard prints on the same page settles it: Formula (8.26) gives
        [$\alpha_v = \arctan(v_{Ed,y}/v_{Ed,x})$] and Formula (8.25) gives
        [$d = d_x \cdot \cos^2\alpha_v + d_y \cdot \sin^2\alpha_v$], which is even in [$\alpha_v$] and therefore
        insensitive to the sign. Formulas (8.22) to (8.24) are the stepped approximation of that same continuous
        function, so their boundaries of 0,5 and 2 order a ratio of magnitudes. Formula (8.21) reaches the same
        place by squaring both components.

        The LaTeX prints the absolute value bars that the standard leaves out, so that the substituted numbers
        match the branch that was taken.

        The requirement that [$d_x$] and [$d_y$] be strictly positive is an addition made here: neither appears
        in a denominator in these three formulas, and the standard prints no such condition. An effective depth
        of zero is not a cross-section.

        Parameters
        ----------
        v_ed_x : N_MM
            [$v_{Ed,x}$] Out-of-plane design shear force per unit width acting on the cross-section perpendicular
            to the x direction [$N/mm$].
        v_ed_y : N_MM
            [$v_{Ed,y}$] Out-of-plane design shear force per unit width acting on the cross-section perpendicular
            to the y direction [$N/mm$].
        d_x : MM
            [$d_x$] Effective depth in the x direction [$mm$].
        d_y : MM
            [$d_y$] Effective depth in the y direction [$mm$].
        """
        super().__init__()
        self.v_ed_x = v_ed_x
        self.v_ed_y = v_ed_y
        self.d_x = d_x
        self.d_y = d_y

    @staticmethod
    def _evaluate(v_ed_x: N_MM, v_ed_y: N_MM, d_x: MM, d_y: MM) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(abs_v_ed_x=abs(v_ed_x), d_x=d_x, d_y=d_y)

        ratio = abs(v_ed_y) / abs(v_ed_x)
        if ratio <= 0.5:
            return d_x
        if ratio < 2:
            return 0.5 * (d_x + d_y)
        return d_y

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 8.22, 8.23 and 8.24."""
        _equation: str = (
            r"\begin{cases} d_x & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \leq 0.5 \\ "
            r"0.5 \cdot (d_x + d_y) & \text{if } 0.5 < \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} < 2 \\ "
            r"d_y & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \geq 2 \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"v_{Ed,x}": f"{self.v_ed_x:.{n}f}",
                r"v_{Ed,y}": f"{self.v_ed_y:.{n}f}",
                r"d_x": f"{self.d_x:.{n}f}",
                r"d_y": f"{self.d_y:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"v_{Ed,x}": rf"{self.v_ed_x:.{n}f} \ N/mm",
                r"v_{Ed,y}": rf"{self.v_ed_y:.{n}f} \ N/mm",
                r"d_x": rf"{self.d_x:.{n}f} \ mm",
                r"d_y": rf"{self.d_y:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        # Only the middle branch has a step between the selected expression and the result. LatexFormula skips
        # an empty intermediate result, so the other two branches show none.
        _intermediate: str = ""
        if 0.5 < abs(self.v_ed_y) / abs(self.v_ed_x) < 2:
            _intermediate = rf"0.5 \cdot ({self.d_x:.{n}f} + {self.d_y:.{n}f})"

        return LatexFormula(
            return_symbol=r"d",
            result=f"{self:.{n}f}",
            intermediate_result=_intermediate,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
