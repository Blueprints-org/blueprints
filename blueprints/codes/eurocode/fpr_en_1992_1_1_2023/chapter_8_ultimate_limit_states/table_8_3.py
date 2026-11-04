"""Table 8.3 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import ClassVar

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class PunchingSupportType(StrEnum):
    """Types of support of Table 8.3 of FprEN 1992-1-1:2023 (E).

    The five types are the row headings of Table 8.3, so this list is closed: a support that fits none of
    them has no coefficient in the standard.
    """

    INTERNAL_COLUMN = "internal columns"
    EDGE_COLUMN = "edge columns"
    CORNER_COLUMN = "corner columns"
    END_OF_WALL = "ends of walls"
    CORNER_OF_WALL = "corners of walls"

    @property
    def has_refined_value(self) -> bool:
        """Whether Table 8.3 gives a refined coefficient for this type of support.

        The rows for ends of walls and corners of walls print a single cell spanning both the approximated and
        the refined column, so those two supports have one value and no refined route.

        Returns
        -------
        bool
            True for the three column types, False for the two wall types.
        """
        return self in (
            PunchingSupportType.INTERNAL_COLUMN,
            PunchingSupportType.EDGE_COLUMN,
            PunchingSupportType.CORNER_COLUMN,
        )


class SubTable8Dot3RefinedCoefficientShearForceConcentration(Formula):
    r"""Class representing the refined coefficient [$\beta_e$] of Table 8.3 of FprEN 1992-1-1:2023.

    The table prints the expression once for internal, edge and corner columns; only the eccentricity
    [$e_b$] that goes into it is defined per type of support. It is printed as an expression with a lower
    bound, [$1 + 1,1 e_b / b_b \geq 1,05$], and implemented as a maximum against that bound.
    """

    label = "Table 8.3"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        e_b: MM,
        b_b: MM,
    ) -> None:
        r"""[$\beta_e$] Refined coefficient accounting for concentrations of the shear forces [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.2(6) - Table 8.3

        Parameters
        ----------
        e_b : MM
            [$e_b$] Eccentricity of the line of action of the support forces with respect to the centroid of
            the control perimeter, combined from [$e_{b,x}$] and [$e_{b,y}$] according to the type of support,
            see footnote a of Table 8.3 [$mm$].
        b_b : MM
            [$b_b$] Geometric mean of the minimum and maximum overall widths of the control perimeter, see
            footnote a of Table 8.3 and Figure 8.21 b) [$mm$].
        """
        super().__init__()
        self.e_b = e_b
        self.b_b = b_b

    @staticmethod
    def _evaluate(
        e_b: MM,
        b_b: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(e_b=e_b)
        raise_if_less_or_equal_to_zero(b_b=b_b)

        return max(1 + 1.1 * e_b / b_b, 1.05)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the refined coefficient of Table 8.3."""
        _equation: str = r"\max\left(1 + 1.1 \cdot \frac{e_b}{b_b}, 1.05\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"e_b": f"{self.e_b:.{n}f}",
                r"b_b": f"{self.b_b:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"e_b": rf"{self.e_b:.{n}f} \ mm",
                r"b_b": rf"{self.b_b:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\beta_e",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )


@dataclass(frozen=True)
class Table8Dot3CoefficientsShearForceConcentration:
    r"""Implementation of Table 8.3 from FprEN 1992-1-1:2023.

    Coefficients [$\beta_e$] accounting for concentrations of the shear forces, which Formula (8.92) needs.
    The table offers two routes per type of support. The approximated route is a single printed number. The
    refined route is [$1 + 1,1 e_b / b_b \geq 1,05$], the same expression for all three column types, with an
    eccentricity [$e_b$] whose definition differs per type.

    8.4.2(6) allows the approximated values for internal, edge and corner columns to be used only if all four
    conditions listed there are fulfilled, and states that the refined values may be applied in those cases as
    well for a more refined calculation. Choosing between the two routes is therefore a decision of the caller,
    which is why this class exposes both instead of one coefficient.

    The rows for ends of walls and corners of walls print one cell spanning both columns of the table, so
    those two supports have a single value and no refined route. The four conditions of 8.4.2(6) name only
    columns, so they do not gate the wall values either.

    Footnote a of the table reads: [$e_{b,x}$], [$e_{b,y}$] are the eccentricities of the line of action of the
    support forces with respect to the centroid of the control perimeter. The line of action should be
    determined accounting for the axial force and the moments in the two directions transferred by the slab to
    the support, including the internal forces in a column over the slab if present.

    **The two directions are not interchangeable for an edge column.** Figure 8.21 a) draws the slab edge as a
    straight line with [$e_{b,x}$] measured across it and [$e_{b,y}$] measured along it, so x is the direction
    perpendicular to the slab edge and y the direction parallel to it. The edge column row halves the
    perpendicular component, so passing the two the other way round gives a different coefficient without any
    error being raised: for [$e_{b,x} = 30$] mm and [$e_{b,y} = 40$] mm it is 55 mm as printed against 65 mm
    swapped. For internal columns the definition is a root of squares and for corner columns it is symmetric in
    the two, so there the orientation makes no difference.

    Footnote a also reads: [$b_b$] is the geometric mean of the minimum and maximum overall widths of the
    control perimeter, see Figure 8.21 b). Where the length of straight segments of the control perimeter is
    limited to [$3 d_v$] according to 8.4.2(3), the overall width of the control perimeter should not be
    reduced. That is a rule for how the caller measures [$b_{b,min}$] and [$b_{b,max}$], not a value, so it is
    stated here and not applied to them.

    Parameters
    ----------
    support_type : PunchingSupportType
        The type of support, being the row of Table 8.3.
    e_b_x : MM | None
        [$e_{b,x}$] Eccentricity perpendicular to the slab edge, being the x-direction of Figure 8.21 a). Its
        sign does not matter, since every definition of [$e_b$] takes either its square or its absolute value.
        Only needed for the refined route. Defaults to None [$mm$].
    e_b_y : MM | None
        [$e_{b,y}$] Eccentricity parallel to the slab edge, being the y-direction of Figure 8.21 a). Only
        needed for the refined route. Defaults to None [$mm$].
    b_b_min : MM | None
        [$b_{b,min}$] Minimum overall width of the control perimeter according to Figure 8.21 b). Only needed
        for the refined route. Defaults to None [$mm$].
    b_b_max : MM | None
        [$b_{b,max}$] Maximum overall width of the control perimeter according to Figure 8.21 b). Only needed
        for the refined route. Defaults to None [$mm$].

    Examples
    --------
    >>> table = Table8Dot3CoefficientsShearForceConcentration(PunchingSupportType.INTERNAL_COLUMN)
    >>> table.beta_e_approximated
    1.15
    """

    support_type: PunchingSupportType
    e_b_x: MM | None = None
    e_b_y: MM | None = None
    b_b_min: MM | None = None
    b_b_max: MM | None = None
    label: str = field(init=False, default="Table 8.3")
    source_document: str = field(init=False, default=FPR_EN_1992_1_1_2023)

    # The approximated value printed per type of support. For the two wall types the printed cell spans both
    # columns of the table, so this is the only value the standard gives for them.
    _approximated: ClassVar[dict[PunchingSupportType, DIMENSIONLESS]] = {
        PunchingSupportType.INTERNAL_COLUMN: 1.15,
        PunchingSupportType.EDGE_COLUMN: 1.4,
        PunchingSupportType.CORNER_COLUMN: 1.5,
        PunchingSupportType.END_OF_WALL: 1.4,
        PunchingSupportType.CORNER_OF_WALL: 1.2,
    }

    @property
    def beta_e_approximated(self) -> DIMENSIONLESS:
        r"""[$\beta_e$] Approximated coefficient accounting for concentrations of the shear forces [$-$].

        Returns
        -------
        DIMENSIONLESS
            The value printed in the approximated column of Table 8.3. For ends of walls and corners of walls
            the printed cell spans both columns, so the same value is the only one the standard gives.
        """
        return self._approximated[self.support_type]

    @property
    def e_b(self) -> MM:
        r"""[$e_b$] Eccentricity of the line of action of the support forces, combined according to the type of
        support as printed in the refined column of Table 8.3.

        Returns
        -------
        MM
            [$\sqrt{e_{b,x}^2 + e_{b,y}^2}$] for internal columns, [$0,5 |e_{b,x}| + |e_{b,y}|$] for edge
            columns and [$0,27 \left(|e_{b,x}| + |e_{b,y}|\right)$] for corner columns. The edge column
            definition halves the component perpendicular to the slab edge only, so the two eccentricities are
            not interchangeable there, see the class docstring [$mm$].

        Raises
        ------
        ValueError
            If the type of support has no refined route, or if an eccentricity was not given.
        """
        self._raise_if_refined_route_unavailable()
        if self.e_b_x is None or self.e_b_y is None:
            raise ValueError("Both e_b_x and e_b_y are needed for the refined coefficient of Table 8.3.")

        match self.support_type:
            case PunchingSupportType.INTERNAL_COLUMN:
                return float(np.sqrt(self.e_b_x**2 + self.e_b_y**2))
            case PunchingSupportType.EDGE_COLUMN:
                return 0.5 * abs(self.e_b_x) + abs(self.e_b_y)
            case _:
                return 0.27 * (abs(self.e_b_x) + abs(self.e_b_y))

    @property
    def b_b(self) -> MM:
        r"""[$b_b$] Geometric mean of the minimum and maximum overall widths of the control perimeter,
        [$\sqrt{b_{b,min} \cdot b_{b,max}}$], according to footnote a of Table 8.3.

        Returns
        -------
        MM
            The geometric mean of the two widths [$mm$].

        Raises
        ------
        ValueError
            If the type of support has no refined route, or if a width was not given.
        LessOrEqualToZeroError
            If one of the widths is zero or negative.
        """
        self._raise_if_refined_route_unavailable()
        if self.b_b_min is None or self.b_b_max is None:
            raise ValueError("Both b_b_min and b_b_max are needed for the refined coefficient of Table 8.3.")
        raise_if_less_or_equal_to_zero(b_b_min=self.b_b_min, b_b_max=self.b_b_max)

        return float(np.sqrt(self.b_b_min * self.b_b_max))

    @property
    def beta_e_refined(self) -> SubTable8Dot3RefinedCoefficientShearForceConcentration:
        r"""[$\beta_e$] Refined coefficient accounting for concentrations of the shear forces [$-$].

        Returns
        -------
        SubTable8Dot3RefinedCoefficientShearForceConcentration
            The refined coefficient. It is a float, so it can be used wherever the approximated value can, and
            it carries a ``latex`` method for the expression printed in the table.

        Raises
        ------
        ValueError
            If the type of support has no refined route, or if one of the four inputs was not given.
        """
        return SubTable8Dot3RefinedCoefficientShearForceConcentration(e_b=self.e_b, b_b=self.b_b)

    def _raise_if_refined_route_unavailable(self) -> None:
        """Guards the refined route against the two types of support for which the table prints no expression.

        Raises
        ------
        ValueError
            If the type of support is an end or a corner of a wall.
        """
        if not self.support_type.has_refined_value:
            raise ValueError(
                f"Table 8.3 gives no refined coefficient for {self.support_type.value}, only the value of "
                f"{self.beta_e_approximated} that spans both columns of the table."
            )
