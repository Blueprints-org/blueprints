"""Test the rebar module."""

import pytest

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar


class TestRebar:
    """Tests for the Rebar class."""

    @pytest.fixture
    def rebar(self) -> Rebar:
        """Return a Rebar instance."""
        return Rebar(
            diameter=20.0,
            x=0.0,
            y=0.0,
            material=ReinforcementSteelMaterial(),
            relative_start_position=0.1,
            relative_end_position=0.9,
        )

    def test_diameter(self, rebar: Rebar) -> None:
        """Test the diameter property of the Rebar class."""
        assert rebar.diameter == 20.0

    @pytest.mark.parametrize(
        "diameter",
        [
            0.0,
            -10.0,
        ],
    )
    def test_diameter_error(self, diameter: float) -> None:
        """Test the diameter property of the Rebar class."""
        with pytest.raises(ValueError):
            Rebar(
                diameter=diameter,
                x=0.0,
                y=0.0,
                material=ReinforcementSteelMaterial(),
            )

    def test_weight_per_meter(self, rebar: Rebar) -> None:
        """Test the weight_per_meter property of the Rebar class."""
        assert rebar.weight_per_meter == pytest.approx(expected=2.4661, rel=1e-2)

    def test_relative_start_position(self, rebar: Rebar) -> None:
        """Test the relative_start_position property of the Rebar class."""
        assert rebar.relative_start_position == 0.1

    def test_relative_end_position(self, rebar: Rebar) -> None:
        """Test the relative_end_position property of the Rebar class."""
        assert rebar.relative_end_position == 0.9

    @pytest.mark.parametrize(
        "relative_start_position",
        [
            1.1,
            -0.1,
        ],
    )
    def test_relative_start_position_error(self, relative_start_position: float) -> None:
        """Test the relative_start_position property of the Rebar class."""
        with pytest.raises(ValueError):
            Rebar(
                diameter=20.0,
                x=0.0,
                y=0.0,
                material=ReinforcementSteelMaterial(),
                relative_start_position=relative_start_position,
            )

    @pytest.mark.parametrize(
        "relative_end_position",
        [
            1.1,
            -0.1,
        ],
    )
    def test_relative_end_position_error(self, relative_end_position: float) -> None:
        """Test the relative_end_position property of the Rebar class."""
        with pytest.raises(ValueError):
            Rebar(
                diameter=20.0,
                x=0.0,
                y=0.0,
                material=ReinforcementSteelMaterial(),
                relative_end_position=relative_end_position,
            )
