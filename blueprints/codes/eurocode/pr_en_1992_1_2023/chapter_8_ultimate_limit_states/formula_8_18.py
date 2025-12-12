"""Formula 8.18 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.formula import Formula
from blueprints.codes.eurocode.pr_en_1992_1_2023 import pr_EN_1992_1_1_2023
from blueprints.type_alias import MPA, N, MM
from blueprints.validations import raise_if_negative, raise_if_less_or_equal_to_zero
from blueprints.codes.latex_formula import LatexFormula
from blueprints.codes.latex_formula import latex_replace_symbols


class Form8Dot18AverageShearStress(Formula):
    """Class representing formula 8.18 for the calculation of the average shear stress over the cross-section
    in regions of members without geometric discontinuities."""

    label = "8.18"
    source_document = pr_EN_1992_1_1_2023

    def __init__(self, v_ed: N, b_w: MM, z: MM) -> None:
        r"""[$\tau_{Ed}$] Average shear stress over the cross-section area.

        pr_NEN-EN 1992-1-1-2023 art 8.2.1 (3) - Formula (8.18)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design shear force at the control section in linear members
        b_w : MM
            [$b_w$] Width of the cross-section of linear members.
        z : MM
            [$z$] Lever arm for the shear stress calculation defined as z = 0.9d
        """
        super().__init__()
        self.v_ed = v_ed
        self.b_w = b_w
        self.z = z

    @staticmethod
    def _evaluate(v_ed: MPA, b_w: MM, z: MM, *args, **kwargs) -> float:  # noqa: ARG004
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            v_ed=v_ed,
        )

        raise_if_less_or_equal_to_zero(
            b_w=b_w,
            z=z
        )
        return v_ed / (b_w * z)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.18."""
        _equation: str = r"\frac{V_{Ed}}{b_w \cdot z}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            replacements={r"V_{Ed}": f"{self.v_ed:.{n}f}",
                          r"b_w": f"{self.b_w:.{n}f}",
                          r"z": f"{self.z:.{n}f}"},
            unique_symbol_check=False
        )
        return LatexFormula(
            return_symbol=r"\tau_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa"
        )


if __name__ == '__main__':
    my_form = Form8Dot18AverageShearStress(v_ed=10000.0, b_w=-50.0, z=215.0)
    print(my_form)
    print(my_form.latex())
    print(my_form.latex().complete)
    print(my_form.latex().short)
