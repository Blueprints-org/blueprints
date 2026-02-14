"""Tests for bending moment strength according to Eurocode 3."""

import pytest

from blueprints.checks.eurocode.steel.strength_bending import CheckStrengthBendingClass3, CheckStrengthBendingClass12
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestCheckStrengthBendingClass12:
    """Tests for CheckStrengthBendingClass12."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no bending moment."""
        calc = CheckStrengthBendingClass12(heb_steel_cross_section, 0, axis="My")
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

    def test_result_my_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about y-axis."""
        m = 355 * 1.869 * 0.99
        calc = CheckStrengthBendingClass12(heb_steel_cross_section, m, axis="My")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_my_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about y-axis."""
        m = 355 * 1.869 * 1.01
        calc = CheckStrengthBendingClass12(heb_steel_cross_section, m, axis="My")
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_result_mz_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about z-axis."""
        m = 355 * 0.870 * 0.99
        calc = CheckStrengthBendingClass12(heb_steel_cross_section, m, axis="Mz")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_mz_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about z-axis."""
        m = 355 * 0.870 * 1.01
        calc = CheckStrengthBendingClass12(heb_steel_cross_section, m, axis="Mz")
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_negative_moment(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for negative bending moments (should be treated as positive)."""
        m = -355 * 1.869 * 0.99
        calc = CheckStrengthBendingClass12(heb_steel_cross_section, m, axis="My")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99

        m = -355 * 0.870 * 0.99
        calc = CheckStrengthBendingClass12(heb_steel_cross_section, m, axis="Mz")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99

    def test_invalid_axis(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test ValueError is raised for invalid axis input."""
        with pytest.raises(ValueError):
            CheckStrengthBendingClass12(heb_steel_cross_section, 100, axis="Mx").calculation_formula()

    def test_report(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test report output for bending moment check."""
        m = 100
        calc = CheckStrengthBendingClass12(heb_steel_cross_section, m, axis="My")
        assert calc.report()

    def test_source_docs(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test source_docs() method."""
        m = 100
        calc = CheckStrengthBendingClass12(heb_steel_cross_section, m, gamma_m0=1.0)
        docs = calc.source_docs()
        assert isinstance(docs, list)
        assert len(docs) == 1


class TestCheckStrengthBendingClass3:
    """Tests for CheckStrengthBendingClass3."""

    def test_result_none(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() returns True for no bending moment."""
        calc = CheckStrengthBendingClass3(heb_steel_cross_section, 0, axis="My")
        result = calc.result()
        assert result.is_ok is True
        assert result.unity_check == 0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0.0
        assert calc.report()

    def test_result_my_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about y-axis."""
        m = 355 * 1.678 * 0.99
        calc = CheckStrengthBendingClass3(heb_steel_cross_section, m, axis="My")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_my_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about y-axis."""
        m = 355 * 1.678 * 1.01
        calc = CheckStrengthBendingClass3(heb_steel_cross_section, m, axis="My")
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_result_mz_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for ok bending moment about z-axis."""
        m = 355 * 0.571 * 0.99
        calc = CheckStrengthBendingClass3(heb_steel_cross_section, m, axis="Mz")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 0.99

    def test_result_mz_not_ok(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for not ok bending moment about z-axis."""
        m = 355 * 0.571 * 1.01
        calc = CheckStrengthBendingClass3(heb_steel_cross_section, m, axis="Mz")
        result = calc.result()
        assert result.is_ok is False
        assert pytest.approx(result.unity_check, 0.005) == 1.01
        assert pytest.approx(result.factor_of_safety, 0.005) == 1 / 1.01
        assert calc.report()

    def test_negative_moment(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test result() for negative bending moments (should be treated as positive)."""
        m = -355 * 1.678 * 0.99
        calc = CheckStrengthBendingClass3(heb_steel_cross_section, m, axis="My")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99
        
        m = -355 * 0.571 * 0.99
        calc = CheckStrengthBendingClass3(heb_steel_cross_section, m, axis="Mz")
        result = calc.result()
        assert result.is_ok is True
        assert pytest.approx(result.unity_check, 0.005) == 0.99

    def test_invalid_axis(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test ValueError is raised for invalid axis input."""
        with pytest.raises(ValueError):
            CheckStrengthBendingClass3(heb_steel_cross_section, 100, axis="Mx").calculation_formula()

    def test_report(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test report output for bending moment check."""
        m = 100
        calc = CheckStrengthBendingClass3(heb_steel_cross_section, m, axis="My")
        assert calc.report()

    def test_source_docs(self, heb_steel_cross_section: SteelCrossSection) -> None:
        """Test source_docs() method."""
        m = 100
        calc = CheckStrengthBendingClass3(heb_steel_cross_section, m, gamma_m0=1.0)
        docs = calc.source_docs()
        assert isinstance(docs, list)
        assert len(docs) == 1
