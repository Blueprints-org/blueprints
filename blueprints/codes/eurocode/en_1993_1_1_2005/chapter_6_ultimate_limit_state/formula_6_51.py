"""Formula 6.51 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot51NonDimensionalSlendernessClass4(Formula):
    r"""Class representing formula 6.51 for the calculation of the non-dimensional slenderness for flexural buckling
    of a member with a Class 4 cross-section, from the elastic critical force.
    """

    label = "6.51"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a_eff: MM2,
        f_y: MPA,
        n_cr: N,
    ) -> None:
        r"""[$\overline{\lambda}$] Non-dimensional slenderness for flexural buckling, for Class 4 cross-sections [-].

        EN 1993-1-1:2005 art.6.3.1.3(1) - Formula (6.51)

        This is the first of the two expressions the standard prints for (6.51). The second one is implemented in
        Form6Dot51NonDimensionalSlendernessFromBucklingLengthClass4.

        Parameters
        ----------
        a_eff : MM2
            [$A_{eff}$] Effective area of the cross-section [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength [$MPa$].
        n_cr : N
            [$N_{cr}$] Elastic critical force for the relevant buckling mode based on the gross cross sectional
            properties [$N$].
        """
        super().__init__()
        self.a_eff = a_eff
        self.f_y = f_y
        self.n_cr = n_cr

    @staticmethod
    def _evaluate(
        a_eff: MM2,
        f_y: MPA,
        n_cr: N,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_eff=a_eff, f_y=f_y)
        raise_if_less_or_equal_to_zero(n_cr=n_cr)

        return np.sqrt(a_eff * f_y / n_cr)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.51."""
        _equation: str = r"\sqrt{\frac{A_{eff} \cdot f_y}{N_{cr}}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_{eff}": f"{self.a_eff:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"N_{cr}": f"{self.n_cr:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A_{eff}": rf"{self.a_eff:.{n}f} \ mm^2",
                r"f_y": rf"{self.f_y:.{n}f} \ MPa",
                r"N_{cr}": rf"{self.n_cr:.{n}f} \ N",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\overline{\lambda}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


class Form6Dot51NonDimensionalSlendernessFromBucklingLengthClass4(Formula):
    r"""Class representing formula 6.51 for the calculation of the non-dimensional slenderness for flexural buckling
    of a member with a Class 4 cross-section, from the buckling length.
    """

    label = "6.51"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        l_cr: MM,
        i: MM,
        a_eff: MM2,
        a: MM2,
        lambda_1: DIMENSIONLESS,
    ) -> None:
        r"""[$\overline{\lambda}$] Non-dimensional slenderness for flexural buckling, for Class 4 cross-sections [-].

        EN 1993-1-1:2005 art.6.3.1.3(1) - Formula (6.51)

        This is the second of the two expressions the standard prints for (6.51). The first one is implemented in
        Form6Dot51NonDimensionalSlendernessClass4.

        Parameters
        ----------
        l_cr : MM
            [$L_{cr}$] Buckling length in the buckling plane considered [$mm$].
        i : MM
            [$i$] Radius of gyration about the relevant axis, determined using the properties of the gross
            cross-section [$mm$].
        a_eff : MM2
            [$A_{eff}$] Effective area of the cross-section [$mm^2$].
        a : MM2
            [$A$] Area of the cross-section [$mm^2$].
        lambda_1 : DIMENSIONLESS
            [$\lambda_1$] Slenderness value to determine the relative slenderness, see SubForm6Dot50SlendernessValueLambda1
            in formula 6.50 [-].
        """
        super().__init__()
        self.l_cr = l_cr
        self.i = i
        self.a_eff = a_eff
        self.a = a
        self.lambda_1 = lambda_1

    @staticmethod
    def _evaluate(
        l_cr: MM,
        i: MM,
        a_eff: MM2,
        a: MM2,
        lambda_1: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(l_cr=l_cr, a_eff=a_eff)
        raise_if_less_or_equal_to_zero(i=i, a=a, lambda_1=lambda_1)

        return l_cr / i * np.sqrt(a_eff / a) / lambda_1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.51."""
        _equation: str = r"\frac{L_{cr}}{i} \cdot \frac{\sqrt{\frac{A_{eff}}{A}}}{\lambda_1}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"L_{cr}": f"{self.l_cr:.{n}f}",
                r"{i}": f"{{{self.i:.{n}f}}}",
                r"A_{eff}": f"{self.a_eff:.{n}f}",
                r"{A}": f"{{{self.a:.{n}f}}}",
                r"\lambda_1": f"{self.lambda_1:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"L_{cr}": rf"{self.l_cr:.{n}f} \ mm",
                r"{i}": rf"{{{self.i:.{n}f} \ mm}}",
                r"A_{eff}": rf"{self.a_eff:.{n}f} \ mm^2",
                r"{A}": rf"{{{self.a:.{n}f} \ mm^2}}",
                r"\lambda_1": f"{self.lambda_1:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\overline{\lambda}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
