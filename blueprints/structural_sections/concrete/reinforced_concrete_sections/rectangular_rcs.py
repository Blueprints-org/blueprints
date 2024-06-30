"""Reinforced concrete sections module. WORK IN PROGRESS !. NOT READY FOR USE OR REVIEW."""
# ruff: noqa: PLR0913, SLF001, PLR0911, TRY004, C901, PLR0912, PLR0915, PERF203, ARG002

from matplotlib import patches as mplpatches
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from shapely import Point

from blueprints.geometry.line import Line, Reference
from blueprints.materials.concrete import ConcreteMaterial
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import REBAR_COLOR, Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.covers import CoversRectangular
from blueprints.structural_sections.concrete.reinforced_concrete_sections.cross_sections_shapes import (
    RCS_CROSS_SECTION_COLOR,
    Edges,
    RectangularCrossSection,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import (
    ReinforcementByDistance,
    ReinforcementByQuantity,
)
from blueprints.structural_sections.concrete.stirrups import STIRRUP_COLOR, Stirrup
from blueprints.type_alias import DIMENSIONLESS, MM


class RectangularReinforcedCrossSection(ReinforcedCrossSection):
    """Representation of a reinforced rectangular concrete cross-section like a beam.

    Parameters
    ----------
    width: MM
        Width of the reinforced cross-section [mm]
    height: MM
        Height of the reinforced cross-section [mm]
    covers: blueprints.structural_sections.concrete.reinforced_concrete_sections.covers.CoversRectangular
        Covers of the cross-section.
    concrete_material: ConcreteMaterial
        Representation of the properties of concrete suitable for use with NEN-EN 1992-1-1
    steel_material : ReinforcementSteelMaterial
        Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1
    name : str
        Name of the reinforced cross-section.
    """

    def __init__(
        self,
        width: MM,
        height: MM,
        covers: CoversRectangular,
        concrete_material: ConcreteMaterial,
        steel_material: ReinforcementSteelMaterial,
        name: str | None = None,
    ) -> None:
        super().__init__(
            cross_section=RectangularCrossSection(width=width, height=height),
            concrete_material=concrete_material,
        )
        self.steel_material = steel_material
        self.width = width
        self.height = height
        self.name = (
            name
            if name
            else f"RectangularReinforcedCrossSection {self.width}x{self.height}mm|{self.concrete_material.name}|{self.steel_material.name}"
        )
        self.covers = covers
        self.plotter = RectangularCrossSectionPlotter(self)

    def set_covers(
        self,
        upper: MM | None = None,
        right: MM | None = None,
        lower: MM | None = None,
        left: MM | None = None,
    ) -> None:
        """Method to change covers in the cross-section.

        Parameters
        ----------
        upper: MM | None, default None
            New reinforcement coverage for the upper side of the cross-section [mm]
        right: MM | None, default None
            New reinforcement coverage for the right side of the cross-section [mm]
        lower: MM | None, default None
            New reinforcement coverage for the lower side of the cross-section [mm]
        left: MM | None, default None
            New reinforcement coverage for the left side of the cross-section [mm]
        """
        self.covers.upper = upper or self.covers.upper
        self.covers.right = right or self.covers.right
        self.covers.lower = lower or self.covers.lower
        self.covers.left = left or self.covers.left

    def add_stirrups(
        self,
        coordinates: list[Point],
        diameter: MM,
        distance: MM,
        material: ReinforcementSteelMaterial,
        shear_check: bool = True,
        torsion_check: bool = True,
        mandrel_diameter_factor: DIMENSIONLESS | None = None,
        anchorage_length: MM = 0.0,
        based_on_cover: bool = False,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
    ) -> Stirrup:
        """Add a single stirrup to the reinforced cross-section based on given coordinates.

        Parameters
        ----------
        coordinates: list[Point]
            list of (x,y) coordinates to describe the stirrup relative to the centroid point of the cross-section. [mm]
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
        based_on_cover: bool
            Default is False. This helps to categorise stirrups that are created based on the covers present
            in the cross-section.
        relative_start_position: DIMENSIONLESS
            Relative position of the start of the rebar in the x-direction of the host cross-section [-]
        relative_end_position: DIMENSIONLESS
            Relative position of the end of the rebar in the x-direction of the host cross-section [-]

        Returns
        -------
        Stirrup
            Newly created Stirrup
        """
        # initiate the stirrup
        stirrup = Stirrup(
            coordinates=coordinates,
            diameter=diameter,
            distance=distance,
            material=material,
            shear_check=shear_check,
            torsion_check=torsion_check,
            mandrel_diameter_factor=mandrel_diameter_factor,
            anchorage_length=anchorage_length,
            based_on_cover=based_on_cover,
            relative_start_position=relative_start_position,
            relative_end_position=relative_end_position,
        )

        # add the stirrup to the list of stirrups
        self.stirrups.append(stirrup)

        return stirrup

    def add_stirrup_along_edges(
        self,
        diameter: MM,
        distance: MM,
        material: ReinforcementSteelMaterial,
        shear_check: bool = True,
        torsion_check: bool = True,
        mandrel_diameter_factor: float | None = None,
        anchorage_length: MM = 0.0,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
    ) -> Stirrup:
        """Add stirrups to the reinforced cross-section based on the present covers.

        (No coordinates are needed for the creation of this stirrup.)

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
        relative_start_position: DIMENSIONLESS
            Relative position of the start of the rebar in the x-direction of the host cross-section [-]
        relative_end_position: DIMENSIONLESS
            Relative position of the end of the rebar in the x-direction of the host cross-section [-]

        Returns
        -------
        Stirrup
            Newly created Stirrup
        """
        _max_x = max(x for x, _ in self.cross_section.vertices)
        _min_x = min(x for x, _ in self.cross_section.vertices)
        _min_y = min(y for _, y in self.cross_section.vertices)
        _max_y = max(y for _, y in self.cross_section.vertices)

        _left_bottom_corner = Point(_min_x + self.covers.left + (diameter / 2), _min_y + self.covers.lower + (diameter / 2))
        _left_top_corner = Point(_min_x + self.covers.left + (diameter / 2), _max_y - self.covers.upper - (diameter / 2))
        _right_top_corner = Point(_max_x - self.covers.right - (diameter / 2), _max_y - self.covers.upper - (diameter / 2))
        _right_bottom_corner = Point(_max_x - self.covers.right - (diameter / 2), _min_y + self.covers.lower + (diameter / 2))

        return self.add_stirrups(
            coordinates=[_left_top_corner, _left_bottom_corner, _right_bottom_corner, _right_top_corner],
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
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
    ) -> Stirrup:
        """Add stirrups to the center of the reinforced cross-section based on a given width (ctc of the legs).

        (No coordinates are needed for the creation of this stirrup.)

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
        relative_start_position: DIMENSIONLESS
            Relative position of the start of the rebar in the x-direction of the host cross-section [-]
        relative_end_position: DIMENSIONLESS
            Relative position of the end of the rebar in the x-direction of the host cross-section [-]

        Returns
        -------
        Stirrup
            Newly created Stirrup
        """
        _min_y = min(y for _, y in self.cross_section.vertices)
        _max_y = max(y for _, y in self.cross_section.vertices)

        _left_bottom_corner = Point(-width / 2, _min_y + self.covers.lower + (diameter / 2))
        _left_top_corner = Point(-width / 2, _max_y - self.covers.upper - (diameter / 2))
        _right_top_corner = Point(width / 2, _max_y - self.covers.upper - (diameter / 2))
        _right_bottom_corner = Point(width / 2, _min_y + self.covers.lower + (diameter / 2))

        return self.add_stirrups(
            coordinates=[_left_top_corner, _left_bottom_corner, _right_bottom_corner, _right_top_corner],
            diameter=diameter,
            distance=distance,
            material=material,
            shear_check=shear_check,
            torsion_check=torsion_check,
            mandrel_diameter_factor=mandrel_diameter_factor,
            anchorage_length=anchorage_length,
            based_on_cover=False,
            relative_start_position=relative_start_position,
            relative_end_position=relative_end_position,
        )

    def _get_reference_line_by_edge(
        self,
        edge: Edges,
        diameter: float,
        different_cover: float = 0.0,
        cover_as_defined_in_cross_section: bool = True,
    ) -> Line:
        """Get a reference line for a reinforcement layer taking into account to desired edge,
         present covers and presence of stirrups in the cross-section.

        Parameters
        ----------
        edge: Edges
            Desired edge of the cross-section. (Edges.ALL_EDGES is not supported)
        diameter: float
            Diameter of the rebars in the layer [mm]
        different_cover: float
            Use to introduce a different cover of the reinforcement layer [mm]
        cover_as_defined_in_cross_section: bool
            Use the previously defined cover in the cross-section

        Returns
        -------
        Line
        """
        if edge == Edges.ALL_EDGES:
            msg = "This operation is currently not supported for Edges.ALL_EDGES"
            raise NotImplementedError(msg)
        if diameter < 1:
            msg = "Diameter must be greater than 1"
            raise ValueError(msg)

        # get the vertices of the shape
        lower_left, lower_right, upper_right, upper_left, _ = self.cross_section.vertices

        # start of the reference line is a half diameter from the reinforcement cover eventually increased by the diameter of the biggest stirrup
        half_diameter = diameter / 2
        if self.stirrups:
            half_diameter += max(stirrup.diameter for stirrup in self.stirrups)

        # define the start and end point of the reference line for the desired reinforcement configuration (default = upper side)
        reinforcement_cover = self.covers.upper if cover_as_defined_in_cross_section else max(different_cover, 0.0)
        match edge:
            case Edges.UPPER_SIDE:
                x1, y1 = upper_left
                x2, y2 = upper_right
                first_point = Point(x1 + self.covers.left + half_diameter, y1 - reinforcement_cover - half_diameter, 0)
                second_point = Point(x2 - self.covers.right - half_diameter, y2 - reinforcement_cover - half_diameter, 0)
            case Edges.RIGHT_SIDE:
                reinforcement_cover = self.covers.right if cover_as_defined_in_cross_section else max(different_cover, 0.0)
                x1, y1 = upper_right
                x2, y2 = lower_right
                first_point = Point(x1 - reinforcement_cover - half_diameter, y1 - self.covers.upper - half_diameter, 0)
                second_point = Point(x2 - reinforcement_cover - half_diameter, y2 + self.covers.lower + half_diameter, 0)
            case Edges.LOWER_SIDE:
                reinforcement_cover = self.covers.lower if cover_as_defined_in_cross_section else max(different_cover, 0.0)
                x1, y1 = lower_right
                x2, y2 = lower_left
                first_point = Point(x1 - self.covers.right - half_diameter, y1 + reinforcement_cover + half_diameter, 0)
                second_point = Point(x2 + self.covers.left + half_diameter, y2 + reinforcement_cover + half_diameter, 0)
            case Edges.LEFT_SIDE:
                reinforcement_cover = self.covers.left if cover_as_defined_in_cross_section else max(different_cover, 0.0)
                x1, y1 = lower_left
                x2, y2 = upper_left
                first_point = Point(x1 + reinforcement_cover + half_diameter, y1 + self.covers.lower + half_diameter, 0)
                second_point = Point(x2 + reinforcement_cover + half_diameter, y2 - self.covers.upper - half_diameter, 0)
            case _:
                msg = "This operation is currently not supported for Edges.ALL_EDGES"
                raise NotImplementedError(msg)

        return Line(start_point=first_point, end_point=second_point)

    def _get_rebars_from_reinforcement_by_quantity(self, configuration: ReinforcementByQuantity) -> list[Rebar]:
        """Gets a list of the rebars for the desired reinforcement layer configuration taking into account the properties of the cross-section.

        Parameters
        ----------
        configuration: ReinforcementByQuantity
            Reinforcement layer by quantity (example= 5⌀20).

        Returns
        -------
        list[Rebar]
        """
        reference_line = self._get_reference_line_by_edge(
            edge=configuration.edge,
            diameter=configuration.diameter,
            different_cover=configuration.cover,
            cover_as_defined_in_cross_section=configuration.cover_as_defined_in_cross_section,
        )
        reference_line.extend(extra_length=configuration.offset, direction=Reference.START)
        reference_line.extend(extra_length=configuration.offset, direction=Reference.END)
        if configuration.n == 1:
            mid_point = reference_line.midpoint
            return [Rebar(diameter=configuration.diameter, material=configuration.material, x=mid_point.x, y=mid_point.y)]
        return [
            Rebar(diameter=configuration.diameter, x=point.x, y=point.y, material=configuration.material)
            for point in reference_line.get_evenly_spaced_points(n=configuration.n)
        ]

    def _get_rebars_from_reinforcement_by_distance(self, configuration: ReinforcementByDistance) -> list[Rebar]:
        """Raises not implemented error."""
        msg = (
            "Reinforcement configurations by distance (ReinforcementByDistance) are not supported for "
            "RectangularReinforcedCrossSection, Use a OneWaySlabReinforcedCrossSection instead"
        )
        raise NotImplementedError(msg)

    def plot(
        self,
        figsize: tuple[float, float] = (15.0, 8.0),
        title: str | None = None,
        font_size_title: float = 18.0,
        font_size_legend: float = 10.0,
        include_legend: bool = True,
        font_size_dimension: float = 12.0,
        custom_text_legend: str | None = None,
        custom_text_width: str | None = None,
        custom_text_height: str | None = None,
        offset_line_width: float = 1.25,
        offset_line_height: float = 1.2,
        show: bool = False,
        axes_i: int = 0,
    ) -> plt.Figure:
        """Get matplotlib figure plot of the reinforced cross-section including longitudinal_rebars and stirrups.

        Parameters
        ----------
        figsize: tuple[float, float]
            Size of the plot window.
        title: str
            Title of the plot.
        font_size_title: float
            Font size of the title.
        font_size_legend: float
            Font size of the legend.
        include_legend: bool
            Include legend in the plot.
        font_size_dimension: float
            Font size of the dimensions.
        custom_text_legend: str
            Custom text for the legend.
        custom_text_width: str
            Custom text for the width dimension. Replaces the width of the cross-section with the custom text.
        custom_text_height: str
            Custom text for the height dimension. Replaces the height of the cross-section with the custom text.
        offset_line_width: float
            Offset of the width line.
        offset_line_height: float
            Offset of the height line.
        show: bool
            Show the plot.
        axes_i: int
            Index of the axes to plot on. Default is 0.

        Returns
        -------
        plt.Figure
        """
        return self.plotter.plot(
            figsize=figsize,
            title=title,
            font_size_title=font_size_title,
            font_size_legend=font_size_legend,
            include_legend=include_legend,
            font_size_dimension=font_size_dimension,
            custom_text_legend=custom_text_legend,
            custom_text_width=custom_text_width,
            custom_text_height=custom_text_height,
            offset_line_width=offset_line_width,
            offset_line_height=offset_line_height,
            show=show,
            axes_i=axes_i,
        )


class RectangularCrossSectionPlotter:
    """Plotter for Reinforced Rectangular Cross-Sections (RRCS)."""

    def __init__(
        self,
        cross_section: RectangularReinforcedCrossSection,
    ) -> None:
        """Initialize the RRCSPlotter.

        Parameters
        ----------
        cross_section: RectangularReinforcedCrossSection
            Reinforced cross-section to plot.
        """
        self.cross_section = cross_section
        self.fig: plt.Figure | None = None
        self.axes: list[Axes] = []

    def plot(
        self,
        figsize: tuple[float, float] = (15.0, 8.0),
        title: str | None = None,
        font_size_title: float = 18.0,
        font_size_legend: float = 10.0,
        include_legend: bool = True,
        font_size_dimension: float = 12.0,
        custom_text_legend: str | None = None,
        custom_text_width: str | None = None,
        custom_text_height: str | None = None,
        offset_line_width: float = 1.25,
        offset_line_height: float = 1.2,
        show: bool = False,
        axes_i: int = 0,
    ) -> plt.Figure:
        """Plots the cross-section.

        Parameters
        ----------
        figsize: tuple[float, float]
            Size of the plot window.
        title: str
            Title of the plot.
        font_size_title: float
            Font size of the title.
        font_size_legend: float
            Font size of the legend.
        include_legend: bool
            Include legend in the plot.
        font_size_dimension: float
            Font size of the dimensions.
        custom_text_legend: str
            Custom text for the legend.
        custom_text_width: str
            Custom text for the width dimension. Replaces the width of the cross-section with the custom text.
        custom_text_height: str
            Custom text for the height dimension. Replaces the height of the cross-section with the custom text.
        offset_line_width: float
            Offset of the width line.
        offset_line_height: float
            Offset of the height line.
        show: bool
            Show the plot.
        axes_i: int
            Index of the axes to plot on. Default is 0.

        Returns
        -------
        plt.Figure
            Matplotlib figure.
        """
        self._start_plot(figsize=figsize)
        self._add_rectangle(axes_i=axes_i)
        self._add_center_lines(axes_i=axes_i)
        self._add_dimension_lines(
            axes_i=axes_i,
            font_size_dimension=font_size_dimension,
            custom_text_height=custom_text_height,
            custom_text_width=custom_text_width,
            offset_line_width=offset_line_width,
            offset_line_height=offset_line_height,
        )
        self._add_stirrups(axes_i=axes_i)
        self._add_longitudinal_rebars(axes_i=axes_i)

        # set limits and title
        self.axes[axes_i].axis("off")
        self.axes[axes_i].axis("equal")
        self.axes[axes_i].set_title(
            label=title or "",
            fontdict={"fontsize": font_size_title},
        )

        if include_legend:
            self._add_legend(
                axes_i=axes_i,
                font_size_legend=font_size_legend,
                custom_legend_text=custom_text_legend,
            )
        if show:
            plt.show()
        assert self.fig is not None
        return self.fig

    def _start_plot(self, figsize: tuple[float, float] = (15.0, 8.0)) -> tuple[float, float]:
        """Starts the plot by initialising a matplotlib plot window of the given size.

        Parameters
        ----------
        figsize: tuple[float, float]
            Size of the plot window.

        """
        plt.close("all")
        self.fig = plt.figure(figsize=figsize)
        self.axes = [self.fig.add_subplot(111)]
        return self.fig.get_figwidth(), self.fig.get_figheight()

    def _add_rectangle(
        self,
        edge_color: str = "black",
        axes_i: int = 0,
    ) -> mplpatches.Rectangle:
        """Adds a rectangle to the plot.

        Parameters
        ----------
        axes_i: int
            Index of the axes to plot on. Default is 0.
        """
        patch = mplpatches.Rectangle(
            xy=(-self.cross_section.width / 2, -self.cross_section.height / 2),
            width=self.cross_section.width,
            height=self.cross_section.height,
            edgecolor=edge_color,
            facecolor=RCS_CROSS_SECTION_COLOR,
            fill=True,
            lw=1,
        )
        self.axes[axes_i].add_patch(patch)
        return patch

    def _add_center_lines(self, axes_i: int = 0, style: dict[str, float | str] | None = None) -> None:
        """Adds center lines to the plot.

        Parameters
        ----------
        axes_i: int
            Index of the axes to plot on. Default is 0.
        style: dict[str, float]
            Style of the center lines. Check matplotlib documentation for more information (Annotation-arrowprops).
        """
        center_line_style = style or {"arrowstyle": "-", "linewidth": 0.8, "color": "gray", "linestyle": "dashdot"}
        offset_center_line = 1.05
        self.axes[axes_i].annotate(
            text="z",
            xy=(0, (-self.cross_section.height / 2) * offset_center_line),
            xytext=(0, (self.cross_section.height / 2) * offset_center_line),
            arrowprops=center_line_style,
            verticalalignment="bottom",
            horizontalalignment="center",
        )
        self.axes[axes_i].annotate(
            text="y",
            xy=((self.cross_section.width / 2) * offset_center_line, 0),
            xytext=(-(self.cross_section.width / 2) * offset_center_line, 0),
            arrowprops=center_line_style,
            verticalalignment="center",
            horizontalalignment="right",
        )

    def _add_dimension_lines(
        self,
        axes_i: int = 0,
        style: mplpatches.ArrowStyle | None = None,
        offset_line_width: float = 1.25,
        offset_line_height: float = 1.2,
        custom_text_width: str | None = None,
        custom_text_height: str | None = None,
        font_size_dimension: float = 12.0,
    ) -> None:
        """Adds dimension lines to the plot.

        Parameters
        ----------
        axes_i: int
            Index of the axes to plot on. Default is 0.
        style: dict[str, float]
            Style of the dimension lines. Check matplotlib documentation for more information (Annotation-arrowprops).
        offset_line_width: float
            Offset of the width line.
        offset_line_height: float
            Offset of the height line.
        custom_text_width: str
            Custom text for the width dimension. Replaces the width of the cross-section with the custom text.
        custom_text_height: str
            Custom text for the height dimension. Replaces the height of the cross-section with the custom text.
        font_size_dimension: float
            Font size of the dimensions.
        """
        # add the width dimension line
        diameter_line_style = {
            "arrowstyle": style or mplpatches.ArrowStyle(stylename="<->", head_length=0.5, head_width=0.5),
        }
        offset_width = (-self.cross_section.height / 2) * offset_line_width
        self.axes[axes_i].annotate(
            text="",
            xy=(-self.cross_section.width / 2, offset_width),
            xytext=(self.cross_section.width / 2, offset_width),
            verticalalignment="center",
            horizontalalignment="center",
            arrowprops=diameter_line_style,
            annotation_clip=False,
        )
        self.axes[axes_i].text(
            s=custom_text_width or f"{self.cross_section.width:.0f} mm",
            x=0,
            y=offset_width,
            verticalalignment="bottom",
            horizontalalignment="center",
            fontsize=font_size_dimension,
        )

        # add the height dimension line
        offset_height = (-self.cross_section.width / 2) * offset_line_height
        self.axes[axes_i].annotate(
            text="",
            xy=(offset_height, self.cross_section.height / 2),
            xytext=(offset_height, -self.cross_section.height / 2),
            verticalalignment="center",
            horizontalalignment="center",
            arrowprops=diameter_line_style,
            rotation=90,
            annotation_clip=False,
        )
        self.axes[axes_i].text(
            s=custom_text_height or f"{self.cross_section.height:.0f} mm",
            x=offset_height,
            y=0,
            verticalalignment="center",
            horizontalalignment="right",
            fontsize=font_size_dimension,
            rotation=90,
        )

    def _add_stirrups(
        self,
        axes_i: int = 0,
    ) -> None:
        """Adds stirrups to the plot.

        Parameters
        ----------
        axes_i: int
            Index of the axes to plot on. Default is 0.
        """
        for stirrup in self.cross_section.stirrups:
            left_bottom = stirrup.coordinates[1]  # left bottom point of the stirrup (center line)
            self.axes[axes_i].add_patch(
                mplpatches.Rectangle(
                    xy=(left_bottom.x - stirrup.diameter / 2, left_bottom.y - stirrup.diameter / 2),
                    width=stirrup.ctc_distance_legs + stirrup.diameter,
                    height=self.cross_section.height - self.cross_section.covers.upper - self.cross_section.covers.lower,
                    facecolor=STIRRUP_COLOR,
                    fill=True,
                )
            )
            self.axes[axes_i].add_patch(
                mplpatches.Rectangle(
                    xy=(left_bottom.x + stirrup.diameter / 2, left_bottom.y + stirrup.diameter / 2),
                    width=stirrup.ctc_distance_legs - stirrup.diameter,
                    height=self.cross_section.height - self.cross_section.covers.upper - self.cross_section.covers.lower - 2 * stirrup.diameter,
                    facecolor=RCS_CROSS_SECTION_COLOR,
                    fill=True,
                )
            )

    def _add_longitudinal_rebars(
        self,
        axes_i: int = 0,
    ) -> None:
        """Adds longitudinal rebars to the plot.

        Parameters
        ----------
        axes_i: int
            Index of the axes to plot on. Default is 0.
        """
        for rebar in self.cross_section.longitudinal_rebars:
            self.axes[axes_i].add_patch(
                mplpatches.Circle(
                    xy=(rebar.x, rebar.y),
                    radius=rebar.radius,
                    linewidth=1,
                    color=REBAR_COLOR,
                )
            )

    def _legend_text(self) -> str:
        """Creates the legend text.

        Returns
        -------
        str
            Legend text.
        """
        # start building legend
        legend_text = f"{self.cross_section.concrete_material.concrete_class.value} - {self.cross_section.steel_material.name}"

        legend_text += self._add_stirrups_to_legend()
        legend_text += self._add_longitudinal_rebars_to_legend()
        legend_text += self._add_single_longitudinal_rebars_to_legend()
        legend_text += self._add_rebar_configurations_to_legend_quantity_on_edge()
        legend_text += self._add_rebar_configurations_to_legend_quantity_in_line()
        legend_text += self._add_covers_info_to_legend()

        return legend_text

    def _add_stirrups_to_legend(self) -> str:
        """Adds stirrups to the legend text."""
        stirrups_text = ""
        if self.cross_section.stirrups:
            stirrups_text += f"\nStirrups ({sum(stirrup.as_w for stirrup in self.cross_section.stirrups):.0f}mm²/m):"
            for stirrup in self.cross_section.stirrups:
                stirrups_text += f"\n  ⌀{stirrup.diameter}-{stirrup.distance} mm (b:{stirrup.ctc_distance_legs:.0f} mm) ({stirrup.as_w:.0f} mm²/m)"
        return stirrups_text

    def _add_longitudinal_rebars_to_legend(self) -> str:
        """Add longitudinal rebars to the legend text."""
        longitudinal_rebars = ""
        if self.cross_section.longitudinal_rebars:
            longitudinal_rebars += f"\nReinforcement ({sum(rebar.area for rebar in self.cross_section.longitudinal_rebars):.0f}mm²/m): "
        return longitudinal_rebars

    def _add_single_longitudinal_rebars_to_legend(self) -> str:
        """Add single longitudinal rebars to legend text."""
        single_longitudinal_text = ""
        if self.cross_section.single_longitudinal_rebars:
            rebar_diameters: dict[float, list[Rebar]] = {}
            for rebar in self.cross_section.single_longitudinal_rebars:
                rebar_diameters.setdefault(rebar.diameter, []).append(rebar)
            for diameter, rebars in rebar_diameters.items():
                single_longitudinal_text += f"\n  {len(rebars)}⌀{round(diameter, 2)} ({int(sum(rebar.area for rebar in rebars))} mm²/m)"
        return single_longitudinal_text

    def _add_rebar_configurations_to_legend_quantity_on_edge(self) -> str:
        """Add rebar configurations to legend text (quantity on edge)."""
        rebar_configurations_text = ""
        if self.cross_section.reinforcement_by_quantity_on_edge:
            for configuration in self.cross_section.reinforcement_by_quantity_on_edge:
                position = ""
                if configuration.edge in [Edges.LEFT_SIDE, Edges.RIGHT_SIDE]:
                    y_position = self.cross_section.get_rebars_from_reinforcement_configuration(configuration)[0].x
                    position += f"[y:{y_position:.0f}mm]"
                if configuration.edge in [Edges.UPPER_SIDE, Edges.LOWER_SIDE]:
                    z_position = self.cross_section.get_rebars_from_reinforcement_configuration(configuration)[0].y
                    position += f"[z:{z_position:.0f}mm]"
                rebar_configurations_text += f"\n  {position} {configuration.n}⌀{configuration.diameter} ({configuration.area:.0f} mm²/m)"
        return rebar_configurations_text

    def _add_rebar_configurations_to_legend_quantity_in_line(self) -> str:
        """Add rebar configurations to legend text (quantity in line)."""
        rebar_configurations_text = ""
        if self.cross_section.reinforcement_layer_in_line:
            for line_configuration in self.cross_section.reinforcement_layer_in_line:
                rebar_configurations_text += f"\n  {line_configuration.n}⌀{line_configuration.diameter} ({line_configuration.area:.0f} mm²/m)"
        return rebar_configurations_text

    def _add_covers_info_to_legend(self) -> str:
        """Add covers info to legend text."""
        covers_text = ""
        if self.cross_section.stirrups or self.cross_section.longitudinal_rebars:
            covers_text += "\n" + self.cross_section.covers.get_covers_info()
        return covers_text

    def _add_legend(
        self,
        axes_i: int = 0,
        custom_legend_text: str | None = None,
        font_size_legend: float = 10.0,
        offset_center_line: float = 1.05,
    ) -> None:
        """Adds the legend to the plot.

        Parameters
        ----------
        axes_i: int
            Index of the axes to plot on. Default is 0.
        custom_legend_text: str
            Custom legend text.
        font_size_legend: float
            Font size of the legend.
        offset_center_line: float
            Offset of the center line.
        """
        legend_text = custom_legend_text or self._legend_text()
        self.axes[axes_i].annotate(
            text=legend_text,
            xy=((self.cross_section.width / 2) * offset_center_line, -self.cross_section.height / 2),
            verticalalignment="bottom",
            horizontalalignment="left",
            fontsize=font_size_legend,
            annotation_clip=False,
        )
