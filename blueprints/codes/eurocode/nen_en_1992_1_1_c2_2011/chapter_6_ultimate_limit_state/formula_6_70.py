"""Formula 6.70 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_lists_differ_in_length, raise_if_negative


class Form6Dot70FatigueDamageFactor(Formula):
    """Class representing formula 6.70 for the calculation of the fatigue damage factor [$D_{Ed}$]."""

    label = "6.70"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, n_delta_sigma_i: list[MPA], capital_n_delta_sigma_i: list[MPA]) -> None:
        r"""[D_{Ed}] The calculation of the fatigue damage factor [-].

        NEN-EN 1992-1-1+C2:2011 art.6.8.4(2) - Formula (6.70)

        Parameters
        ----------
        n_delta_sigma_i : list[MPA]
            [$n(\Delta \sigma_i)$] The applied number of cycles for a stress range [MPa].
        capital_n_delta_sigma_i : list[MPA]
            [$N(\Delta \sigma_i)$] The resisting number of cycles for a stress range [MPa]

        Returns
        -------
        None
        """
        super().__init__()
        self.n_delta_sigma_i = n_delta_sigma_i
        self.capital_n_delta_sigma_i = capital_n_delta_sigma_i

    @staticmethod
    def _evaluate(
        n_delta_sigma_i: list[MPA],
        capital_n_delta_sigma_i: list[MPA],
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_lists_differ_in_length(n_delta_sigma_i=n_delta_sigma_i, capital_n_delta_sigma_i=capital_n_delta_sigma_i)
        raise_if_negative(min_n_delta_sigma_i=min(n_delta_sigma_i))
        raise_if_less_or_equal_to_zero(min_capital_n_delta_sigma_i=min(capital_n_delta_sigma_i))
        return sum(n / capital_n for n, capital_n in zip(n_delta_sigma_i, capital_n_delta_sigma_i)) < 1

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.70."""
        _equation: str = r"\sum_{i} \frac{n(\Delta \sigma_i)}{N(\Delta \sigma_i)} < 1"
        _numeric_equation: str = ""
        for n, capital_n in zip(self.n_delta_sigma_i, self.capital_n_delta_sigma_i):
            _numeric_equation += f"\\frac{{{n:.3f}}}{{{capital_n:.3f}}} + "
        _numeric_equation = _numeric_equation[:-3] + " < 1"
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
