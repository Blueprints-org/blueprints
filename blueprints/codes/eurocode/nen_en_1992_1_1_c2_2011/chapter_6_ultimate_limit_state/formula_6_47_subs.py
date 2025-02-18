"""Formula 6.47 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class SubForm6Dot47FactorK(Formula):
    r"""Class representing the sub-formula which calculates the factor [$k$] for formula 6.47 ."""

    label = "6.47 (factor k)"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, d: MM) -> None:
        r"""[$k$] Calculation of factor k.

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Factor k for Formula (6.47)

        Parameters
        ----------
        d : MM
            [$d$] Effective depth [$mm$].
        """
        super().__init__()
        self.d = d

    @staticmethod
    def _evaluate(d: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(d=d)
        return min(1 + np.sqrt(200 / d), 2.0)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for sub-formula 6.47 (factor k)."""
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


class SubForm6Dot47FactorRhoL(Formula):
    r"""Class representing the sub-formula which calculates the factor [$\rho_l$] for formula 6.47 ."""

    label = "6.47 (factor rho_l)"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, rho_ly: DIMENSIONLESS, rho_lz: DIMENSIONLESS) -> None:
        r"""[$\rho_l$] Calculation of factor [$\rho_l$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Factor rho_l for Formula (6.47)

        Parameters
        ----------
        rho_ly : DIMENSIONLESS
            [$\rho_{ly}$] Related to the bonded tension steel in y- drection. The value $\rho_ly$ should be calculated as mean values taking
            into account a slab width equal to the column width plus 3d each side [$-$].
        rho_lz : DIMENSIONLESS
            [$\rho_{lz}$] Related to the bonded tension steel in z- drection. The value $\rho_lz$ should be calculated as mean values taking
            into account a slab width equal to the column width plus 3d each side [$-$].
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
        """Returns LatexFormula object for sub-formula 6.47 (factor rho_l)."""
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


class SubForm6Dot47FactorSigmaCp(Formula):
    r"""Class representing the sub-formula which calculates the factor [$\sigma_{cp}$] for formula 6.47,."""

    label = "6.47 (factor sigma_cp)"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, sigma_cy: MPA, sigma_cz: MPA) -> None:
        r"""[$\sigma_{cp}$] Calculation of factor [$\sigma_{cp}$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Factor sigma_cp for Formula (6.47)

        Parameters
        ----------
        sigma_cy : MPA
            [$\sigma_{cy}$] Normal concrete stress in the critical section in the y-direction [$MPa$], Positive if compression.
            See equation SubForm6Dot47FactorSigmaCy.
        sigma_cz : MPA
            [$\sigma_{cz}$] Normal concrete stress inm the critical section in the z-direction [$MPa$], Positive if compression.
            See equation SubForm6Dot47FactorSigmaCz.
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
        """Returns LatexFormula object for sub-formula 6.47 (sigma_cp)."""
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


class SubForm6Dot47FactorSigmaCy(Formula):
    r"""Class representing the sub-formula which calculates the factor [$\sigma_{cy}$] for formula 6.47."""

    label = "6.47 (factor sigma_cy)"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, n_ed_y: N, a_cy: MM2) -> None:
        r"""[$\sigma_{cy}$] Calculation of factor [$\sigma_{cy}$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Factor sigma_cy for Formula (6.47)

        Parameters
        ----------
        n_ed_y : N
            [$N_{Ed,y}$] Longitudinal forces across the full bay for internal columns and the logintudinal force across
            the control section for edge columns. The force may be from a load or prestressing action [$N$].
        a_cy : MM2
            [$A_{cy}$] Cross-sectional area in y-direction [$mm^2$].
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
        """Returns LatexFormula object for sub-formula 6.47 (sigma_cy)."""
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


class SubForm6Dot47FactorSigmaCz(Formula):
    r"""Class representing the sub-formula which calculates the factor [$\sigma_{cz}$] for formula 6.47."""

    label = "6.47 (factor sigma_cz)"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, n_ed_z: N, a_cz: MM2) -> None:
        r"""[$\sigma_{cz}$] Calculation of factor [$\sigma_{cz}$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(1) - Factor sigma_cz for Formula (6.47)

        Parameters
        ----------
        n_ed_z : N
            [$N_{Ed,z}$] Longitudinal forces across the full bay for internal columns and the logintudinal force across
            the control section for edge columns. The force may be from a load or prestressing action [$N$].
        a_cz : MM2
            [$A_{cz}$] Cross-sectional area in z-direction [$mm^2$].
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
        """Returns LatexFormula object for sub-formula 6.47 sigma_cz."""
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
