"""Formula 8.3 from EN 1992-1-1:2004: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction, latex_replace_symbols
from blueprints.type_alias import MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot3RequiredAnchorageLength(Formula):
    r"""Class representing formula 8.3 for the calculation of the basic required anchorage length, assuming constant bond stress [$f_{bd}$]."""

    label = "8.3"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        diameter: MM,
        sigma_sd: MPA,
        f_bd: MPA,
    ) -> None:
        r"""[$l_{b,rqd}$] Basic required anchorage length, for anchoring the force [$A_{s} \cdot \sigma_{sd}$] in a straight bar assuming
        constant bond stress [$f_{bd}$]. [mm].

        EN 1992-1-1:2004 art.8.4.3(2) - Formula (8.3)

        Parameters
        ----------
        diameter: MM
            [$Ø$] Diameter of the bar [mm].
        sigma_sd: MPA
            [$\sigma_{sd}$] design stress of the bar at the position from where the anchorage is measured from [MPa].
        f_bd: MPA
            [$f_{bd}$] Design value ultimate bond stress [MPa].
            Use your own implementation for this value or use the Form8Dot2UltimateBondStress class.
        """
        super().__init__()
        self.diameter = diameter
        self.sigma_sd = sigma_sd
        self.f_bd = f_bd

    @staticmethod
    def _evaluate(
        diameter: MM,
        sigma_sd: MPA,
        f_bd: MPA,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(diameter=diameter, sigma_sd=sigma_sd)
        raise_if_less_or_equal_to_zero(f_bd=f_bd)
        return (diameter / 4) * (sigma_sd / f_bd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns a LatexFormula object for this formula."""
        _equation: str = rf"{latex_fraction(r'Ø',4)} \cdot {latex_fraction(r'\sigma_{sd}', r'f_{bd}')}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"Ø": f"{self.diameter:.{n}f}",
                r"\sigma_{sd}": f"{self.sigma_sd:.{n}f}",
                r"f_{bd}": f"{self.f_bd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"Ø": rf"{self.diameter:.{n}f} \ mm",
                r"\sigma_{sd}": rf"{self.sigma_sd:.{n}f} \ MPa",
                r"f_{bd}": rf"{self.f_bd:.{n}f} \ MPa",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"l_{b,rqd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )

