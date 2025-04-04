"""Formula 4.2 from NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020: Chapter 4 - Durability and cover to reinforcement."""

from blueprints.codes.eurocode.nen_en_1992_1_1_a1_2020 import NEN_EN_1992_1_1_A1_2020
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_max_curly_brackets
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form4Dot2MinimumConcreteCover(Formula):
    """Class representing the formula 4.2 for the calculation of the minimum concrete cover [$c_{min}$] [$mm$]."""

    label = "4.2"
    source_document = NEN_EN_1992_1_1_A1_2020

    def __init__(
        self,
        c_min_b: MM,
        c_min_dur: MM,
        delta_c_dur_gamma: MM = 0,
        delta_c_dur_st: MM = 0,
        delta_c_dur_add: MM = 0,
    ) -> None:
        r"""[$c_{min}$] Calculates the minimum concrete cover [$mm$].

        A minimum concrete cover of 10 mm is required, even if the calculated value is lower.

        NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 art.4.4.1.2 (2) - formula (4.2)

        Parameters
        ----------
        c_min_b: MM
            [$c_{min,b}$] The minimum concrete cover based on the adhesion requirements based on art. 4.4.1.2 (3) [$mm$].
        c_min_dur: MM
            [$c_{min,dur}$] The minimum concrete cover based on environmental conditions based on art. 4.4.1.2 (5) [$mm$].
        delta_c_dur_gamma: MM
            [$\Delta c_{dur,\gamma}$] An additional safety requirement based on art. 4.4.1.2 (6) [$mm$].
            The value of [$\Delta c_{dur,\gamma}$] for use in a Country may be found in its National Annex.
            The recommended value is 0 mm. 0 mm is the default value in the formula if not specified otherwise.
        delta_c_dur_st: MM
            [$\Delta c_{dur,st}$] A reduction of minimum concrete cover when using stainless steel based on art. 4.4.1.2 (7) [$mm$].
            The value of [$\Delta c_{dur,st}$] for use in a Country may be found in its National Annex.
            The recommended value, without further specification, is 0 mm. 0 mm is the default value in the formula if not specified otherwise.
        delta_c_dur_add: MM
            [$\Delta c_{dur,add}$] A reduction of minimum concrete cover when using additional protection based on art. 4.4.1.2 (8) [$mm$].
            The value of [$\Delta c_{dur,add}$] for use in a Country may be found in its National Annex.
            The recommended value, without further specification, is 0 mm. 0 mm is the default value in the formula if not specified otherwise.
        """
        super().__init__()
        self.c_min_b = c_min_b
        self.c_min_dur = c_min_dur
        self.delta_c_dur_gamma = delta_c_dur_gamma
        self.delta_c_dur_st = delta_c_dur_st
        self.delta_c_dur_add = delta_c_dur_add

    @staticmethod
    def _evaluate(
        c_min_b: MM,
        c_min_dur: MM,
        delta_c_dur_gamma: MM = 0,
        delta_c_dur_st: MM = 0,
        delta_c_dur_add: MM = 0,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            c_min_b=c_min_b,
            c_min_dur=c_min_dur,
            delta_c_dur_gamma=delta_c_dur_gamma,
            delta_c_dur_st=delta_c_dur_st,
            delta_c_dur_add=delta_c_dur_add,
        )
        minimum_cover = 10  # mm
        return max(c_min_b, c_min_dur + delta_c_dur_gamma - delta_c_dur_st - delta_c_dur_add, minimum_cover)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 4.2."""
        return LatexFormula(
            return_symbol=r"c_{min}",
            result=str(self),
            equation=latex_max_curly_brackets(
                r"c_{min,b}",
                r"c_{min,dur}+\Delta c_{dur,\gamma}-\Delta c_{dur,st}-\Delta c_{dur,add}",
                r"10 \text{mm}",
            ),
            numeric_equation=latex_max_curly_brackets(
                self.c_min_b,
                f"{self.c_min_dur}+{self.delta_c_dur_gamma}-{self.delta_c_dur_st}-{self.delta_c_dur_add}",
                10,
            ),
            comparison_operator_label="=",
        )
