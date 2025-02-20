"""Formula 8.20 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot20BondStrengthAnchorageULS(Formula):
    r"""Class representing formula 8.20 for the calculation of bond strength for anchorage in the ultimate limit state [$f_{bpd}$].

    NEN-EN 1992-1-1+C2:2011 art.8.10.2.2(3) - Formula (8.20)

    Parameters
    ----------
    eta_p2 : DIMENSIONLESS
        [$\eta_{p2}$] Coefficient that takes into account the type of tendon and the bond situation at anchorage [$-$].

        1.4 for indented wires or 1.2 for 7-wire strands.
    eta_1 : DIMENSIONLESS
        [$\eta_{1}$] Coefficient for concrete, defined in 8.10.2.2 (1) [$-$].
    f_ctd : MPA
        Design tensile strength of concrete [$MPa$].
    """

    label = "8.20"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, eta_p2: DIMENSIONLESS, eta_1: DIMENSIONLESS, f_ctd: MPA) -> None:
        super().__init__()
        self.eta_p2 = eta_p2
        self.eta_1 = eta_1
        self.f_ctd = f_ctd

    @staticmethod
    def _evaluate(eta_p2: DIMENSIONLESS, eta_1: DIMENSIONLESS, f_ctd: MPA) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(eta_p2=eta_p2, eta_1=eta_1, f_ctd=f_ctd)
        return eta_p2 * eta_1 * f_ctd

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 8.20."""
        return LatexFormula(
            return_symbol=r"f_{bpd}",
            result=f"{self:.3f}",
            equation=r"\eta_{p2} \cdot \eta_{1} \cdot f_{ctd}",
            numeric_equation=rf"{self.eta_p2:.3f} \cdot {self.eta_1:.3f} \cdot {self.f_ctd:.3f}",
            comparison_operator_label="=",
        )
