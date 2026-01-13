"""Formula 8.37 from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot37Rho(Formula):
    r"""Class representing formula 8.37 for the calculation of [$\rho$], where no torsion is present."""

    label = "8.37"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        v_ed: N,
        v_c_rd: N,
    ) -> None:
        r"""[$\rho$] Calculation of the reduction factor, where no torsion is present [$\text{dimensionless}$].

        EN 1993-1-1:2025 art.8.2.8(4) - Formula (8.37)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design shear force [$N$].
        v_c,rd : N
            [$V_{pl,Rd}$] Plastic shear resistance, obtained from 8.2.6(2) [$N$].
            Note, see also 8.2.8(4)
        """
        super().__init__()
        self.v_ed = v_ed
        self.v_c_rd = v_c_rd

    @staticmethod
    def _evaluate(
        v_ed: N,
        v_c_rd: N,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(v_c_rd=v_c_rd)
        raise_if_negative(v_ed=v_ed)

        if v_ed <= 0.5 * v_c_rd:
            return 0
        return ((2 * v_ed / v_c_rd) - 1) ** 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.37."""
        _equation: str = (
            r"\begin{cases} "
            r"0 & \text{if } V_{Ed} \leq 0.5 \cdot V_{pl,Rd} \\ "
            r"\left( \frac{2 \cdot V_{Ed}}{V_{pl,Rd}} - 1 \right)^2 & \text{if } V_{Ed} > 0.5 \cdot V_{pl,Rd} "
            r"\end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
                r"V_{pl,Rd}": f"{self.v_c_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                r"V_{pl,Rd}": rf"{self.v_c_rd:.{n}f} \ N",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\rho",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


class Form8Dot37RhoWithTorsion(Formula):
    r"""Class representing formula 8.37 with torsion for the calculation of [$\rho$]."""

    label = "8.37_with_torsion"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        v_ed: N,
        v_pl_t_rd: N,
    ) -> None:
        r"""[$\rho$] Calculation of the reduction factor with torsion [$\text{dimensionless}$].

        EN 1993-1-1:2025 art.8.2.8(4) - Formula (8.37 with torsion)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design shear force [$N$].
        v_pl_t_rd : N
            [$V_{pl,T,Rd}$] Plastic shear resistance with torsion [$N$].
            Note, see also 6.2.7
        """
        super().__init__()
        self.v_ed = v_ed
        self.v_pl_t_rd = v_pl_t_rd

    @staticmethod
    def _evaluate(
        v_ed: N,
        v_pl_t_rd: N,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(v_pl_t_rd=v_pl_t_rd)
        raise_if_negative(v_ed=v_ed)

        if v_ed <= 0.5 * v_pl_t_rd:
            return 0
        return ((2 * v_ed / v_pl_t_rd) - 1) ** 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.29rho with torsion."""
        _equation: str = (
            r"\begin{cases} "
            r"0 & \text{if } V_{Ed} \leq 0.5 \cdot V_{pl,T,Rd} \\ "
            r"\left( \frac{2 \cdot V_{Ed}}{V_{pl,T,Rd}} - 1 \right)^2 & \text{if } V_{Ed} > 0.5 \cdot V_{pl,T,Rd} "
            r"\end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
                r"V_{pl,T,Rd}": f"{self.v_pl_t_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                r"V_{pl,T,Rd}": rf"{self.v_pl_t_rd:.{n}f} \ N",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\rho",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
