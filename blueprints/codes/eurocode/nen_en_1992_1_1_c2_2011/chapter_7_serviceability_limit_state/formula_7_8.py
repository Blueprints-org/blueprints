"""Formula 7.8 from NEN-EN 1992-1-1+C2:2011: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_negative


class Form7Dot8CrackWidth(Formula):
    r"""Class representing formula 7.8 for the calculation of the crack width [$w_k$]."""

    label = "7.8"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        s_r_max: MM,
        epsilon_sm_minus_epsilon_cm: DIMENSIONLESS,
    ) -> None:
        r"""[$w_k$] Calculation of the crack width [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.7.3.4(1) - Formula (7.8)

        Parameters
        ----------
        s_r_max : MM
            [$s_{r,max}$] Maximum crack spacing [$mm$].
        epsilon_sm_minus_epsilon_cm : DIMENSIONLESS
            [$\epsilon_{sm} - \epsilon_{cm}$] Difference between mean strain in reinforcement and mean strain in concrete [$-$].
        """
        super().__init__()
        self.s_r_max = s_r_max
        self.epsilon_sm_minus_epsilon_cm = epsilon_sm_minus_epsilon_cm

    @staticmethod
    def _evaluate(
        s_r_max: MM,
        epsilon_sm_minus_epsilon_cm: DIMENSIONLESS,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(s_r_max=s_r_max, epsilon_sm_minus_epsilon_cm=epsilon_sm_minus_epsilon_cm)

        return s_r_max * epsilon_sm_minus_epsilon_cm

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 7.8."""
        _equation: str = r"s_{r,max} \cdot (\epsilon_{sm} - \epsilon_{cm})"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"s_{r,max}": f"{self.s_r_max:.3f}",
                r"\epsilon_{sm} - \epsilon_{cm}": f"{self.epsilon_sm_minus_epsilon_cm:.6f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"w_k",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm",
        )
