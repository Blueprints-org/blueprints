"""Formula 6.24 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM
from blueprints.validations import raise_if_negative


class Form6Dot24TotalTorsionalMoment(Formula):
    r"""Class representing formula 6.24 for the calculation of [$T_{Ed}$]."""

    label = "6.24"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        t_t_ed: NMM,
        t_w_ed: NMM,
    ) -> None:
        r"""[$T_{Ed}$] Calculation of the total torsional moment [$Nmm$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.7(2) - Formula (6.24)

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
