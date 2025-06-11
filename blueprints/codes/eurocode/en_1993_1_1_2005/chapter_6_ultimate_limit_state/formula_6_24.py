"""Formula 6.24 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM
from blueprints.validations import raise_if_negative


class Form6Dot24TotalTorsionalMoment(Formula):
    r"""Class representing formula 6.24 for the calculation of [$T_{Ed}$]."""

    label = "6.24"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        t_t_ed: NMM,
        t_w_ed: NMM,
    ) -> None:
        r"""[$T_{Ed}$] Calculation of the total torsional moment [$Nmm$].

        EN 1993-1-1:2005 art.6.2.7(2) - Formula (6.24)

        Parameters
        ----------
        t_t_ed : NMM
            [$T_{t,Ed}$] Internal St. Venant torsion [$Nmm$].
        t_w_ed : NMM
            [$T_{w,Ed}$] Internal warping torsion [$Nmm$].
        """
        super().__init__()
        self.t_t_ed = t_t_ed
        self.t_w_ed = t_w_ed

    @staticmethod
    def _evaluate(
        t_t_ed: NMM,
        t_w_ed: NMM,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(t_t_ed=t_t_ed, t_w_ed=t_w_ed)

        return t_t_ed + t_w_ed

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.24."""
        _equation: str = r"T_{t,Ed} + T_{w,Ed}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"T_{t,Ed}": f"{self.t_t_ed:.{n}f}",
                r"T_{w,Ed}": f"{self.t_w_ed:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"T_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="Nmm",
        )
