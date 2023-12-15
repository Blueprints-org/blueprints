"""Formula 8.4 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons"""
# pylint: disable=arguments-differ
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_negative


class Form8Dot4DesignAnchorageLength(Formula):
    """Class representing formula 8.4 for the calculation of the design anchorage length lbd [mm]."""

    label = "8.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_1: DIMENSIONLESS,
        alpha_2: DIMENSIONLESS,
        alpha_3: DIMENSIONLESS,
        alpha_4: DIMENSIONLESS,
        alpha_5: DIMENSIONLESS,
        l_b_rqd: MM,
        l_b_min: MM,
    ) -> None:
        """[lbd] Design anchorage length [mm].

        NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.4)

        Parameters
        ----------
        alpha_1 : DIMENSIONLESS
            [α1] Coefficient for the effect of the form of the bars assuming adequate cover (see figure 8.1) [-].
            = 1.0 for bars in compression.
            = 1.0 for straight bars in tension.
            = 1.0 if cd <= 3 * Ø for bars other than straight in tension (see figure 8.1 (b), (c) and (d)).
            = 0.7 if cd > 3 * Ø for bars other than straight in tension (see figure 8.1 (b), (c) and (d)).
            Note: see figure 8.3 for values of cd.
        alpha_2 : DIMENSIONLESS
            [α2] Coefficient for the effect of minimum concrete cover (see figure 8.3) [-].
            = 1.0 for bars in compression.
            = 1 - 0.15 * (cd - Ø) / Ø <= 1 with a minimum of 0.7 for straight bars in tension.
            = 1 - 0.15 * (cd - 3 * Ø) / Ø <= 1 with a minimum of 0.7 for bars other than straight in tension (see figure 8.1 (b), (c) and (d)).
            Note: see figure 8.3 for values of cd.
        alpha_3 : DIMENSIONLESS
            [α3] Coefficient for the effect of confinement by transverse reinforcement [-].
            = 1.0 for bars in compression.
            = 1 - K * λ <= 1 with a minimum of 0.7 for bars in tension.
            Where: λ = (ΣAst - ΣAst,min) / As.
            Where: ΣAst,min = cross-sectional area of the minimum transverse reinforcement = 0,25 As for beams and 0 for slabs.
            Note: see figure 8.4 for values of K, As and Ast.
        alpha_4 : DIMENSIONLESS
            [α4] Coefficient for the influence of one or more welded transverse bars (Øt > 0,6 Ø) along the design anchorage length lbd (see 8.6) [-].
            = 0.7 for all types, position and size as specified in figure 8.6 (e) in both tension and compression.
        alpha_5 : DIMENSIONLESS
            [α5] Coefficient for the effect of the pressure transverse to the plane of splitting along the design anchorage length lbd (see 8.6) [-].
            = 1 - 0.04 * p <= 1 with a minimum of 0.7 for all types of anchorage in compression.
            Where: p = transverse pressure at ultimate limit state along lbd [MPa].
        l_b_rqd: MM
            [lb,rqd] Basic required anchorage length, for anchoring the force As*σsd in a straight bar assuming constant
            bond stress (formula 8.3) [mm].
            Use your own implementation for this value or use the Form8Dot3RequiredAnchorageLength class.
        l_b_min : MM
            [lbmin] Minimum anchorage length if no other limitation is applied [mm].
            = max(0.3 * l_b_rqd, 10 * Ø, 100) for tension anchorage (formula 8.6).
            = max(0.6 * l_b_rqd, 10 * Ø, 100) for compression anchorage (formula 8.7).
            Use your own implementation of this formula or use the Form8Dot6MinimumTensionAnchorage class for tension or
            Form8Dot7MinimumCompressionAnchorage for compression.

        Notes
        -----
        NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.5) prescribes that (α2 * α3 * α5) >= 0.7.
        """
        super().__init__()
        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2
        self.alpha_3 = alpha_3
        self.alpha_4 = alpha_4
        self.alpha_5 = alpha_5
        self.l_b_rqd = l_b_rqd
        self.l_b_min = l_b_min

    @staticmethod
    def _evaluate(
        alpha_1: DIMENSIONLESS,
        alpha_2: DIMENSIONLESS,
        alpha_3: DIMENSIONLESS,
        alpha_4: DIMENSIONLESS,
        alpha_5: DIMENSIONLESS,
        l_b_rqd: MM,
        l_b_min: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method"""
        raise_if_negative(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_4=alpha_4,
            alpha_5=alpha_5,
            l_b_rqd=l_b_rqd,
            l_b_min=l_b_min,
        )
        return max(alpha_1 * alpha_2 * alpha_3 * alpha_4 * alpha_5 * l_b_rqd, l_b_min)
