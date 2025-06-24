"""Cross-section base class."""

from abc import ABC, abstractmethod

from sectionproperties.analysis import Section
from sectionproperties.post.post import SectionProperties
from sectionproperties.pre import Geometry
from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2


class CrossSection(ABC):
    """Base class for cross-section shapes."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the cross-section."""

    @property
    @abstractmethod
    def polygon(self) -> Polygon:
        """Shapely Polygon representing the cross-section."""

    @property
    def area(self) -> MM2:
        """Area of the cross-section [mm²].

        When using circular cross-sections, the area is an approximation of the area of the polygon.
        The area is calculated using the `area` property of the Shapely Polygon.

        In case you need an exact answer then you need to override this method in the derived class.
        """
        return self.polygon.area

    @property
    def perimeter(self) -> MM:
        """Perimeter of the cross-section [mm]."""
        return self.polygon.length

    @property
    def centroid(self) -> Point:
        """Centroid of the cross-section [mm]."""
        return self.polygon.centroid

    def geometry(self, mesh_size: MM | None = None) -> Geometry:
        """Geometry of the cross-section.

        Properties
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.
        """
        if mesh_size is None:
            mesh_size = 2.0

        geom = Geometry(geom=self.polygon)
        geom.create_mesh(mesh_sizes=mesh_size)
        return geom

    def section(self) -> Section:
        """Section object representing the cross-section."""
        return Section(geometry=self.geometry())

    def section_properties(
        self,
        coordinate_system: str = "YZ",
        geometric: bool = True,
        plastic: bool = True,
        warping: bool = True,
    ) -> SectionProperties:
        """Calculate and return the section properties of the cross-section.

        Parameters
        ----------
        coordinate_system : str
            Coordinate system to use for the section properties.
            Default is "YZ", Y=horizontal, Z=vertical, X reserved for longitudinal direction.
            Other options is "XY", X=horizontal, Y=vertical, Z reserved for longitudinal direction.
        geometric : bool
            Whether to calculate geometric properties.
        plastic: bool
            Whether to calculate plastic properties.
        warping: bool
            Whether to calculate warping properties.
        """
        section = self.section()

        if any([geometric, plastic, warping]):
            section.calculate_geometric_properties()
        if warping:
            section.calculate_warping_properties()
        if plastic:
            section.calculate_plastic_properties()

        props = section.section_props.asdict()
        if coordinate_system == "YZ":
            # Remap section property keys for YZ coordinate system
            key_map = {
                "qx": "qy",
                "qy": "qz",
                "ixx_g": "iyy_g",
                "iyy_g": "izz_g",
                "ixy_g": "iyz_g",
                "cx": "cy",
                "cy": "cz",
                "ixx_c": "iyy_c",
                "iyy_c": "izz_c",
                "ixy_c": "iyz_c",
                "zxx_plus": "zyy_plus",
                "zxx_minus": "zyy_minus",
                "zyy_plus": "zzz_plus",
                "zyy_minus": "zzz_minus",
                "rx_c": "ry_c",
                "ry_c": "rz_c",
                "my_xx": "my_yy",
                "my_yy": "my_zz",
                "x_se": "y_se",
                "y_se": "z_se",
                "x_st": "y_st",
                "y_st": "z_st",
                "a_sx": "a_sy",
                "a_sy": "a_sz",
                "a_sxy": "a_syz",
                "beta_x_plus": "beta_y_plus",
                "beta_x_minus": "beta_y_minus",
                "beta_y_plus": "beta_z_plus",
                "beta_y_minus": "beta_z_minus",
                "x_pc": "y_pc",
                "y_pc": "z_pc",
                "sxx": "syy",
                "syy": "szz",
                "sf_xx_plus": "sf_yy_plus",
                "sf_xx_minus": "sf_yy_minus",
                "sf_yy_plus": "sf_zz_plus",
                "sf_yy_minus": "sf_zz_minus",
            }
            # Rename keys in-place and remove old keys
            for old_key, new_key in key_map.items():
                if old_key in props:
                    props[new_key] = props.pop(old_key)

        class CrossSectionProperties:
            """Custom section properties container."""

            def __init__(self, **kwargs) -> None:
                """Initialize with properties."""
                for k, v in kwargs.items():
                    setattr(self, k, v)

            def asdict(self) -> dict:
                """Convert properties to a dictionary."""
                return self.__dict__

        return CrossSectionProperties(**props)
