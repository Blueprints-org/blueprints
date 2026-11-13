"""Formula 6.50 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot50NonDimensionalSlendernessClass1And2And3(Formula):
    r"""Class representing formula 6.50 for the calculation of the non-dimensional slenderness for flexural buckling
    of a member with a Class 1, 2 or 3 cross-section, from the elastic critical force.
    """

    label = "6.50"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a: MM2,
        f_y: MPA,
        n_cr: N,
    ) -> None:
        r"""[$\overline{\lambda}$] Non-dimensional slenderness for flexural buckling, for Class 1, 2 and 3
        cross-sections [-].

        EN 1993-1-1:2005 art.6.3.1.3(1) - Formula (6.50)

        This is the first of the two expressions the standard prints for (6.50). The second one is implemented in
        Form6Dot50NonDimensionalSlendernessFromBucklingLengthClass1And2And3.

        Parameters
        ----------
        a : MM2
            [$A$] Area of the cross-section [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength [$MPa$].
        n_cr : N
            [$N_{cr}$] Elastic critical force for the relevant buckling mode based on the gross cross sectional
            properties [$N$].
        """
        super().__init__()
        self.a = a
        self.f_y = f_y
        self.n_cr = n_cr

    @staticmethod
    def _evaluate(
        a: MM2,
        f_y: MPA,
        n_cr: N,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, f_y=f_y)
        raise_if_less_or_equal_to_zero(n_cr=n_cr)

        return np.sqrt(a * f_y / n_cr)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.50."""
        _equation: str = r"\sqrt{\frac{A \cdot f_y}{N_{cr}}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"N_{cr}": f"{self.n_cr:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A": rf"{self.a:.{n}f} \ mm^2",
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


class Form6Dot50NonDimensionalSlendernessFromBucklingLengthClass1And2And3(Formula):
    r"""Class representing formula 6.50 for the calculation of the non-dimensional slenderness for flexural buckling
    of a member with a Class 1, 2 or 3 cross-section, from the buckling length.
    """

    label = "6.50"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        l_cr: MM,
        i: MM,
        lambda_1: DIMENSIONLESS,
    ) -> None:
        r"""[$\overline{\lambda}$] Non-dimensional slenderness for flexural buckling, for Class 1, 2 and 3
        cross-sections [-].

        EN 1993-1-1:2005 art.6.3.1.3(1) - Formula (6.50)

        This is the second of the two expressions the standard prints for (6.50). The first one is implemented in
        Form6Dot50NonDimensionalSlendernessClass1And2And3.

        Parameters
        ----------
        l_cr : MM
            [$L_{cr}$] Buckling length in the buckling plane considered [$mm$].
        i : MM
            [$i$] Radius of gyration about the relevant axis, determined using the properties of the gross
            cross-section [$mm$].
        lambda_1 : DIMENSIONLESS
            [$\lambda_1$] Slenderness value to determine the relative slenderness, see SubForm6Dot50SlendernessValueLambda1 [-].
        """
        super().__init__()
        self.l_cr = l_cr
        self.i = i
        self.lambda_1 = lambda_1

    @staticmethod
    def _evaluate(
        l_cr: MM,
        i: MM,
        lambda_1: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(l_cr=l_cr)
        raise_if_less_or_equal_to_zero(i=i, lambda_1=lambda_1)

        return l_cr / i * 1 / lambda_1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.50."""
        _equation: str = r"\frac{L_{cr}}{i} \cdot \frac{1}{\lambda_1}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"L_{cr}": f"{self.l_cr:.{n}f}",
                r"{i}": f"{{{self.i:.{n}f}}}",
                r"\lambda_1": f"{self.lambda_1:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"L_{cr}": rf"{self.l_cr:.{n}f} \ mm",
                r"{i}": rf"{{{self.i:.{n}f} \ mm}}",
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


class SubForm6Dot50SlendernessValueLambda1(Formula):
    r"""Class representing the sub-formula of formulas 6.50 and 6.51 for the calculation of [$\lambda_1$]."""

    label = "6.50"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        e: MPA,
        f_y: MPA,
    ) -> None:
        r"""[$\lambda_1$] Slenderness value to determine the relative slenderness [-].

        EN 1993-1-1:2005 art.6.3.1.3(1) - Formula (6.50)

        The standard also prints this value as [$93.9 \cdot \epsilon$] with [$\epsilon = \sqrt{235 / f_y}$]. That is this
        expression for [$E = 210000$] [$MPa$] with the factor rounded to 93.9, so the two differ in the fourth significant digit.

        Parameters
        ----------
        e : MPA
            [$E$] Modulus of elasticity [$MPa$].
        f_y : MPA
            [$f_y$] Yield strength [$MPa$].
        """
        super().__init__()
        self.e = e
        self.f_y = f_y

    @staticmethod
    def _evaluate(
        e: MPA,
        f_y: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(e=e)
        raise_if_less_or_equal_to_zero(f_y=f_y)

        return np.pi * np.sqrt(e / f_y)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the sub-formula of formulas 6.50 and 6.51."""
        _equation: str = r"\pi \cdot \sqrt{\frac{E}{f_y}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"{E}": f"{{{self.e:.{n}f}}}",
                r"f_y": f"{self.f_y:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"{E}": rf"{{{self.e:.{n}f} \ MPa}}",
                r"f_y": rf"{self.f_y:.{n}f} \ MPa",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\lambda_1",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
