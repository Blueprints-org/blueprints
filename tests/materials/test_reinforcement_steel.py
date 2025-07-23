"""Test class for the reinforcement steel material object."""

import pytest

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality


class TestReinforcementSteelMaterial:
    """Test class for the reinforcement steel material object."""

    def test_default_name(self, fixture_reinforcement_steel_material_b500b: ReinforcementSteelMaterial) -> None:
        """Tests the name."""
        assert fixture_reinforcement_steel_material_b500b.name == "B500B"

    def test_name(self) -> None:
        """Tests the name."""
        steel_with_given_name = ReinforcementSteelMaterial(
            steel_quality=ReinforcementSteelQuality.B500B,
            custom_name="B500B with a different name",
        )
        assert steel_with_given_name.name == "B500B with a different name"

    def test_e_s(self, fixture_reinforcement_steel_material_b500b: ReinforcementSteelMaterial) -> None:
        """Tests the E_s property."""
        assert fixture_reinforcement_steel_material_b500b.e_s == 200000

    def test_custom_given_e_s(self) -> None:
        """Tests the custom given E_s."""
        steel_with_given_e_s = ReinforcementSteelMaterial(
            steel_quality=ReinforcementSteelQuality.B500B,
            custom_e_s=300000,
        )
        assert steel_with_given_e_s.e_s == 300000

    def test_f_yk(self, fixture_reinforcement_steel_material_b500b: ReinforcementSteelMaterial) -> None:
        """Tests the f_yk property."""
        assert fixture_reinforcement_steel_material_b500b.f_yk == 500

    def test_f_yd(self, fixture_reinforcement_steel_material_b500b: ReinforcementSteelMaterial) -> None:
        """Tests the f_yd property."""
        assert fixture_reinforcement_steel_material_b500b.f_yd == pytest.approx(expected=434.78260869, rel=1e-4)

    def test_steel_class(self, fixture_reinforcement_steel_material_b500b: ReinforcementSteelMaterial) -> None:
        """Tests the steel_class property."""
        assert fixture_reinforcement_steel_material_b500b.steel_class == "B"

    def test_f_tk(self, fixture_reinforcement_steel_material_b500b: ReinforcementSteelMaterial) -> None:
        """Tests the f_tk property."""
        assert fixture_reinforcement_steel_material_b500b.f_tk == 540

    @pytest.mark.parametrize(
        ("steel_quality", "expected"),
        [
            (ReinforcementSteelQuality.B500A, 1.05),
            (ReinforcementSteelQuality.B500B, 1.08),
            (ReinforcementSteelQuality.B500C, 1.15),
        ],
    )
    def test_ductility_factor_k(self, steel_quality: ReinforcementSteelQuality, expected: str) -> None:
        """Tests the ductility_factor_k property."""
        steel_material = ReinforcementSteelMaterial(steel_quality=steel_quality)
        assert steel_material.ductility_factor_k == expected

    def test_ductility_factor_k_raises_value_error(self) -> None:
        """Tests the ductility_factor_k property raises a ValueError when the ReinforcementSteelQuality is invalid."""
        invalid_steel_quality = type("InvalidReinforcementSteelQuality", (), {"value": "invalid_value"})()
        invalid_steel_material = ReinforcementSteelMaterial(steel_quality=invalid_steel_quality)
        with pytest.raises(ValueError):
            invalid_steel_material.ductility_factor_k

    @pytest.mark.parametrize(
        ("steel_quality", "expected"),
        [
            (ReinforcementSteelQuality.B500A, 250),
            (ReinforcementSteelQuality.B500B, 500),
            (ReinforcementSteelQuality.B500C, 750),
        ],
    )
    def test_eps_uk(self, steel_quality: ReinforcementSteelQuality, expected: str) -> None:
        """Tests the eps_uk property."""
        steel_material = ReinforcementSteelMaterial(steel_quality=steel_quality)
        assert steel_material.eps_uk == expected

    def test_eps_uk_raises_value_error(self) -> None:
        """Tests the eps_uk property raises a ValueError when the ReinforcementSteelQuality is invalid."""
        invalid_steel_quality = type("InvalidReinforcementSteelQuality", (), {"value": "invalid_value"})()
        invalid_steel_material = ReinforcementSteelMaterial(steel_quality=invalid_steel_quality)
        with pytest.raises(ValueError):
            invalid_steel_material.eps_uk
