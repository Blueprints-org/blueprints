"""Formula 5.6 from EN 1993-1-1:2005 - Classification of compression parts under bending and compression."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN, MM, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Table5Dot2PartSubjecttoBendingandCompression(Formula):
    """Implements EN 1993-1-1:2005 Table 5.2 (Sheet 1 of 3) for classification of compression parts under bending."""

    label = "5.6"
    source_document = EN_1993_1_1_2005

    def __init__(self, epsilon: DIMENSIONLESS, c: MM, t_w: MM, n_ed: KN, a: MM2, f_y: MPA) -> None:
        r"""
        [$-$] EN 1993-1-1:2005 Table 5.2 (sheet 1 of 3): Maximum widht-to-thickness ratios for compression parts [$-$].

        Parameters
        ----------
        epsilon : DIMENSIONLESS
            [$\epsilon$] Material slenderness factor [$-$].
        c : MM
            [$c$] Distance between flange with relation to the Axins of bendingdirection under check [$mm$]
        t_w : MM
            [$t_w$] Web thickness [$mm$]. If the web thickness is not constant, t_w should be taken as the minimum thickness.
        n_ed : kN
            [$N_{Ed}$] Contains the design axial force [$kN$].
        A : MM2
            [$A$] Gross cross-sectional area [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].

        Returns
        -------
        Section Classification
        """
        super().__init__()
        self.epsilon = epsilon
        self.c = c
        self.t_w = t_w
        self.n_ed = n_ed
        self.a = a
        self.f_y = f_y

    @staticmethod
    def _evaluate(epsilon: float, c: MM, t_w: MM, n_ed: KN, a: MM2, f_y: MPA) -> int:
        """Evaluate section classification based on slenderness ratios."""
        raise_if_less_or_equal_to_zero(epsilon=epsilon, c=c, t_w=t_w, a=a, f_y=f_y)

        alpha = min(0.5 * (1 + n_ed / (c * t_w * f_y)), 1.0)
        psi = 2 * n_ed / (a * f_y) - 1
        c_t_w = c / t_w

        if alpha > 0.5:
            beta_1w = 396 * epsilon / (13 * alpha - 1)
            beta_2w = 456 * epsilon / (13 * alpha - 1)
        else:
            beta_1w = 36 * epsilon / alpha
            beta_2w = 41.5 * epsilon / alpha

        beta_3w = 62 * epsilon * (1 - psi) * np.sqrt(abs(psi)) if psi <= -1 else 42 * epsilon / (0.67 + 0.33 * psi)

        if c_t_w <= beta_1w:
            return 1
        if c_t_w <= beta_2w:
            return 2
        if c_t_w <= beta_3w:
            return 3
        return 4  # Slender

    def evaluate(self) -> int:
        """Compute and return the section classification."""
        return self._evaluate(self.epsilon, self.c, self.t_w, self.n_ed, self.a, self.f_y)

    def latex(self, n: int = 3) -> LatexFormula:
        """Return a LatexFormula representation of the section classification."""
        class_num = self.evaluate()
        alpha = min(0.5 * (1 + self.n_ed * 1000 / (self.c * self.t_w * self.f_y)), 1.0)
        psi = 2 * self.n_ed * 1000 / (self.a * self.f_y) - 1
        c_t_w = self.c / self.t_w

        if alpha > 0.5:
            beta_1w = 396 * self.epsilon / (13 * alpha - 1)
            beta_2w = 456 * self.epsilon / (13 * alpha - 1)
            beta_1_label = r"\alpha > 0.5: \frac{c}{t_w} \leq \frac{396\varepsilon}{13\alpha - 1}"
            beta_2_label = r"\alpha > 0.5: \frac{c}{t_w} \leq \frac{456\varepsilon}{13\alpha - 1}"
        else:
            beta_1w = 36 * self.epsilon / alpha
            beta_2w = 41.5 * self.epsilon / alpha
            beta_1_label = r"\alpha \leq 0.5: \frac{c}{t_w} \leq \frac{36\varepsilon}{\alpha}"
            beta_2_label = r"\alpha \leq 0.5: \frac{c}{t_w} \leq \frac{41.5\varepsilon}{\alpha}"

        beta_3w = 62 * self.epsilon * (1 - psi) * np.sqrt(abs(psi)) if psi <= -1 else 42 * self.epsilon / (0.67 + 0.33 * psi)

        result_label = ["Plastic", "Compact", "Semi-Compact", "Slender"][class_num - 1]

        symbolic_eq = (
            r"\alpha = \min\left[\frac{1}{2}\left(1 + \frac{N_{Ed}}{d \cdot t_w \cdot f_y}\right),\ 1.0\right] \\"
            rf"\alpha = {alpha:.{n}f} \\"
            r"\psi = 2 \cdot \frac{N_{Ed}}{A \cdot f_y} - 1 \\"
            rf"\psi = {psi:.{n}f} \\"
            rf"\text{{Class 1: }} {beta_1_label} \\"
            rf"\text{{Class 2: }} {beta_2_label} \\"
            rf"\text{{Class 3: }} \frac{{c}}{{t_w}} \leq 62\varepsilon(1 - \psi)\sqrt{{|\psi|}}"
        )

        numeric_eq = (
            rf"\beta_{{1w}} = {beta_1w:.{n}f} \\ "
            rf"\beta_{{2w}} = {beta_2w:.{n}f} \\ "
            rf"\beta_{{3w}} = {beta_3w:.{n}f} \\ "
            rf"\frac{{c}}{{t_w}} = {c_t_w:.{n}f} \\ "
            rf"\text{{Hence, web is Class }} {class_num}: {result_label}"
        )

        return LatexFormula(
            return_symbol=r"\text{Web Class}",
            result=f"Class {class_num}: {result_label}",
            equation=symbolic_eq,
            numeric_equation=numeric_eq,
            comparison_operator_label="\\Rightarrow",
            unit="-",
        )
