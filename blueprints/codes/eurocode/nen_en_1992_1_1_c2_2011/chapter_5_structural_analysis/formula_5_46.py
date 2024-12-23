"""Formula 5.46 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MM4, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot46TimeDependentLosses(Formula):
    r"""Class representing formula 5.46 for the calculation of the time dependent pre- and post-tensioning losses at location
    x under the permanent loads, :math:`\Delta P_{c+s+r}`.
    """

    label = "5.46"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_p: MM2,
        epsilon_cs: DIMENSIONLESS,
        e_p: MPA,
        delta_sigma_pr: MPA,
        e_cm: MPA,
        phi_t_t0: DIMENSIONLESS,
        sigma_c_qp: MPA,
        a_c: MM2,
        i_c: MM4,
        z_cp: MM,
    ) -> None:
        r"""[:math:`\Delta P_{c+s+r}`] Time dependent pre- and post-tensioning losses at location x under the permanent loads [:math:`N`].

        NEN-EN 1992-1-1+C2:2011 art.5.10.6(2) - Formula (5.46)

        Parameters
        ----------
        a_p : MM2
            [:math:`A_p`] Area of all the prestressing tendons at the location x [:math:`mm^2`].
        epsilon_cs : DIMENSIONLESS
            [:math:`\epsilon_{cs}`] The estimated shrinkage strain according to 3.1.4(6) in absolute value [-].
        e_p : MPA
            [:math:`E_p`] Modulus of elasticity for the prestressing steel, see 3.3.3 (9) [:math:`MPa`].
        delta_sigma_pr : MPA
            [:math:`\Delta \sigma_{pr}`] is the absolute value of the variation of stress in the tendons at location x, at
            time t, due to the relaxation of the prestressing steel [:math:`MPa`].
        e_cm : MPA
            [:math:`E_{cm}`] Modulus of elasticity for the concrete (Table 3.1) [:math:`MPa`].
        phi_t_t0 : DIMENSIONLESS
            [:math:`\phi(t, t_0)`] Creep coefficient at a time t and load application at time t0 [-].
        sigma_c_qp : MPA
            [:math:`\sigma_{c,QP}`] stress in the concrete adjacent to the tendons, due to self-weight and
            initial prestress and other quasi-permanent actions where relevant. [:math:`MPa`].
        a_c : MM2
            [:math:`A_c`] Area of concrete section [:math:`mm^2`].
        i_c : MM4
            [:math:`I_c`] Second moment of area of concrete section [:math:`mm^4`].
        z_cp : MM
            [:math:`z_{cp}`] Distance between the centre of gravity of the concrete section and the tendons [:math:`mm`].
        """
        super().__init__()
        self.a_p = a_p
        self.epsilon_cs = epsilon_cs
        self.e_p = e_p
        self.delta_sigma_pr = delta_sigma_pr
        self.e_cm = e_cm
        self.phi_t_t0 = phi_t_t0
        self.sigma_c_qp = sigma_c_qp
        self.a_c = a_c
        self.i_c = i_c
        self.z_cp = z_cp

    @staticmethod
    def _evaluate(
        a_p: MM2,
        epsilon_cs: DIMENSIONLESS,
        e_p: MPA,
        delta_sigma_pr: MPA,
        e_cm: MPA,
        phi_t_t0: DIMENSIONLESS,
        sigma_c_qp: MPA,
        a_c: MM2,
        i_c: MM4,
        z_cp: MM,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            epsilon_cs=epsilon_cs,
            delta_sigma_pr=delta_sigma_pr,
            phi_t_t0=phi_t_t0,
            sigma_c_qp=sigma_c_qp,
            z_cp=z_cp,
        )
        raise_if_less_or_equal_to_zero(a_p=a_p, e_p=e_p, e_cm=e_cm, a_c=a_c, i_c=i_c)

        numerator = epsilon_cs * e_p + 0.8 * delta_sigma_pr + (e_p / e_cm) * phi_t_t0 * sigma_c_qp
        denominator = 1 + (e_p / e_cm) * (a_p / a_c) * (1 + (a_c / i_c) * z_cp**2) * (1 + 0.8 * phi_t_t0)
        return a_p * numerator / denominator

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.46."""
        return LatexFormula(
            return_symbol=r"\Delta P_{c+s+r}",
            result=f"{self:.3f}",
            equation=r"A_p \cdot \frac{\epsilon_{cs} \cdot E_p + 0.8 \cdot \Delta \sigma_{pr} + \frac{E_p}{E_{cm}} \cdot "
            r"\phi(t, t_0) \cdot \sigma_{c,QP}}{1 + \frac{E_p}{E_{cm}} \cdot \frac{A_p}{A_c} \cdot \left(1 + \frac{A_c}{I_c} "
            r"\cdot z_{cp}^2\right) \cdot \left(1 + 0.8 \cdot \phi(t, t_0)\right)}",
            numeric_equation=rf"{self.a_p:.3f} \cdot \frac{{{self.epsilon_cs:.6f} \cdot {self.e_p:.3f} + 0.800"
            rf" \cdot {self.delta_sigma_pr:.3f} + \frac{{{self.e_p:.3f}}}{{{self.e_cm:.3f}}} \cdot {self.phi_t_t0:.3f} "
            rf"\cdot {self.sigma_c_qp:.3f}}}{{1 + \frac{{{self.e_p:.3f}}}{{{self.e_cm:.3f}}} \cdot \frac{{{self.a_p:.3f}}}{{{self.a_c:.3f}}} "
            rf"\cdot \left(1 + \frac{{{self.a_c:.3f}}}{{{self.i_c:.3f}}} \cdot {self.z_cp:.3f}^2\right) \cdot \left(1 + 0.800 "
            rf"\cdot {self.phi_t_t0:.3f}\right)}}",
            comparison_operator_label="=",
            unit="N",
        )
