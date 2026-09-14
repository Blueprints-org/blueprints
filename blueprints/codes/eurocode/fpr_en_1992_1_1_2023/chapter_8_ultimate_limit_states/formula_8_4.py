"""Formula 8.4 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot4DesignStressCompressionZone(Formula):
    r"""Class representing formula 8.4 for the calculation of the design stress in the compression zone,
    following the parabola-rectangle stress distribution.
    """

    label = "8.4"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        f_cd: MPA,
        epsilon_c: DIMENSIONLESS,
    ) -> None:
        r"""[$\sigma_{cd}$] Design stress in the compression zone [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.1.2(1) - Formula (8.4)

        The strain limits [$\varepsilon_{c2} = 0{,}002$] and [$\varepsilon_{cu} = 0{,}0035$] are fixed by the
        standard for this stress distribution and are not inputs of this class.

        Parameters
        ----------
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        epsilon_c : DIMENSIONLESS
            [$\varepsilon_c$] Compressive strain in the concrete, taken positive, within the range
            [$0 \leq \varepsilon_c \leq \varepsilon_{cu}$] [$-$].
        """
        super().__init__()
        self.f_cd = f_cd
        self.epsilon_c = epsilon_c

    @staticmethod
    def _evaluate(
        f_cd: MPA,
        epsilon_c: DIMENSIONLESS,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_cd=f_cd, epsilon_c=epsilon_c)

        epsilon_c2 = 0.002
        epsilon_cu = 0.0035
        if epsilon_c > epsilon_cu:
            raise ValueError(f"epsilon_c of {epsilon_c} is outside the range covered by formula (8.4): 0 <= epsilon_c <= {epsilon_cu}.")

        if epsilon_c <= epsilon_c2:
            return f_cd * (1 - (1 - epsilon_c / epsilon_c2) ** 2)
        return f_cd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.4."""
        _equation: str = (
            r"\begin{cases} f_{cd} \left[1 - \left(1 - \frac{\varepsilon_c}{\varepsilon_{c2}}\right)^2\right] "
            r"& \text{for } 0 \leq \varepsilon_c \leq \varepsilon_{c2} \\ "
            r"f_{cd} & \text{for } \varepsilon_{c2} \leq \varepsilon_c \leq \varepsilon_{cu} \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"f_{cd}": f"{self.f_cd:.{n}f}",
                r"\varepsilon_c": f"{self.epsilon_c:.{n}f}",
                r"\varepsilon_{c2}": "0.002",
                r"\varepsilon_{cu}": "0.0035",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
                r"\varepsilon_c": f"{self.epsilon_c:.{n}f}",
                r"\varepsilon_{c2}": "0.002",
                r"\varepsilon_{cu}": "0.0035",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{cd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
