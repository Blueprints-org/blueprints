"""Formula 8.20 from EN 1992-1-1:2004: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot20BondStrengthAnchorageULS(Formula):
    r"""Class representing formula 8.20 for the calculation of bond strength for anchorage in the ultimate limit state [$f_{bpd}$].

    EN 1992-1-1:2004 art.8.10.2.2(3) - Formula (8.20)

    Parameters
    ----------
    eta_p2 : DIMENSIONLESS
        [$\eta_{p2}$] Coefficient that takes into account the type of tendon and the bond situation at anchorage [$-$].

        1.4 for indented wires or 1.2 for 7-wire strands.
    eta_1 : DIMENSIONLESS
        [$\eta_{1}$] Coefficient for concrete, defined in 8.10.2.2 (1) [$-$].
    f_ctd : MPA
        Design tensile strength of concrete [$MPa$].
    """

    label = "8.20"
    source_document = EN_1992_1_1_2004

    def __init__(self, eta_p2: DIMENSIONLESS, eta_1: DIMENSIONLESS, f_ctd: MPA) -> None:
        super().__init__()
        self.eta_p2 = eta_p2
        self.eta_1 = eta_1
        self.f_ctd = f_ctd

    @staticmethod
    def _evaluate(eta_p2: DIMENSIONLESS, eta_1: DIMENSIONLESS, f_ctd: MPA) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(eta_p2=eta_p2, eta_1=eta_1, f_ctd=f_ctd)
        return eta_p2 * eta_1 * f_ctd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.20."""
        _equation: str = r"\eta_{p2} \cdot \eta_{1} \cdot f_{ctd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\eta_{p2}": f"{self.eta_p2:.{n}f}",
                r"\eta_{1}": f"{self.eta_1:.{n}f}",
                r"f_{ctd}": f"{self.f_ctd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"\eta_{p2}": f"{self.eta_p2:.{n}f}",
                r"\eta_{1}": f"{self.eta_1:.{n}f}",
                r"f_{ctd}": rf"{self.f_ctd:.{n}f} \ MPa",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"f_{bpd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )

class SubForm8Dot20EtaP2(Formula):
    r"""Class representing sub-formula 8.20 for the calculation of the coefficient [$\eta_{p2}$]."""

    label = "8.20"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        type_of_wire: str,
    ) -> None:
        r"""[$\eta_{p2}$] Coefficient that takes into account the type of tendon and the bond situation at the anchorage [$-$].

        EN 1992-1-1:2004 art.8.10.2.3(2) - Formula (8.20)

        Parameters
        ----------
        type_of_wire : str
            Type of wire.

            = 'indented' for indented wires;

            = '7_wire_strands' for 7-wire strands;
        """
        super().__init__()
        self.type_of_wire = type_of_wire

    @staticmethod
    def _evaluate(type_of_wire: str) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        match type_of_wire.lower():
            case "indented":
                return 1.4
            case "7_wire_strands":
                return 1.2
            case _:
                raise ValueError(f"Invalid type of wire: {type_of_wire}. Options: 'indented' or '7_wire_strands'")

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for the subformula of formula 8.20."""
        _equation: str = r"type\;of\;wire"
        _numeric_equation: str = f"{self.type_of_wire}".replace("_", r"\;")
        _numeric_equation_with_units: str = _numeric_equation
        return LatexFormula(
            return_symbol=r"\eta_{p2}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\rightarrow",
        )