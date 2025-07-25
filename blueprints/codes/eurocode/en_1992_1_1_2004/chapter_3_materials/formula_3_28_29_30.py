"""Sub-formula 3.28, 3.29 and 3.30 from EN 1992-1-1:2004: Chapter 3 - Materials."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class SubForm3Dot28And29And30Mu(Formula):
    """Class representing sub-formula for 3.28, 3.29 and 3.30 for the calculation of μ."""

    label = "3.28 - 3.29 - 3.30"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        sigma_pi: MPA,
        f_pk: MPA,
    ) -> None:
        r"""[$\mu$] Ratio between initial pre-stress and characteristic tensile strength  [$\sigma_{pi} / f_{pk}$] [$-$].

        EN 1992-1-1:2004 art.3.3.2(7) - [$\mu$]

        Parameters
        ----------
        sigma_pi : MPA
            [$\sigma_{pi}$] Initial pre-stress [$MPa$]
        f_pk : MPA
            [$f_{pk}$] Characteristic tensile strength of pre-stress steel [$MPa$]

        Returns
        -------
        None
        """
        super().__init__()
        self.sigma_pi = sigma_pi
        self.f_pk = f_pk

    @staticmethod
    def _evaluate(
        sigma_pi: MPA,
        f_pk: MPA,
    ) -> DIMENSIONLESS:
        r"""Evaluates the formula, for more information see the __init__ method."""
        if f_pk < 0:
            raise ValueError(f"Invalid f_pk: {f_pk}. f_pk cannot be negative")
        return sigma_pi / f_pk

    def latex(self, n: int = 3) -> LatexFormula:
        r"""Returns LatexFormula object for [$\mu$] in formula 3.28 and 3.29 and 3.30."""
        return LatexFormula(
            return_symbol=r"\mu",
            result=f"{self:.{n}f}",
            equation=r"\sigma_{pi} / f_{pk}",
            numeric_equation=rf"{self.sigma_pi:.{n}f} / {self.f_pk:.{n}f}",
            comparison_operator_label="=",
        )
