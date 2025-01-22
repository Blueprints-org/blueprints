"""Formula 12.4 from NEN-EN 1992-1-1+C2:2011: Chapter 12 - Plain and Lightly Reinforced Concrete Structures."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form12Dot4PlainConcreteShearStress(Formula):
    r"""Class representing formula 12.4 for the calculation of the design shear stress of plain concrete, :math:`\tau_{cp}`.

    NEN-EN 1992-1-1+C2:2011 art.12.6.3 - Formula (12.4)
    """

    label = "12.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        k: float,
        v_ed: N,
        a_cc: MM2,
    ) -> None:
        r"""[:math:`\tau_{cp}`] Design shear stress of plain concrete [:math:`MPa`].

        NEN-EN 1992-1-1+C2:2011 art.12.6.3 - Formula (12.4)

        Parameters
        ----------
        k : float
            [:math:`k`] Nationally determined parameter [-].
        v_ed : N
            [:math:`V_{Ed}`] Design shear force [:math:`N`].
        a_cc : MM2
            [:math:`A_{cc}`] Compressed area [:math:`mm^2`].
        """
        super().__init__()
        self.k = k
        self.v_ed = v_ed
        self.a_cc = a_cc

    @staticmethod
    def _evaluate(
        k: float,
        v_ed: N,
        a_cc: MM2,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            v_ed=v_ed,
            a_cc=a_cc,
        )
        raise_if_less_or_equal_to_zero(
            v_ed=v_ed,
            a_cc=a_cc,
        )
        return k * v_ed / a_cc

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 12.4."""
        return LatexFormula(
            return_symbol=r"\tau_{cp}",
            result=f"{self:.3f}",
            equation=r"k \cdot \frac{V_{Ed}}{A_{cc}}",
            numeric_equation=rf"{self.k:.3f} \cdot \frac{{{self.v_ed:.3f}}}{{{self.a_cc:.3f}}}",
            comparison_operator_label="=",
        )


"""Helper class for sigma_cp vs sigma_c,lim evaluation."""


class Form12Dot4PlainConcreteShearStressComparison:
    r"""Class representing the comparison of σcp and σc,lim for plain concrete shear stress."""

    label = "12.4 Comparison"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, sigma_cp: MPA, sigma_c_lim: MPA) -> None:
        r"""[:math:`σ_{cp} ≤ σ_{c,lim}`] Comparison of design shear stress and limit compressive stress.

        NEN-EN 1992-1-1+C2:2011 art.12.6.3

        Parameters
        ----------
        sigma_cp : MPA
            [:math:`σ_{cp}`] Design shear stress [:math:`MPa`].
        sigma_c_lim : MPA
            [:math:`σ_{c,lim}`] Limit compressive stress [:math:`MPa`].
        """
        super().__init__()
        self.sigma_cp = sigma_cp
        self.sigma_c_lim = sigma_c_lim
        raise_if_negative(sigma_cp=sigma_cp, sigma_c_lim=sigma_c_lim)

    @property
    def comparison(self) -> bool:
        """Evaluate the comparison σcp ≤ σc,lim.

        Returns
        -------
        bool
            True if σcp ≤ σc,lim, False otherwise.
        """
        return self.sigma_cp <= self.sigma_c_lim

    def __bool__(self) -> bool:
        """Evaluates the comparison, for more information see the __init__ method."""
        return self.comparison

    def __str__(self) -> str:
        """Return the result of the comparison."""
        return self.latex().complete

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for the comparison."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\sigma_{cp} ≤ \sigma_{c,lim}",
            numeric_equation=rf"{self.sigma_cp:.3f} ≤ {self.sigma_c_lim:.3f}",
            comparison_operator_label=r"\rightarrow",
        )
