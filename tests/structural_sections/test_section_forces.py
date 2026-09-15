"""Tests for the SectionForces dataclass."""

import pytest

from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn
from blueprints.structural_sections.section_forces import SectionForces


class TestSectionForces:
    """Test class for the SectionForces object."""

    def test_defaults_are_zero(self) -> None:
        """All six components default to zero."""
        forces = SectionForces()
        assert forces.n == 0.0
        assert forces.v_y == 0.0
        assert forces.v_z == 0.0
        assert forces.t == 0.0
        assert forces.m_y == 0.0
        assert forces.m_z == 0.0

    def test_full_construction(self) -> None:
        """All six components are stored as given."""
        forces = SectionForces(n=-100.0, v_y=10.0, v_z=20.0, t=5.0, m_y=150.0, m_z=30.0)
        assert forces.n == -100.0
        assert forces.v_y == 10.0
        assert forces.v_z == 20.0
        assert forces.t == 5.0
        assert forces.m_y == 150.0
        assert forces.m_z == 30.0

    def test_is_frozen(self) -> None:
        """SectionForces is immutable."""
        forces = SectionForces(n=-100.0)
        with pytest.raises(AttributeError):
            forces.n = 0.0  # type: ignore[misc]

    def test_from_saf_result(self) -> None:
        """from_saf_result maps every component (mx -> t) without unit or sign conversion."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=-100.0,
            vy=10.0,
            vz=20.0,
            mx=5.0,
            my=150.0,
            mz=30.0,
        )
        forces = SectionForces.from_saf_result(result)
        assert forces == SectionForces(n=-100.0, v_y=10.0, v_z=20.0, t=5.0, m_y=150.0, m_z=30.0)
