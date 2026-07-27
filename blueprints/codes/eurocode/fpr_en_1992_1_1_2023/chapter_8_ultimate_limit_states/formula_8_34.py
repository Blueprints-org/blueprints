"""Formula 8.34 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot34FactorK1(Formula):
    """Class representing formula 8.34 for the calculation of the factor accounting for the effect of
    compressive normal forces.
    """

    label = "8.34"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, a_cs_0: MM, e_p: MM, d: MM, a_c: MM2, b_w: MM, z: MM) -> None:
        r"""[$k_1$] Factor accounting for the effect of compressive normal forces [$-$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (5) - Formula (8.34)

        The standard offers this factor unless the National Annex gives another value. The printed upper
        bound is implemented as a minimum.

        Parameters
        ----------
        a_cs_0 : MM
            [$a_{cs,0}$] Effective shear span determined according to Formula (8.30), without considering in
            [$M_{Ed}$] and [$V_{Ed}$] the effect of prestressing or external load that produces the compressive
            axial force [$mm$].
        e_p : MM
            [$e_p$] Eccentricity of the prestressing force or of the external load that produces the compressive
            axial force, with respect to the centre of gravity of the cross-section, considered as positive
            towards the tensile side. A negative value is therefore valid. For statically indeterminate members,
            the effect of hyperstatic moments due to prestressing should be considered by modifying the tendons
            eccentricity accordingly [$mm$].
        d : MM
            [$d$] Effective depth [$mm$].
        a_c : MM2
            [$A_c$] Area of concrete cross-section [$mm^2$].
        b_w : MM
            [$b_w$] Width of the cross-section of linear members [$mm$].
        z : MM
            [$z$] Lever arm for the shear stress calculation [$mm$].
        """
        super().__init__()
        self.a_cs_0 = a_cs_0
        self.e_p = e_p
        self.d = d
        self.a_c = a_c
        self.b_w = b_w
        self.z = z

    @staticmethod
    def _evaluate(a_cs_0: MM, e_p: MM, d: MM, a_c: MM2, b_w: MM, z: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        # Zero is refused for all of these. For the ones that sit in a denominator that is a reading of the
        # standard. For a_cs_0 it is also a reading, one step removed: Formula (8.30) defines the effective
        # shear span as at least the effective depth, so it cannot be zero. For the rest it is an addition made
        # here, so that the same quantity is not admitted in one formula of this clause and refused in the next.
        # The eccentricity e_p is deliberately not guarded: the standard defines it as positive towards the
        # tensile side, so a negative value is ordinary input and may drive the result below zero, which the
        # standard does not bound.
        raise_if_less_or_equal_to_zero(a_cs_0=a_cs_0, b_w=b_w, z=z, d=d, a_c=a_c)

        ratio = a_c / (b_w * z)
        return min((0.5 / a_cs_0) * (e_p + d / 3) * ratio, 0.18 * ratio)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.34."""
        _equation: str = (
            r"\min\left(\frac{0.5}{a_{cs,0}} \cdot \left(e_p + \frac{d}{3}\right) \cdot "
            r"\frac{A_c}{b_w \cdot z}, 0.18 \cdot \frac{A_c}{b_w \cdot z}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_{cs,0}": f"{self.a_cs_0:.{n}f}",
                r"e_p": f"{self.e_p:.{n}f}",
                r"{d}": "{" + f"{self.d:.{n}f}" + "}",
                r"A_c": f"{self.a_c:.{n}f}",
                r"b_w": f"{self.b_w:.{n}f}",
                r"z": f"{self.z:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_{cs,0}": rf"{self.a_cs_0:.{n}f} \ mm",
                r"e_p": rf"{self.e_p:.{n}f} \ mm",
                r"{d}": "{" + rf"{self.d:.{n}f} \ mm" + "}",
                r"A_c": rf"{self.a_c:.{n}f} \ mm^2",
                r"b_w": rf"{self.b_w:.{n}f} \ mm",
                r"z": rf"{self.z:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"k_1",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
