"""Formula 6.51 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA, NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot51AppliedPunchingShearStressEccentricLoading(Formula):
    r"""Class representing formula 6.51 for the calculation of punching shear stress for eccentric loading [$v_{Ed}$]
    of slabs and column bases without shear reinforcement.
    """

    label = "6.51"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        v_ed_red: N,
        u: MM,
        d: MM,
        k: DIMENSIONLESS,
        m_ed: NMM,
        w: MM2,
    ) -> None:
        r"""[$v_{Ed}$] Calculation of punching shear stress for eccentric loading of slabs and column bases without shear reinforcement.

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(2) - Formula (6.51)

        Parameters
        ----------
        v_ed_red : N
            [$V_{Ed,red}$] Net applied punching force [$N$].
        u : MM
            [$u$] Perimeter of the critical section [$mm$].
        d : MM
            [$d$] Mean effective depth of the slab [$mm$].
        k : DIMENSIONLESS
            [$k$] Coefficient dependent on the ratio between the column dimensions as defined in 6.4.3(3) or 6.4.3(4) [$-$].
        m_ed : NMM
            [$M_{Ed}$] Design bending moment [$Nmm$].
        w : MM2
            [$W$] Similar to [$W_1$] as defined in 6.4.3(3) and 6.4.3.(4) but for perimeter [$u$] [$mm^2$].
        """
        super().__init__()
        self.v_ed_red = v_ed_red
        self.u = u
        self.d = d
        self.k = k
        self.m_ed = m_ed
        self.w = w

    @staticmethod
    def _evaluate(
        v_ed_red: N,
        u: MM,
        d: MM,
        k: DIMENSIONLESS,
        m_ed: NMM,
        w: MM2,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(m_ed=m_ed)
        raise_if_less_or_equal_to_zero(v_ed_red=v_ed_red, u=u, d=d, k=k, w=w)

        return (v_ed_red / (u * d)) * (1 + k * (m_ed * u) / (v_ed_red * w))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.51."""
        _equation: str = r"\frac{V_{Ed,red}}{u \cdot d} \cdot \left(1 + k \cdot \frac{M_{Ed} \cdot u}{V_{Ed,red} \cdot W}\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"V_{Ed,red}": f"{self.v_ed_red:.3f}",
                r"u": f"{self.u:.3f}",
                r" d": f" {self.d:.3f}",
                r"k": f"{self.k:.3f}",
                r"M_{Ed}": f"{self.m_ed:.3f}",
                r"W": f"{self.w:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"v_{Ed}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
