"""Formula 8.125 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, N
from blueprints.utils.math_helpers import tan
from blueprints.validations import raise_if_negative


class Form8Dot125TransverseTieForceNearEdge(Formula):
    r"""Class representing formula 8.125 for the calculation of the transverse tie force for a concentrated
    force acting close to an edge.
    """

    label = "8.125"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        f_d: N,
        theta_cf: DEG,
    ) -> None:
        r"""[$F_{td}$] Design value of the transverse tie force [$N$].

        FprEN 1992-1-1:2023 (E) art. 8.5.5(3) - Formula (8.125)

        Parameters
        ----------
        f_d : N
            [$F_d$] Concentrated force acting close to an edge [$N$].
        theta_cf : DEG
            [$\theta_{cf}$] Spreading angle, where [$\tan\theta_{cf} \geq 1/4$] may be assumed [$degrees$].
        """
        super().__init__()
        self.f_d = f_d
        self.theta_cf = theta_cf

    @staticmethod
    def _evaluate(
        f_d: N,
        theta_cf: DEG,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_d=f_d, theta_cf=theta_cf)

        return f_d * tan(theta_cf)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.125."""
        _equation: str = r"F_d \cdot \tan(\theta_{cf})"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_d": f"{self.f_d:.{n}f}",
                r"\theta_{cf}": f"{self.theta_cf:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_d": rf"{self.f_d:.{n}f} \ N",
                r"\theta_{cf}": rf"{self.theta_cf:.{n}f} ^\circ",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"F_{td}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )
