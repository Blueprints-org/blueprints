"""Table 3.4 from EN 1993-1-8:2005: Chapter 3 - Connections made with bolts, rivets or pins.

Table 3.4 gives the design resistance of individual fasteners subjected to shear and/or tension. Four
of its five rows return a resistance in newtons; only the last row, combined shear and tension, is a
check. Each printed expression is implemented as its own class, so that a caller who needs a single
row does not have to build the rest of the table.

The source read for this implementation is the consolidated text including corrigendum C2. The
corrigendum touches the bearing resistance row, so an implementation of the uncorrected 2005 print
would differ there.
"""

import math
import operator
from collections.abc import Callable
from enum import StrEnum

from blueprints.codes.eurocode.en_1993_1_8_2005 import EN_1993_1_8_2005
from blueprints.codes.eurocode.en_1993_1_8_2005.chapter_3_connections_made_with_bolts_rivets_or_pins.table_3_1 import BoltClass
from blueprints.codes.formula import ComparisonFormula, Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative

# The shear factor of Table 3.4, for a shear plane through the threaded portion of the bolt. Where the
# plane passes through the unthreaded shank the table gives 0.6 for every class, so the class does not
# enter the calculation there. Every class of Table 3.1 is mapped, so an unmapped class raises a
# KeyError rather than silently taking a value the table does not give it.
ALPHA_V_THREADED: dict[BoltClass, DIMENSIONLESS] = {
    BoltClass.CLASS_4_6: 0.6,
    BoltClass.CLASS_4_8: 0.5,
    BoltClass.CLASS_5_6: 0.6,
    BoltClass.CLASS_5_8: 0.5,
    BoltClass.CLASS_6_8: 0.5,
    BoltClass.CLASS_8_8: 0.6,
    BoltClass.CLASS_10_9: 0.5,
}

ALPHA_V_SHANK: DIMENSIONLESS = 0.6


class ShearPlane(StrEnum):
    """Location of the shear plane through the bolt, which Table 3.4 distinguishes.

    THREADED: the shear plane passes through the threaded portion of the bolt, so the area to use is
    the tensile stress area and the factor depends on the bolt class.

    SHANK: the shear plane passes through the unthreaded portion of the bolt, so the area to use is
    the gross cross-section of the bolt and the factor is 0.6 for every class.
    """

    THREADED = "Shear plane through the threaded portion"
    SHANK = "Shear plane through the unthreaded shank"


class BoltHead(StrEnum):
    """Head shape of the bolt, which sets the factor of the tension resistance row of Table 3.4."""

    NORMAL = "Normal head"
    COUNTERSUNK = "Countersunk head"

    @property
    def k_2(self) -> DIMENSIONLESS:
        r"""[$k_2$] that Table 3.4 gives for this head shape [$-$].

        Returns
        -------
        DIMENSIONLESS
            0.63 for a countersunk head and 0.9 for a normal one. Every member is mapped, so a head
            shape added later raises a KeyError instead of silently taking one of the two.
        """
        return {BoltHead.NORMAL: 0.9, BoltHead.COUNTERSUNK: 0.63}[self]


class HoleType(StrEnum):
    """Hole shape, with the reduction on the bearing resistance from note 1 of Table 3.4.

    The note reduces the bearing resistance to 0.8 times its value for a bolt in an oversized hole,
    and to 0.6 times its value for a bolt in a slotted hole whose long axis is perpendicular to the
    direction of load transfer. It prints no factor for a slotted hole whose long axis is parallel to
    that direction, so that case is not offered here.
    """

    NORMAL = "Normal round hole"
    OVERSIZED = "Oversized hole"
    SLOTTED_PERPENDICULAR = "Slotted hole, long axis perpendicular to the load transfer"

    @property
    def reduction(self) -> DIMENSIONLESS:
        """Factor by which note 1 of Table 3.4 multiplies the bearing resistance for this hole shape.

        Returns
        -------
        DIMENSIONLESS
            1.0 for a normal round hole, 0.8 for an oversized one and 0.6 for a slotted one. Every
            member is mapped, so a hole shape added later raises a KeyError instead of silently
            passing as unreduced.
        """
        return {HoleType.NORMAL: 1.0, HoleType.OVERSIZED: 0.8, HoleType.SLOTTED_PERPENDICULAR: 0.6}[self]


class BoltPositionParallel(StrEnum):
    """Position of the bolt in the direction of load transfer, which selects the expression for alpha_d."""

    END = "End bolt"
    INNER = "Inner bolt"


class BoltPositionPerpendicular(StrEnum):
    """Position of the bolt perpendicular to the direction of load transfer, which selects the expression for k_1."""

    EDGE = "Edge bolt"
    INNER = "Inner bolt"


class Table3Dot4ShearResistanceBolt(Formula):
    """Class representing the shear resistance per shear plane of a bolt, from Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(
        self,
        f_ub: MPA,
        a: MM2,
        bolt_class: BoltClass,
        shear_plane: ShearPlane,
        gamma_m2: DIMENSIONLESS,
    ) -> None:
        r"""[$F_{v,Rd}$] Design shear resistance per shear plane of a bolt [$N$].

        EN 1993-1-8:2005 art.3.6.1 (16) - Table 3.4

        The area to pass depends on where the shear plane sits, and the table says which one: the
        tensile stress area [$A_s$] where the plane passes through the threads, the gross area of the
        bolt where it passes through the shank. The class only checks that the two are consistent
        through [$\alpha_v$], it cannot check the area itself.

        Where the fastener passes through packings of a total thickness greater than [$d/3$],
        art.3.6.1(12) multiplies this resistance by [$\beta_p$] of Formula (3.3). That reduction
        applies to the shear resistance only, not to the bearing or the tension resistance, and it is
        left to the caller since it is printed outside the table.

        Parameters
        ----------
        f_ub : MPA
            [$f_{ub}$] Ultimate tensile strength of the bolt [$MPa$].
        a : MM2
            [$A$] Area of the bolt at the shear plane. The tensile stress area [$A_s$] where the shear
            plane passes through the threaded portion, the gross cross-section where it passes through
            the unthreaded shank [$mm^2$].
        bolt_class : BoltClass
            Class of the bolt, which sets [$\alpha_v$] where the shear plane passes through the threads.
        shear_plane : ShearPlane
            Location of the shear plane through the bolt.
        gamma_m2 : DIMENSIONLESS
            [$\gamma_{M2}$] Partial factor for the resistance of the fastener [$-$].
        """
        super().__init__()
        self.f_ub = f_ub
        self.a = a
        self.bolt_class = bolt_class
        self.shear_plane = shear_plane
        self.gamma_m2 = gamma_m2

    @property
    def alpha_v(self) -> DIMENSIONLESS:
        r"""[$\alpha_v$] Shear factor that Table 3.4 gives for this bolt class and shear plane [$-$]."""
        return self._alpha_v(self.bolt_class, self.shear_plane)

    @staticmethod
    def _alpha_v(bolt_class: BoltClass, shear_plane: ShearPlane) -> DIMENSIONLESS:
        r"""Returns [$\alpha_v$], which depends on the class only where the shear plane crosses the threads."""
        return ALPHA_V_THREADED[bolt_class] if shear_plane is ShearPlane.THREADED else ALPHA_V_SHANK

    @classmethod
    def _evaluate(
        cls,
        f_ub: MPA,
        a: MM2,
        bolt_class: BoltClass,
        shear_plane: ShearPlane,
        gamma_m2: DIMENSIONLESS,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ub=f_ub, a=a)
        raise_if_less_or_equal_to_zero(gamma_m2=gamma_m2)

        return cls._alpha_v(bolt_class, shear_plane) * f_ub * a / gamma_m2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the shear resistance of a bolt."""
        _equation: str = r"\frac{\alpha_v \cdot f_{ub} \cdot A}{\gamma_{M2}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_v": f"{self.alpha_v:.{n}f}",
                r"f_{ub}": f"{self.f_ub:.{n}f}",
                r"A": f"{self.a:.{n}f}",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_v": f"{self.alpha_v:.{n}f}",
                r"f_{ub}": rf"{self.f_ub:.{n}f} \ MPa",
                r"A": rf"{self.a:.{n}f} \ mm^2",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"F_{v,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )


class Table3Dot4ShearResistanceRivet(Formula):
    """Class representing the shear resistance per shear plane of a rivet, from Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(self, f_ur: MPA, a_0: MM2, gamma_m2: DIMENSIONLESS) -> None:
        r"""[$F_{v,Rd}$] Design shear resistance per shear plane of a rivet [$N$].

        EN 1993-1-8:2005 art.3.6.1 - Table 3.4

        Where the fastener passes through packings of a total thickness greater than [$d/3$],
        art.3.6.1(12) multiplies this resistance by [$\beta_p$] of Formula (3.3). That reduction
        applies to the shear resistance only, and it is left to the caller since it is printed outside
        the table.

        Parameters
        ----------
        f_ur : MPA
            [$f_{ur}$] Ultimate tensile strength of the rivet. For steel grade S 235 art.3.6.1(15)
            allows 400 [$MPa$] to be taken [$MPa$].
        a_0 : MM2
            [$A_0$] Area of the hole of the rivet [$mm^2$].
        gamma_m2 : DIMENSIONLESS
            [$\gamma_{M2}$] Partial factor for the resistance of the fastener [$-$].
        """
        super().__init__()
        self.f_ur = f_ur
        self.a_0 = a_0
        self.gamma_m2 = gamma_m2

    @staticmethod
    def _evaluate(f_ur: MPA, a_0: MM2, gamma_m2: DIMENSIONLESS) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ur=f_ur, a_0=a_0)
        raise_if_less_or_equal_to_zero(gamma_m2=gamma_m2)

        return 0.6 * f_ur * a_0 / gamma_m2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the shear resistance of a rivet."""
        _equation: str = r"\frac{0.6 \cdot f_{ur} \cdot A_0}{\gamma_{M2}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"f_{ur}": f"{self.f_ur:.{n}f}",
                r"A_0": f"{self.a_0:.{n}f}",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"f_{ur}": rf"{self.f_ur:.{n}f} \ MPa",
                r"A_0": rf"{self.a_0:.{n}f} \ mm^2",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"F_{v,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )


class Table3Dot4AlphaD(Formula):
    """Class representing the factor alpha_d of the bearing resistance row of Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(self, position: BoltPositionParallel, spacing: MM, d_0: MM) -> None:
        r"""[$\alpha_d$] Factor in the direction of load transfer, feeding [$\alpha_b$] [$-$].

        EN 1993-1-8:2005 art.3.6.1 - Table 3.4

        The table prints two expressions, one for an end bolt and one for an inner bolt, each taking a
        different distance. The distance to pass therefore follows from the position.

        Parameters
        ----------
        position : BoltPositionParallel
            Position of the bolt in the direction of load transfer.
        spacing : MM
            [$e_1$] End distance from the centre of the fastener hole to the adjacent end of any part,
            measured in the direction of load transfer, for an end bolt. [$p_1$] Spacing between the
            centres of fasteners in a line in the direction of load transfer, for an inner bolt [$mm$].
        d_0 : MM
            [$d_0$] Diameter of the fastener hole [$mm$].
        """
        super().__init__()
        self.position = position
        self.spacing = spacing
        self.d_0 = d_0

    @staticmethod
    def _evaluate(position: BoltPositionParallel, spacing: MM, d_0: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(spacing=spacing)
        raise_if_less_or_equal_to_zero(d_0=d_0)

        if position is BoltPositionParallel.END:
            return spacing / (3 * d_0)
        return spacing / (3 * d_0) - 0.25

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the factor alpha_d."""
        end = self.position is BoltPositionParallel.END
        _equation: str = r"\frac{e_1}{3 \cdot d_0}" if end else r"\frac{p_1}{3 \cdot d_0} - \frac{1}{4}"
        _symbol: str = r"e_1" if end else r"p_1"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={_symbol: f"{self.spacing:.{n}f}", r"d_0": f"{self.d_0:.{n}f}"},
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={_symbol: rf"{self.spacing:.{n}f} \ mm", r"d_0": rf"{self.d_0:.{n}f} \ mm"},
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\alpha_d",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


class Table3Dot4AlphaB(Formula):
    """Class representing the factor alpha_b of the bearing resistance row of Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(self, alpha_d: DIMENSIONLESS, f_ub: MPA, f_u: MPA) -> None:
        r"""[$\alpha_b$] Smallest of [$\alpha_d$], [$f_{ub}/f_u$] and 1.0 [$-$].

        EN 1993-1-8:2005 art.3.6.1 - Table 3.4

        Parameters
        ----------
        alpha_d : DIMENSIONLESS
            [$\alpha_d$] Factor in the direction of load transfer, see Table3Dot4AlphaD. It is not
            required to be positive, since Table3Dot4AlphaD returns the printed expression unclamped
            and that expression turns negative for a small spacing [$-$].
        f_ub : MPA
            [$f_{ub}$] Ultimate tensile strength of the bolt [$MPa$].
        f_u : MPA
            [$f_u$] Ultimate tensile strength of the connected plate [$MPa$].
        """
        super().__init__()
        self.alpha_d = alpha_d
        self.f_ub = f_ub
        self.f_u = f_u

    @staticmethod
    def _evaluate(alpha_d: DIMENSIONLESS, f_ub: MPA, f_u: MPA) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ub=f_ub)
        raise_if_less_or_equal_to_zero(f_u=f_u)

        return min(alpha_d, f_ub / f_u, 1.0)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the factor alpha_b."""
        _equation: str = r"\min\left(\alpha_d, \frac{f_{ub}}{f_u}, 1.0\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_d": f"{self.alpha_d:.{n}f}",
                r"f_{ub}": f"{self.f_ub:.{n}f}",
                r"f_u": f"{self.f_u:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_d": f"{self.alpha_d:.{n}f}",
                r"f_{ub}": rf"{self.f_ub:.{n}f} \ MPa",
                r"f_u": rf"{self.f_u:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\alpha_b",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


class Table3Dot4K1(Formula):
    """Class representing the factor k_1 of the bearing resistance row of Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(
        self,
        position: BoltPositionPerpendicular,
        d_0: MM,
        p_2: MM | None = None,
        e_2: MM | None = None,
    ) -> None:
        r"""[$k_1$] Factor perpendicular to the direction of load transfer [$-$].

        EN 1993-1-8:2005 art.3.6.1 - Table 3.4

        For an edge bolt the table takes the smallest of three values, for an inner bolt the smallest
        of two. The term in [$p_2$] presumes a neighbouring line of fasteners. Where there is only one
        line, so that no [$p_2$] exists, that term is left out and the remaining terms decide. That is
        an addition made here, not printed text: the table gives no rule for a missing [$p_2$].

        Parameters
        ----------
        position : BoltPositionPerpendicular
            Position of the bolt perpendicular to the direction of load transfer.
        d_0 : MM
            [$d_0$] Diameter of the fastener hole [$mm$].
        p_2 : MM, optional
            [$p_2$] Spacing measured perpendicular to the direction of load transfer between adjacent
            lines of fasteners. Leave it out where the connection has a single line [$mm$].
        e_2 : MM, optional
            [$e_2$] Edge distance from the centre of the fastener hole to the adjacent edge of any
            part, measured perpendicular to the direction of load transfer. Required for an edge bolt
            and unused for an inner bolt [$mm$].
        """
        super().__init__()
        self.position = position
        self.d_0 = d_0
        self.p_2 = p_2
        self.e_2 = e_2

    @staticmethod
    def _evaluate(
        position: BoltPositionPerpendicular,
        d_0: MM,
        p_2: MM | None = None,
        e_2: MM | None = None,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(d_0=d_0)
        if p_2 is not None:
            raise_if_negative(p_2=p_2)
        if e_2 is not None:
            raise_if_negative(e_2=e_2)

        candidates = [2.5]
        if p_2 is not None:
            candidates.append(1.4 * p_2 / d_0 - 1.7)
        if position is BoltPositionPerpendicular.EDGE:
            if e_2 is None:
                raise ValueError("e_2 must be given for an edge bolt, since Table 3.4 takes 2.8 * e_2 / d_0 - 1.7 into account there.")
            candidates.append(2.8 * e_2 / d_0 - 1.7)
        elif p_2 is None:
            raise ValueError("p_2 must be given for an inner bolt, since Table 3.4 offers no other term than 1.4 * p_2 / d_0 - 1.7 there.")

        return min(candidates)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the factor k_1."""
        terms: list[str] = []
        numeric: list[str] = []
        numeric_with_units: list[str] = []
        if self.position is BoltPositionPerpendicular.EDGE:
            terms.append(r"2.8 \cdot \frac{e_2}{d_0} - 1.7")
            numeric.append(rf"2.8 \cdot \frac{{{self.e_2:.{n}f}}}{{{self.d_0:.{n}f}}} - 1.7")
            numeric_with_units.append(rf"2.8 \cdot \frac{{{self.e_2:.{n}f} \ mm}}{{{self.d_0:.{n}f} \ mm}} - 1.7")
        if self.p_2 is not None:
            terms.append(r"1.4 \cdot \frac{p_2}{d_0} - 1.7")
            numeric.append(rf"1.4 \cdot \frac{{{self.p_2:.{n}f}}}{{{self.d_0:.{n}f}}} - 1.7")
            numeric_with_units.append(rf"1.4 \cdot \frac{{{self.p_2:.{n}f} \ mm}}{{{self.d_0:.{n}f} \ mm}} - 1.7")
        terms.append("2.5")
        numeric.append("2.5")
        numeric_with_units.append("2.5")

        return LatexFormula(
            return_symbol=r"k_1",
            result=f"{self:.{n}f}",
            equation=rf"\min\left({', '.join(terms)}\right)",
            numeric_equation=rf"\min\left({', '.join(numeric)}\right)",
            numeric_equation_with_units=rf"\min\left({', '.join(numeric_with_units)}\right)",
            comparison_operator_label="=",
            unit="-",
        )


class Table3Dot4BearingResistance(Formula):
    """Class representing the bearing resistance of a bolt or rivet, from Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(
        self,
        k_1: DIMENSIONLESS,
        alpha_b: DIMENSIONLESS,
        f_u: MPA,
        d: MM,
        t: MM,
        gamma_m2: DIMENSIONLESS,
        hole_type: HoleType = HoleType.NORMAL,
    ) -> None:
        r"""[$F_{b,Rd}$] Design bearing resistance of a bolt or rivet [$N$].

        EN 1993-1-8:2005 art.3.6.1 - Table 3.4

        The cell of the table spans both columns, so the same expression covers bolts and rivets. Note
        1 of the table reduces the result for a bolt in an oversized or a slotted hole; that reduction
        is applied here through hole_type.

        For a countersunk bolt, note 2 asks for a plate thickness reduced by half the depth of the
        countersinking. That is a property of the thickness passed in, so it is left to the caller
        rather than turned into a parameter here.

        Note 3 permits the bearing resistance to be verified separately for the components of the bolt
        force parallel and perpendicular to the end of the plate, where the force is not parallel to
        the edge. That is a permission rather than a number, so it is left to the caller, who applies
        it by evaluating this class once per component.

        The table prints no lower bound on the result. Both [$\alpha_b$] and [$k_1$] can turn negative
        for very small distances, and such a result is returned unchanged rather than clamped, since a
        clamp would be an addition beyond the printed text.

        Parameters
        ----------
        k_1 : DIMENSIONLESS
            [$k_1$] Factor perpendicular to the direction of load transfer, see Table3Dot4K1. It is
            not required to be positive, for the reason given above [$-$].
        alpha_b : DIMENSIONLESS
            [$\alpha_b$] Factor in the direction of load transfer, see Table3Dot4AlphaB. It is not
            required to be positive, for the reason given above [$-$].
        f_u : MPA
            [$f_u$] Ultimate tensile strength of the connected plate [$MPa$].
        d : MM
            [$d$] Diameter of the fastener [$mm$].
        t : MM
            [$t$] Thickness of the connected plate. For a countersunk bolt, the thickness of the
            connected plate minus half the depth of the countersinking [$mm$].
        gamma_m2 : DIMENSIONLESS
            [$\gamma_{M2}$] Partial factor for the resistance of the fastener [$-$].
        hole_type : HoleType
            Shape of the hole, which sets the reduction of note 1 of the table. Defaults to a normal
            round hole, for which the reduction is 1.0.
        """
        super().__init__()
        self.k_1 = k_1
        self.alpha_b = alpha_b
        self.f_u = f_u
        self.d = d
        self.t = t
        self.gamma_m2 = gamma_m2
        self.hole_type = hole_type

    @staticmethod
    def _evaluate(
        k_1: DIMENSIONLESS,
        alpha_b: DIMENSIONLESS,
        f_u: MPA,
        d: MM,
        t: MM,
        gamma_m2: DIMENSIONLESS,
        hole_type: HoleType = HoleType.NORMAL,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_u=f_u, d=d, t=t)
        raise_if_less_or_equal_to_zero(gamma_m2=gamma_m2)

        return hole_type.reduction * k_1 * alpha_b * f_u * d * t / gamma_m2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the bearing resistance."""
        # Built with f-strings rather than latex_replace_symbols: the single-letter symbols d and t of
        # this row also occur inside the \cdot of the template, so a plain text substitution corrupts it.
        prefix = "" if self.hole_type is HoleType.NORMAL else rf"{self.hole_type.reduction} \cdot "
        _equation: str = prefix + r"\frac{k_1 \cdot \alpha_b \cdot f_u \cdot d \cdot t}{\gamma_{M2}}"
        _numeric_equation: str = (
            prefix + rf"\frac{{{self.k_1:.{n}f} \cdot {self.alpha_b:.{n}f} \cdot {self.f_u:.{n}f} \cdot "
            rf"{self.d:.{n}f} \cdot {self.t:.{n}f}}}{{{self.gamma_m2:.{n}f}}}"
        )
        _numeric_equation_with_units: str = (
            prefix + rf"\frac{{{self.k_1:.{n}f} \cdot {self.alpha_b:.{n}f} \cdot {self.f_u:.{n}f} \ MPa \cdot "
            rf"{self.d:.{n}f} \ mm \cdot {self.t:.{n}f} \ mm}}{{{self.gamma_m2:.{n}f}}}"
        )
        return LatexFormula(
            return_symbol=r"F_{b,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )


class Table3Dot4TensionResistanceBolt(Formula):
    """Class representing the tension resistance of a bolt, from Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(
        self,
        f_ub: MPA,
        a_s: MM2,
        gamma_m2: DIMENSIONLESS,
        bolt_head: BoltHead = BoltHead.NORMAL,
    ) -> None:
        r"""[$F_{t,Rd}$] Design tension resistance of a bolt [$N$].

        EN 1993-1-8:2005 art.3.6.1 - Table 3.4

        Note 2 of the table adds that for a countersunk bolt the angle and depth of the countersinking
        must conform to the reference standards of 1.2.4, and that the resistance is to be adjusted
        otherwise. That adjustment is not printed, so it is not applied here.

        Parameters
        ----------
        f_ub : MPA
            [$f_{ub}$] Ultimate tensile strength of the bolt [$MPa$].
        a_s : MM2
            [$A_s$] Tensile stress area of the bolt [$mm^2$].
        gamma_m2 : DIMENSIONLESS
            [$\gamma_{M2}$] Partial factor for the resistance of the fastener [$-$].
        bolt_head : BoltHead
            Head shape of the bolt, which sets [$k_2$] to 0.63 for a countersunk head and to 0.9
            otherwise. Defaults to a normal head.
        """
        super().__init__()
        self.f_ub = f_ub
        self.a_s = a_s
        self.gamma_m2 = gamma_m2
        self.bolt_head = bolt_head

    @property
    def k_2(self) -> DIMENSIONLESS:
        r"""[$k_2$] Factor that Table 3.4 gives for this head shape [$-$]."""
        return self.bolt_head.k_2

    @staticmethod
    def _evaluate(
        f_ub: MPA,
        a_s: MM2,
        gamma_m2: DIMENSIONLESS,
        bolt_head: BoltHead = BoltHead.NORMAL,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ub=f_ub, a_s=a_s)
        raise_if_less_or_equal_to_zero(gamma_m2=gamma_m2)

        return bolt_head.k_2 * f_ub * a_s / gamma_m2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the tension resistance of a bolt."""
        _equation: str = r"\frac{k_2 \cdot f_{ub} \cdot A_s}{\gamma_{M2}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"k_2": f"{self.k_2:.{n}f}",
                r"f_{ub}": f"{self.f_ub:.{n}f}",
                r"A_s": f"{self.a_s:.{n}f}",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"k_2": f"{self.k_2:.{n}f}",
                r"f_{ub}": rf"{self.f_ub:.{n}f} \ MPa",
                r"A_s": rf"{self.a_s:.{n}f} \ mm^2",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"F_{t,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )


class Table3Dot4TensionResistanceRivet(Formula):
    """Class representing the tension resistance of a rivet, from Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(self, f_ur: MPA, a_0: MM2, gamma_m2: DIMENSIONLESS) -> None:
        r"""[$F_{t,Rd}$] Design tension resistance of a rivet [$N$].

        EN 1993-1-8:2005 art.3.6.1 - Table 3.4

        Art.3.6.1(14) asks riveted connections to be designed to transfer shear forces, and limits the
        design tensile force to this resistance where tension is present.

        Parameters
        ----------
        f_ur : MPA
            [$f_{ur}$] Ultimate tensile strength of the rivet. For steel grade S 235 art.3.6.1(15)
            allows 400 [$MPa$] to be taken [$MPa$].
        a_0 : MM2
            [$A_0$] Area of the hole of the rivet [$mm^2$].
        gamma_m2 : DIMENSIONLESS
            [$\gamma_{M2}$] Partial factor for the resistance of the fastener [$-$].
        """
        super().__init__()
        self.f_ur = f_ur
        self.a_0 = a_0
        self.gamma_m2 = gamma_m2

    @staticmethod
    def _evaluate(f_ur: MPA, a_0: MM2, gamma_m2: DIMENSIONLESS) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ur=f_ur, a_0=a_0)
        raise_if_less_or_equal_to_zero(gamma_m2=gamma_m2)

        return 0.6 * f_ur * a_0 / gamma_m2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the tension resistance of a rivet."""
        _equation: str = r"\frac{0.6 \cdot f_{ur} \cdot A_0}{\gamma_{M2}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"f_{ur}": f"{self.f_ur:.{n}f}",
                r"A_0": f"{self.a_0:.{n}f}",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"f_{ur}": rf"{self.f_ur:.{n}f} \ MPa",
                r"A_0": rf"{self.a_0:.{n}f} \ mm^2",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"F_{t,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )


class Table3Dot4PunchingShearResistance(Formula):
    """Class representing the punching shear resistance of the bolt head or the nut, from Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(self, d_m: MM, t_p: MM, f_u: MPA, gamma_m2: DIMENSIONLESS) -> None:
        r"""[$B_{p,Rd}$] Design punching shear resistance of the bolt head and the nut [$N$].

        EN 1993-1-8:2005 art.3.6.1 - Table 3.4

        The table asks for no punching shear check on a rivet, so this row covers bolts only.

        Parameters
        ----------
        d_m : MM
            [$d_m$] Mean of the across points and across flats dimensions of the bolt head or the nut,
            whichever is smaller, as defined in the list of symbols of the standard [$mm$].
        t_p : MM
            [$t_p$] Thickness of the plate under the bolt head or the nut. The standard writes
            [$t_p$] for the total thickness of the packings in art.3.6.1(12) as well, which is a
            different quantity [$mm$].
        f_u : MPA
            [$f_u$] Ultimate tensile strength of the plate under the bolt head or the nut [$MPa$].
        gamma_m2 : DIMENSIONLESS
            [$\gamma_{M2}$] Partial factor for the resistance of the fastener [$-$].
        """
        super().__init__()
        self.d_m = d_m
        self.t_p = t_p
        self.f_u = f_u
        self.gamma_m2 = gamma_m2

    @staticmethod
    def _evaluate(d_m: MM, t_p: MM, f_u: MPA, gamma_m2: DIMENSIONLESS) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d_m=d_m, t_p=t_p, f_u=f_u)
        raise_if_less_or_equal_to_zero(gamma_m2=gamma_m2)

        return 0.6 * math.pi * d_m * t_p * f_u / gamma_m2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the punching shear resistance."""
        _equation: str = r"\frac{0.6 \cdot \pi \cdot d_m \cdot t_p \cdot f_u}{\gamma_{M2}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_m": f"{self.d_m:.{n}f}",
                r"t_p": f"{self.t_p:.{n}f}",
                r"f_u": f"{self.f_u:.{n}f}",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_m": rf"{self.d_m:.{n}f} \ mm",
                r"t_p": rf"{self.t_p:.{n}f} \ mm",
                r"f_u": rf"{self.f_u:.{n}f} \ MPa",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"B_{p,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )


class Table3Dot4CombinedShearAndTension(ComparisonFormula):
    """Class representing the combined shear and tension check of Table 3.4."""

    label = "3.4"
    source_document = EN_1993_1_8_2005

    def __init__(self, f_v_ed: N, f_v_rd: N, f_t_ed: N, f_t_rd: N) -> None:
        r"""Check of a fastener under combined shear and tension.

        EN 1993-1-8:2005 art.3.6.1 - Table 3.4

        The cell of the table spans both columns, so the check covers rivets as well as bolts. The
        tension force to pass includes any force due to prying action, see art.3.11.

        Parameters
        ----------
        f_v_ed : N
            [$F_{v,Ed}$] Design shear force per fastener at the ultimate limit state [$N$].
        f_v_rd : N
            [$F_{v,Rd}$] Design shear resistance per fastener, see Table3Dot4ShearResistanceBolt and
            Table3Dot4ShearResistanceRivet [$N$].
        f_t_ed : N
            [$F_{t,Ed}$] Design tensile force per fastener at the ultimate limit state [$N$].
        f_t_rd : N
            [$F_{t,Rd}$] Design tension resistance per fastener, see Table3Dot4TensionResistanceBolt
            and Table3Dot4TensionResistanceRivet [$N$].
        """
        super().__init__()
        self.f_v_ed = f_v_ed
        self.f_v_rd = f_v_rd
        self.f_t_ed = f_t_ed
        self.f_t_rd = f_t_rd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """The table prints the interaction as an upper bound on the sum of the two ratios."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(f_v_ed: N, f_v_rd: N, f_t_ed: N, f_t_rd: N, *_args, **_kwargs) -> float:
        """Evaluates the left-hand side of the comparison, see __init__ for details."""
        raise_if_negative(f_v_ed=f_v_ed, f_t_ed=f_t_ed)
        raise_if_less_or_equal_to_zero(f_v_rd=f_v_rd, f_t_rd=f_t_rd)

        return f_v_ed / f_v_rd + f_t_ed / (1.4 * f_t_rd)

    @staticmethod
    def _evaluate_rhs(*_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the comparison, see __init__ for details."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the combined shear and tension check."""
        _equation: str = r"\frac{F_{v,Ed}}{F_{v,Rd}} + \frac{F_{t,Ed}}{1.4 \cdot F_{t,Rd}} \leq 1.0"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_{v,Ed}": f"{self.f_v_ed:.{n}f}",
                r"F_{v,Rd}": f"{self.f_v_rd:.{n}f}",
                r"F_{t,Ed}": f"{self.f_t_ed:.{n}f}",
                r"F_{t,Rd}": f"{self.f_t_rd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_{v,Ed}": rf"{self.f_v_ed:.{n}f} \ N",
                r"F_{v,Rd}": rf"{self.f_v_rd:.{n}f} \ N",
                r"F_{t,Ed}": rf"{self.f_t_ed:.{n}f} \ N",
                r"F_{t,Rd}": rf"{self.f_t_rd:.{n}f} \ N",
            },
            unique_symbol_check=False,
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
