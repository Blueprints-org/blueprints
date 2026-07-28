"""Formula 8.54 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot54NominalWebWidth(Formula):
    """Class representing formula 8.54 for the calculation of the nominal web width of a web containing ducts."""

    label = "8.54"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, b_w: MM, k_duct: DIMENSIONLESS, sum_phi_duct: MM) -> None:
        r"""[$b_{w,nom}$] Nominal web width to be used where the web contains ducts [$mm$].

        FprEN 1992-1-1:2023 (E) art 8.2.3 (10) - Formula (8.54)

        The standard applies this reduction where the web contains ducts of diameters such that
        [$\Sigma\phi_{duct} > b_w/8$]. That is a condition of application, not a bound on the result, so it is
        not enforced here: the caller decides whether the clause applies. For a smaller sum of duct diameters
        the formula still returns a value, it is simply not the one the standard asks for.

        Parameters
        ----------
        b_w : MM
            [$b_w$] Width of the web of the cross-section. For sections with variable width see 8.2.3(9) and
            Figure 8.10 [$mm$].
        k_duct : DIMENSIONLESS
            [$k_{duct}$] Coefficient evaluated depending on the material and filling of the duct. The standard
            gives 0,5 for grouted steel ducts, 0,8 for grouted plastic ducts with a wall thickness
            [$\leq \max\{0,035 \cdot \phi_{duct}; 2 mm\}$], and 1,2 for non-grouted ducts, for grouted plastic
            ducts with a wall thickness [$> \max\{0,035 \cdot \phi_{duct}; 2 mm\}$] or for ducts injected with
            soft filling material. None of these three carries a formula number, so the classification is made
            by the caller. Zero and negative values are rejected, since neither is a coefficient the standard
            offers and zero would leave the web width unreduced. Membership of the three values is not checked,
            so the choice between them stays with the caller [$-$].
        sum_phi_duct : MM
            [$\Sigma\phi_{duct}$] Sum of the outer diameters of the ducts, determined for the most unfavourable
            level. In the case of variable cross-section widths, calculations at different heights can be
            necessary to determine the decisive nominal value of the web width [$mm$].
        """
        super().__init__()
        self.b_w = b_w
        self.k_duct = k_duct
        self.sum_phi_duct = sum_phi_duct

    @staticmethod
    def _evaluate(b_w: MM, k_duct: DIMENSIONLESS, sum_phi_duct: MM) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sum_phi_duct=sum_phi_duct)
        raise_if_less_or_equal_to_zero(b_w=b_w, k_duct=k_duct)

        return b_w - k_duct * sum_phi_duct

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.54."""
        _equation: str = r"b_w - k_{duct} \cdot \Sigma\phi_{duct}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_w": f"{self.b_w:.{n}f}",
                r"k_{duct}": f"{self.k_duct:.{n}f}",
                r"\Sigma\phi_{duct}": f"{self.sum_phi_duct:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_w": rf"{self.b_w:.{n}f} \ mm",
                r"k_{duct}": f"{self.k_duct:.{n}f}",
                r"\Sigma\phi_{duct}": rf"{self.sum_phi_duct:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"b_{w,nom}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
