"""Test Concrete material from table 3.1 of EN 1992-1-1:2004."""

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
            custom_name="C30/37 with a different name",
        )
        assert concrete_with_given_name.name == "C30/37 with a different name"

    def test_e_c(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the E_c property."""
        assert fixture_concrete_material_c30_37.e_c == 32836

    def test_custom_given_e_c(self) -> None:
        """Tests the custom given E_c."""
        concrete_with_given_e_c = ConcreteMaterial(
            concrete_class=ConcreteStrengthClass.C30_37,
            custom_e_c=30000,
        )
        assert concrete_with_given_e_c.e_c == 30000

    def test_custom_e_c_present_is_not_present(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the custom E_c."""
        assert not fixture_concrete_material_c30_37.custom_e_c_present

    def test_custom_e_c_present_is_present(self) -> None:
        """Tests the custom E_c."""
        concrete_with_given_e_c = ConcreteMaterial(
            concrete_class=ConcreteStrengthClass.C30_37,
            custom_e_c=30000,
        )
        assert concrete_with_given_e_c.custom_e_c_present

    def test_f_ck(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_ck property."""
        assert fixture_concrete_material_c30_37.f_ck == 30

    def test_f_ck_raises_value_error(self) -> None:
        """Tests the f_ck property raises a ValueError when the ConcreteStrengthClass is invalid."""
        invalid_concrete_strength_class = type("InvalidConcreteStrengthClass", (), {"value": "invalid_value"})()
        invalid_concrete_material = ConcreteMaterial(invalid_concrete_strength_class)
        with pytest.raises(ValueError):
            invalid_concrete_material.f_ck

    def test_f_ck_cube(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_ck_cube property."""
        assert fixture_concrete_material_c30_37.f_ck_cube == 37

    def test_f_ck_cube_raises_value_error(self) -> None:
        """Tests the f_ck_cube property raises a ValueError when the ConcreteStrengthClass is invalid."""
        invalid_concrete_strength_class = type("InvalidConcreteStrengthClass", (), {"value": "invalid_value"})()
        invalid_concrete_material = ConcreteMaterial(invalid_concrete_strength_class)
        with pytest.raises(ValueError):
            invalid_concrete_material.f_ck_cube

    def test_f_cd(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_cd property."""
        assert fixture_concrete_material_c30_37.f_cd == 20.0

    def test_f_cm(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_cm property."""
        assert fixture_concrete_material_c30_37.f_cm == 38.0

    def test_f_cm_cube(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_cm_cube property."""
        assert fixture_concrete_material_c30_37.f_cm_cube == 45.0

    def test_f_ctm_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_ctm for low concrete."""
        assert fixture_concrete_material_c30_37.f_ctm == 2.896468153816889

    def test_f_ctm_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the f_ctm for high concrete."""
        assert fixture_concrete_material_c90_105.f_ctm == 5.044637804355969

    def test_sigma_cr(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the sigma_cr."""
        assert fixture_concrete_material_c30_37.sigma_cr == 1.7378808922901334

    def test_strain_cr(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the strain_cr."""
        assert fixture_concrete_material_c30_37.strain_cr == 5.2926083941105295e-05

    def test_f_ctk_0_05(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_ctk_0_05 property."""
        assert fixture_concrete_material_c30_37.f_ctk_0_05 == 2.027527707671822

    def test_f_ctd(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_ctd property."""
        assert fixture_concrete_material_c30_37.f_ctd == 1.3516851384478814

    def test_f_ctk_0_95(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the f_ctk_0_95 property."""
        assert fixture_concrete_material_c30_37.f_ctk_0_95 == 3.765408599961956

    def test_e_cm(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the e_cm property."""
        assert fixture_concrete_material_c30_37.e_cm == 32836

    def test_eps_c1(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the eps_c1 property."""
        assert fixture_concrete_material_c30_37.eps_c1 == 2.1618768697354804

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
        """Tests the eps_cu2 property."""
        assert fixture_concrete_material_c30_37.eps_cu2 == 3.5

    def test_eps_cu2_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the eps_cu2 property."""
        assert fixture_concrete_material_c90_105.eps_cu2 == 2.6

    def test_n_factor_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the n_factor property."""
        assert fixture_concrete_material_c30_37.n_factor == 2.0

    def test_n_factor_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the n_factor property."""
        assert fixture_concrete_material_c90_105.n_factor == 1.4

    def test_eps_c3_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the eps_c3 property."""
        assert fixture_concrete_material_c30_37.eps_c3 == 1.75

    def test_eps_c3_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the eps_c3 property."""
        assert fixture_concrete_material_c90_105.eps_c3 == 2.3

    def test_eps_cu3_low_concrete(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the eps_cu3 property."""
        assert fixture_concrete_material_c30_37.eps_cu3 == 3.5

    def test_eps_cu3_high_concrete(self, fixture_concrete_material_c90_105: ConcreteMaterial) -> None:
        """Tests the eps_cu3 property."""
        assert fixture_concrete_material_c90_105.eps_cu3 == 2.6

    def test_rho_min(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Tests the rho_min."""
        assert fixture_concrete_material_c30_37.rho_min(f_yd=250) == 0.2583649593204665

    def test_eq_with_different_name(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Test equality with different name."""
        assert fixture_concrete_material_c30_37 == ConcreteMaterial(
            concrete_class=ConcreteStrengthClass.C30_37,
            custom_name="different name doesn't affect equality",
        )

    def test_inequality_with_different_e_c(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Test inequality with different E_c."""
        assert fixture_concrete_material_c30_37 != ConcreteMaterial(
            concrete_class=ConcreteStrengthClass.C30_37,
            custom_e_c=30000,
        )

    def test_inequality_with_different_concrete_class(self, fixture_concrete_material_c30_37: ConcreteMaterial) -> None:
        """Test inequality with different concrete class."""
        assert fixture_concrete_material_c30_37 != ConcreteMaterial(concrete_class=ConcreteStrengthClass.C12_15)
