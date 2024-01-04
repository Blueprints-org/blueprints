"""Formula 9.1N from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailing of members and particular rules."""
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction, latex_max_curly_brackets, latex_value_to_text, latex_variable_with_subscript
from blueprints.type_alias import MM, MM2, MPA
from blueprints.validations import raise_if_negative


class Form9Dot1NMinimumTensileReinforcementBeam(Formula):
    """Class representing the formula 9.1N for the calculation of minimum tensile reinforcement area in longitudinal direction for beams
    :math:`A_{s,min}` [:math:`mm^2`].
    """

    label = "9.1N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ctm: MPA,
        f_yk: MPA,
        b_t: MM,
        d: MM,
    ) -> None:
        """[:math:`A_{s,min}`] Calculates the minimum required tensile reinforcement area in longitudinal direction for beams [:math:`mm^2`].

        NEN-EN 1992-1-1+C2:2011 art.9.2.1.1(1) - Formula (9.1N)

        Notes
        -----
        As,min is no less than 0,0013 * bt * d

        Parameters
        ----------
        f_ctm: MPA
            [:math:`f_{ctm}`] Mean axial tensile stress concrete [:math:`MPa`].
            Should be determined with respect to the relevant strength class according to Table 3.1
        f_yk: MPA
            [:math:`f_{yk}`] Characteristic yield strength reinforcement steel [:math:`MPa`].
        b_t: MM
            [:math:`b_t`] Mean width of the concrete tension zone, for T-beams with a flange under compression only the width of the web is considered
            for calculating bt [:math:`mm`].
        d: MM
            [:math:`d`] Effective height of the cross-section [:math:`mm`].
        """
        super().__init__()
        self.f_ctm = f_ctm
        self.f_yk = f_yk
        self.b_t = b_t
        self.d = d

    @staticmethod
    def _evaluate(
        f_ctm: MPA,
        f_yk: MPA,
        b_t: MM,
        d: MM,
    ) -> MM2:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)
        return max(0.26 * (f_ctm / f_yk) * b_t * d, 0.0013 * b_t * d)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 9.1N."""
        latex_f_ctm = latex_variable_with_subscript(variable="f", subscript="ctm")
        latex_f_yk = latex_variable_with_subscript(variable="f", subscript="yk")
        latex_b_t = latex_variable_with_subscript(variable="b", subscript="t")
        return LatexFormula(
            return_symbol=latex_variable_with_subscript(variable="A", subscript="s,min"),
            result=latex_value_to_text(self),
            equation=latex_max_curly_brackets(
                rf"{latex_value_to_text(0.26)} \cdot {latex_fraction(latex_f_ctm, latex_f_yk)} \cdot {latex_b_t} \cdot d",
                rf"{latex_value_to_text(0.0013)} \cdot {latex_b_t} \cdot d",
            ),
            numeric_equation=latex_max_curly_brackets(
                rf"{latex_value_to_text(0.26)} \cdot {latex_fraction(self.f_ctm, self.f_yk)} \cdot {latex_value_to_text(self.b_t)} \cdot "
                f"{latex_value_to_text(self.d)}",
                rf"{latex_value_to_text(0.0013)} \cdot {latex_value_to_text(self.b_t)} \cdot {latex_value_to_text(self.d)}",
            ),
            comparison_operator_label="=",
        )
