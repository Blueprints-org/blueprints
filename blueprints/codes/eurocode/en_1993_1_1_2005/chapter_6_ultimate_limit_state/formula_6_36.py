"""Formula 6.36 from EN 1993-1-1:2005: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot36MomentReduction(Formula):
    r"""Class representing formula 6.36 for the calculation of reduced bending moment when axially loaded."""

    label = "6.36"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        mpl_y_rd: NMM,
        a: DIMENSIONLESS,
        n: DIMENSIONLESS,
    ) -> None:
        r"""[$M_{N,y,Rd}$] Reduced bending moment [$Nmm$].

        EN 1993-1-1:2005 art.6.2.9.1(5) - Formula (6.36)

        Parameters
        ----------
        mpl_y_rd : NMM
            [$M_{pl,y,Rd}$] Plastic bending moment about the y-axis [$Nmm$].
        a : DIMENSIONLESS
            Reduction factor for cross-sectional area, see formula 6.38a (`Form6Dot38A`) [-].
        n : DIMENSIONLESS
            Axial force ratio, see formula 6.38n (`Form6Dot38N`) [-].
        """
        super().__init__()
        self.mpl_y_rd = mpl_y_rd
        self.a = a
        self.n = n

    @staticmethod
    def _evaluate(
        mpl_y_rd: NMM,
        a: DIMENSIONLESS,
        n: DIMENSIONLESS,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(mpl_y_rd=mpl_y_rd, n=n, a=a)

        denominator = 1 - 0.5 * a
        raise_if_less_or_equal_to_zero(denominator=denominator)

        result = mpl_y_rd * (1 - n) / denominator
        return min(result, mpl_y_rd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.36."""
        _equation: str = r"\min\left(M_{pl,y,Rd}, M_{pl,y,Rd} \cdot (1 - n) / (1 - 0.5 \cdot a)\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,y,Rd}": f"{self.mpl_y_rd:.{n}f}",
                " n": f" {self.n:.{n}f}",
                "a": f"{self.a:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,y,Rd}": rf"{self.mpl_y_rd:.{n}f} \ Nmm",
                " n": rf" {self.n:.{n}f}",
                "a": rf"{self.a:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"M_{N,y,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )
