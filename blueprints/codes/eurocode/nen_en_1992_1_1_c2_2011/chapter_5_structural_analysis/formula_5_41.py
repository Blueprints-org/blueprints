"""Formula 5.41 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_negative


class Form5Dot41MaxForceTendon(Formula):
    r"""Class representing formula 5.41 for the calculation of the maximum force applied to a tendon, [$P_{max}$]."""

    label = "5.41"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_p: MM2,
        k_1: DIMENSIONLESS,
        f_pk: MPA,
        k_2: DIMENSIONLESS,
        f_p0_1k: MPA,
    ) -> None:
        r"""[$P_{max}$] Maximum force applied to a tendon at active end [$N$].

        NEN-EN 1992-1-1+C2:2011 art.5.10.2.1(1) - Formula (5.41)

        Parameters
        ----------
        a_p : MM2
            [$A_{p}$] Cross-sectional area of the tendon [$mm^2$].
        k_1 : DIMENSIONLESS
            [$k_{1}$] Coefficient for characteristic tensile strength, recommended value is 0.8 [$-$].
        f_pk : MPA
            [$f_{pk}$] Characteristic tensile strength of the tendon [$MPa$].
        k_2 : DIMENSIONLESS
            [$k_{2}$] Coefficient for 0.1% proof stress, recommended value is 0.9 [$-$].
        f_p0_1k : MPA
            [$f_{p0.1k}$] 0.1% proof stress of the tendon [$MPa$].
        """
        super().__init__()
        self.a_p = a_p
        self.k_1 = k_1
        self.f_pk = f_pk
        self.k_2 = k_2
        self.f_p0_1k = f_p0_1k

    @staticmethod
    def _evaluate(
        a_p: MM2,
        k_1: DIMENSIONLESS,
        f_pk: MPA,
        k_2: DIMENSIONLESS,
        f_p0_1k: MPA,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            a_p=a_p,
            k_1=k_1,
            f_pk=f_pk,
            k_2=k_2,
            f_p0_1k=f_p0_1k,
        )

        return a_p * min(k_1 * f_pk, k_2 * f_p0_1k)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.41."""
        return LatexFormula(
            return_symbol=r"P_{max}",
            result=f"{self:.3f}",
            equation=r"A_{p} \cdot \min(k_1 \cdot f_{pk}, k_2 \cdot f_{p0.1k})",
            numeric_equation=rf"{self.a_p:.3f} \cdot \min({self.k_1:.3f} \cdot {self.f_pk:.3f}, {self.k_2:.3f} \cdot {self.f_p0_1k:.3f})",
            comparison_operator_label="=",
            unit="N",
        )
