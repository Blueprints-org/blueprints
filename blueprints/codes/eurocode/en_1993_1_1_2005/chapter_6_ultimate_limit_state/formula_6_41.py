"""formula 6.41 from EN 1993-1-1:2005: chapter 6 - ultimate limit state."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot41BiaxialBendingCheck(Formula):
    r"""class representing formula 6.41 for bi-axial bending."""

    label = "6.41"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        my_ed: NMM,
        m_n_y_rd: NMM,
        mz_ed: NMM,
        m_n_z_rd: NMM,
        alpha: DIMENSIONLESS,
        beta: DIMENSIONLESS,
    ) -> None:
        r"""Check the bi-axial bending criterion.

        EN 1993-1-1:2005 art.6.2.9.1(6) - formula (6.41)

        Parameters
        ----------
        my_ed : NMM
            [$m_{y,ed}$] design bending moment about the y-axis [$Nmm$].
        m_n_y_rd : NMM
            [$m_{n,y,rd}$] design resistance moment about the y-axis [$Nmm$].
        mz_ed : NMM
            [$m_{z,ed}$] design bending moment about the z-axis [$Nmm$].
        m_n_z_rd : NMM
            [$m_{n,z,rd}$] design resistance moment about the z-axis [$Nmm$].
        alpha : DIMENSIONLESS
            [$\alpha$] exponent for the y-axis term.
        beta : DIMENSIONLESS
            [$\beta$] exponent for the z-axis term.

        In which $\alpha$ and $\beta$ are constants, which may conservatively be taken as unity, otherwise as follows:
        - I and H sections:
            $\alpha = 2$ and $\beta = 5 \cdot n$, but $\beta \geq 1$.
        - Circular hollow sections:
            $\alpha = 2$ and $\beta = 2$.
        - Rectangular hollow sections:
            $\alpha = \beta = \frac{1.66}{1-1.13 \cdot n^2}$, but $\alpha = \beta \leq 6$.

        Where $n = N_{Ed} / N_{pl,Rd}$, see equation 6.38n.
        """
        super().__init__()
        self.my_ed = my_ed
        self.m_n_y_rd = m_n_y_rd
        self.mz_ed = mz_ed
        self.m_n_z_rd = m_n_z_rd
        self.alpha = alpha
        self.beta = beta

    @staticmethod
    def _evaluate(
        my_ed: NMM,
        m_n_y_rd: NMM,
        mz_ed: NMM,
        m_n_z_rd: NMM,
        alpha: DIMENSIONLESS,
        beta: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(m_n_y_rd=m_n_y_rd, m_n_z_rd=m_n_z_rd)
        raise_if_negative(my_ed=my_ed, mz_ed=mz_ed, alpha=alpha, beta=beta)

        return (my_ed / m_n_y_rd) ** alpha + (mz_ed / m_n_z_rd) ** beta <= 1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.41."""
        _equation: str = r"\left[ \frac{M_{y,Ed}}{M_{N,y,Rd}} \right]^{\alpha} + \left[ \frac{M_{z,Ed}}{M_{N,z,Rd}} \right]^{\beta} \leq 1"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "M_{y,Ed}": f"{self.my_ed:.{n}f}",
                "M_{N,y,Rd}": f"{self.m_n_y_rd:.{n}f}",
                "M_{z,Ed}": f"{self.mz_ed:.{n}f}",
                "M_{N,z,Rd}": f"{self.m_n_z_rd:.{n}f}",
                r"\alpha": f"{self.alpha:.{n}f}",
                r"\beta": f"{self.beta:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "M_{y,Ed}": rf"{self.my_ed:.{n}f} \ Nmm",
                "M_{N,y,Rd}": rf"{self.m_n_y_rd:.{n}f} \ Nmm",
                "M_{z,Ed}": rf"{self.mz_ed:.{n}f} \ Nmm",
                "M_{N,z,Rd}": rf"{self.m_n_z_rd:.{n}f} \ Nmm",
                r"\alpha": rf"{self.alpha:.{n}f}",
                r"\beta": rf"{self.beta:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="\\to",
            unit="",
        )
