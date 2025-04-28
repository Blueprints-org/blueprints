"""Circular reinforced cross-section."""

from matplotlib import pyplot as plt
from numpy import cos, pi, sin
from shapely import LineString, Polygon

from blueprints.geometry.operations import rotate_linearring
from blueprints.materials.concrete import ConcreteMaterial
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.covers import DEFAULT_COVER
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.plotters.circular import CircularCrossSectionPlotter
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import ReinforcementByQuantity
from blueprints.structural_sections.concrete.stirrups import StirrupConfiguration
from blueprints.structural_sections.cross_section_circle import CircularCrossSection
from blueprints.type_alias import DEG, DIMENSIONLESS, MM, RATIO


class CircularReinforcedCrossSection(ReinforcedCrossSection):
    """Representation of a reinforced circular concrete cross-section like a column.

    Parameters
    ----------
    diameter : MM
        The diameter of the circular cross-section [mm].
    concrete_material : ConcreteMaterial
        Material properties of the concrete.
    cover : MM, optional
        The reinforcement cover for the cross-section [mm]. The default is 50 mm.
    """

    def __init__(self, diameter: MM, concrete_material: ConcreteMaterial, cover: MM = DEFAULT_COVER) -> None:
        """Initialize the circular reinforced concrete section."""
        super().__init__(
            cross_section=CircularCrossSection(
                diameter=diameter,
                x=0,  # x=0 and y=0 to place the cross-section at the origin
                y=0,
            ),
            concrete_material=concrete_material,
        )
        self.diameter = diameter
        self.cover = cover
        self.plotter = CircularCrossSectionPlotter(cross_section=self)

    def add_stirrup_along_perimeter(
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
        """Adds a stirrup configuration along the perimeter of the cross-section taking the covers into account. The created configuration goes around
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
        # create the stirrup configuration based on the covers present
        radius = self.diameter / 2 - self.cover - (diameter / 2)
        stirrup_geometry = Polygon([(radius * cos(angle), radius * sin(angle)) for angle in [2 * pi * i / 100 for i in range(100)]])

        # add the stirrup configuration
        return self.add_stirrup_configuration(
            StirrupConfiguration(
                geometry=stirrup_geometry,
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
        diameter: MM,
        cover: MM | None = None,
        start_angle: DEG = 90.0,
    ) -> LineString:
        """Get the reference circle for the cross-section.

        Parameters
        ----------
        diameter: MM
            Diameter of the rebars [mm].
        cover: MM, optional
            Cover of the rebars [mm]. If not provided, the default cover is used.
        start_angle: DEG
            Starting position of the reference line in degrees. 90 degrees is the top of the circle.
            0 degrees is the right side of the circle. 180 degrees is the right side of the circle.
            Default is 90 degrees.

        Returns
        -------
        LineString
            Reference circle for the cross-section.
        """
        # calculate the effective radius for the rebars
        cover = cover if cover is not None else self.cover

        # check if there is a stirrup configuration present to adjust the radius
        max_stirrups_diameter = 0.0
        if self._stirrups:
            max_stirrups_diameter = max([stirrup.diameter for stirrup in self._stirrups])

        radius = self.diameter / 2 - cover - max_stirrups_diameter - (diameter / 2)

        # create the circle using shapely's Point and buffer
        circle = self.cross_section.centroid.buffer(radius, quad_segs=360, join_style="round")

        return rotate_linearring(linearring=circle.exterior, angle_degrees=start_angle)

    def add_longitudinal_reinforcement_by_quantity(
        self,
        n: int,
        diameter: MM,
        material: ReinforcementSteelMaterial,
        cover: MM | None = None,
        start_angle: DEG = 90.0,
    ) -> None:
        """Add longitudinal reinforcement to the cross-section based on the quantity configuration of rebars.

        Parameters
        ----------
        n: int
            Amount of longitudinal bars.
        diameter: MM
            Diameter of the rebars [mm].
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
        cover: MM, optional
            Cover of the rebars [mm]. If not provided, the default cover is used.
        start_angle: DEG
            Starting position of the first rebar. Default is 90 degrees which is the top of the circle.
            0 degrees is the right side of the circle. 180 degrees is the right side of the circle.
        """
        return self.add_reinforcement_configuration(
            configuration=ReinforcementByQuantity(
                diameter=diameter,
                material=material,
                n=n,
            ),
            line=self._get_reference_line,
            cover=cover,
            diameter=diameter,
            start_angle=start_angle,
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
