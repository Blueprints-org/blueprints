"""Formula 6.36 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM, DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot36MomentReduction(Formula):
    r"""Class representing formula 6.36 for the calculation of reduced bending moment when axially loaded."""

    label = "6.36"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        mpl_y_rd: NMM,
        a: DIMENSIONLESS,
        n: DIMENSIONLESS,
    ) -> None:
        r"""[$M_{N,y,Rd}$] Reduced bending moment [$Nmm$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.9(5) - Formula (6.36)

        Parameters
        ----------
        mpl_y_rd : NMM
            [$M_{pl,y,Rd}$] Plastic bending moment about the y-axis [$Nmm$].
        a : DIMENSIONLESS
            Reduction factor for cross-sectional area, see equation 6.38a.
        n : DIMENSIONLESS
            Axial force ratio, see equation 6.38n.
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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.36."""
        _equation: str = r"\min\left(M_{pl,y,Rd}, M_{pl,y,Rd} \cdot (1 - n) / (1 - 0.5 \cdot a)\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,y,Rd}": f"{self.mpl_y_rd:.3f}",
                " n": f" {self.n:.3f}",
                "a": f"{self.a:.3f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,y,Rd}": rf"{self.mpl_y_rd:.3f} \ Nmm",
                " n": rf" {self.n:.3f}",
                "a": rf"{self.a:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"M_{N,y,Rd}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )
