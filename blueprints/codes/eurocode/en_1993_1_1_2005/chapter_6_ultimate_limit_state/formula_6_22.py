"""Formula 6.22 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot22CheckShearBucklingResistance(Formula):
    r"""Class representing formula 6.22 for checking shear buckling resistance for webs without intermediate stiffeners."""

    label = "6.22"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        h_w: MM,
        t_w: MM,
        epsilon: DIMENSIONLESS,
        eta: DIMENSIONLESS = 1.0,
    ) -> None:
        r"""Check the shear buckling resistance for webs without intermediate stiffeners.

        EN 1993-1-1:2005 art.6.2.6(6) - Formula (6.22)

        Parameters
        ----------
        h_w : MM
            [$h_{w}$] Web height [mm].
        t_w : MM
            [$t_{w}$] Web thickness [mm].
        epsilon : DIMENSIONLESS
            [$\epsilon$] Coefficient depending on $f_y$ [-].
        eta : DIMENSIONLESS, optional
            [$\eta$] See section 5 of EN 1993-1-5, conservatively taken as 1.0 [-].
        """
        super().__init__()
        self.h_w = h_w
        self.t_w = t_w
        self.epsilon = epsilon
        self.eta = eta

    @staticmethod
    def _evaluate(
        h_w: MM,
        t_w: MM,
        epsilon: DIMENSIONLESS,
        eta: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(t_w=t_w, eta=eta)
        raise_if_negative(h_w=h_w, epsilon=epsilon)

        return (h_w / t_w) > (72 * (epsilon / eta))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.22."""
        _equation: str = r"\left( \frac{h_w}{t_w} > 72 \cdot \frac{\epsilon}{\eta} \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"h_w": f"{self.h_w:.{n}f}",
                r"t_w": f"{self.t_w:.{n}f}",
                r"\epsilon": f"{self.epsilon:.{n}f}",
                r"\eta": f"{self.eta:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
