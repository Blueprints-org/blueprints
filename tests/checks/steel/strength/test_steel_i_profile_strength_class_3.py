"""Tests for SteelIProfileStrengthClass3.NormalForceCheck according to Eurocode 3."""

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

    def test_latex(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test latex output for SteelIProfileStrengthClass3."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(N=0, Vy=0, Vz=0, Mx=0, My=0, Mz=0)
        calc = SteelIProfileStrengthClass3(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        latex_output = calc.latex()
        assert len(latex_output) > 0


class TestSteelIProfileStrengthClass3NormalForceCheck:
    """Tests for SteelIProfileStrengthClass3.NormalForcecalc."""

    def test_check_none(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(N=0)
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        assert calc.check() is True

    def test_check_tension(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for tension load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_tension = ResultInternalForce1D(N=100)
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, load_tension, gamma_m0=1.0)
        assert calc.check() is True

    def test_check_compression(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for compression load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_compression = ResultInternalForce1D(N=-100)
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, load_compression, gamma_m0=1.0)
        assert calc.check() is True

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
        assert len(latex_output) > 0

    def test_latex_none(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test latex output with summary flag for no normal force."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_forces_1d = ResultInternalForce1D(N=0)
        calc = SteelIProfileStrengthClass3.NormalForce(heb_profile, heb_properties, result_internal_forces_1d, gamma_m0=1.0)
        latex_output = calc.latex()
        assert len(latex_output) > 0
