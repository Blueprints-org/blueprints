"""Formula 3.6 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class Form3Dot6CreepDeformationOfConcrete(Formula):
    """Class representing formula 3.6 for the calculation of creep deformation of concrete."""

    label = "3.6"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        phi_inf_t0: DIMENSIONLESS,
        sigma_c: MPA,
        e_c: MPA,
    ) -> None:
        r"""εcc(∞,t0) Creep deformation of concrete at the time t = ∞ for a constant concrete
        compressive stress [$\sigma_c$] applied at time [$t_0$] [$-$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(3) - Formula (3.6)

        Parameters
        ----------
        phi_inf_t0 : DIMENSIONLESS
            [$\varphi(\infty, t_0)$] Creep coefficient if high accuracy is not required use figure 3.1 else use appendix B [$-$].
        sigma_c : MPA
            [$\sigma_c$] Concrete compressive stress [$MPa$].
        e_c : MPA
            [$E_c$] tangent modulus = 1.05 * [$E_{cm}$]. According to art.3.1.4(2) [$MPa$].

        Returns
        -------
        None
        """
        super().__init__()
        self.phi_inf_t0 = phi_inf_t0
        self.sigma_c = sigma_c
        self.e_c = e_c

    @staticmethod
    def _evaluate(
        phi_inf_t0: DIMENSIONLESS,
        sigma_c: MPA,
        e_c: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        if phi_inf_t0 < 0:
            raise ValueError(f"Negative phi_inf_t0: {phi_inf_t0}. phi_inf_t0 cannot be negative")
        if sigma_c < 0:
            raise ValueError(f"Negative sigma_c: {sigma_c}. sigma_c cannot be negative")
        if e_c < 0:
            raise ValueError(f"Negative e_c: {e_c}. e_c cannot be negative")
        return phi_inf_t0 * sigma_c / e_c

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.6."""
        return LatexFormula(
            return_symbol=r"\epsilon_{cc}(\infty, t_0)",
            result=f"{self:.3f}",
            equation=r"\varphi(\infty, t_0) \cdot ( \sigma_c / E_c )",
            numeric_equation=rf"{self.phi_inf_t0:.3f} \cdot ( {self.sigma_c:.3f} / {self.e_c:.3f} )",
            comparison_operator_label="=",
        )
