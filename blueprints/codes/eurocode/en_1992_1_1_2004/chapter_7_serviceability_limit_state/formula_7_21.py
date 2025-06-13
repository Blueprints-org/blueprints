"""Formula 7.21 from EN 1992-1-1:2004: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM3, MM4, MPA, ONE_OVER_MM
from blueprints.validations import raise_if_negative


class Form7Dot21CurvatureDueToShrinkage(Formula):
    r"""Class representing formula 7.21 for the calculation of [$\frac{1}{r_{cs}}$]."""

    label = "7.21"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        epsilon_cs: DIMENSIONLESS,
        es: MPA,
        ec_eff: MPA,
        capital_s: MM3,
        capital_i: MM4,
    ) -> None:
        r"""[$\frac{1}{r_{cs}}$] Calculation of the curvature due to shrinkage [$mm^{-1}$].

        S and i should be calculated for the uncracked condition and the fully cracked condition, the
        final curvature being assessed by use of Expression (7.18).

        EN 1992-1-1:2004 art.7.4.3(6) - Formula (7.21)

        Parameters
        ----------
        epsilon_cs : DIMENSIONLESS
            [$\epsilon_{cs}$] Free shrinkage strain, see 3.1.4.
        es : MPA
            [$E_s$] Modulus of elasticity of the reinforcement [$MPa$].
        ec_eff : MPA
            [$E_{c,eff}$] Effective modulus of elasticity of the concrete [$MPa$].
        s : MM3
            [$S$] First moment of area of the reinforcement about the centroid of the section [$mm^3$].
        i : MM4
            [$I$] Second moment of area of the section [$mm^4$].
        """
        super().__init__()
        self.epsilon_cs = epsilon_cs
        self.es = es
        self.ec_eff = ec_eff
        self.capital_s = capital_s
        self.capital_i = capital_i

    @staticmethod
    def _evaluate(
        epsilon_cs: DIMENSIONLESS,
        es: MPA,
        ec_eff: MPA,
        capital_s: MM3,
        capital_i: MM4,
    ) -> ONE_OVER_MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(epsilon_cs=epsilon_cs, es=es, ec_eff=ec_eff, capital_s=capital_s, capital_i=capital_i)

        return epsilon_cs * es / ec_eff * (capital_s / capital_i)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.21."""
        _equation: str = r"\epsilon_{cs} \cdot \frac{E_s}{E_{c,eff}} \cdot \frac{S}{I}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\epsilon_{cs}": f"{self.epsilon_cs:.{n + 1}f}",
                r"E_s": f"{self.es:.{n}f}",
                r"E_{c,eff}": f"{self.ec_eff:.{n}f}",
                r"S": f"{self.capital_s:.{n}f}",
                r"I": f"{self.capital_i:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\frac{1}{r_{cs}}",
            result=f"{self:.{n + 3}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^{-1}",
        )
