"""Formula 8.31 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot31AxialForceCoefficient(Formula):
    """Class representing formula 8.31 for the calculation of the coefficient accounting for axial forces
    at the control section.
    """

    label = "8.31"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, n_ed: N, v_ed: N, d: MM, a_cs: MM) -> None:
        r"""[$k_{vp}$] Coefficient by which the effective depth in Formula (8.27), or the mechanical shear span
        in Formula (8.29), is multiplied in the presence of axial forces [$-$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (4) - Formula (8.31)

        The standard prints the shear force in absolute value bars but the axial force without them, so the sign
        of [$N_{Ed}$] carries meaning and a negative value is valid: it lowers [$k_{vp}$]. The printed lower bound
        of 0.1 is implemented as a maximum.

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design axial force acting at the control section, passed with its sign [$N$].
        v_ed : N
            [$V_{Ed}$] Design shear force at the control section. Only its magnitude is used, so it may be
            passed signed [$N$].
        d : MM
            [$d$] Effective depth [$mm$].
        a_cs : MM
            [$a_{cs}$] Effective shear span with respect to the control section according to Formula (8.30),
            see Form8Dot30EffectiveShearSpan [$mm$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.v_ed = v_ed
        self.d = d
        self.a_cs = a_cs

    @staticmethod
    def _evaluate(n_ed: N, v_ed: N, d: MM, a_cs: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        # The guard is on the magnitude, so a negative shear force passes and only zero is refused. Naming
        # the keyword after the magnitude keeps the error from claiming that a negative value is illegal.
        # Refusing a shear force of zero is a reading of the standard, since it is a denominator. Refusing an
        # effective depth of zero is an addition made here: the standard prints no such condition.
        raise_if_less_or_equal_to_zero(abs_v_ed=abs(v_ed), a_cs=a_cs, d=d)

        return max(1 + (n_ed / abs(v_ed)) * (d / (3 * a_cs)), 0.1)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.31."""
        _equation: str = r"\max\left(1 + \frac{N_{Ed}}{\left|V_{Ed}\right|} \cdot \frac{d}{3 \cdot a_{cs}}, 0.1\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
                r"a_{cs}": f"{self.a_cs:.{n}f}",
                r"{d}": "{" + f"{self.d:.{n}f}" + "}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                r"a_{cs}": rf"{self.a_cs:.{n}f} \ mm",
                r"{d}": "{" + rf"{self.d:.{n}f} \ mm" + "}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"k_{vp}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
