"""Formula 8.46 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form8Dot46AverageStrainBottomTopChords(Formula):
    r"""Class representing formula 8.46 for the average strain of the bottom and top chords.

    Average strain of the bottom and top chords according to:
    [$\epsilon_x = \frac{\epsilon_{xt} + \epsilon_{xc}}{2} \geq 0$]
    """

    label = "8.46"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        epsilon_xt: DIMENSIONLESS,
        epsilon_xc: DIMENSIONLESS,
    ) -> None:
        r"""Average strain of the bottom and top chords (dimensionless).

        prEN 1992-1-1:2023 art. 8.2.3 (7) - Formula (8.46)

        Parameters
        ----------
        epsilon_xt : DIMENSIONLESS
            [$\epsilon_{xt}$] Strain of the bottom (tension) chord (dimensionless).
        epsilon_xc : DIMENSIONLESS
            [$\epsilon_{xc}$] Strain of the top (compression) chord (dimensionless).
        """
        super().__init__()
        self.epsilon_xt = epsilon_xt
        self.epsilon_xc = epsilon_xc

    @staticmethod
    def _evaluate(
        epsilon_xt: DIMENSIONLESS,
        epsilon_xc: DIMENSIONLESS,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(epsilon_xt=epsilon_xt)
        return max((epsilon_xt + epsilon_xc) / 2, 0.0)

    def latex(self, n: int = 4) -> LatexFormula:
        """Returns LatexFormula object for formula 8.46."""
        _equation: str = r"\frac{\epsilon_{xt} + \epsilon_{xc}}{2}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\epsilon_{xt}": f"{self.epsilon_xt:.{n}f}",
                r"\epsilon_{xc}": f"{self.epsilon_xc:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"\epsilon_{xt}": f"{self.epsilon_xt:.{n}f}",
                r"\epsilon_{xc}": f"{self.epsilon_xc:.{n}f}",
            },
            False,
        )
        intermediate_result = rf"{self._evaluate(epsilon_xt=self.epsilon_xt, epsilon_xc=self.epsilon_xc):.{n}f} \ge 0"

        return LatexFormula(
            return_symbol=r"\epsilon_x",
            result=f"{self:.{n}f}",
            intermediate_result=intermediate_result,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="",
        )
