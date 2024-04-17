"""Test Concrete material from table 3.1 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass


class TestConcreteMaterial:
    """Test class for the concrete material object."""

    def test_default_name(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the name."""
        assert fixture_concrete_material_c30_37.name == "C30/37"

    def test_name(self) -> None:
        """Tests the name."""
        concrete_with_given_name = ConcreteMaterial(
            concrete_class=ConcreteStrengthClass.C30_37,
            name="C30/37 with a different name",
        )
        assert concrete_with_given_name.name == "C30/37 with a different name"

    def test_custom_given_e_c(self) -> None:
        """Tests the custom given E_c."""
        concrete_with_given_e_c = ConcreteMaterial(
            concrete_class=ConcreteStrengthClass.C30_37,
            e_c=30000,
        )
        assert concrete_with_given_e_c.e_c == 30000

    def test_custom_e_c_present_is_not_present(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the custom E_c."""
        assert not fixture_concrete_material_c30_37.custom_e_c_present

    def test_custom_e_c_present_is_present(self) -> None:
        """Tests the custom E_c."""
        concrete_with_given_e_c = ConcreteMaterial(
            concrete_class=ConcreteStrengthClass.C30_37,
            e_c=30000,
        )
        assert concrete_with_given_e_c.custom_e_c_present

    def test_concrete_class(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the concrete class."""
        assert fixture_concrete_material_c30_37.concrete_class.value == "C30/37"

    def test_material_factor(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the material factor."""
        assert fixture_concrete_material_c30_37.material_factor == 1.5

    def test_f_ctm_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_ctm for low concrete."""
        assert fixture_concrete_material_c30_37.f_ctm == 2.896468153816889

    def test_f_ctm_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the f_ctm for high concrete."""
        assert fixture_concrete_material_c90_105.f_ctm == 5.044637804355969

    def test_thermal_coefficient(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the thermal coefficient."""
        assert fixture_concrete_material_c30_37.thermal_coefficient == 1e-05

    def test_eps_cu1_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the eps_cu1."""
        assert fixture_concrete_material_c30_37.eps_cu1 == 3.5

    def test_eps_cu1_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the eps_cu1."""
        assert fixture_concrete_material_c90_105.eps_cu1 == 2.8

    def test_eps_c2_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the eps_c2."""
        assert fixture_concrete_material_c30_37.eps_c2 == 2.0

    def test_eps_c2_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the eps_c2."""
        assert fixture_concrete_material_c90_105.eps_c2 == 2.6004968327615767

    def test_eps_cu2_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the eps_cu2."""
        assert fixture_concrete_material_c30_37.eps_cu2 == 3.5

    def test_eps_cu2_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the eps_cu2."""
        assert fixture_concrete_material_c90_105.eps_cu2 == 2.6

    def test_n_factor_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the n_factor."""
        assert fixture_concrete_material_c30_37.n_factor == 2.0

    def test_n_factor_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the n_factor."""
        assert fixture_concrete_material_c90_105.n_factor == 1.4

    def test_eps_c3_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the eps_c3."""
        assert fixture_concrete_material_c30_37.eps_c3 == 1.75

    def test_eps_c3_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the eps_c3."""
        assert fixture_concrete_material_c90_105.eps_c3 == 2.3

    def test_eps_cu3_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the eps_cu3."""
        assert fixture_concrete_material_c30_37.eps_cu3 == 3.5

    def test_eps_cu3_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the eps_cu3."""
        assert fixture_concrete_material_c90_105.eps_cu3 == 2.6

    def test_rho_min(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the rho_min."""
        assert fixture_concrete_material_c30_37.rho_min(f_yd=250) == 0.2583649593204665

    def test_eq(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Test equality checks."""
        assert fixture_concrete_material_c30_37 == ConcreteMaterial(
            concrete_class=ConcreteStrengthClass.C30_37,
            name="different name doesn't affect equality",
        )
        assert fixture_concrete_material_c30_37 != ConcreteMaterial(concrete_class=ConcreteStrengthClass.C12_15)
        with pytest.raises(NotImplementedError):
            _ = fixture_concrete_material_c30_37 == "invalid input"
