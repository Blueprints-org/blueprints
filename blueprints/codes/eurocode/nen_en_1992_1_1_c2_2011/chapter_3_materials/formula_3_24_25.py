"""Formula 3.24 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_negative


class Form3Dot24And25IncreasedCharacteristicCompressiveStrength(Formula):
    """Class representing formula 3.24 and 3.25 for the calculation of the increased characteristic compressive strength due to enclosed concrete."""

    label = "3.24 - 3.25"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
        sigma_2: MPA,
    ) -> None:
        r"""[$f_{ck,c}$] Increased characteristic compressive strength due to enclosed concrete [$MPa$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.9(2) - Formula (3.24 and 3.25)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength concrete [$MPa$].
            Valid range: [$f_{ck} \leq 90 \, MPa$].
        sigma_2 : MPA
            [$\sigma_2$] Effective compressive stress in transverse direction [$MPa$].

        Returns
        -------
        None
        """
        super().__init__()
        self.f_ck = f_ck
        self.sigma_2 = sigma_2

    @staticmethod
    def _evaluate(
        f_ck: MPA,
        sigma_2: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ck=f_ck, sigma_2=sigma_2)
        if sigma_2 <= 0.05 * f_ck:
            return f_ck * (1.000 + 5.0 * sigma_2 / f_ck)
        return f_ck * (1.125 + 2.5 * sigma_2 / f_ck)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.24 and 3.25."""
        if self.sigma_2 <= 0.05 * self.f_ck:
            return LatexFormula(
                return_symbol=r"f_{ck,c}",
                result=f"{self:.2f}",
                equation=r"f_{ck} \cdot (1.000 + 5.0 \cdot \sigma_2 / f_{ck})",
                numeric_equation=rf"{self.f_ck:.2f} \cdot (1.000 + 5.0 \cdot {self.sigma_2:.2f} / {self.f_ck:.2f})",
                comparison_operator_label="=",
            )
        return LatexFormula(
            return_symbol=r"f_{ck,c}",
            result=f"{self:.2f}",
            equation=r"f_{ck} \cdot (1.125 + 2.5 \cdot \sigma_2 / f_{ck})",
            numeric_equation=rf"{self.f_ck:.2f} \cdot (1.125 + 2.5 \cdot {self.sigma_2:.2f} / {self.f_ck:.2f})",
            comparison_operator_label="=",
        )
