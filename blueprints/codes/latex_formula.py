from dataclasses import dataclass


@dataclass(frozen=True)
class LatexFormula:
    return_symbol: str
    result: str
    equation: str = ""
    numeric_equation: str = ""

    @property
    def complete(self) -> str:
        all_sub_equations = [self.return_symbol, self.equation, self.numeric_equation, self.result]
        return " = ".join([eq for eq in all_sub_equations if eq != ""])

    @property
    def short(self) -> str:
        return f"{self.return_symbol} = {self.result}"
