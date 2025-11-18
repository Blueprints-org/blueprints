"""Tests for LoadCombination dataclass."""

from blueprints.checks.loads.load_combination import LoadCombination


class TestLoadCombination:
    """Tests for LoadCombination dataclass."""

    def test_load_combination_initialization(self) -> None:
        """Test that LoadCombination can be initialized with all parameters."""
        load_combo = LoadCombination(
            normal_force=100.0, shear_force_y=20.0, shear_force_z=30.0, bending_moment_y=50.0, bending_moment_z=60.0, torsion=10.0
        )

        assert load_combo.normal_force == 100.0
        assert load_combo.shear_force_y == 20.0
        assert load_combo.shear_force_z == 30.0
        assert load_combo.bending_moment_y == 50.0
        assert load_combo.bending_moment_z == 60.0
        assert load_combo.torsion == 10.0

    def test_load_combination_with_negative_values(self) -> None:
        """Test that LoadCombination accepts negative values (compression, etc.)."""
        load_combo = LoadCombination(
            normal_force=-150.0, shear_force_y=-25.0, shear_force_z=-35.0, bending_moment_y=-55.0, bending_moment_z=-65.0, torsion=-15.0
        )

        assert load_combo.normal_force == -150.0
        assert load_combo.shear_force_y == -25.0
        assert load_combo.shear_force_z == -35.0
        assert load_combo.bending_moment_y == -55.0
        assert load_combo.bending_moment_z == -65.0
        assert load_combo.torsion == -15.0

    def test_load_combination_with_zero_values(self) -> None:
        """Test that LoadCombination accepts zero values."""
        load_combo = LoadCombination()

        assert load_combo.normal_force == 0.0
        assert load_combo.shear_force_y == 0.0
        assert load_combo.shear_force_z == 0.0
        assert load_combo.bending_moment_y == 0.0
        assert load_combo.bending_moment_z == 0.0
        assert load_combo.torsion == 0.0

    def test_load_combination_equality(self) -> None:
        """Test that two LoadCombination instances with same values are equal."""
        load_combo1 = LoadCombination(
            normal_force=100.0, shear_force_y=20.0, shear_force_z=30.0, bending_moment_y=50.0, bending_moment_z=60.0, torsion=10.0
        )
        load_combo2 = LoadCombination(
            normal_force=100.0, shear_force_y=20.0, shear_force_z=30.0, bending_moment_y=50.0, bending_moment_z=60.0, torsion=10.0
        )

        assert load_combo1 == load_combo2

    def test_load_combination_inequality(self) -> None:
        """Test that two LoadCombination instances with different values are not equal."""
        load_combo1 = LoadCombination(
            normal_force=100.0, shear_force_y=20.0, shear_force_z=30.0, bending_moment_y=50.0, bending_moment_z=60.0, torsion=10.0
        )
        load_combo2 = LoadCombination(
            normal_force=200.0, shear_force_y=20.0, shear_force_z=30.0, bending_moment_y=50.0, bending_moment_z=60.0, torsion=10.0
        )

        assert load_combo1 != load_combo2

    def test_load_combination_hashable(self) -> None:
        """Test that LoadCombination instances are hashable (can be used in sets/dicts)."""
        load_combo1 = LoadCombination(
            normal_force=100.0, shear_force_y=20.0, shear_force_z=30.0, bending_moment_y=50.0, bending_moment_z=60.0, torsion=10.0
        )
        load_combo2 = LoadCombination(
            normal_force=100.0, shear_force_y=20.0, shear_force_z=30.0, bending_moment_y=50.0, bending_moment_z=60.0, torsion=10.0
        )

        load_set = {load_combo1, load_combo2}
        assert len(load_set) == 1
