"""Formula 5.34 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot34Curvature(Formula):
    r"""Class representing formula 5.34 for the calculation of the curvature, [$\frac{1}{r}$]."""

    label = "5.34"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        k_r: DIMENSIONLESS,
        k_phi: DIMENSIONLESS,
        f_yd: MPA,
        e_s: MPA,
        d: MM,
    ) -> None:
        r"""[$\frac{1}{r}$] Curvature [$1/mm$].

        EN 1992-1-1:2004 art.5.8.8.3 - Formula (5.34)

        Parameters
        ----------
        k_r : DIMENSIONLESS
            [$K_r$] Correction factor depending on axial load, see 5.8.8.3 (3) [-].
        k_phi : DIMENSIONLESS
            [$K_\phi$] Factor for taking account of creep, see 5.8.8.3 (4) [-].
        f_yd : MPA
            [$f_{yd}$] Design yield strength of reinforcement [$MPa$].
        e_s : MPA
            [$E_s$] Modulus of elasticity of reinforcement [$MPa$].
        d : MM
            [$d$] Effective depth; see also 5.8.8.3 (2) [$mm$].
        """
        super().__init__()
        self.k_r = k_r
        self.k_phi = k_phi
        self.f_yd = f_yd
        self.e_s = e_s
        self.d = d

    @staticmethod
    def _evaluate(
        k_r: DIMENSIONLESS,
        k_phi: DIMENSIONLESS,
        f_yd: MPA,
        e_s: MPA,
        d: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            k_r=k_r,
            k_phi=k_phi,
        )
        raise_if_less_or_equal_to_zero(f_yd=f_yd, e_s=e_s, d=d)

        return k_r * k_phi * (f_yd / e_s) / (0.45 * d)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.34."""
        return LatexFormula(
            return_symbol=r"\frac{1}{r}",
            result=f"{self:.6f}",
            equation=r"K_r \cdot K_\phi \cdot \frac{f_{yd}}{E_s \cdot 0.45 \cdot d}",
            numeric_equation=rf"{self.k_r:.{n}f} \cdot {self.k_phi:.{n}f} "
            rf"\cdot \frac{{{self.f_yd:.{n}f}}}{{{self.e_s:.{n}f} \cdot 0.45 \cdot {self.d:.{n}f}}}",
            comparison_operator_label="=",
            unit="1/mm",
        )
