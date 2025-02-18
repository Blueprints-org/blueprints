"""Formula 9.1N from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailing of members and particular rules."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction, latex_max_curly_brackets
from blueprints.type_alias import MM, MM2, MPA
from blueprints.validations import raise_if_negative


class Form9Dot1nMinimumTensileReinforcementBeam(Formula):
    """Class representing the formula 9.1N for the calculation of minimum tensile reinforcement area in longitudinal direction for beams."""

    label = "9.1N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ctm: MPA,
        f_yk: MPA,
        b_t: MM,
        d: MM,
    ) -> None:
        r"""[$A_{s,min}$] Calculates minimum required tensile reinforcement area in longitudinal direction for beams [$\text{mm}^2$].

        NEN-EN 1992-1-1+C2:2011 art.9.2.1.1(1) - Formula (9.1N)

        Notes
        -----
        [${A_{s,min}}$] is no less than [${0.0013 \cdot b_t \cdot d}$]

        Parameters
        ----------
        f_ctm: MPA
            [${f_{ctm}}$] Mean axial tensile stress concrete [$\text{MPa}$].
            Should be determined with respect to the relevant strength class according to Table 3.1
        f_yk: MPA
            [${f_{yk}}$] Characteristic yield strength reinforcement steel [$\text{MPa}$].
        b_t: MM
            [${b_t}$] Mean width of the concrete tension zone, for T-beams with a flange under compression only the width of the web is
            considered for calculating [${b_t}$] [$\text{mm}$].
        d: MM
            [${d}$] Effective height of the cross-section [$\text{mm}$].
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
        fraction = latex_fraction(numerator=f"{self.f_ctm:.2f}", denominator=f"{self.f_yk:.2f}")
        return LatexFormula(
            return_symbol=r"A_{s,min}",
            result=f"{self:.2f}",
            equation=latex_max_curly_brackets(
                rf"0.26 \cdot {latex_fraction(numerator=r'f_{ctm}', denominator=r'f_{yk}')} \cdot b_t \cdot d",
                r"0.0013 \cdot b_t \cdot d",
            ),
            numeric_equation=latex_max_curly_brackets(
                rf"0.26 \cdot {fraction} \cdot {self.b_t:.2f} \cdot {self.d:.2f}",
                rf"0.0013 \cdot {self.b_t:.2f} \cdot {self.d:.2f}",
            ),
            comparison_operator_label="=",
        )
