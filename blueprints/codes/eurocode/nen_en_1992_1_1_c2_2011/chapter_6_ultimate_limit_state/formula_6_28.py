"""Formula 6.28 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.math_helpers import cot
from blueprints.type_alias import DEG, MM, MM2, MPA, NMM
from blueprints.validations import raise_if_greater_than_90, raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot28RequiredCrossSectionalArea(Formula):
    r"""Class representing formula 6.28 for the calculation of the required cross-sectional area of the longitudinal reinforcement.
    The description of the equation states that it is used to calculate the total reinforcement area. Therefore the
    calculation has been rewritten to find the solution to that question, [$\Sigma A_{sl}$].
    """

    label = "6.28"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        u_k: MM,
        f_yd: MPA,
        t_ed: NMM,
        a_k: MM2,
        theta: DEG,
    ) -> None:
        r"""[$\Sigma A_{sl}$] Required cross-sectional area of the longitudinal reinforcement [$mm^2$].

        NEN-EN 1992-1-1+C2:2011 art.6.3.2(3) - Formula (6.28)

        Parameters
        ----------
        u_k : MM
            [$u_k$] Perimeter of the area A_k [$mm$].
        f_yd : MPA
            [$f_{yd}$] Design yield stress of the longitudinal reinforcement [$MPa$].
        t_ed : NMM
            [$T_{Ed}$] Design value of the torsional moment [$Nmm$].
        a_k : MM2
            [$A_k$] Area enclosed by the centre-lines of the connecting walls, including inner hollow areas [$mm^2$].
        theta : DEG
            [$\theta$] Angle of compression struts (see Figure 6.5) [$degrees$].
        """
        super().__init__()
        self.u_k = u_k
        self.f_yd = f_yd
        self.t_ed = t_ed
        self.a_k = a_k
        self.theta = theta

    @staticmethod
    def _evaluate(
        u_k: MM2,
        f_yd: MPA,
        t_ed: NMM,
        a_k: MM2,
        theta: DEG,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            u_k=u_k,
            t_ed=t_ed,
        )
        raise_if_less_or_equal_to_zero(f_yd=f_yd, a_k=a_k, theta=theta)
        raise_if_greater_than_90(theta=theta)

        return (u_k / f_yd) * (t_ed / (2 * a_k)) * cot(theta)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.28."""
        return LatexFormula(
            return_symbol=r"\Sigma A_{sl}",
            result=f"{self:.3f}",
            equation=r"\frac{u_k}{f_{yd}} \cdot \frac{T_{Ed}}{2 \cdot A_k} \cdot \cot(\theta)",
            numeric_equation=rf"\frac{{{self.u_k:.3f}}}{{{self.f_yd:.3f}}} \cdot \frac{{{self.t_ed:.3f}}}"
            rf"{{2 \cdot {self.a_k:.3f}}} \cdot \cot({self.theta:.3f})",
            comparison_operator_label="=",
            unit="mm^2",
        )
