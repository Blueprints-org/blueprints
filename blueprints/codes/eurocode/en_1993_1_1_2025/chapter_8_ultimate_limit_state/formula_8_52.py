"""Formula 8.52 from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot52ReducedBendingMomentResistance(Formula):
    r"""Class representing formula 8.52 for the calculation of [$M_{N,z,Rd}$]."""

    label = "8.52"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        mpl_z_rd: NMM,
        n: DIMENSIONLESS,
        a_f: DIMENSIONLESS,
    ) -> None:
        r"""[$M_{N,z,Rd}$] Calculation of the reduced bending moment [$Nmm$].

        EN 1993-1-1:2025 art.8.2.9.1(6) - Formula (8.52)

        Parameters
        ----------
        mpl_z_rd : NMM
            [$M_{pl,z,Rd}$] Plastic bending moment resistance about the z-axis [$Nmm$].
        n : DIMENSIONLESS
            [$n$] Axial force ratio, see equation 8.50n (dimensionless).
        a_f : DIMENSIONLESS
            [$a_f$] Reduction factor for the flange (dimensionless).
        """
        super().__init__()
        self.mpl_z_rd = mpl_z_rd
        self.n = n
        self.a_f = a_f

    @staticmethod
    def _evaluate(
        mpl_z_rd: NMM,
        n: DIMENSIONLESS,
        a_f: DIMENSIONLESS,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(mpl_z_rd=mpl_z_rd, n=n, a_f=a_f)
        raise_if_less_or_equal_to_zero(denominator=(1 - 0.5 * a_f))

        return min(mpl_z_rd * (1 - n) / (1 - 0.5 * a_f), mpl_z_rd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.52."""
        _equation: str = r"\min \left( M_{pl,z,Rd} \cdot \frac{1 - n}{1 - 0.5 \cdot a_f}, M_{pl,z,Rd} \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"M_{pl,z,Rd}": f"{self.mpl_z_rd:.{n}f}",
                r" n": f" {self.n:.{n}f}",
                r"a_f": f"{self.a_f:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"M_{pl,z,Rd}": rf"{self.mpl_z_rd:.{n}f} \ Nmm",
                r" n": rf" {self.n:.{n}f}",
                r"a_f": rf"{self.a_f:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"M_{N,z,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"=",
            unit="Nmm",
        )
