"""Formula 6.36 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2, NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot36MomentReduction(Formula):
    r"""Class representing formula 6.36 for the calculation of reduced bending moment when axially loaded."""

    label = "6.36"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        mpl_y_rd: NMM,
        capital_a: MM2,
        b: MM,
        tf: MM,
        n_ed: N,
        n_pl_rd: N,
    ) -> None:
        r"""[$M_{N,y,Rd}$] Reduced bending moment [$Nmm$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.9(5) - Formula (6.36)

        Parameters
        ----------
        mpl_y_rd : NMM
            [$M_{pl,y,Rd}$] Plastic bending moment about the y-axis [$Nmm$].
        capital_a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        b : MM
            [$b$] Width of the cross-section [$mm$].
        tf : MM
            [$t_f$] Thickness of the flange [$mm$].
        n_ed : N
            [$N_{Ed}$] Design axial force [$N$].
        n_pl_rd : N
            [$N_{pl,Rd}$] Plastic resistance of the cross-section [$N$].
        """
        super().__init__()
        self.mpl_y_rd = mpl_y_rd
        self.capital_a = capital_a
        self.b = b
        self.tf = tf
        self.n_ed = n_ed
        self.n_pl_rd = n_pl_rd

    @staticmethod
    def _evaluate(
        mpl_y_rd: NMM,
        capital_a: MM2,
        b: MM,
        tf: MM,
        n_ed: N,
        n_pl_rd: N,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(capital_a=capital_a, b=b, tf=tf, n_pl_rd=n_pl_rd)
        raise_if_negative(mpl_y_rd=mpl_y_rd, n_ed=n_ed)

        a = min((capital_a - 2 * b * tf) / capital_a, 0.5)
        denominator = 1 - 0.5 * a

        raise_if_less_or_equal_to_zero(denominator=denominator)

        n = n_ed / n_pl_rd
        result = mpl_y_rd * (1 - n) / denominator
        return min(result, mpl_y_rd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.36."""
        _equation: str = (
            r"\min\left(M_{pl,y,Rd}, M_{pl,y,Rd} \cdot \left( 1 - \frac{N_{Ed}}{N_{pl,Rd}} \cdot "
            r"\frac{1}{1 - 0.5 \cdot \frac{A - 2 \cdot b \cdot t_f}{A}} \right)\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,y,Rd}": f"{self.mpl_y_rd:.3f}",
                "N_{Ed}": f"{self.n_ed:.3f}",
                "N_{pl,Rd}": f"{self.n_pl_rd:.3f}",
                "A": f"{self.capital_a:.3f}",
                "b": f"{self.b:.3f}",
                "t_f": f"{self.tf:.3f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "M_{pl,y,Rd}": rf"{self.mpl_y_rd:.3f} \ Nmm",
                "N_{Ed}": rf"{self.n_ed:.3f} \ N",
                "N_{pl,Rd}": rf"{self.n_pl_rd:.3f} \ N",
                "A": rf"{self.capital_a:.3f} \ mm^2",
                "b": rf"{self.b:.3f} \ mm",
                "t_f": rf"{self.tf:.3f} \ mm",
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
