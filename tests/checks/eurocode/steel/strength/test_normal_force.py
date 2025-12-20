"""Tests for NormalForceClass123Check according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.checks.eurocode.steel.strength.normal_force import NormalForceClass123
from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile


class TestSteelIProfileStrengthClass3NormalForce:
    """Tests for NormalForceClass123."""

    def test_check_none(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() returns True for no normal force."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        result_internal_force_1d = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=0
        )
        calc = NormalForceClass123(heb_profile, heb_properties, result_internal_force_1d, gamma_m0=1.0)
        assert calc.check() is True
        assert len(calc.latex()) > 0

    def test_check_tension_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for ok tension load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_tension = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=355 * 14908 / 1.0 / 1e3 * 0.99
        )  # 99% of capacity
        calc = NormalForceClass123(heb_profile, heb_properties, load_tension, gamma_m0=1.0)
        assert calc.check() is True

    def test_check_tension_not_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for not ok tension load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_tension = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=355 * 14908 / 1.0 / 1e3 * 1.01
        )  # 101% of capacity
        calc = NormalForceClass123(heb_profile, heb_properties, load_tension, gamma_m0=1.0)
        assert calc.check() is False

    def test_check_compression_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for ok compression load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_compression = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=-355 * 14908 / 1.0 / 1e3 * 0.99
        )  # 99% of capacity
        calc = NormalForceClass123(heb_profile, heb_properties, load_compression, gamma_m0=1.0)
        assert calc.check() is True

    def test_check_compression_not_ok(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test check() for not ok compression load."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_compression = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=-355 * 14908 / 1.0 / 1e3 * 1.01
        )  # 101% of capacity
        calc = NormalForceClass123(heb_profile, heb_properties, load_compression, gamma_m0=1.0)
        assert calc.check() is False

    def test_latex_compression_summary(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test summary latex output."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_compression = ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=-100)
        calc = NormalForceClass123(heb_profile, heb_properties, load_compression, gamma_m0=1.0)
        latex_output = calc.latex(latex_format="summary")
        expected = (
            r"\text{Checking normal force (compression) using chapter 6.2.4.}\newline "
            r"CHECK \to \left( \frac{N_{Ed}}{N_{c,Rd}} \leq 1 \right) \to \left( "
            r"\frac{100000.0}{5293746.7} \leq 1 \right) \to \left( 0.0 \leq 1 \right) \to OK "
        )
        assert expected == latex_output

    def test_latex_compression_long(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test long latex output."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_compression = ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=-100)
        calc = NormalForceClass123(heb_profile, heb_properties, load_compression, gamma_m0=1.0)
        latex_output = calc.latex(latex_format="long")
        expected = (
            r"\text{Checking normal force (compression) using chapter 6.2.4.}\newline "
            r"\text{With formula 6.10:} \newline N_{c,Rd} = \frac{A \cdot f_y}{\gamma_{M0}} = "
            r"\frac{14912.0 \cdot 355.0}{1.0} = 5293746.7 \ N \newline \text{With formula 6.9:} \newline CHECK "
            r"\to \left( \frac{N_{Ed}}{N_{c,Rd}} \leq 1 \right) \to \left( \frac{100000.0}{5293746.7} "
            r"\leq 1 \right) \to \left( 0.0 \leq 1 \right) \to OK "
        )
        assert expected == latex_output

    def test_latex_tension(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test latex output with summary flag for tension."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_tension = ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=100)
        calc = NormalForceClass123(heb_profile, heb_properties, load_tension, gamma_m0=1.0)
        latex_output = calc.latex()
        expected = (
            r"\text{Checking normal force (tension) using chapter 6.2.3.}\newline "
            r"\text{With formula 6.6:} \newline N_{pl,Rd} = \frac{A \cdot f_y}{\gamma_{M0}} = "
            r"\frac{14912.0 \cdot 355.0}{1.0} = 5293746.7 \ N \newline \text{With formula 6.5:} \newline CHECK "
            r"\to \left( \frac{N_{Ed}}{N_{t,Rd}} \leq 1 \right) \to \left( \frac{100000.0}{5293746.7} "
            r"\leq 1 \right) \to \left( 0.0 \leq 1 \right) \to OK "
        )
        assert expected == latex_output

    def test_latex_wrong_format(self, heb_profile_and_properties: tuple[ISteelProfile, SectionProperties]) -> None:
        """Test that wrong format raises ValueError."""
        (heb_profile, heb_properties) = heb_profile_and_properties
        load_tension = ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", n=100)
        calc = NormalForceClass123(heb_profile, heb_properties, load_tension, gamma_m0=1.0)

        with pytest.raises(ValueError):
            calc.latex(latex_format="table")
