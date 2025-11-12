"""Formula 7.11 from EN 1992-1-1:2004: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot11MaximumCrackSpacing(Formula):
    r"""Class representing formula 7.11 for the calculation of [$s_{r,max}$]."""

    label = "7.11"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        k_3: DIMENSIONLESS,
        c: MM,
        k_1: DIMENSIONLESS,
        k_2: DIMENSIONLESS,
        k_4: DIMENSIONLESS,
        diam: MM,
        rho_p_eff: DIMENSIONLESS,
    ) -> None:
        r"""[$s_{r,max}$] Calculation of the maximum crack spacing [$mm$].

        EN 1992-1-1:2004 art.7.3.4(3) - Formula (7.11)

        Parameters
        ----------
        k_3 : DIMENSIONLESS
            [$k_3$] Coefficient, the recommended value is 3.4 [$-$].
        c : MM
            [$c$] Cover to the longitudinal reinforcement [$mm$].
        k_1 : DIMENSIONLESS
            [$k_1$] Coefficient which takes account of the bond properties of the bonded reinforcement.
            Use 0.8 for high bond bars and 1.6 for bars with an efffectively plain surface
            (e.g. prestressing tendons) [$-$].
        k_2 : DIMENSIONLESS
            [$k_2$] Coefficient which takes account of the distribution of strain.
            Use 0.5 for bending, 1.0 for pure tension. For cases of eccentric tension or for local areas,
            intermediate values of k2 should be used which may be calculated with equation (7.13) [$-$] .
        k_4 : DIMENSIONLESS
            [$k_4$] Coefficient, the recommended value is 0.425 [$-$].
        diam : MM
            [$diam$] Bar diameter [$mm$]. Where a mixture of bar diameters is used in a section, an
            equivalent diameter, $⌀_{eq}$, should be used. For a section with $n_1$ bars of diameter $⌀_1$
            and $n_2$ bars of diameter $⌀_2$, expression (7.12) should be used to calculate $⌀_{eq}$.
        rho_p_eff : DIMENSIONLESS
            [$\rho_{p,eff}$] Effective reinforcement ratio [$-$].
        """
        super().__init__()
        self.k_3 = k_3
        self.c = c
        self.k_1 = k_1
        self.k_2 = k_2
        self.k_4 = k_4
        self.diam = diam
        self.rho_p_eff = rho_p_eff

    @staticmethod
    def _evaluate(
        k_3: DIMENSIONLESS,
        c: MM,
        k_1: DIMENSIONLESS,
        k_2: DIMENSIONLESS,
        k_4: DIMENSIONLESS,
        diam: MM,
        rho_p_eff: DIMENSIONLESS,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(k_3=k_3, c=c, k_1=k_1, k_2=k_2, k_4=k_4, diam=diam)
        raise_if_less_or_equal_to_zero(rho_p_eff=rho_p_eff)

        return k_3 * c + k_1 * k_2 * k_4 * diam / rho_p_eff

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.11."""
        _equation: str = r"k_3 \cdot c + k_1 \cdot k_2 \cdot k_4 \cdot \frac{⌀}{\rho_{p,eff}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"k_3": f"{self.k_3:.{n}f}",
                r"c ": f"{self.c:.{n}f} ",
                r"k_1": f"{self.k_1:.{n}f}",
                r"k_2": f"{self.k_2:.{n}f}",
                r"k_4": f"{self.k_4:.{n}f}",
                r"⌀": f"{self.diam:.{n}f}",
                r"\rho_{p,eff}": f"{self.rho_p_eff:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"s_{r,max}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm",
        )
