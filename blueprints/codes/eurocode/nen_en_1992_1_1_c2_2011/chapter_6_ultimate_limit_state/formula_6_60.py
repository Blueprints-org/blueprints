"""Formula 6.60 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form6Dot60DesignValueCompressiveStressResistance(Formula):
    r"""Class representing formula 6.60 for the calculation of [$\sigma_{Rd,max}$]."""

    label = "6.60"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        k_1: DIMENSIONLESS,
        nu_prime: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        r"""[$\sigma_{Rd,max}$] Calculation of [$\sigma_{Rd,max}$].

        NEN-EN 1992-1-1+C2:2011 art.6.5.4(4) - Formula (6.60)

        Parameters
        ----------
        k_1 : DIMENSIONLESS
            [$k_1$] Coefficient for the design value of compressive stress resistance [$-$].
            Note: The value of [$k_1$] for use in a Country may be found in its National Annex.
            The recommended value is 1.0.
        nu_prime : DIMENSIONLESS
            [$\nu'$] Reduction factor for the design value of compressive stress resistance [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of compressive strength [$MPa$].
        """
        super().__init__()
        self.k_1 = k_1
        self.nu_prime = nu_prime
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        k_1: DIMENSIONLESS,
        nu_prime: DIMENSIONLESS,
        f_cd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(k_1=k_1, nu_prime=nu_prime, f_cd=f_cd)

        return k_1 * nu_prime * f_cd

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.60."""
        _equation: str = r"k_1 \cdot \nu' \cdot f_{cd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"k_1": f"{self.k_1:.3f}",
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
