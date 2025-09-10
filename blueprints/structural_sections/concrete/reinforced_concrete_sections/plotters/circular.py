"""Plotter for Reinforced Circular Cross-Sections."""

# ruff: noqa: PLR0913, F821
from typing import TypeVar

from matplotlib import patches as mplpatches
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from blueprints.structural_sections.concrete.rebar import Rebar

T = TypeVar("T", bound="CircularReinforcedCrossSection")  # type: ignore[name-defined]

RCS_CROSS_SECTION_COLOR = (0.827, 0.827, 0.827)
STIRRUP_COLOR = (0.412, 0.412, 0.412)
REBAR_COLOR = (0.717, 0.255, 0.055)


class CircularCrossSectionPlotter:
    """Plotter for Reinforced Circular Cross-Sections (RCCS)."""

    def __init__(
        self,
        cross_section: T,
    ) -> None:
        """Initialize the RCCSPlotter.

        Parameters
        ----------
        cross_section: CircularReinforcedCrossSection
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
        custom_text_diameter: str | None = None,
        offset_line_diameter: float = 1.25,
        center_line_style: dict[str, float | str] | None = None,
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
        custom_text_diameter: str
            Custom text for the diameter dimension. Replaces the diameter of the cross-section with the custom text.
        offset_line_diameter: float
            Offset of the diameter line.
        center_line_style: dict[str, float | str] | None
            Style of the center lines. Check matplotlib documentation for more information (Annotation-arrowprops).
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
        self._add_circle(axes_i=axes_i)
        self._add_center_lines(axes_i=axes_i, style=center_line_style)
        self._add_dimension_lines(
            axes_i=axes_i,
            font_size_dimension=font_size_dimension,
            custom_text_diameter=custom_text_diameter,
            offset_line_diameter=offset_line_diameter,
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
            plt.show()  # pragma: no cover
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
        self.axes = [self.fig.add_subplot()]
        return self.fig.get_figwidth(), self.fig.get_figheight()

    def _add_circle(
        self,
        edge_color: str = "black",
        axes_i: int = 0,
    ) -> mplpatches.Circle:
        """Adds a circle to the plot.

        Parameters
        ----------
        edge_color: str
            Color of the edge of the circle. Use any matplotlib color.
        axes_i: int
            Index of the axes to plot on. Default is 0.
        """
        patch = mplpatches.Circle(
            xy=(0, 0),
            radius=self.cross_section.diameter / 2,
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
        default_style = {"arrowstyle": "-", "linewidth": 0.8, "color": "gray", "linestyle": "dashdot"}
        if style:
            default_style.update(style)
        offset_center_line = 1.05
        self.axes[axes_i].annotate(
            text="z",
            xy=(0, (-self.cross_section.diameter / 2) * offset_center_line),
            xytext=(0, (self.cross_section.diameter / 2) * offset_center_line),
            arrowprops=default_style,
            verticalalignment="bottom",
            horizontalalignment="center",
        )
        self.axes[axes_i].annotate(
            text="y",
            xy=((self.cross_section.diameter / 2) * offset_center_line, 0),
            xytext=(-(self.cross_section.diameter / 2) * offset_center_line, 0),
            arrowprops=default_style,
            verticalalignment="center",
            horizontalalignment="right",
        )

    def _add_dimension_lines(
        self,
        axes_i: int = 0,
        style: mplpatches.ArrowStyle | None = None,
        offset_line_diameter: float = 1.25,
        custom_text_diameter: str | None = None,
        font_size_dimension: float = 12.0,
    ) -> None:
        """Adds dimension lines to the plot.

        Parameters
        ----------
        axes_i: int
            Index of the axes to plot on. Default is 0.
        style: dict[str, float]
            Style of the dimension lines. Check matplotlib documentation for more information (Annotation-arrowprops).
        offset_line_diameter: float
            Offset of the diameter line.
        custom_text_diameter: str
            Custom text for the diameter dimension. Replaces the diameter of the cross-section with the custom text.
        font_size_dimension: float
            Font size of the dimensions.
        """
        # add the diameter dimension line
        diameter_line_style = {
            "arrowstyle": style or mplpatches.ArrowStyle(stylename="<->", head_length=0.5, head_width=0.5),
        }
        offset_diameter = (-self.cross_section.diameter / 2) * offset_line_diameter
        self.axes[axes_i].annotate(
            text="",
            xy=(-self.cross_section.diameter / 2, offset_diameter),
            xytext=(self.cross_section.diameter / 2, offset_diameter),
            verticalalignment="center",
            horizontalalignment="center",
            arrowprops=diameter_line_style,
            annotation_clip=False,
        )
        self.axes[axes_i].text(
            s=custom_text_diameter or f"{self.cross_section.diameter:.0f} mm",
            x=0,
            y=offset_diameter,
            verticalalignment="bottom",
            horizontalalignment="center",
            fontsize=font_size_dimension,
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
            # add stirrup to the plot by adding two circles (one for "the stirrup plus inner circle" and one minus inner circle)
            # coded this way as the circle patch does not have a "donut" option and linewidth is in pixels and not in mm
            self.axes[axes_i].add_patch(
                mplpatches.Circle(
                    xy=(0, 0),
                    radius=self.cross_section.diameter / 2 - self.cross_section.cover,
                    edgecolor=STIRRUP_COLOR,
                    facecolor=STIRRUP_COLOR,
                )
            )
            self.axes[axes_i].add_patch(
                mplpatches.Circle(
                    xy=(0, 0),
                    radius=self.cross_section.diameter / 2 - self.cross_section.cover - stirrup.diameter,
                    edgecolor=RCS_CROSS_SECTION_COLOR,
                    facecolor=RCS_CROSS_SECTION_COLOR,
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

    def legend_text(self) -> str:
        """Creates the legend text.

        Returns
        -------
        str
            Legend text.
        """
        # start building legend
        steel_materials = self.cross_section.get_present_steel_materials()
        if steel_materials:
            main_steel_material_used = steel_materials[0].name
            legend_text = f"{self.cross_section.concrete_material.concrete_class.value} - {main_steel_material_used}"
        else:
            legend_text = f"{self.cross_section.concrete_material.concrete_class.value}"

        legend_text += self._add_stirrups_to_legend()
        legend_text += self._add_longitudinal_rebars_to_legend()
        legend_text += self._add_rebar_configurations_to_legend()
        legend_text += self._add_single_longitudinal_rebars_to_legend()
        legend_text += self._add_covers_info_to_legend()

        return legend_text

    def _add_stirrups_to_legend(self) -> str:
        """Adds stirrups to the legend text."""
        stirrups_text = ""
        if self.cross_section.stirrups:
            stirrups_text += f"\nStirrups ({sum(stirrup.as_w for stirrup in self.cross_section.stirrups):.0f} mm²/m):"
            for stirrup in self.cross_section.stirrups:
                stirrups_text += f"\n  ⌀{stirrup.diameter}-{stirrup.distance} mm ({stirrup.as_w:.0f} mm²/m)"
        return stirrups_text

    def _add_longitudinal_rebars_to_legend(self) -> str:
        """Add longitudinal rebars to the legend text."""
        longitudinal_rebars = ""
        if self.cross_section.longitudinal_rebars:
            longitudinal_rebars += f"\nReinforcement ({sum(rebar.area for rebar in self.cross_section.longitudinal_rebars):.0f} mm²/m): "
        return longitudinal_rebars

    def _add_single_longitudinal_rebars_to_legend(self) -> str:
        """Add single longitudinal rebars to legend text."""
        single_longitudinal_text = ""
        if self.cross_section._single_longitudinal_rebars:  # noqa: SLF001
            rebar_diameters: dict[float, list[Rebar]] = {}
            for rebar in self.cross_section._single_longitudinal_rebars:  # noqa: SLF001
                rebar_diameters.setdefault(rebar.diameter, []).append(rebar)
            for diameter, rebars in rebar_diameters.items():
                single_longitudinal_text += f"\n  {len(rebars)}⌀{round(diameter, 2)} ({int(sum(rebar.area for rebar in rebars))} mm²/m)"
        return single_longitudinal_text

    def _add_rebar_configurations_to_legend(self) -> str:
        """Add rebar configurations to legend text (quantity in line)."""
        rebar_configurations_text = ""
        if self.cross_section._reinforcement_configurations:  # noqa: SLF001
            for _, configuration in self.cross_section._reinforcement_configurations:  # noqa: SLF001
                rebar_configurations_text += f"\n  {configuration!s} ({int(configuration.area)} mm²/m)"
        return rebar_configurations_text

    def _add_covers_info_to_legend(self) -> str:
        """Add covers info to legend text."""
        covers_text = ""
        if self.cross_section.stirrups or self.cross_section.longitudinal_rebars:
            covers_text += f"\nCover: {self.cross_section.cover:.0f} mm"
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
        legend_text = custom_legend_text or self.legend_text()
        self.axes[axes_i].annotate(
            text=legend_text,
            xy=((self.cross_section.diameter / 2) * offset_center_line, -self.cross_section.diameter / 2),
            verticalalignment="bottom",
            horizontalalignment="left",
            fontsize=font_size_legend,
            annotation_clip=False,
        )
