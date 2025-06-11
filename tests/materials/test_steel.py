"""Test Steel material from NEN-EN standards."""

import pytest

from blueprints.materials.steel import DiagramType, SteelMaterial, SteelStrengthClass


class TestSteelMaterial:
    """Test class for the steel material object."""

    def test_default_name(self) -> None:
        """Tests the default name."""
        steel = SteelMaterial()
        assert steel.name == "S 355 (NEN-EN 10025-2)"

    def test_custom_name(self) -> None:
        """Tests the custom name."""
        steel = SteelMaterial(custom_name="Custom Steel")
        assert steel.name == "Custom Steel"

    def test_default_e_modulus(self) -> None:
        """Tests the default modulus of elasticity."""
        steel = SteelMaterial()
        assert steel.e_modulus == 210_000.0

    def test_custom_e_modulus(self) -> None:
        """Tests the custom modulus of elasticity."""
        steel = SteelMaterial(custom_e_modulus=200_000.0)
        assert steel.e_modulus == 200_000.0

    def test_default_poisson_ratio(self) -> None:
        """Tests the default Poisson's ratio."""
        steel = SteelMaterial()
        assert steel.poisson_ratio == 0.3

    def test_custom_poisson_ratio(self) -> None:
        """Tests the custom Poisson's ratio."""
        steel = SteelMaterial(custom_poisson_ratio=0.25)
        assert steel.poisson_ratio == 0.25

    def test_default_thermal_coefficient(self) -> None:
        """Tests the default thermal coefficient."""
        steel = SteelMaterial()
        assert steel.thermal_coefficient == 1.2e-5

    def test_custom_thermal_coefficient(self) -> None:
        """Tests the custom thermal coefficient."""
        steel = SteelMaterial(custom_thermal_coefficient=1.5e-5)
        assert steel.thermal_coefficient == 1.5e-5

    def test_shear_modulus(self) -> None:
        """Tests the shear modulus calculation."""
        steel = SteelMaterial()
        assert steel.shear_modulus == pytest.approx(80_769.23, rel=1e-5)

    def test_default_yield_strength(self) -> None:
        """Tests the default yield strength."""
        steel = SteelMaterial(steel_class=SteelStrengthClass.S275)
        assert steel.yield_strength(10) == 275.0

    def test_custom_yield_strength(self) -> None:
        """Tests the custom yield strength."""
        steel = SteelMaterial(custom_yield_strength=300.0)
        assert steel.yield_strength(10) == 300.0

    def test_default_ultimate_strength(self) -> None:
        """Tests the default ultimate strength."""
        steel = SteelMaterial(steel_class=SteelStrengthClass.S275)
        assert steel.ultimate_strength(thickness=30) == 430.0

    def test_custom_ultimate_strength(self) -> None:
        """Tests the custom ultimate strength."""
        steel = SteelMaterial(custom_ultimate_strength=500.0)
        assert steel.ultimate_strength(thickness=30) == 500.0

    def test_yield_strength_above_40mm(self) -> None:
        """Tests the yield strength for thickness > 40 mm."""
        steel = SteelMaterial(steel_class=SteelStrengthClass.S275)
        assert steel.yield_strength(thickness=50) == 255.0

    def test_ultimate_strength_above_40mm(self) -> None:
        """Tests the ultimate strength for thickness > 40 mm."""
        steel = SteelMaterial(steel_class=SteelStrengthClass.S275)
        assert steel.ultimate_strength(thickness=50.0) == 410.0

    def test_yield_strength_invalid_thickness(self) -> None:
        """Tests yield strength raises ValueError for invalid thickness."""
        steel = SteelMaterial(steel_class=SteelStrengthClass.S275)
        with pytest.raises(ValueError):
            steel.yield_strength(thickness=85.0)

    def test_ultimate_strength_invalid_thickness(self) -> None:
        """Tests ultimate strength raises ValueError for invalid thickness."""
        steel = SteelMaterial(steel_class=SteelStrengthClass.S275)
        with pytest.raises(ValueError):
            steel.ultimate_strength(thickness=85.0)

    def test_diagram_type_default(self) -> None:
        """Tests the default diagram type."""
        steel = SteelMaterial()
        assert steel.diagram_type == DiagramType.BI_LINEAR

    def test_diagram_type_custom(self) -> None:
        """Tests the custom diagram type."""
        steel = SteelMaterial(diagram_type=DiagramType.PARABOLIC)
        assert steel.diagram_type == DiagramType.PARABOLIC

    def test_density_default(self) -> None:
        """Tests the default density."""
        steel = SteelMaterial()
        assert steel.density == 7850.0

    def test_density_custom(self) -> None:
        """Tests the custom density."""
        steel = SteelMaterial(density=8000.0)
        assert steel.density == 8000.0

    def test_eq_with_different_name(self) -> None:
        """Test equality with different name."""
        steel1 = SteelMaterial(steel_class=SteelStrengthClass.S355)
        steel2 = SteelMaterial(steel_class=SteelStrengthClass.S355, custom_name="Custom Name")
        assert steel1 == steel2

    def test_inequality_with_different_e_modulus(self) -> None:
        """Test inequality with different modulus of elasticity."""
        steel1 = SteelMaterial(steel_class=SteelStrengthClass.S355)
        steel2 = SteelMaterial(steel_class=SteelStrengthClass.S355, custom_e_modulus=200_000.0)
        assert steel1 != steel2

    def test_inequality_with_different_steel_class(self) -> None:
        """Test inequality with different steel class."""
        steel1 = SteelMaterial(steel_class=SteelStrengthClass.S355)
        steel2 = SteelMaterial(steel_class=SteelStrengthClass.S275)
        assert steel1 != steel2

    def test_invalid_steel_class(self) -> None:
        """Test invalid steel class raises ValueError."""
        with pytest.raises(ValueError):
            SteelMaterial(steel_class="INVALID_CLASS").yield_strength(thickness=50.0)  # type: ignore[arg-type]

    def test_invalid_yield_above_40mm_thickness(self) -> None:
        """Test invalid thickness raises ValueError."""
        with pytest.raises(ValueError):
            SteelMaterial(steel_class=SteelStrengthClass.S355_H_10219_1).yield_strength(thickness=50.0)

    def test_invalid_ultimate_above_40mm_thickness(self) -> None:
        """Test invalid thickness raises ValueError."""
        with pytest.raises(ValueError):
            SteelMaterial(steel_class=SteelStrengthClass.S355_NH_NLH_10219_1).ultimate_strength(thickness=50.0)
