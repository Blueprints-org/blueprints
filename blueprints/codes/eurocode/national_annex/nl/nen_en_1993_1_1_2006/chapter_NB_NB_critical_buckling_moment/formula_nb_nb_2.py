"""Formula NB.NB.2 from NEN-EN 1993-1-1:2006: Chapter NB.NB - Critical elastic buckling moment."""

import numpy as np

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006 import NEN_EN_1993_1_1_2006_A1_2014_NB_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM4, MPA, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class FormNBDotNB2CriticalElasticBucklingMoment(Formula):
    r"""Class representing formula NB.NB.2 for the calculation of [$M_{cr}$]."""

    label = "NB.NB.2"
    source_document = NEN_EN_1993_1_1_2006_A1_2014_NB_2016

    def __init__(
        self,
        k_red: DIMENSIONLESS,
        c: DIMENSIONLESS,
        l_g: MM,
        e: MPA,
        i_z: MM4,
        g: MPA,
        i_t: MM4,
    ) -> None:
        r"""[$M_{cr}$] Calculation of the critical elastic buckling moment [$Nmm$].

        NEN-EN 1993-1-1:2006 art.NB.NB.4.1 - Formula (NB.NB.2)

        Parameters
        ----------
        k_red : DIMENSIONLESS
            [$k_{red}$] Reduction factor dependent on the degree of deformation of the beam cross-section with regard to beam length;
            for calculating [$k_{red}$] applies NB.NB.4.2 [-].
        c : DIMENSIONLESS
            [$C$] Coefficient dependent on beam length and load point location, and support point of the load;
            for calculating [$C$] applies NB.NB.4.3 [-].
        l_g : MM
            [$L_g$] Length of the beam between supports [$mm$].
        e : MPA
            [$E$] Elasticity modulus [$MPa$].
        i_z : MM4
            [$I_z$] Moment of inertia about the z-axis [$mm^4$].
        g : MPA
            [$G$] Shear modulus [$MPa$].
        i_t : MM4
            [$I_t$] Torsional moment of inertia [$mm^4$].
        """
        super().__init__()
        self.k_red = k_red
        self.c = c
        self.l_g = l_g
        self.e = e
        self.i_z = i_z
        self.g = g
        self.i_t = i_t

    @staticmethod
    def _evaluate(
        k_red: DIMENSIONLESS,
        c: DIMENSIONLESS,
        l_g: MM,
        e: MPA,
        i_z: MM4,
        g: MPA,
        i_t: MM4,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(l_g=l_g)
        raise_if_negative(k_red=k_red, c=c, e=e, i_z=i_z, g=g, i_t=i_t)

        return k_red * (c / l_g) * np.sqrt(e * i_z * g * i_t)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula NB.NB.2."""
        _equation: str = r"k_{red} \cdot \frac{C}{L_g} \cdot \sqrt{E \cdot I_z \cdot G \cdot I_t}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"k_{red}": f"{self.k_red:.{n}f}",
                r"C": f"{self.c:.{n}f}",
                r"L_g": f"{self.l_g:.{n}f}",
                r"E": f"{self.e:.{n}f}",
                r"I_z": f"{self.i_z:.{n}f}",
                r"G": f"{self.g:.{n}f}",
                r"I_t": f"{self.i_t:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"k_{red}": f"{self.k_red:.{n}f}",
                r"C": f"{self.c:.{n}f}",
                r"L_g": rf"{self.l_g:.{n}f} \ mm",
                r"E": rf"{self.e:.{n}f} \ MPa",
                r"I_z": rf"{self.i_z:.{n}f} \ mm^4",
                r"G": rf"{self.g:.{n}f} \ MPa",
                r"I_t": rf"{self.i_t:.{n}f} \ mm^4",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"M_{cr}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )
