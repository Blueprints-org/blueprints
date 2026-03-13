"""Tests reinforcement configurations."""

import pytest
from shapely import LineString

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import (
    ReinforcementByDistance,
    ReinforcementByQuantity,
)


class TestReinforcementByDistance:
    """Tests for the reinforcement by distance configuration."""

    def test_n_rebars_per_meter(self, reinforcement_by_distance: ReinforcementByDistance) -> None:
        """Test the number of rebars per meter."""
        n_rebars_per_meter = reinforcement_by_distance.n_rebars_per_meter
        assert n_rebars_per_meter == 10

    def test_area(self, reinforcement_by_distance: ReinforcementByDistance) -> None:
        """Test the area of the reinforcement."""
        area = reinforcement_by_distance.area
        assert area == pytest.approx(expected=1130.9733, rel=1e-4)

    def test__repr__(self, reinforcement_by_distance: ReinforcementByDistance) -> None:
        """Test the representation of the reinforcement."""
        representation = repr(reinforcement_by_distance)
        assert representation == "ReinforcementByDistance|⌀12-100|1131 mm²/m"

    def test_wrong_ctc(self) -> None:
        """Test the wrong center-to-center distance."""
        with pytest.raises(ValueError):
            ReinforcementByDistance(
                diameter=12,
                center_to_center=0,
                material=ReinforcementSteelMaterial(),
            )

    def test_to_rebars(self, reinforcement_by_distance: ReinforcementByDistance) -> None:
        """Test the conversion to rebars."""
        line = LineString([(0, 0), (1000, 0)])
        rebars = reinforcement_by_distance.to_rebars(line=line)
        assert len(rebars) == 10
        assert all(rebar.diameter == 12 for rebar in rebars)
        assert all(rebar.material == ReinforcementSteelMaterial() for rebar in rebars)

    def test_error_when_using_linearring(self, reinforcement_by_distance: ReinforcementByDistance) -> None:
        """Test the error when using a Linearring."""
        linearring = LineString([(0, 0), (1000, 0), (1000, 1000), (0, 1000), (0, 0)])
        with pytest.raises(ValueError):
            reinforcement_by_distance.to_rebars(line=linearring)


class TestReinforcementByQuantity:
    """Tests for the reinforcement by quantity configuration."""

    def test_area(self, reinforcement_by_quantity: ReinforcementByQuantity) -> None:
        """Test the area of the reinforcement."""
        area = reinforcement_by_quantity.area
        assert area == pytest.approx(expected=1130.9733, rel=1e-4)

    @pytest.mark.parametrize("diameter", [0, -1])
    def test_wrong_diameter(self, diameter: int) -> None:
        """Test the wrong diameter."""
        with pytest.raises(ValueError):
            ReinforcementByQuantity(
                diameter=diameter,
                material=ReinforcementSteelMaterial(),
                n=10,
            )

    @pytest.mark.parametrize(("wrong_n", "expected_error"), [(0, ValueError), (-1, ValueError), (1.5, TypeError)])
    def test_wrong_n_float(self, wrong_n: int, expected_error: type[BaseException]) -> None:
        """Test the wrong number of rebars."""
        with pytest.raises(expected_error):
            ReinforcementByQuantity(
                diameter=12,
                material=ReinforcementSteelMaterial(),
                n=wrong_n,
            )

    def test_to_rebars(self, reinforcement_by_quantity: ReinforcementByQuantity) -> None:
        """Test the conversion to rebars."""
        line = LineString([(0, 0), (1000, 0)])
        rebars = reinforcement_by_quantity.to_rebars(line=line)
        assert len(rebars) == 10
        assert all(rebar.diameter == 12 for rebar in rebars)
        assert all(rebar.material == ReinforcementSteelMaterial() for rebar in rebars)

    def test__repr__(self, reinforcement_by_quantity: ReinforcementByQuantity) -> None:
        """Test the representation of the reinforcement."""
        representation = repr(reinforcement_by_quantity)
        assert representation == "ReinforcementByQuantity|10⌀12|1131 mm²"
