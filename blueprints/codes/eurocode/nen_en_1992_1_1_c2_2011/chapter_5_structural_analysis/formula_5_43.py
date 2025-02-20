"""Formula 5.43 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_negative


class Form5Dot43InitialPrestressForce(Formula):
    r"""Class representing formula 5.43 for the calculation of the initial prestress force, [$P_{m0}(x)$]."""

    label = "5.43"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_p: MM2,
        k_7: DIMENSIONLESS,
        f_pk: MPA,
        k_8: DIMENSIONLESS,
        f_p0_1k: MPA,
    ) -> None:
        r"""[$P_{m0}(x)$] Initial prestress force [$N$].

        NEN-EN 1992-1-1+C2:2011 art.5.10.3(2) - Formula (5.43)

        Parameters
        ----------
        a_p : MM2
            [$A_{p}$] Area of prestressing steel [$mm^2$].
        k_7 : DIMENSIONLESS
            [$k_{7}$] Coefficient for characteristic tensile strength, recommended value is 0.75 [$-$].
        f_pk : MPA
            [$f_{pk}$] Characteristic tensile strength of prestressing steel [$MPa$].
        k_8 : DIMENSIONLESS
            [$k_{8}$] Coefficient for 0.1% proof stress, recommended value is 0.85 [$-$].
        f_p0_1k : MPA
            [$f_{p0,1k}$] 0.1% proof stress of prestressing steel [$MPa$].
        """
        super().__init__()
        self.a_p = a_p
        self.k_7 = k_7
        self.f_pk = f_pk
        self.k_8 = k_8
        self.f_p0_1k = f_p0_1k

    @staticmethod
    def _evaluate(
        a_p: MM2,
        k_7: DIMENSIONLESS,
        f_pk: MPA,
        k_8: DIMENSIONLESS,
        f_p0_1k: MPA,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            a_p=a_p,
            k_7=k_7,
            f_pk=f_pk,
            k_8=k_8,
            f_p0_1k=f_p0_1k,
        )

        return a_p * min(k_7 * f_pk, k_8 * f_p0_1k)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.43."""
        return LatexFormula(
            return_symbol=r"P_{m0}(x)",
            result=f"{self:.3f}",
            equation=r"A_{p} \cdot \min \left(k_7 \cdot f_{pk} ; k_8 \cdot f_{p0.1k} \right)",
            numeric_equation=rf"{self.a_p:.3f} \cdot \min \left({self.k_7:.3f} \cdot {self.f_pk:.3f} ;"
            rf" {self.k_8:.3f} \cdot {self.f_p0_1k:.3f} \right)",
            comparison_operator_label="=",
            unit="N",
        )
