"""Formula 6.39 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot39ReducedBendingMomentResistance(Formula):
    r"""Class representing formula 6.39 for the calculation of [$M_{N,y,Rd}$]."""

    label = "6.39"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        mpl_y_rd: NMM,
        n: DIMENSIONLESS,
        a_w: DIMENSIONLESS,
    ) -> None:
        r"""[$M_{N,y,Rd}$] Calculation of the reduced bending moment [$Nmm$].

        EN 1993-1-1:2005 art.6.2.9.1(5) - Formula (6.39)

        Parameters
        ----------
        mpl_y_rd : NMM
            [$M_{pl,y,Rd}$] Plastic bending moment resistance about the y-axis [$Nmm$].
        n : DIMENSIONLESS
            [$n$] Axial force ratio, see equation 6.38n (dimensionless).
        a_w : DIMENSIONLESS
            [$a_w$] Reduction factor for the web (dimensionless), see equation 6.39aw.
        """
        super().__init__()
        self.mpl_y_rd = mpl_y_rd
        self.n = n
        self.a_w = a_w

    @staticmethod
    def _evaluate(
        mpl_y_rd: NMM,
        n: DIMENSIONLESS,
        a_w: DIMENSIONLESS,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(mpl_y_rd=mpl_y_rd, n=n, a_w=a_w)
        raise_if_less_or_equal_to_zero(denominator=(1 - 0.5 * a_w))

        return min(mpl_y_rd * (1 - n) / (1 - 0.5 * a_w), mpl_y_rd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.39."""
        _equation: str = r"\min \left( M_{pl,y,Rd} \cdot \frac{1 - n}{1 - 0.5 \cdot a_w}, M_{pl,y,Rd} \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"M_{pl,y,Rd}": f"{self.mpl_y_rd:.{n}f}",
                r" n": f" {self.n:.{n}f}",
                r"a_w": f"{self.a_w:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"M_{pl,y,Rd}": rf"{self.mpl_y_rd:.{n}f} \ Nmm",
                r" n": rf" {self.n:.{n}f}",
                r"a_w": rf"{self.a_w:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"M_{N,y,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"=",
            unit="Nmm",
        )
