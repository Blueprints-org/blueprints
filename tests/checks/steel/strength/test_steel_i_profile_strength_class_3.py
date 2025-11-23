"""Tests for SteelIProfileStrengthClass3.NormalForceCheck according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.forces.result_internal_forces_1d import ResultInternalForce1D
from blueprints.checks.steel.strength.steel_i_profile_strength_class_3 import SteelIProfileStrengthClass3
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile


class TestSteelIProfileStrengthClass3:
    """Tests for SteelIProfileStrengthClass3."""

    def test_check(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(N=0, Vy=0, Vz=0, Mx=0, My=0, Mz=0)
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        assert calc.check() is True
        assert len(calc.latex()) > 0

    def test_latex_all(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test latex output for SteelIProfileStrengthClass3."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(N=1, Vy=1, Vz=1, Mx=1, My=1, Mz=1)
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        latex_output = calc.latex()
        assert calc.check() is True
        assert len(latex_output) > 0

    @pytest.mark.parametrize(
        "forces_kwargs",
        [
            {"N": 0, "Vy": 0, "Vz": 0, "Mx": 0, "My": 0, "Mz": 0},  # none
            {"N": 1, "Vy": 1, "Vz": 1, "Mx": 1, "My": 1, "Mz": 1},  # all
            {"N": 1, "Vy": 0, "Vz": 0, "Mx": 0, "My": 0, "Mz": 0},  # only N
            {"N": 0, "Vy": 1, "Vz": 0, "Mx": 0, "My": 0, "Mz": 0},  # only Vy
            {"N": 0, "Vy": 0, "Vz": 1, "Mx": 0, "My": 0, "Mz": 0},  # only Vz
            {"N": 0, "Vy": 0, "Vz": 0, "Mx": 1, "My": 0, "Mz": 0},  # only Mx
            {"N": 0, "Vy": 0, "Vz": 0, "Mx": 0, "My": 1, "Mz": 0},  # only My
            {"N": 0, "Vy": 0, "Vz": 0, "Mx": 0, "My": 0, "Mz": 1},  # only Mz
            {"N": 0, "Vy": 0, "Vz": 0, "Mx": 0, "My": 1, "Mz": 1},  # My and Mz
            {"N": 0, "Vy": 1, "Vz": 1, "Mx": 0, "My": 1, "Mz": 1},  # My, Mz and Vy, Vz
            {"N": 1, "Vy": 0, "Vz": 0, "Mx": 0, "My": 1, "Mz": 0},  # N and My
            {"N": 1, "Vy": 0, "Vz": 0, "Mx": 0, "My": 0, "Mz": 1},  # N and Mz
        ],
    )
    def test_latex_only_single_force_permutations(
        self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties], forces_kwargs: dict[str, float]
    ) -> None:
        """Test latex output for SteelIProfileStrengthClass3 with 0 and 1 for all N, Vy, Vz, Mx, My, Mz."""
        (heb_profile, heb_properties) = heb_profile_and_properties

        result_internal_forces_1d = ResultInternalForce1D(
            N=forces_kwargs["N"],
            Vy=forces_kwargs["Vy"],
            Vz=forces_kwargs["Vz"],
            Mx=forces_kwargs["Mx"],
            My=forces_kwargs["My"],
            Mz=forces_kwargs["Mz"],
        )
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        latex_output = calc.latex()
        assert calc.check() is True
        assert len(latex_output) > 0

    def test_removal_slashes_at_start(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        r"""Test that latex output does not start with '\\'."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(Mz=1)
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        latex_output = calc.latex()
        assert latex_output[:2] != r"\\"


class TestSteelIProfileStrengthClass3NormalForce:
    """Tests for SteelIProfileStrengthClass3.NormalForce."""

    def test_check_none(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(N=0)
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        assert calc.check() is True
        assert len(calc.latex()) > 0

    def test_check_tension_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for ok tension load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_tension = ResultInternalForce1D(N=355 * 14908 / 1.0 / 1e3 * 0.99)  # 99% of capacity
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, load_tension, gamma_m0=1.0)
        assert calc.check() is True

    def test_check_tension_not_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for not ok tension load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_tension = ResultInternalForce1D(N=355 * 14908 / 1.0 / 1e3 * 1.01)  # 101% of capacity
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, load_tension, gamma_m0=1.0)
        assert calc.check() is False

    def test_check_compression_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for ok compression load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_compression = ResultInternalForce1D(N=-355 * 14908 / 1.0 / 1e3 * 0.99)  # 99% of capacity
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, load_compression, gamma_m0=1.0)
        assert calc.check() is True

    def test_check_compression_not_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for not ok compression load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_compression = ResultInternalForce1D(N=-355 * 14908 / 1.0 / 1e3 * 1.01)  # 101% of capacity
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, load_compression, gamma_m0=1.0)
        assert calc.check() is False

    def test_latex_compression_summary(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test summary latex output."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_compression = ResultInternalForce1D(N=-100)
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, load_compression, gamma_m0=1.0)
        latex_output = calc.latex(summary=True)
        expected = (
            r"\text{Normal force check compression checks applied using chapter 6.2.4.}"
            r"\\CHECK \to \left( \frac{N_{Ed}}{N_{c,Rd}} \leq 1 \right) \to \left( "
            r"\frac{100000.0}{5293746.7} \leq 1 \right) \to OK"
        )
        assert expected == latex_output

    def test_latex_compression_long(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test long latex output."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_compression = ResultInternalForce1D(N=-100)
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, load_compression, gamma_m0=1.0)
        latex_output = calc.latex(summary=False)
        expected = (
            r"\text{Normal force check compression checks applied using chapter 6.2.4.}\\"
            r"\text{With formula 6.10:}\\N_{c,Rd} = \frac{A \cdot f_y}{\gamma_{M0}} = "
            r"\frac{14912.0 \cdot 355.0}{1.0} = 5293746.7 \ N\\\text{With formula 6.9:}\\CHECK "
            r"\to \left( \frac{N_{Ed}}{N_{c,Rd}} \leq 1 \right) \to \left( \frac{100000.0}{5293746.7} "
            r"\leq 1 \right) \to OK"
        )
        assert expected == latex_output

    def test_latex_tension(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test latex output with summary flag for tension."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_tension = ResultInternalForce1D(N=100)
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, load_tension, gamma_m0=1.0)
        latex_output = calc.latex()
        expected = (
            r"\text{Normal force check tension checks applied using chapter 6.2.3.}\\"
            r"\text{With formula 6.6:}\\N_{pl,Rd} = \frac{A \cdot f_y}{\gamma_{M0}} = "
            r"\frac{14912.0 \cdot 355.0}{1.0} = 5293746.7 \ N\\\text{With formula 6.5:}\\CHECK "
            r"\to \left( \frac{N_{Ed}}{N_{t,Rd}} \leq 1 \right) \to \left( \frac{100000.0}{5293746.7} "
            r"\leq 1 \right) \to OK"
        )
        assert expected == latex_output


class TestSteelIProfileStrengthClass3SingleAxisBendingMoment:
    """Tests for SteelIProfileStrengthClass3.SingleAxisBendingMoment."""

    def test_check_none(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(My=0)
        calc = SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        assert calc.check() is True
        assert len(calc.latex()) > 0

    def test_check_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for ok load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(My=355 * 1678000 / 1.0 / 1e6 * 0.99)  # 99% of capacity
        calc = SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        assert calc.check() is True

    def test_check_not_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for not ok load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(My=355 * 1678000 / 1.0 / 1e6 * 1.01)  # 101% of capacity
        calc = SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        assert calc.check() is False

    def test_negative(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for ok load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(My=-355 * 1678000 / 1.0 / 1e6 * 0.99)  # 99% of capacity, opposite sign
        calc = SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        assert calc.check() is True

    def test_check_weak_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for ok load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(Mz=355 * 571000 / 1.0 / 1e6 * 0.99)  # 99% of capacity
        calc = SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, axis="Mz", gamma_m0=1.0)
        assert calc.check() is True

    def test_check_weak_not_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for not ok load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(Mz=355 * 571000 / 1.0 / 1e6 * 1.01)  # 101% of capacity
        calc = SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, axis="Mz", gamma_m0=1.0)
        assert calc.check() is False

    def test_invalid_axis(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test that invalid axis raises ValueError."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(My=100)
        with pytest.raises(ValueError):
            SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, axis="invalid", gamma_m0=1.0)

    def test_latex_summary(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test summary latex output."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(My=100)
        calc = SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        latex_output = calc.latex(summary=True)
        expected = (
            r"\text{Bending moment My axis checks applied using chapter 6.2.5.}"
            r"\\ CHECK \to \left( \frac{M_{Ed}}{M_{c,Rd}} \leq 1 \right) \to \left( \frac{100000000.0}{595733834.6} \leq 1 \right) \to OK"
        )
        assert expected == latex_output

    def test_latex_compression_long(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test long latex output."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(My=100)
        calc = SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        latex_output = calc.latex(summary=False)
        expected = (
            r"\text{Bending moment My axis checks applied using chapter 6.2.5.}"
            r"\\ \text{With formula 6.14:}\\M_{c,Rd} = \frac{W_{el,min} \cdot f_y}{\gamma_{M0}} = "
            r"\frac{1678123.5 \cdot 355.0}{1.0} = 595733834.6 \ Nmm\\ \text{With formula 6.12:}\\CHECK \to "
            r"\left( \frac{M_{Ed}}{M_{c,Rd}} \leq 1 \right) \to \left( \frac{100000000.0}{595733834.6} \leq 1 \right) \to OK"
        )
        assert expected == latex_output

    def test_latex_weak_axis_summary(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test summary latex output for weak axis."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(Mz=100)
        calc = SteelIProfileStrengthClass3.SingleAxisBendingMoment(heb_profile, heb_properties, result_internal_forces_1d, axis="Mz", gamma_m0=1.0)
        latex_output = calc.latex(summary=True)
        assert len(latex_output) > 0


class TestSteelIProfileStrengthClass3NotImplemented:
    """Tests for not implemented checks in SteelIProfileStrengthClass3."""

    def test_shear_force_not_implemented(self) -> None:
        """Test that shear force check raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            SteelIProfileStrengthClass3.ShearForce()

    def test_torsion_not_implemented(self) -> None:
        """Test that torsion check raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            SteelIProfileStrengthClass3.Torsion()

    def test_bending_and_shear_not_implemented(self) -> None:
        """Test that bending and shear check raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            SteelIProfileStrengthClass3.BendingAndShear()

    def test_multi_bending_and_axial_force_not_implemented(self) -> None:
        """Test that multi bending and axial force check raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            SteelIProfileStrengthClass3.MultiBendingAndAxialForce()

    def test_multi_bending_shear_and_axial_force_not_implemented(self) -> None:
        """Test that multi bending, shear, and axial force check raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            SteelIProfileStrengthClass3.MultiBendingShearAndAxialForce()
