"""Formula 6.18 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.math_helpers import cot
from blueprints.type_alias import DEG, KN
from blueprints.validations import raise_if_negative


class Form6Dot18AdditionalTensileForce(Formula):
    r"""Class representing formula 6.18 for the calculation of the additional tensile force, [$\Delta F_{td}$]."""

    label = "6.18"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        v_ed: KN,
        theta: DEG,
        alpha: DEG,
    ) -> None:
        r"""[$\Delta F_{td}$] Additional tensile force [$kN$].

        EN 1992-1-1:2004 art.6.2.3(7) - Formula (6.18)

        Parameters
        ----------
        v_ed : KN
            [$V_{Ed}$] Design value of the shear force [$kN$].
        theta : DEG
            [$\theta$] Angle between the concrete compression strut and the beam axis perpendicular to the shear force [$degrees$].
        alpha : DEG
            [$\alpha$] Angle between shear reinforcement and the beam axis perpendicular to the shear force [$degrees$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.theta = theta
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        v_ed: KN,
        theta: DEG,
        alpha: DEG,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            v_ed=v_ed,
            theta=theta,
            alpha=alpha,
        )

        return 0.5 * v_ed * (cot(theta) - cot(alpha))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18."""
        return LatexFormula(
            return_symbol=r"\Delta F_{td}",
            result=f"{self:.{n}f}",
            equation=r"0.5 \cdot V_{Ed} \cdot \left(\cot(\theta) - \cot(\alpha)\right)",
            numeric_equation=rf"0.5 \cdot {self.v_ed:.{n}f} \cdot \left(\cot({self.theta:.{n}f}) - \cot({self.alpha:.{n}f})\right)",
            comparison_operator_label="=",
            unit="kN",
        )
