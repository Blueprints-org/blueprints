"""Formula 3.14 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class Form3Dot14StressStrainForShortTermLoading(Formula):
    """Class representing formula 3.14, which calculates the compressive stress-strength ratio."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.14"

    def __init__(
        self,
        k: DIMENSIONLESS,
        eta: DIMENSIONLESS,
    ) -> None:
        r"""[$\sigma_c / f_{cm}$] Compressive stress-strength ratio [$-$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.5(1) - Formula (3.14)

        Parameters
        ----------
        k : DIMENSIONLESS
            [$k$] [$-$].
            = 1.05 * Ecm * |$\epsilon_{c1}$| / fcm
            Use your own implementation of this formula or use the SubForm3Dot14K class.
        eta : DIMENSIONLESS
            [$\eta$] Strain - peak-strain ratio [$-$].
            = $\epsilon_c / \epsilon_{c1}$
            Use your own implementation of this formula or use the SubForm3Dot14Eta class.

        Returns
        -------
        None
        """
        super().__init__()
        self.k = k
        self.eta = eta

    @staticmethod
    def _evaluate(
        k: DIMENSIONLESS,
        eta: DIMENSIONLESS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if k < 0:
            raise ValueError(f"Invalid k: {k}. k cannot be negative")
        if eta < 0:
            raise ValueError(f"Invalid eta: {eta}. eta cannot be negative")
        return (k * eta - eta**2) / (1 + (k - 2) * eta)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.14."""
        return LatexFormula(
            return_symbol=r"\frac{\sigma_c}{f_{cm}}",
            result=f"{self:.3f}",
            equation=r"\frac{k \cdot \eta - \eta^2}{1 + (k-2) \cdot \eta}",
            numeric_equation=rf"\frac{{{self.k:.3f} \cdot {self.eta:.3f} - {self.eta:.3f}^2}}{{1 + ({self.k:.3f}-2) \cdot {self.eta:.3f}}}",
            comparison_operator_label="=",
        )


class SubForm3Dot14Eta(Formula):
    """Class representing sub-formula 1 for formula 3.14, which calculates eta."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.14"

    def __init__(
        self,
        epsilon_c: DIMENSIONLESS,
        epsilon_c1: DIMENSIONLESS,
    ) -> None:
        r"""[$\eta$] Strain - peak-strain ratio [$-$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.5(1) - η

        Parameters
        ----------
        epsilon_c : DIMENSIONLESS
            [$\epsilon_c$] Strain concrete [$-$].
        epsilon_c1 : DIMENSIONLESS
            [$\epsilon_{c1}$] Strain concrete at peak-stress following table 3.1 [$-$].
        """
        super().__init__()
        self.epsilon_c = epsilon_c
        self.epsilon_c1 = epsilon_c1

    @staticmethod
    def _evaluate(
        epsilon_c: DIMENSIONLESS,
        epsilon_c1: DIMENSIONLESS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        return epsilon_c / epsilon_c1

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.14 sub 1."""
        return LatexFormula(
            return_symbol=r"\eta",
            result=f"{self:.3f}",
            equation=r"\epsilon_c / \epsilon_{c1}",
            numeric_equation=rf"{self.epsilon_c:.3f} / {self.epsilon_c1:.3f}",
            comparison_operator_label="=",
        )


class SubForm3Dot14K(Formula):
    """Class representing sub-formula 2 for formula 3.14, which calculates k."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.14"

    def __init__(self, e_cm: MPA, epsilon_c1: DIMENSIONLESS, f_cm: MPA) -> None:
        r"""[$k$] [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.5(1) - k

        Parameters
        ----------
        e_cm : MPA
            [$E_{cm}$] Elastic modulus concrete [$MPa$].
        epsilon_c1 : DIMENSIONLESS
            [$\epsilon_{c1}$] Strain concrete at peak-stress following table 3.1 [$-$].
        f_cm : MPA
            [$f_{cm}$] Compressive strength concrete [$MPa$].
        """
        super().__init__()
        self.e_cm = e_cm
        self.epsilon_c1 = epsilon_c1
        self.f_cm = f_cm

    @staticmethod
    def _evaluate(
        e_cm: MPA,
        epsilon_c1: DIMENSIONLESS,
        f_cm: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if e_cm < 0:
            raise ValueError(f"Invalid e_cm: {e_cm}. e_cm cannot be negative")
        if f_cm <= 0:
            raise ValueError(f"Invalid f_cm: {f_cm}. f_cm cannot be negative or zero")
        return 1.05 * e_cm * abs(epsilon_c1) / f_cm

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.14 sub 2."""
        return LatexFormula(
            return_symbol=r"k",
            result=f"{self:.3f}",
            equation=r"1.05 \cdot E_{cm} \cdot |\epsilon_{c1}| / f_{cm}",
            numeric_equation=rf"1.05 \cdot {self.e_cm:.3f} \cdot |{self.epsilon_c1:.3f}| / {self.f_cm:.3f}",
            comparison_operator_label="=",
        )
