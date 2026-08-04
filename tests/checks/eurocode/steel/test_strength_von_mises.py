"""Tests for von Mises equivalent stress check according to Eurocode 3."""

import pytest

from blueprints.checks.eurocode.steel.strength_von_mises import CheckStrengthVonMises
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.validations import LessOrEqualToZeroError


class TestCheckStrengthVonMises:
    """Tests for CheckStrengthVonMises."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no internal forces."""
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=0, v_y=0, v_z=0, m_x=0, m_y=0, m_z=0, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

    def test_result_axial_tension_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok axial tension load."""
        # Cross-section area: 14908 mm², yield strength S355: 355 N/mm²
        # Maximum axial load: 355 * 14908 / 1e3 = 5292.34 kN
        n = 355 * 14908 / 1.0 / 1e3 * 0.99
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99
        assert calc.report()

    def test_result_axial_tension_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok axial tension load."""
        n = 355 * 14908 / 1.0 / 1e3 * 1.01
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_result_axial_compression_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok axial compression load."""
        # For class 1, 2, 3 sections, no buckling check needed for compression
        n = -355 * 14908 / 1.0 / 1e3 * 0.99
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_axial_compression_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok axial compression load."""
        n = -355 * 14908 / 1.0 / 1e3 * 1.01
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

    def test_result_bending_mz_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about z-axis (strong axis)."""
        m_z = 355 * 571 * 1e3 / 1e6 / 1.0 * 0.99
        calc = CheckStrengthVonMises(heb_steel_cross_section, m_z=m_z, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_bending_mz_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about z-axis."""
        m_z = 355 * 571 * 1e3 / 1e6 / 1.0 * 1.01
        calc = CheckStrengthVonMises(heb_steel_cross_section, m_z=m_z, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

    def test_result_bending_my_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about y-axis (weak axis)."""
        m_y = 355 * 1678 * 1e3 / 1e6 / 1.0 * 0.99
        calc = CheckStrengthVonMises(heb_steel_cross_section, m_y=m_y, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_bending_my_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about y-axis."""
        m_y = 355 * 1678 * 1e3 / 1e6 / 1.0 * 1.01
        calc = CheckStrengthVonMises(heb_steel_cross_section, m_y=m_y, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01

    def test_result_shear_vy_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok shear force in y-direction."""
        v_y = 1405 * 0.99
        calc = CheckStrengthVonMises(heb_steel_cross_section, v_y=v_y, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True

    def test_result_shear_vy_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok shear force in y-direction."""
        v_y = 1405 * 1.01
        calc = CheckStrengthVonMises(heb_steel_cross_section, v_y=v_y, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False

    def test_result_shear_vz_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok shear force in z-direction."""
        v_z = 607 * 0.99
        calc = CheckStrengthVonMises(heb_steel_cross_section, v_z=v_z, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is True

    def test_result_shear_vz_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok shear force in z-direction."""
        v_z = 607 * 1.01
        calc = CheckStrengthVonMises(heb_steel_cross_section, v_z=v_z, gamma_m0=1.0)
        result = calc.result()
        assert result.is_ok is False

    def test_result_combined_loads_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok combined internal forces."""
        # Apply multiple loads at lower levels
        n = 1
        v_y = 2
        v_z = 3
        m_x = 4
        m_y = 5
        m_z = 6
        calc = CheckStrengthVonMises(
            heb_steel_cross_section,
            n=n,
            v_y=v_y,
            v_z=v_z,
            m_x=m_x,
            m_y=m_y,
            m_z=m_z,
            gamma_m0=1.0,
        )
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check < 1.0
        assert result.factor_of_safety > 1.0
        assert calc.report()

    def test_result_combined_loads_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok combined internal forces."""
        # Apply large loads to exceed capacity
        n = 1000
        v_y = 2000
        v_z = 3000
        m_x = 4000
        m_y = 5000
        m_z = 6000
        calc = CheckStrengthVonMises(
            heb_steel_cross_section,
            n=n,
            v_y=v_y,
            v_z=v_z,
            m_x=m_x,
            m_y=m_y,
            m_z=m_z,
            gamma_m0=1.0,
        )
        result = calc.result()
        assert result.is_ok is False
        assert result.unity_check > 1.0
        assert result.factor_of_safety < 1.0
        assert calc.report()

    def test_result_with_gamma_m0_greater_than_one(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() with partial safety factor gamma_m0 > 1.0."""
        n = 500
        gamma_m0 = 1.25
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=gamma_m0)
        calc_ref = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=1.0)

        # With higher gamma_m0, unity check should be higher (more critical)
        assert calc.unity_check() > calc_ref.unity_check()

    def test_maximum_von_mises_stress(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test maximum_von_mises_stress() calculation."""
        n = 1000
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=1.0)
        max_stress = calc.maximum_von_mises_stress()
        assert isinstance(max_stress, float)
        assert max_stress > 0

    def test_unity_check_method(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test unity_check() method."""
        n = 1000
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=1.0)
        uc = calc.unity_check()
        assert isinstance(uc, float)
        assert uc > 0
        assert uc == calc.result().unity_check

    def test_report_with_axial_load(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test report output with axial load."""
        n = 100
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=1.0)
        report = calc.report()
        assert report is not None

    def test_report_with_combined_loads(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test report output with combined loads."""
        calc = CheckStrengthVonMises(
            heb_steel_cross_section,
            n=100,
            v_y=50,
            v_z=75,
            m_x=25,
            m_y=200,
            m_z=300,
            gamma_m0=1.0,
        )
        report = calc.report()
        assert report is not None

    def test_source_docs(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test source_docs() method."""
        n = 100
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=n, gamma_m0=1.0)
        docs = calc.source_docs()
        assert isinstance(docs, list)
        assert len(docs) == 1

    def test_equality(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test equality of two CheckStrengthVonMises instances."""
        calc1 = CheckStrengthVonMises(heb_steel_cross_section, n=100, v_y=50, gamma_m0=1.0)
        calc2 = CheckStrengthVonMises(heb_steel_cross_section, n=100, v_y=50, gamma_m0=1.0)
        assert calc1 == calc2

    def test_inequality(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test inequality of two CheckStrengthVonMises instances."""
        calc1 = CheckStrengthVonMises(heb_steel_cross_section, n=100, gamma_m0=1.0)
        calc2 = CheckStrengthVonMises(heb_steel_cross_section, n=200, gamma_m0=1.0)
        assert calc1 != calc2

    def test_validate_design_resistance_valid_parameters(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test _validate_design_resistance() with valid parameters."""
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=100, gamma_m0=1.0)
        # Should not raise any exception
        calc._validate_design_resistance()

    def test_validate_design_resistance_with_gamma_m0_zero(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test _validate_design_resistance() raises ValueError when gamma_m0 is zero."""
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=100, gamma_m0=0.0)
        with pytest.raises(LessOrEqualToZeroError):
            calc._validate_design_resistance()

    def test_validate_design_resistance_with_gamma_m0_negative(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test _validate_design_resistance() raises ValueError when gamma_m0 is negative."""
        calc = CheckStrengthVonMises(heb_steel_cross_section, n=100, gamma_m0=-1.25)
        with pytest.raises(LessOrEqualToZeroError):
            calc._validate_design_resistance()
