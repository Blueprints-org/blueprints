"""Rectangular reinforced cross-section."""

# ruff: noqa: PLR0913
from typing import Literal

from matplotlib import pyplot as plt
from shapely import LineString, Point, Polygon

from blueprints.materials.concrete import ConcreteMaterial
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.covers import CoversRectangular
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.plotters.rectangular import RectangularCrossSectionPlotter
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import ReinforcementByQuantity
from blueprints.structural_sections.concrete.stirrups import StirrupConfiguration
from blueprints.structural_sections.cross_section_shapes import RectangularCrossSection
from blueprints.type_alias import DIMENSIONLESS, MM, RATIO


class RectangularReinforcedCrossSection(ReinforcedCrossSection):
    """Representation of a reinforced rectangular concrete cross-section like a beam.

    Parameters
    ----------
    width : MM
        The width of the rectangular cross-section [mm].
    height : MM
        The height of the rectangular cross-section [mm].
    concrete_material : ConcreteMaterial
        Material properties of the concrete.
    covers : CoversRectangular, optional
        The reinforcement covers for the cross-section [mm]. The default on all sides is 50 mm.
    """

    def __init__(
        self,
        width: MM,
        height: MM,
        concrete_material: ConcreteMaterial,
        covers: CoversRectangular = CoversRectangular(),
    ) -> None:
        """Initialize the rectangular reinforced concrete section."""
        super().__init__(
            cross_section=RectangularCrossSection(
                width=width,
                height=height,
            ),
            concrete_material=concrete_material,
        )
        self.width = width
        self.height = height
        self.covers = covers
        self.plotter = RectangularCrossSectionPlotter(cross_section=self)

    def add_stirrup_along_edges(
        self,
        diameter: MM,
        distance: MM,
        material: ReinforcementSteelMaterial,
        shear_check: bool = True,
        torsion_check: bool = True,
        mandrel_diameter_factor: DIMENSIONLESS | None = None,
        anchorage_length: MM = 0.0,
        relative_start_position: RATIO = 0.0,
        relative_end_position: RATIO = 1.0,
    ) -> StirrupConfiguration:
        """Adds a stirrup configuration along the edges of the cross-section taking the covers into account. The created configuration goes around
        the longitudinal rebars (if any).

        Use .add_stirrup_configuration() to add a stirrup configuration of any shape, size, and position (as long as it is inside the cross-section).


        Parameters
        ----------
        diameter: MM
            Diameter of the stirrups [mm].
        distance: MM
            Longitudinal distance between stirrups [mm].
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1
        shear_check: bool
            Take stirrup into account in shear check
        torsion_check: bool
            Take stirrup into account in torsion check
        mandrel_diameter_factor: DIMENSIONLESS
            Inner diameter of mandrel as multiple of stirrup diameter [-]
            (default: 4⌀ for ⌀<=16mm and 5⌀ for ⌀>16mm) Tabel 8.1Na NEN-EN 1992-1-1 Dutch National Annex.
        anchorage_length: MM
            Anchorage length [mm]
        relative_start_position: RATIO
            Relative position of the start of the stirrup configuration inside the cross-section (longitudinal direction). Value between 0 and 1.
            Default is 0 (start).
        relative_end_position: RATIO
            Relative position of the end of the stirrup configuration inside the cross-section (longitudinal direction). Value between 0 and 1.
            Default is 1 (end).


        Returns
        -------
        StirrupConfiguration
            Newly created stirrup configuration inside the cross-section.
        """
        # get the corners of the cross-section
        min_x, min_y, max_x, max_y = self.cross_section.geometry.bounds

        # create the corners of the stirrup configuration based on the covers present
        left_bottom_corner = Point(min_x + self.covers.left + (diameter / 2), min_y + self.covers.lower + (diameter / 2))
        left_top_corner = Point(min_x + self.covers.left + (diameter / 2), max_y - self.covers.upper - (diameter / 2))
        right_top_corner = Point(max_x - self.covers.right - (diameter / 2), max_y - self.covers.upper - (diameter / 2))
        right_bottom_corner = Point(max_x - self.covers.right - (diameter / 2), min_y + self.covers.lower + (diameter / 2))

        return self.add_stirrup_configuration(
            StirrupConfiguration(
                geometry=Polygon([left_bottom_corner, left_top_corner, right_top_corner, right_bottom_corner]),
                diameter=diameter,
                distance=distance,
                material=material,
                shear_check=shear_check,
                torsion_check=torsion_check,
                mandrel_diameter_factor=mandrel_diameter_factor,
                anchorage_length=anchorage_length,
                based_on_cover=True,
                relative_start_position=relative_start_position,
                relative_end_position=relative_end_position,
            )
        )

    def add_stirrup_in_center(
        self,
        width: MM,
        diameter: MM,
        distance: MM,
        material: ReinforcementSteelMaterial,
        shear_check: bool = True,
        torsion_check: bool = True,
        mandrel_diameter_factor: float | None = None,
        anchorage_length: MM = 0.0,
        relative_start_position: RATIO = 0.0,
        relative_end_position: RATIO = 1.0,
    ) -> StirrupConfiguration:
        """Add stirrups to the center of the reinforced cross-section based on a given width (ctc of the legs). The created configuration goes around
        the longitudinal rebars (if any).

        Use .add_stirrup_configuration() to add a stirrup configuration of any shape, size, and position (as long as it is inside the cross-section).

        Parameters
        ----------
        width: MM
            Total width of the stirrup taken from the center lines of the legs [mm].
        diameter: MM
            Diameter of the stirrups [mm].
        distance: MM
            Longitudinal distance between stirrups [mm].
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1
        shear_check: bool
            Take stirrup into account in shear check
        torsion_check: bool
            Take stirrup into account in torsion check
        mandrel_diameter_factor: DIMENSIONLESS
            Inner diameter of mandrel as multiple of stirrup diameter [-]
            (default: 4⌀ for ⌀<=16mm and 5⌀ for ⌀>16mm) Tabel 8.1Na NEN-EN 1992-1-1 Dutch National Annex.
        anchorage_length: MM
            Anchorage length [mm]
        relative_start_position: RATIO
            Relative position of the start of the stirrup configuration inside the cross-section (longitudinal direction). Value between 0 and 1.
            Default is 0 (start).
        relative_end_position: RATIO
            Relative position of the end of the stirrup configuration inside the cross-section (longitudinal direction). Value between 0 and 1.
            Default is 1 (end).

        Returns
        -------
        StirrupConfiguration
            Newly created stirrup configuration inside the cross-section.
        """
        # get the corners of the cross-section
        _, min_y, _, max_y = self.cross_section.geometry.bounds

        # create the corners of the stirrup configuration based on the covers present
        left_bottom_corner = Point(-width / 2, min_y + self.covers.lower + (diameter / 2))
        left_top_corner = Point(-width / 2, max_y - self.covers.upper - (diameter / 2))
        right_top_corner = Point(width / 2, max_y - self.covers.upper - (diameter / 2))
        right_bottom_corner = Point(width / 2, min_y + self.covers.lower + (diameter / 2))

        return self.add_stirrup_configuration(
            StirrupConfiguration(
                geometry=Polygon([left_bottom_corner, left_top_corner, right_top_corner, right_bottom_corner]),
                diameter=diameter,
                distance=distance,
                material=material,
                shear_check=shear_check,
                torsion_check=torsion_check,
                mandrel_diameter_factor=mandrel_diameter_factor,
                anchorage_length=anchorage_length,
                based_on_cover=True,
                relative_start_position=relative_start_position,
                relative_end_position=relative_end_position,
            )
        )

    def _get_reference_line(
        self,
        edge: Literal["upper", "right", "lower", "left"],
        diameter: MM,
        cover: MM | None = None,
        corner_offset: MM = 0.0,
    ) -> LineString:
        """Get the reference line for the given edge of the cross-section.

        Parameters
        ----------
        edge: Literal["upper", "right", "lower", "left"]
            Edge of the cross-section.
        diameter: MM
            Diameter of the rebars [mm].
        cover: MM, optional
            Cover of the rebars [mm]. If not provided, the default cover on the given edge of the cross-section is used.
        corner_offset: MM, optional
            The offset of the first and last rebars from the corners of the cross-section towards the center of the cross-section [mm]. If not
            provided, the rebars are to be placed at the corners taking into account the present covers and stirrups inside the cross-section.

        Returns
        -------
        LineString
            Reference line for the given edge of the cross-section.
        """
        # get cross-section corners
        min_x, min_y, max_x, max_y = self.cross_section.geometry.bounds

        # check if a custom cover is provided
        upper_cover = cover if cover is not None else self.covers.upper
        lower_cover = cover if cover is not None else self.covers.lower

        # check if there is a stirrup configuration present and adjust the cover
        max_stirrups_diameter = 0.0
        if self._stirrups:
            max_stirrups_diameter = max([stirrup.diameter for stirrup in self._stirrups])

        # define corner positions of a bar inside the cross-section
        upper_left = (
            min_x + self.covers.left + max_stirrups_diameter + corner_offset + diameter / 2,
            max_y - upper_cover - max_stirrups_diameter - diameter / 2,
        )
        upper_right = (
            max_x - self.covers.right - max_stirrups_diameter - corner_offset - diameter / 2,
            max_y - upper_cover - max_stirrups_diameter - diameter / 2,
        )
        lower_left = (
            min_x + self.covers.left + max_stirrups_diameter + corner_offset + diameter / 2,
            min_y + lower_cover + max_stirrups_diameter + diameter / 2,
        )
        lower_right = (
            max_x - self.covers.right - max_stirrups_diameter - corner_offset - diameter / 2,
            min_y + lower_cover + max_stirrups_diameter + diameter / 2,
        )

        match edge.lower():
            case "upper":
                start, end = upper_left, upper_right
            case "right":
                start, end = upper_right, lower_right
            case "lower":
                start, end = lower_left, lower_right
            case "left":
                start, end = upper_left, lower_left
            case _:  # pragma: no cover
                msg = f"Edge '{edge}' is not supported. Supported edges are 'upper', 'right', 'lower', and 'left'."
                raise ValueError(msg)

        return LineString([start, end])

    def add_longitudinal_reinforcement_by_quantity(
        self,
        n: int,
        diameter: MM,
        material: ReinforcementSteelMaterial,
        edge: Literal["upper", "right", "lower", "left"],
        cover: MM | None = None,
        corner_offset: MM = 0.0,
    ) -> None:
        """Add longitudinal reinforcement to the cross-section based on the quantity configuration of rebars and a given edge of the cross-section.

         for example: 5⌀12 on upper edge, 4⌀16 on lower edge, etc.

        Parameters
        ----------
        n: int
            Amount of longitudinal bars.
        diameter: MM
            Diameter of the rebars [mm].
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
        edge: Literal["upper", "right", "lower", "left"]
            Edge of the cross-section where the rebars are placed.
        cover: MM, optional
            Cover of the rebars [mm]. If not provided, the default cover on the given edge of the cross-section is used.
        corner_offset: MM, optional
            The offset of the first and last rebars from the corners of the cross-section towards the center of the cross-section [mm]. If not
            provided, the rebars are to be placed at the corners taking into account the present covers and stirrups inside the cross-section.
        """
        line = self._get_reference_line(
            edge=edge,
            diameter=diameter,
            cover=cover,
            corner_offset=corner_offset,
        )
        assert line
        return self.add_reinforcement_configuration(
            line=self._get_reference_line,
            configuration=ReinforcementByQuantity(
                diameter=diameter,
                material=material,
                n=n,
            ),
            edge=edge,
            cover=cover,
            corner_offset=corner_offset,
            diameter=diameter,
        )

    def plot(self, *args, **kwargs) -> plt.Figure:
        """Plot the cross-section. Making use of the standard plotter.

        If you want to use a custom plotter, use the .plotter attribute to plot the cross-section.

        Parameters
        ----------
        *args
            Additional arguments passed to the plotter.
        **kwargs
            Additional keyword arguments passed to the plotter.
        """
        return self.plotter.plot(*args, **kwargs)
