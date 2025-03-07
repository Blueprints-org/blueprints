"""Formula 6.27 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM, N_MM, N
from blueprints.validations import raise_if_negative


class Form6Dot27ShearForceInWall(Formula):
    r"""Class representing formula 6.27 for the calculation of the shear force in a wall, [$V_{Ed,i}$]."""

    label = "6.27"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        tau_t_i_t_ef_i: N_MM,
        z_i: MM,
    ) -> None:
        r"""[$V_{Ed,i}$] Shear force in a wall [$N$].

        NEN-EN 1992-1-1+C2:2011 art.6.3.2(1) - Formula (6.27)

        Parameters
        ----------
        tau_t_i_t_ef_i : N_MM
            [$\tau_{t,i} t_{ef,i}$] Shear stress in a wall of a section subject to a pure torsional moment multiplied with the
            effective thickness [$N/mm$].
        z_i : MM
            [$z_{i}$] is the side length of wall i defined by the distance between the intersection points with the adjacent walls [$mm$].
        """
        super().__init__()
        self.tau_t_i_t_ef_i = tau_t_i_t_ef_i
        self.z_i = z_i

    @staticmethod
    def _evaluate(
        tau_t_i_t_ef_i: N_MM,
        z_i: MM,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(tau_t_i_t_ef_i=tau_t_i_t_ef_i, z_i=z_i)

        return tau_t_i_t_ef_i * z_i

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.27."""
        return LatexFormula(
            return_symbol=r"V_{Ed,i}",
            result=f"{self:.3f}",
            equation=r"\tau_{t,i} t_{ef,i} \cdot z_{i}",
            numeric_equation=rf"{self.tau_t_i_t_ef_i:.3f} \cdot {self.z_i:.3f}",
            comparison_operator_label="=",
            unit="N",
        )
