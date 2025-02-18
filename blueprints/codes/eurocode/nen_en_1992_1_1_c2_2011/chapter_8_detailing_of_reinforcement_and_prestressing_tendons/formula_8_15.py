"""Formula 8.15 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot15PrestressTransferStress(Formula):
    """Class representing formula 8.15 for the calculation of the constant bond stress at which prestress is assumed to be transferred to the
    concrete, at the release of tendons.
    """

    label = "8.15"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        eta_p1: DIMENSIONLESS,
        eta_1: DIMENSIONLESS,
        f_ctd_t: MPA,
    ) -> None:
        r"""[$f_{bpt}$] Constant bond stress at which prestress is assumed to be transferred to the concrete [$MPa$].
        NEN-EN 1992-1-1+C2:2011 art.8.10.2.2(1) - Formula (8.15).

        Parameters
        ----------
        eta_p1 : DIMENSIONLESS
            [$\eta_{p1}$] Coefficient that takes into account the type of tendon and the bond situation at release [$-$].
            = 2.7 for indented wires.
            = 3.2 for 3 and 7-wire strands
            Use your own implementation for this value or use :class:`SubForm8Dot15EtaP1` class.
        eta_1 : DIMENSIONLESS
            [$\eta_1$] Coefficient related to the quality of the bond condition and the position of bar during concreting (see Figure 8.2) [$-$].
            = 1 when 'good' conditions are obtained;
            = 0.7 other cases and for bars in structural elements built with slip-forms, unless it can be shown that 'good' bond conditions exist;
            Use your own implementation of this formula or use the :class:`SubForm8Dot2CoefficientQualityOfBond` class.
        f_ctd_t : MPA
            [$f_{ctd}(t)$] Design tensile value of strength at time of release [$MPa$].
            = [$\alpha_{ct} \cdot 0.7 \cdot f_{ctm}(t) / \gamma_{c}$] (see 3.1.2(9) and 3.1.6(2)P)
            Use your own implementation for this value or use :class:`SubForm8Dot15TensileStrengthAtRelease` class.
        """
        super().__init__()
        self.eta_p1 = eta_p1
        self.eta_1 = eta_1
        self.f_ctd_t = f_ctd_t

    @staticmethod
    def _evaluate(
        eta_p1: DIMENSIONLESS,
        eta_1: DIMENSIONLESS,
        f_ctd_t: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            eta_p1=eta_p1,
            eta_1=eta_1,
            f_ctd_t=f_ctd_t,
        )
        return eta_p1 * eta_1 * f_ctd_t

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 8.15."""
        return LatexFormula(
            return_symbol=r"f_{bpt}",
            result=f"{self:.2f}",
            equation=r"\eta_{p1} \cdot \eta_1 \cdot f_{ctd}(t)",
            numeric_equation=rf"{self.eta_p1:.2f} \cdot {self.eta_1:.2f} \cdot {self.f_ctd_t:.2f}",
            comparison_operator_label="=",
        )


class SubForm8Dot15EtaP1(Formula):
    """Class representing sub-formula 8.15 for the calculation of the coefficient that takes into account the type of tendon and the bond situation
    at release.
    """

    label = "8.15"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        type_of_wire: str,
    ) -> None:
        r"""[$\eta_{p1}$] Coefficient that takes into account the type of tendon and the bond situation at release [$-$].

        NEN-EN 1992-1-1+C2:2011 art.8.10.2.2(1) - Formula (8.15)

        Parameters
        ----------
        type_of_wire : str
            Type of wire.

            = 'indented' for indented wires;

            = '3_7_wire_strands' for 3 and 7-wire strands;
        """
        super().__init__()
        self.type_of_wire = type_of_wire

    @staticmethod
    def _evaluate(type_of_wire: str) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        match type_of_wire.lower():
            case "indented":
                return 2.7
            case "3_7_wire_strands":
                return 3.2
            case _:
                raise ValueError(f"Invalid type of wire: {type_of_wire}. Options: 'indented' or '3_7_wire_strands'")

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for the first subformula of formula 8.15."""
        return LatexFormula(
            return_symbol=r"\eta_{p1}",
            result=f"{self:.2f}",
            equation=r"type\;of\;wire",
            numeric_equation=f"{self.type_of_wire}".replace(" ", r"\;"),
            comparison_operator_label=r"\rightarrow",
        )


class SubForm8Dot15TensileStrengthAtRelease(Formula):
    """Class representing sub-formula 8.15 for the calculation of the design tensile value of strength at time of release (see  3.1.2(8) and
    3.1.6(2)P).
    """

    label = "8.15"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_ct: DIMENSIONLESS,
        f_ctm_t: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> None:
        r"""[$f_{ctd}(t)$] Design tensile value of strength at time of release [$MPa$].

        NEN-EN 1992-1-1+C2:2011 art.8.10.2.2(1) - Formula (8.15)

        Parameters
        ----------
        alpha_ct : DIMENSIONLESS
            [$\alpha_{ct}$] coefficient taking account of long term effects on the tensile strength and of unfavourable effects, resulting from the
            way the load is applied. [$-$].

            Value may be found in national annex. Recommended value: 1.0
        f_ctm_t : MPA
            [$f_{ctm}(t)$] Mean value of tensile strength at time of release (see formula 3.4) [$MPa$].

            Use your own implementation for this value or use :class:`Form3Dot4DevelopmentTensileStrength` class.
        gamma_c : DIMENSIONLESS
            [$\gamma_{c}$] Partial safety factor for concrete [$-$].
        """
        super().__init__()
        self.alpha_ct = alpha_ct
        self.f_ctm_t = f_ctm_t
        self.gamma_c = gamma_c

    @staticmethod
    def _evaluate(
        alpha_ct: DIMENSIONLESS,
        f_ctm_t: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(alpha_ct=alpha_ct, f_ctm_t=f_ctm_t)
        raise_if_less_or_equal_to_zero(gamma_c=gamma_c)
        return alpha_ct * 0.7 * f_ctm_t / gamma_c

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for the second subformula of formula 8.15."""
        return LatexFormula(
            return_symbol=r"f_{ctd}(t)",
            result=f"{self:.2f}",
            equation=r"\frac{\alpha_{ct} \cdot 0.7 \cdot f_{ctm}(t)}{\gamma_c}",
            numeric_equation=rf"\frac{{{self.alpha_ct:.2f} \cdot 0.7 \cdot {self.f_ctm_t:.2f}}}{{{self.gamma_c:.2f}}}",
            comparison_operator_label="=",
        )
