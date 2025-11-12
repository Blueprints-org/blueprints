"""Formula 7.19 from EN 1992-1-1:2004: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot19DistributionCoefficient(Formula):
    r"""Class representing formula 7.19 for the calculation of [$\zeta$]."""

    label = "7.19"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        beta: DIMENSIONLESS,
        sigma_sr: MPA,
        sigma_s: MPA,
    ) -> None:
        r"""[$\zeta$] Calculation of the distribution coefficient, 0 for uncracked sections [$\zeta$].

        Note: $\sigma_{sr} / \sigma_{s}$ may be replaced by $M_{cr} / M$ for flexure or $N_{cr} / N$ for pure tension,
        where $M_{cr}$ is the cracking moment and $N_{cr}$ is the cracking force.

        EN 1992-1-1:2004 art.7.4.3(3) - Formula (7.19)

        Parameters
        ----------
        beta : DIMENSIONLESS
            [$\beta$] Coefficient taking account of the influence of the duration of the loading or of
            repeated loading on the average strain. For short-term loading, [$\beta$] = 1.0. For sustained loads or
            many cycles of repeated loading [$\beta$] = 0.5 [$-$].
        sigma_sr : MPA
            [$\sigma_{sr}$] Stress in the tension reinforcement calculated on the basis of a
            cracked section under the loading conditions causing first cracking [$MPa$].
        sigma_s : MPA
            [$\sigma_{s}$] Stress in the tension reinforcement calculated on the basis of a cracked section under
            loading conditions causing first cracking [$MPa$].
        """
        super().__init__()
        self.beta = beta
        self.sigma_sr = sigma_sr
        self.sigma_s = sigma_s

    @staticmethod
    def _evaluate(
        beta: DIMENSIONLESS,
        sigma_sr: MPA,
        sigma_s: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(beta=beta, sigma_sr=sigma_sr, sigma_s=sigma_s)
        raise_if_less_or_equal_to_zero(sigma_s=sigma_s)

        return 1 - beta * (sigma_sr / sigma_s) ** 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.19."""
        _equation: str = r"1 - \beta \left(\frac{\sigma_{sr}}{\sigma_{s}}\right)^2"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\beta": f"{self.beta:.{n}f}",
                r"\sigma_{sr}": f"{self.sigma_sr:.{n}f}",
                r"\sigma_{s}": f"{self.sigma_s:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\zeta",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
