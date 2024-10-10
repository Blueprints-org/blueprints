"""Formula 3.9 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula


class Form3Dot9DryingShrinkage(Formula):
    """Class representing formula 3.9 for the calculation of the drying shrinkage."""

    label = "3.9"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        beta_ds_tt_s: float,
        k_h: float,
        epsilon_cd_0: float,
    ) -> None:
        """[εcd(t)] Development of the drying shrinkage [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.9)

        Parameters
        ----------
        beta_ds_tt_s : float
            [βds(t, ts)] Coefficient that depends on the age t (in days) of the concrete for the drying shrinkage [-].
        k_h : float
            [kh] Coefficient depending on the fictional thickness h0 following table 3.3 [-].
            h0 = 100 -> kh = 1.0
            h0 = 200 -> kh = 0.85
            h0 = 300 -> kh = 0.75
            h0 >= 500 -> kh = 0.70
        epsilon_cd_0 : float
            [εcd,0] Nominal unobstructed drying shrinkage, formula in appendix B or use table 3.2 [-].

        Returns
        -------
        None
        """
        super().__init__()
        self.beta_ds_tt_s = beta_ds_tt_s
        self.k_h = k_h
        self.epsilon_cd_0 = epsilon_cd_0

    @staticmethod
    def _evaluate(
        beta_ds_tt_s: float,
        k_h: float,
        epsilon_cd_0: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if beta_ds_tt_s < 0:
            raise ValueError(f"Negative beta_ds_tt_s: {beta_ds_tt_s}. beta_ds_tt_s cannot be negative")
        if k_h < 0:
            raise ValueError(f"Negative k_h: {k_h}. k_h cannot be negative")
        return beta_ds_tt_s * k_h * epsilon_cd_0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.9."""
        return LatexFormula(
            return_symbol=r"\epsilon_{cd}(t)",
            result=f"{self:.3f}",
            equation=r"\beta_{ds}(t,t_s) \cdot k_h \cdot \epsilon_{cd,0}",
            numeric_equation=rf"{self.beta_ds_tt_s:.3f} \cdot {self.k_h:.3f} \cdot {self.epsilon_cd_0:.3f}",
            comparison_operator_label="=",
        )
