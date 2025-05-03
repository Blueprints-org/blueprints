"""Formulas 6.37 and 6.38 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot37Dot38MomentReduction(Formula):
    r"""Class representing formulas 6.37 and 6.38 for the calculation of reduced bending moment."""

    label = "6.37/6.38"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        mpl_z_rd: NMM,
        a: float,
        n: float,
    ) -> None:
        r"""[$M_{N,z,Rd}$] Reduced bending moment [$Nmm$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.9(5) - Formulas (6.37 and 6.38)

        Parameters
        ----------
        mpl_z_rd : NMM
            [$M_{pl,z,Rd}$] Plastic bending moment about the z-axis [$Nmm$].
        a : float
            Reduction factor for cross-sectional area.
        n : float
            Axial force ratio.
        """
        super().__init__()
        self.mpl_z_rd = mpl_z_rd
        self.a = a
        self.n = n

    @staticmethod
    def _evaluate(
        mpl_z_rd: NMM,
        a: float,
        n: float,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(mpl_z_rd=mpl_z_rd, n=n)
        raise_if_less_or_equal_to_zero(a=a)

        denominator = 1 - a
        raise_if_less_or_equal_to_zero(denominator=denominator)

        if n <= a:
            return mpl_z_rd
        return mpl_z_rd * (1 - ((n - a) / denominator) ** 2)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formulas 6.37 and 6.38."""
        _equation: str = (
            r"\begin{cases} M_{pl,z,Rd} & \text{if } n \leq a \\ "
            r"M_{pl,z,Rd} \cdot \left[1 - \left(\frac{ n - a}{1 - a}\right)^2\right] & \text{if } n > a \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,z,Rd}": f"{self.mpl_z_rd:.3f}",
                " n": f" {self.n:.3f}",
                " a": f" {self.a:.3f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,z,Rd}": rf"{self.mpl_z_rd:.3f} \ Nmm",
                " n": rf" {self.n:.3f}",
                " a": rf" {self.a:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"M_{N,z,Rd}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )
