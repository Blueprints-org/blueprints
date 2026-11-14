"""Table 8.2 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import ClassVar

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.type_alias import DIMENSIONLESS


class SurfaceRoughness(StrEnum):
    """Roughness classes of a concrete interface according to FprEN 1992-1-1:2023 (E) art. 8.2.6(6).

    The five classes are the row headings of Table 8.2, so this list is closed: an interface that fits
    none of them has no coefficients in the standard.
    """

    VERY_SMOOTH = "very smooth"
    SMOOTH = "smooth"
    ROUGH = "rough"
    VERY_ROUGH = "very rough"
    KEYED = "keyed"

    @property
    def description(self) -> str:
        """The classification of this roughness class as printed in art. 8.2.6(6).

        Returns
        -------
        str
            The surface that the standard describes for this class.
        """
        return {
            SurfaceRoughness.VERY_SMOOTH: "a surface cast against steel, plastic or specially prepared wooden moulds",
            SurfaceRoughness.SMOOTH: (
                "a surface with less than 3 mm roughness (from peak to valley), e.g. a free surface left without further treatment after compacting"
            ),
            SurfaceRoughness.ROUGH: (
                "a surface with at least 3 mm roughness (from peak-to-valley, maximum 40 mm spacing), achieved by "
                "raking, exposing of aggregate or other methods according to Figure 8.15a)"
            ),
            SurfaceRoughness.VERY_ROUGH: (
                "a surface with at least 6 mm roughness (from peak-to-valley, maximum 40 mm spacing), achieved by "
                "raking, exposing of aggregate or other methods according to Figure 8.15a)"
            ),
            SurfaceRoughness.KEYED: "a surface with shear keys complying with Figure 8.15c)",
        }[self]


@dataclass(frozen=True)
class Table8Dot2CoefficientsSurfaceRoughness:
    r"""Implementation of Table 8.2 from FprEN 1992-1-1:2023.

    Coefficients depending on the roughness of the surface. The table serves two formulas: [$c_{v1}$] and
    [$\mu_v$] belong to Formula (8.76), and [$c_{v2}$], [$k_v$] and [$k_{dowel}$] to Formula (8.77). The
    keyed row prints a dash for the three coefficients of Formula (8.77), which is returned as ``None``.

    Footnote a of the table reads: when the interface is subjected to tensile stresses caused by external
    axial force in perpendicular direction, [$c_{v1} = 0$] and [$c_{v2} = 0$]. The footnote marker sits on
    every printed [$c_{v1}$] except the keyed one, so ``tension_perpendicular_to_interface`` leaves the
    keyed value of 0,37 untouched.

    Footnote b of the table reads: the factors for keyed interfaces shall be applied for the area of each
    key considering its concrete strength. That is a rule for the caller, not a value, so it is stated here
    and not applied to the coefficients.

    Parameters
    ----------
    surface_roughness : SurfaceRoughness
        The roughness of the interface according to art. 8.2.6(6).
    tension_perpendicular_to_interface : bool
        Whether the interface is subjected to tensile stresses caused by external axial force in
        perpendicular direction, which is the condition of footnote a. Defaults to False.

    Examples
    --------
    >>> table = Table8Dot2CoefficientsSurfaceRoughness(SurfaceRoughness.ROUGH)
    >>> table.c_v1
    0.15
    >>> table.mu_v
    0.7
    """

    surface_roughness: SurfaceRoughness
    tension_perpendicular_to_interface: bool = False
    label: str = field(init=False, default="Table 8.2")
    source_document: str = field(init=False, default=FPR_EN_1992_1_1_2023)

    # Per roughness class the printed coefficients in the order c_v1, mu_v, c_v2, k_v, k_dowel. A dash in
    # the table is held as None.
    _coefficients: ClassVar[dict[SurfaceRoughness, tuple[float, float, float | None, float | None, float | None]]] = {
        SurfaceRoughness.VERY_SMOOTH: (0.01, 0.5, 0.0, 0.0, 1.5),
        SurfaceRoughness.SMOOTH: (0.08, 0.6, 0.0, 0.5, 1.1),
        SurfaceRoughness.ROUGH: (0.15, 0.7, 0.08, 0.5, 0.9),
        SurfaceRoughness.VERY_ROUGH: (0.19, 0.9, 0.15, 0.5, 0.9),
        SurfaceRoughness.KEYED: (0.37, 0.9, None, None, None),
    }

    @property
    def _footnote_a_applies(self) -> bool:
        """Whether footnote a of the table has to be applied to this row.

        Returns
        -------
        bool
            True when the interface carries perpendicular tension and the row is one of the four that
            print the footnote marker.
        """
        return self.tension_perpendicular_to_interface and self.surface_roughness is not SurfaceRoughness.KEYED

    @property
    def c_v1(self) -> DIMENSIONLESS:
        r"""[$c_{v1}$] Coefficient of Formula (8.76) depending on the roughness of the interface [$-$].

        Returns
        -------
        DIMENSIONLESS
            The value printed in Table 8.2, or 0 when footnote a applies.
        """
        if self._footnote_a_applies:
            return 0.0
        return self._coefficients[self.surface_roughness][0]

    @property
    def mu_v(self) -> DIMENSIONLESS:
        r"""[$\mu_v$] Coefficient of Formula (8.76) depending on the roughness of the interface [$-$].

        Returns
        -------
        DIMENSIONLESS
            The value printed in Table 8.2.
        """
        return self._coefficients[self.surface_roughness][1]

    @property
    def c_v2(self) -> DIMENSIONLESS | None:
        r"""[$c_{v2}$] Coefficient of Formula (8.77) depending on the roughness of the interface [$-$].

        Returns
        -------
        DIMENSIONLESS | None
            The value printed in Table 8.2, 0 when footnote a applies, or None for a keyed interface,
            for which the table prints a dash.
        """
        printed = self._coefficients[self.surface_roughness][2]
        if printed is None:
            return None
        if self._footnote_a_applies:
            return 0.0
        return printed

    @property
    def k_v(self) -> DIMENSIONLESS | None:
        r"""[$k_v$] Coefficient of Formula (8.77) depending on the roughness of the interface [$-$].

        Returns
        -------
        DIMENSIONLESS | None
            The value printed in Table 8.2, or None for a keyed interface, for which the table prints a
            dash.
        """
        return self._coefficients[self.surface_roughness][3]

    @property
    def k_dowel(self) -> DIMENSIONLESS | None:
        r"""[$k_{dowel}$] Coefficient of Formula (8.77) depending on the roughness of the interface [$-$].

        Returns
        -------
        DIMENSIONLESS | None
            The value printed in Table 8.2, or None for a keyed interface, for which the table prints a
            dash.
        """
        return self._coefficients[self.surface_roughness][4]
