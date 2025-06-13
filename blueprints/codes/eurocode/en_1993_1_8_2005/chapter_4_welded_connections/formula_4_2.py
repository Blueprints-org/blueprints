"""Formula 4.2 from EN 1993-1-8:2005: Chapter 4 - Welded Connections."""

from blueprints.codes.eurocode.en_1993_1_8_2005 import EN_1993_1_8_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_negative


class Form4Dot2CheckWeldedConnection(Formula):
    r"""Class representing formula 4.2 for checking welded connections."""

    label = "4.2"
    source_document = EN_1993_1_8_2005

    def __init__(
        self,
        fw_ed: N,
        fw_rd: N,
    ) -> None:
        r"""Check the force in the weld per unit length against its resistance.

        EN 1993-1-8:2005 art.4.5.3.3(1) - Formula (4.2)

        Parameters
        ----------
        fw_ed : N
            [$F_{w,Ed}$] Design value of the force in the weld per unit length [$N$].
        fw_rd : N
            [$F_{w,Rd}$] Design value of the resistance of the weld per unit length [$N$].
        """
        super().__init__()
        self.fw_ed = fw_ed
        self.fw_rd = fw_rd

    @staticmethod
    def _evaluate(
        fw_ed: N,
        fw_rd: N,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(fw_ed=fw_ed, fw_rd=fw_rd)

        return fw_ed <= fw_rd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 4.2."""
        _equation: str = r"F_{w,Ed} \leq F_{w,Rd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "F_{w,Ed}": f"{self.fw_ed:.{n}f}",
                "F_{w,Rd}": f"{self.fw_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "F_{w,Ed}": rf"{self.fw_ed:.{n}f} \ N",
                "F_{w,Rd}": rf"{self.fw_rd:.{n}f} \ N",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="\\to",
            unit="",
        )
