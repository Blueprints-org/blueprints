"""Formula 3.17 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class Form3Dot17CompressiveStressConcrete(Formula):
    """Class representing formula 3.17 for the calculation of compressive stress in concrete using stress-strain diagram of figure 3.3."""

    label = "3.17"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_cd: MPA,
        epsilon_c: DIMENSIONLESS,
        epsilon_c2: DIMENSIONLESS,
        n: DIMENSIONLESS,
    ) -> None:
        r"""[$\sigma_c$] Compressive stress in concrete using stress-strain diagram of figure 3.3 [$MPa$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.7(1) - Formula (3.17)

        Parameters
        ----------
        f_cd : MPA
            [$f_{cd}$] Design value compressive strength concrete [$MPa$].
        epsilon_c : DIMENSIONLESS
            [$\epsilon_c$] Strain in concrete [$-$].
        epsilon_c2 : DIMENSIONLESS
            [$\epsilon_{c2}$] Strain in concrete when reaching maximum strength following table 3.1 [$-$].
        n : DIMENSIONLESS
            Exponent following table 3.1.

        Returns
        -------
        None
        """
        super().__init__()
        self.f_cd = f_cd
        self.epsilon_c = epsilon_c
        self.epsilon_c2 = epsilon_c2
        self.n = n

    @staticmethod
    def _evaluate(
        f_cd: MPA,
        epsilon_c: DIMENSIONLESS,
        epsilon_c2: DIMENSIONLESS,
        n: DIMENSIONLESS,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_cd < 0:
            raise ValueError(f"Invalid f_cd: {f_cd}. f_cd cannot be negative")
        if epsilon_c < 0:
            raise ValueError(f"Invalid epsilon_c: {epsilon_c}. epsilon_c cannot be negative")
        if epsilon_c > epsilon_c2:
            raise ValueError(f"epsilon_c: {epsilon_c} > epsilon_c2: {epsilon_c2}. Try using Form3Dot18CompressiveStressConcrete class.")
        return f_cd * (1 - (1 - (epsilon_c / epsilon_c2)) ** n)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.17."""
        return LatexFormula(
            return_symbol=r"\sigma_c",
            result=f"{self:.3f}",
            equation=r"f_{cd} \cdot \left[ 1 - \left( 1 - \frac{\epsilon_c}{\epsilon_{c2}} \right)^n \right]",
            numeric_equation=(
                rf"{self.f_cd:.3f} \cdot \left[ 1 - \left( 1 - \frac{{{self.epsilon_c:.3f}}}"
                rf"{{{self.epsilon_c2:.3f}}} \right)^{{{self.n:.2f}}} \right]"
            ),
            comparison_operator_label="=",
        )
