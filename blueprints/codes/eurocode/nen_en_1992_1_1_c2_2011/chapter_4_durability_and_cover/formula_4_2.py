"""Formula 4.2 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement."""
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, max_curly_brackets, to_text, variable_with_subscript
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form4Dot2MinimumConcreteCover(Formula):
    """Class representing the formula 4.2 for the calculation of the minimum concrete cover :math:`c_{min}` [:math:`mm`]."""

    label = "4.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c_min_b: MM,
        c_min_dur: MM,
        delta_c_dur_gamma: MM,
        delta_c_dur_st: MM,
        delta_c_dur_add: MM,
    ) -> None:
        """[:math:`c_{min}`] Calculates the minimum concrete cover [:math:`mm`].

        NEN-EN 1992-1-1+C2:2011 art.4.4.1.2 (2) - formula (4.2)

        Parameters
        ----------
        c_min_b: MM
            [:math:`c_{min,b}`] The minimum concrete cover based on the adhesion requirements based on art. 4.4.1.2 (3) [:math:`mm`].
        c_min_dur: MM
            [:math:`c_{min,dur}`] The minimum concrete cover based on environmental conditions based on art. 4.4.1.2 (5) [:math:`mm`].
        delta_c_dur_gamma: MM
            [:math:`Δc_{dur,γ}`] An additional safety requirement based on art. 4.4.1.2 (6) [:math:`mm`].
        delta_c_dur_st: MM
            [:math:`Δc_{dur,st}`] A reduction of minimum concrete cover when using stainless steel based on art. 4.4.1.2 (7) [:math:`mm`].
        delta_c_dur_add: MM
            [:math:`Δc_{dur,add}`] A reduction of minimum concrete cover when using additional protection based on art. 4.4.1.2 (8) [:math:`mm`].
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
        delta_c_dur_gamma: MM,
        delta_c_dur_st: MM,
        delta_c_dur_add: MM,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            c_min_b=c_min_b,
            c_min_dur=c_min_dur,
            delta_c_dur_gamma=delta_c_dur_gamma,
            delta_c_dur_st=delta_c_dur_st,
            delta_c_dur_add=delta_c_dur_add,
        )
        return max(c_min_b, c_min_dur + delta_c_dur_gamma - delta_c_dur_st - delta_c_dur_add, 10)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 4.2."""
        arg_1 = self.c_min_b
        arg_2 = f"{to_text(self.c_min_dur)}+{to_text(self.delta_c_dur_gamma)}-{to_text(self.delta_c_dur_st)}-{to_text(self.delta_c_dur_add)}"
        arg_3 = 10

        latex_c_min_dur = variable_with_subscript("c", "min,dur")
        latex_delta_c_dur_gamma = variable_with_subscript(r"\Delta c", r"dur,\gamma")
        latex_delta_c_dur_st = variable_with_subscript(r"\Delta c", "dur,st")
        latex_delta_c_dur_add = variable_with_subscript(r"\Delta c", "dur,add")

        return LatexFormula(
            return_symbol=variable_with_subscript("c", "min"),
            result=to_text(self),
            equation=max_curly_brackets(
                variable_with_subscript("c", "min,b"),
                f"{latex_c_min_dur}+{latex_delta_c_dur_gamma}-{latex_delta_c_dur_st}-{latex_delta_c_dur_add}",
                to_text("10 mm"),
            ),
            numeric_equation=max_curly_brackets(arg_1, arg_2, arg_3),
            comparison_operator_label="=",
        )
