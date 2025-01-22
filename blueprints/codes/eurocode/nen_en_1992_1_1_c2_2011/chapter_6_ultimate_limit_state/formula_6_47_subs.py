"""Formula 6.47 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot47Sub1FactorK(Formula):
    r"""Class representing sub-formula 1 for formula 6.47, which calculates the factor $$k$$."""

    label = "6.47sub1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, d: MM) -> None:
        r"""$$k$$ Calculation of factor k.

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Formula (6.47sub1)

        Parameters
        ----------
        d : MM
            $$d$$ Effective depth [$$mm$$].
        """
        super().__init__()
        self.d = d

    @staticmethod
    def _evaluate(d: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(d=d)
        return min(1 + np.sqrt(200 / d), 2.0)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.47sub1."""
        _equation: str = r"\min \left( 1 + \sqrt{\frac{200}{d}}, 2.0 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"d": f"{self.d:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"k",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )


class Form6Dot47Sub2FactorRhoL(Formula):
    r"""Class representing sub-formula 2 for formula 6.47, which calculates the factor $$\rho_l$$."""

    label = "6.47sub2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, rho_ly: DIMENSIONLESS, rho_lz: DIMENSIONLESS) -> None:
        r"""$$\rho_l$$ Calculation of factor $$\rho_l$$.

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Formula (6.47sub2)

        Parameters
        ----------
        rho_ly : DIMENSIONLESS
            $$\rho_{ly}$$ Longitudinal reinforcement ratio in y-direction [-].
        rho_lz : DIMENSIONLESS
            $$\rho_{lz}$$ Longitudinal reinforcement ratio in z-direction [-].
        """
        super().__init__()
        self.rho_ly = rho_ly
        self.rho_lz = rho_lz

    @staticmethod
    def _evaluate(rho_ly: DIMENSIONLESS, rho_lz: DIMENSIONLESS) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(rho_ly=rho_ly, rho_lz=rho_lz)
        return min(np.sqrt(rho_ly * rho_lz), 0.02)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.47sub2."""
        _equation: str = r"\min \left( \sqrt{\rho_{ly} \cdot \rho_{lz}}, 0.02 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\rho_{ly}": f"{self.rho_ly:.3f}",
                r"\rho_{lz}": f"{self.rho_lz:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\rho_l",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )


class Form6Dot47Sub3FactorSigmaCp(Formula):
    r"""Class representing sub-formula 3 for formula 6.47, which calculates the factor $$\sigma_{cp}$$."""

    label = "6.47sub3"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, sigma_cy: MPA, sigma_cz: MPA) -> None:
        r"""$$\sigma_{cp}$$ Calculation of factor $$\sigma_{cp}$$.

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Formula (6.47sub3)

        Parameters
        ----------
        sigma_cy : MPA
            $$\sigma_{cy}$$ Stress in the y-direction [$$MPa$$].
        sigma_cz : MPA
            $$\sigma_{cz}$$ Stress in the z-direction [$$MPa$$].
        """
        super().__init__()
        self.sigma_cy = sigma_cy
        self.sigma_cz = sigma_cz

    @staticmethod
    def _evaluate(sigma_cy: MPA, sigma_cz: MPA) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sigma_cy=sigma_cy, sigma_cz=sigma_cz)
        return (sigma_cy + sigma_cz) / 2

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.47sub3."""
        _equation: str = r"\frac{\sigma_{cy} + \sigma_{cz}}{2}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\sigma_{cy}": f"{self.sigma_cy:.3f}",
                r"\sigma_{cz}": f"{self.sigma_cz:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{cp}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )


class Form6Dot47Sub4FactorSigmaCy(Formula):
    r"""Class representing sub-formula 4 for formula 6.47, which calculates the factor $$\sigma_{cy}$$."""

    label = "6.47sub4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, n_ed_y: N, a_cy: MM2) -> None:
        r"""$$\sigma_{cy}$$ Calculation of factor $$\sigma_{cy}$$.

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Formula (6.47sub4)

        Parameters
        ----------
        n_ed_y : N
            $$N_{Ed,y}$$ Design axial force in y-direction [$$N$$].
        a_cy : MM2
            $$A_{cy}$$ Cross-sectional area in y-direction [$$mm^2$$].
        """
        super().__init__()
        self.n_ed_y = n_ed_y
        self.a_cy = a_cy

    @staticmethod
    def _evaluate(n_ed_y: N, a_cy: MM2) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(a_cy=a_cy)
        raise_if_negative(n_ed_y=n_ed_y)
        return n_ed_y / a_cy

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.47sub4."""
        _equation: str = r"\frac{N_{Ed,y}}{A_{cy}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed,y}": f"{self.n_ed_y:.3f}",
                r"A_{cy}": f"{self.a_cy:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{cy}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )


class Form6Dot47Sub5FactorSigmaCz(Formula):
    r"""Class representing sub-formula 5 for formula 6.47, which calculates the factor $$\sigma_{cz}$$."""

    label = "6.47sub5"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, n_ed_z: N, a_cz: MM2) -> None:
        r"""$$\sigma_{cz}$$ Calculation of factor $$\sigma_{cz}$$.

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Formula (6.47sub5)

        Parameters
        ----------
        n_ed_z : N
            $$N_{Ed,z}$$ Design axial force in z-direction [$$N$$].
        a_cz : MM2
            $$A_{cz}$$ Cross-sectional area in z-direction [$$mm^2$$].
        """
        super().__init__()
        self.n_ed_z = n_ed_z
        self.a_cz = a_cz

    @staticmethod
    def _evaluate(n_ed_z: N, a_cz: MM2) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(a_cz=a_cz)
        raise_if_negative(n_ed_z=n_ed_z)
        return n_ed_z / a_cz

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.47sub5."""
        _equation: str = r"\frac{N_{Ed,z}}{A_{cz}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed,z}": f"{self.n_ed_z:.3f}",
                r"A_{cz}": f"{self.a_cz:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{cz}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
