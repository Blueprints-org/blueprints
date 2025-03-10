"""Circular reinforced cross-section."""

# ruff: noqa: PLR0913

from matplotlib import pyplot as plt
from numpy import cos, pi, sin
from shapely import LineString, Polygon

from blueprints.materials.concrete import ConcreteMaterial
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.covers import CoversCircular
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.plotters.circular import CircularCrossSectionPlotter
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import ReinforcementByQuantity
from blueprints.structural_sections.concrete.stirrups import StirrupConfiguration
from blueprints.structural_sections.cross_section_shapes import CircularCrossSection
from blueprints.type_alias import DIMENSIONLESS, MM, RATIO


class CircularReinforcedCrossSection(ReinforcedCrossSection):
    """Representation of a reinforced circular concrete cross-section like a column.

    Parameters
    ----------
    diameter : MM
        The diameter of the circular cross-section [mm].
    concrete_material : ConcreteMaterial
        Material properties of the concrete.
    covers : CoversCircular, optional
        The reinforcement covers for the cross-section [mm]. The default is 50 mm.
    """

    def __init__(
        self,
        diameter: MM,
        concrete_material: ConcreteMaterial,
        covers: CoversCircular = CoversCircular(),
    ) -> None:
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
        self.covers = covers
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
        radius = self.diameter / 2 - self.covers.cover - (diameter / 2)
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
    ) -> LineString:
        """Get the reference circle for the cross-section.

        Parameters
        ----------
        diameter: MM
            Diameter of the rebars [mm].
        cover: MM, optional
            Cover of the rebars [mm]. If not provided, the default cover is used.

        Returns
        -------
        LineString
            Reference circle for the cross-section.
        """
        # calculate the effective radius for the rebars
        cover = cover if cover is not None else self.covers.cover

        # check if there is a stirrup configuration present to adjust the radius
        max_stirrups_diameter = 0.0
        if self._stirrups:
            max_stirrups_diameter = max([stirrup.diameter for stirrup in self._stirrups])

        radius = self.diameter / 2 - cover - max_stirrups_diameter - (diameter / 2)

        # create the circle using shapely's LineString
        angles = [pi / 2 - 2 * pi * i / 360 for i in range(360)]
        return LineString([(radius * cos(angle), radius * sin(angle)) for angle in angles])

    def add_longitudinal_reinforcement_by_quantity(
        self,
        n: int,
        diameter: MM,
        material: ReinforcementSteelMaterial,
        cover: MM | None = None,
        start_on_half_increment: bool = False,
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
        start_on_half_increment: bool, optional
            If True, the circle is rotated by half the increment.
            If False, the rebar is placed at the top of the cross-section.
            Default is False.
        """
        line = self._get_reference_line(diameter=diameter, cover=cover)
        assert line

        return self.add_reinforcement_configuration(
            line=self._get_reference_line(diameter=diameter, cover=cover),
            configuration=ReinforcementByQuantity(
                diameter=diameter, material=material, n=n, end_at_start=True, start_on_half_increment=start_on_half_increment
            ),
            cover=cover,
            start_on_half_increment=start_on_half_increment,
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


if __name__ == "__main__":
    # Example of the usage of the CircularReinforcedCrossSection
    from blueprints.materials.concrete import ConcreteMaterial
    from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
    from blueprints.structural_sections.concrete.covers import CoversCircular
    from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import ReinforcementByQuantity

    # Define the concrete material
    concrete = ConcreteMaterial()

    # Define the reinforcement steel material
    reinforcement_steel = ReinforcementSteelMaterial()

    covers = CoversCircular(25)

    # Define the cross-section
    cross_section = CircularReinforcedCrossSection(diameter=400, concrete_material=concrete, covers=covers)

    # Add longitudinal reinforcement
    cross_section.add_longitudinal_reinforcement_by_quantity(n=3, diameter=25, material=reinforcement_steel, start_on_half_increment=True)

    # Add longitudinal reinforcement
    cross_section.add_longitudinal_reinforcement_by_quantity(n=3, diameter=10, material=reinforcement_steel, start_on_half_increment=False)

    # Add stirrups
    cross_section.add_stirrup_along_perimeter(diameter=25, distance=200, material=reinforcement_steel)

    # Add stirrups
    cross_section.add_stirrup_along_perimeter(diameter=10, distance=200, material=reinforcement_steel)

    # Plot the cross-section
    cross_section.plot()
    plt.show()
