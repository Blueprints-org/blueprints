"""Formula 8.13 from EN 1992-1-1:2004: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2
from blueprints.validations import raise_if_negative


class Form8Dot13AdditionalShearReinforcement(Formula):
    """Class representing formula 8.13 for the calculation of the minimum additional shear reinforcement in the anchorage zones where transverse
    compression is not present for straight anchorage lengths, in the direction perpendicular to the tension face.
    """

    label = "8.13"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        a_s: MM2,
        n_2: DIMENSIONLESS,
    ) -> None:
        r"""[$A_{sh}$] Minimum additional shear reinforcement in the anchorage zones where transverse compression is not present for straight
        anchorage lengths, in the direction perpendicular to the tension face [$mm^2$].

        EN 1992-1-1:2004 art.8.8(6) - Formula (8.12)

        Parameters
        ----------
        a_s: MM2
            [$A_{s}$] Cross sectional area of reinforcement [$mm^2$].
        n_2: DIMENSIONLESS
            [$n_{2}$] Number of bars anchored in each layer [$-$].
        """
        super().__init__()
        self.a_s = a_s
        self.n_2 = n_2

    @staticmethod
    def _evaluate(
        a_s: MM2,
        n_2: DIMENSIONLESS,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_s=a_s, n_2=n_2)
        return 0.25 * a_s * n_2

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 8.13."""
        _equation: str = r"0.25 \cdot A_s \cdot n_2"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_s": f"{self.a_s:.{n}f}",
                r"n_2": f"{self.n_2:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A_s": rf"{self.a_s:.{n}f} \ mm^2",
                r"n_2": f"{self.n_2:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_{sv}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm^2",
        )
