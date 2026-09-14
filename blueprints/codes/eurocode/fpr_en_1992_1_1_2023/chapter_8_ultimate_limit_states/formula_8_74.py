"""Formula 8.74 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot74DesignShearStressAtInterface(Formula):
    r"""Class representing formula 8.74 for the calculation of the design value of the shear stress in an interface."""

    label = "8.74"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        v_edi: N,
        a_i: MM2,
    ) -> None:
        r"""[$\tau_{Edi}$] Design value of the shear stress in an interface [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.2.6(4) - Formula (8.74)

        Parameters
        ----------
        v_edi : N
            [$V_{Edi}$] Shear force acting parallel to the interface. Note that Formula (8.75) uses
            [$V_{Ed}$], the shear force acting perpendicular to the interface, which is a different quantity
            [$N$].
        a_i : MM2
            [$A_i$] Area of the interface according to Figure 8.14. For keyed interfaces it should be based on
            either the key area A1, A2 or A3 according to Figure 8.14 whichever is governing taking into
            account the corresponding concrete strength [$mm^2$].
        """
        super().__init__()
        self.v_edi = v_edi
        self.a_i = a_i

    @staticmethod
    def _evaluate(
        v_edi: N,
        a_i: MM2,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_edi=v_edi)
        raise_if_less_or_equal_to_zero(a_i=a_i)

        return v_edi / a_i

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.74."""
        _equation: str = r"\frac{V_{Edi}}{A_i}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"V_{Edi}": f"{self.v_edi:.{n}f}",
                r"A_i": f"{self.a_i:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"V_{Edi}": rf"{self.v_edi:.{n}f} \ N",
                r"A_i": rf"{self.a_i:.{n}f} \ mm^2",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Edi}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
