"""Formula 3.5 from EN 1992-1-1:2004: Chapter 3 - Materials."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MPA


class Form3Dot5ApproximationVarianceElasticModulusOverTime(Formula):
    """Class representing formula 3.5 for the approximation of the elastic modulus, Ecm(t) at day t."""

    label = "3.5"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_cm_t: MPA,
        f_cm: MPA,
        e_cm: MPA,
    ) -> None:
        r"""[$E_{cm}(t)$] The approximated elastic modulus at day t [$MPa$].

        EN 1992-1-1:2004 art.3.1.3(3) - Formula (3.5)

        Parameters
        ----------
        f_cm_t : MPA
            [$f_{cm}(t)$] Compressive strength concrete at t days [$MPa$].
        f_cm : MPA
            [$f_{cm}$] Average concrete compressive strength on day 28 based on table 3.1 [$MPa$].
        e_cm : MPA
            [$E_{cm}$] Average elastic modulus on day 28 [$MPa$].

        Returns
        -------
        None
        """
        super().__init__()
        self.f_cm_t = f_cm_t
        self.f_cm = f_cm
        self.e_cm = e_cm

    @staticmethod
    def _evaluate(
        f_cm_t: MPA,
        f_cm: MPA,
        e_cm: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_cm_t < 0:
            raise ValueError(f"Negative f_cm_t: {f_cm_t}. f_cm_t cannot be negative")
        if f_cm < 0:
            raise ValueError(f"Negative f_cm: {f_cm}. f_cm cannot be negative")
        if e_cm < 0:
            raise ValueError(f"Negative e_cm: {e_cm}. e_cm cannot be negative")
        return (f_cm_t / f_cm) ** 0.3 * e_cm

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 3.5."""
        return LatexFormula(
            return_symbol=r"E_{cm}(t)",
            result=f"{self:.{n}f}",
            equation=r"( f_{cm}(t) / f_{cm} )^{0.3} \cdot E_{cm}",
            numeric_equation=rf"( {self.f_cm_t:.{n}f} / {self.f_cm:.{n}f} )^{{0.3}} \cdot {self.e_cm:.{n}f}",
            comparison_operator_label="=",
        )
