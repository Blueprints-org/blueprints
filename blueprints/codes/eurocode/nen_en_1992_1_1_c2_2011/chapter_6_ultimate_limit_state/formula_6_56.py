"""Formula 6.56 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form6Dot56DesignStrengthConcreteStrussTransverseTension(Formula):
    r"""Class representing formula 6.56 for the calculation of [$\sigma_{Rd,max}$]."""

    label = "6.56"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        nu_prime: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        r"""[$\sigma_{Rd,max}$] Calculation of [$\sigma_{Rd,max}$].

        NEN-EN 1992-1-1+C2:2011 art.6.5.2(2) - Formula (6.56)

        Parameters
        ----------
        nu_prime : float
            [$\nu'$] Factor for transverse tension [-]. The value of $\nu'$ for use in a Country may be found in its National Annex.
            The recommended value is given by equation (6.57N).
        f_cd : float
            [$f_{cd}$] Design compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.nu_prime = nu_prime
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        nu_prime: DIMENSIONLESS,
        f_cd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(nu_prime=nu_prime, f_cd=f_cd)

        return 0.6 * nu_prime * f_cd

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.56."""
        _equation: str = r"0.6 \cdot \nu' \cdot f_{cd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\nu'": f"{self.nu_prime:.3f}",
                r"f_{cd}": f"{self.f_cd:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{Rd,max}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
