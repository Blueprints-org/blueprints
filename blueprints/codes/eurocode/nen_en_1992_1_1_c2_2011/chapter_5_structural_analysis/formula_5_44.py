"""Formula 5.44 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import AMOUNT, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_lists_differ_in_length, raise_if_negative


class Form5Dot44PrestressLoss(Formula):
    r"""Class representing formula 5.44 for the calculation of the prestress losses, [$\Delta P_{el}$]."""

    label = "5.44"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_p: MM2,
        e_p: MPA,
        j: list[AMOUNT],
        delta_sigma_c_t: list[MPA],
        e_cm_t: list[MPA],
    ) -> None:
        r"""[$\Delta P_{el}$] Prestress loss [$N$].

        NEN-EN 1992-1-1+C2:2011 art.5.10.5.1(2) - Formula (5.44)

        Parameters
        ----------
        a_p : MM2
            [$A_{p}$] Cross-sectional area of the tendon [$mm^2$].
        e_p : MPA
            [$E_{p}$] Modulus of elasticity of the tendon [$MPa$].
        j : list[AMOUNT]
            [$j$] (n-1)/2n, with n the number of identical tendons successively prestressed [$list[-]$].
        delta_sigma_c_t : list[MPA]
            [$\Delta \sigma_{c}(t)$] variation of stress at the centre of gravity of the tendons applied at time t [$list[MPa]$].
        e_cm_t: list[MPA]
            [$E_{cm}(t)$] 0.1% proof stress of prestressing steel [$list[MPa]$].
        """
        super().__init__()
        self.a_p = a_p
        self.e_p = e_p
        self.j = j
        self.delta_sigma_c_t = delta_sigma_c_t
        self.e_cm_t = e_cm_t

    @staticmethod
    def _evaluate(
        a_p: MPA,
        e_p: MPA,
        j: list[AMOUNT],
        delta_sigma_c_t: list[MPA],
        e_cm_t: list[MPA],
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_p=a_p, e_p=e_p)

        raise_if_lists_differ_in_length(j=j, delta_sigma_c_t=delta_sigma_c_t, e_cm_t=e_cm_t)

        for x, y, z in zip(j, delta_sigma_c_t, e_cm_t):
            raise_if_negative(x=x, y=y)
            raise_if_less_or_equal_to_zero(z=z)

        return a_p * e_p * sum(x * (y / z) for x, y, z in zip(j, delta_sigma_c_t, e_cm_t))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.43."""
        numeric_equation = rf"{self.a_p:.3f} \cdot {self.e_p:.3f} \cdot \left( "
        for i in range(len(self.j)):
            numeric_equation += rf"\frac{{{self.j[i]} \cdot {self.delta_sigma_c_t[i]:.3f}}}{{{self.e_cm_t[i]:.3f}}}"
            if i < len(self.j) - 1:
                numeric_equation += " + "
        numeric_equation += r" \right)"

        return LatexFormula(
            return_symbol=r"\Delta P_{el}",
            result=f"{self:.3f}",
            equation=r"A_{p} \cdot E_{p} \cdot \sum_{i=1}^{n} \frac{j_{i} \cdot \Delta \sigma_{c,i}(t)}{E_{cm,i}(t)}",
            numeric_equation=numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
