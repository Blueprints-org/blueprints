"""Formulas 6.37 and 6.38 from EN 1993-1-1:2005: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot37And38MomentReduction(Formula):
    r"""Class representing formulas 6.37 and 6.38 for the calculation of reduced bending moment."""

    label = "6.37/6.38"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        mpl_z_rd: NMM,
        a: DIMENSIONLESS,
        n: DIMENSIONLESS,
    ) -> None:
        r"""[$M_{N,z,Rd}$] Reduced bending moment [$Nmm$].

        EN 1993-1-1:2005 art.6.2.9.1(5) - Formulas (6.37 and 6.38)

        Parameters
        ----------
        mpl_z_rd : NMM
            [$M_{pl,z,Rd}$] Plastic bending moment about the z-axis [$Nmm$].
        a : DIMENSIONLESS
            Reduction factor for cross-sectional area, see equation 6.38a (`Form6Dot38A`) [-].
        n : DIMENSIONLESS
            Axial force ratio, see equation 6.38n (`Form6Dot38N`) [-].
        """
        super().__init__()
        self.mpl_z_rd = mpl_z_rd
        self.a = a
        self.n = n

    @staticmethod
    def _evaluate(
        mpl_z_rd: NMM,
        a: DIMENSIONLESS,
        n: DIMENSIONLESS,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(mpl_z_rd=mpl_z_rd, n=n)
        raise_if_less_or_equal_to_zero(a=a)

        denominator = 1 - a
        raise_if_less_or_equal_to_zero(denominator=denominator)

        if n <= a:
            return mpl_z_rd
        return mpl_z_rd * (1 - ((n - a) / denominator) ** 2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 6.37 and 6.38."""
        _equation: str = (
            r"\begin{cases} M_{pl,z,Rd} & \text{if } n \leq a \\ "
            r"M_{pl,z,Rd} \cdot \left[1 - \left(\frac{ n - a}{1 - a}\right)^2\right] & \text{if } n > a \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,z,Rd}": f"{self.mpl_z_rd:.{n}f}",
                " n": f" {self.n:.{n}f}",
                " a": f" {self.a:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,z,Rd}": rf"{self.mpl_z_rd:.{n}f} \ Nmm",
                " n": rf" {self.n:.{n}f}",
                " a": rf" {self.a:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"M_{N,z,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )


class Form6Dot38N(Formula):
    r"""Class representing formula 6.38 for the calculation of [$n$]."""

    label = "6.38n"
    source_document = EN_1993_1_1_2005

    def __init__(self, n_ed: N, n_pl_rd: N) -> None:
        r"""[$n$] Axial force ratio [dimensionless].

        EN 1993-1-1:2005 art.6.2.9(5) - Formula (6.38n)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design axial force [$N$].
        n_pl_rd : N
            [$N_{pl,Rd}$] Plastic resistance of the cross-section [$N$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_pl_rd = n_pl_rd

    @staticmethod
    def _evaluate(n_ed: N, n_pl_rd: N) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_pl_rd=n_pl_rd)
        raise_if_negative(n_ed=n_ed)
        return n_ed / n_pl_rd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.38n."""
        _equation: str = r"\frac{N_{Ed}}{N_{pl,Rd}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"N_{pl,Rd}": f"{self.n_pl_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"N_{pl,Rd}": rf"{self.n_pl_rd:.{n}f} \ N",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"n",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


class Form6Dot38A(Formula):
    r"""Class representing formula 6.38 for the calculation of [$a$]."""

    label = "6.38a"
    source_document = EN_1993_1_1_2005

    def __init__(self, capital_a: MM2, b: MM, tf: MM) -> None:
        r"""[$a$] Reduction factor for cross-sectional area [dimensionless].

        EN 1993-1-1:2005 art.6.2.9(5) - Formula (6.38a)

        Parameters
        ----------
        capital_a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        b : MM
            [$b$] Width of the cross-section [$mm$].
        tf : MM
            [$t_f$] Thickness of the flange [$mm$].
        """
        super().__init__()
        self.capital_a = capital_a
        self.b = b
        self.tf = tf

    @staticmethod
    def _evaluate(capital_a: MM2, b: MM, tf: MM) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(capital_a=capital_a)
        raise_if_negative(b=b, tf=tf)
        a = (capital_a - 2 * b * tf) / capital_a
        return min(a, 0.5)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.38a."""
        _equation: str = r"\min\left(\frac{A - 2 \cdot b \cdot t_f}{A}, 0.5\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.capital_a:.{n}f}",
                r"b": f"{self.b:.{n}f}",
                r"t_f": f"{self.tf:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A": rf"{self.capital_a:.{n}f} \ mm^2",
                r"b": rf"{self.b:.{n}f} \ mm",
                r"t_f": rf"{self.tf:.{n}f} \ mm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"a",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
