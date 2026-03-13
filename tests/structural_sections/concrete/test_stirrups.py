"""Test for the stirrups configuration."""

import pytest
from shapely import Polygon

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.stirrups import StirrupConfiguration


class TestStirrup:
    """Tests for the stirrups configuration."""

    @pytest.fixture
    def stirrup(self) -> StirrupConfiguration:
        """Creates a stirrup configuration."""
        return StirrupConfiguration(
            geometry=Polygon([(0, 0), (0, 100), (100, 100), (100, 0)]),
            diameter=8,
            distance=100,
            material=ReinforcementSteelMaterial(),
        )

    def test_mandrel_diameter_factor(self, stirrup: StirrupConfiguration) -> None:
        """Test the mandrel diameter factor."""
        mandrel_diameter_factor = stirrup.mandrel_diameter_factor
        assert mandrel_diameter_factor == 4

    def test_mandrel_diameter_factor_none(self) -> None:
        """Test the mandrel diameter factor."""
        stirrup = StirrupConfiguration(
            geometry=Polygon([(0, 0), (0, 100), (100, 100), (100, 0)]),
            diameter=8,
            distance=100,
            material=ReinforcementSteelMaterial(),
            mandrel_diameter_factor=3.5,
        )
        assert stirrup.mandrel_diameter_factor == 3.5

    def test_as_w(self, stirrup: StirrupConfiguration) -> None:
        """Test total cross-sectional area of the stirrup [mm²/m]."""
        as_w = stirrup.as_w
        assert as_w == pytest.approx(expected=1005.3096, rel=1e-4)

    def test_area(self, stirrup: StirrupConfiguration) -> None:
        """Test the area of the stirrup."""
        area = stirrup.area
        assert area == pytest.approx(expected=50.2655, rel=1e-4)

    def test_radius(self, stirrup: StirrupConfiguration) -> None:
        """Test the radius of the stirrup."""
        radius = stirrup.radius
        assert radius == pytest.approx(expected=4, rel=1e-4)

    def test_centroid(self, stirrup: StirrupConfiguration) -> None:
        """Test the centroid of the stirrup."""
        centroid = stirrup.centroid
        assert centroid.x == pytest.approx(expected=50, rel=1e-4)
        assert centroid.y == pytest.approx(expected=50, rel=1e-4)

    def test_weight_per_meter(self, stirrup: StirrupConfiguration) -> None:
        """Test the weight per meter of the stirrup."""
        weight_per_meter = stirrup.weight_per_meter
        assert weight_per_meter == pytest.approx(expected=1.57833, rel=1e-4)

    def test_ctc_distance_legs(self, stirrup: StirrupConfiguration) -> None:
        """Test the distance between the legs of the stirrup."""
        ctc_distance_legs = stirrup.ctc_distance_legs
        assert ctc_distance_legs == pytest.approx(expected=100, rel=1e-4)

    def test_cover_used(self, stirrup: StirrupConfiguration) -> None:
        """Test the cover used."""
        assert stirrup.cover_used == 0

    def test_cover_used_changed(self) -> None:
        """Test the cover used."""
        stirrup = StirrupConfiguration(
            geometry=Polygon([(0, 0), (0, 100), (100, 100), (100, 0)]), diameter=8, distance=100, material=ReinforcementSteelMaterial(), cover_used=10
        )
        assert stirrup.cover_used == 10

    def test_relative_start_position(self, stirrup: StirrupConfiguration) -> None:
        """Test the relative start position."""
        assert stirrup.relative_start_position == 0.0

    def test_relative_end_position(self, stirrup: StirrupConfiguration) -> None:
        """Test the relative end position."""
        assert stirrup.relative_end_position == 1.0

    @pytest.mark.parametrize(("relative_start_position", "relative_end_position"), [(-1, 1), (-5, 1), (0, 2), (0, 5)])
    def test_relative_positions_wrong(self, relative_start_position: float, relative_end_position: float) -> None:
        """Test the relative positions."""
        with pytest.raises(ValueError):
            StirrupConfiguration(
                geometry=Polygon([(0, 0), (0, 100), (100, 100), (100, 0)]),
                diameter=8,
                distance=100,
                material=ReinforcementSteelMaterial(),
                relative_start_position=relative_start_position,
                relative_end_position=relative_end_position,
            )

    def test__repr__(self, stirrup: StirrupConfiguration) -> None:
        """Test the representation of the stirrup."""
        representation = repr(stirrup)
        assert representation.endswith("|⌀8/B500B")

    def test__str__(self, stirrup: StirrupConfiguration) -> None:
        """Test the string representation of the stirrup."""
        string_representation = str(stirrup)
        assert string_representation == "Stirrups ⌀8-100 mm | B500B | 1005.31 mm²/m"
