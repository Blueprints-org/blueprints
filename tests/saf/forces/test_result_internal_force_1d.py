"""Tests for ResultInternalForce1D dataclass."""

import pytest

from blueprints.saf.results.result_internal_force_1d import ResultFor, ResultInternalForce1D, ResultOn


class TestResultInternalForce1D:
    """Tests for ResultInternalForce1D dataclass."""

    def test_result_internal_force_1d_initialization(self) -> None:
        """Test that ResultInternalForce1D can be initialized with all parameters."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            member_rib="M2",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            load_combination="COM1",
            combination_key="1.35*LC1+1.5*LC2",
            section_at=0.1,
            index=1,
            n=100.0,
            vy=20.0,
            vz=30.0,
            mx=10.0,
            my=50.0,
            mz=60.0,
        )

        assert result.result_on == ResultOn.ON_BEAM
        assert result.member == "M1"
        assert result.member_rib == "M2"
        assert result.result_for == ResultFor.LOAD_CASE
        assert result.load_case == "LC1"
        assert result.load_combination == "COM1"
        assert result.combination_key == "1.35*LC1+1.5*LC2"
        assert result.section_at == 0.1
        assert result.index == 1
        assert result.n == 100.0
        assert result.vy == 20.0
        assert result.vz == 30.0
        assert result.mx == 10.0
        assert result.my == 50.0
        assert result.mz == 60.0

    def test_result_internal_force_1d_with_negative_values(self) -> None:
        """Test that ResultInternalForce1D accepts negative values (compression, etc.)."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=-150.0,
            vy=-25.0,
            vz=-35.0,
            mx=-15.0,
            my=-55.0,
            mz=-65.0,
        )

        assert result.n == -150.0
        assert result.vy == -25.0
        assert result.vz == -35.0
        assert result.mx == -15.0
        assert result.my == -55.0
        assert result.mz == -65.0

    def test_result_internal_force_1d_with_zero_values(self) -> None:
        """Test that ResultInternalForce1D accepts zero values."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_RIB,
            member_rib="M2",
            result_for=ResultFor.LOAD_COMBINATION,
            load_combination="COM1",
        )
        assert result.n == 0
        assert result.vy == 0
        assert result.vz == 0
        assert result.mx == 0
        assert result.my == 0
        assert result.mz == 0

    def test_result_internal_force_1d_equality(self) -> None:
        """Test that two ResultInternalForce1D instances with same values are equal."""
        result1 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            member_rib="",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            load_combination="",
            combination_key="",
            section_at=0,
            index=1,
            n=100.0,
            vy=20.0,
            vz=30.0,
            mx=10.0,
            my=50.0,
            mz=60.0,
        )
        result2 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            member_rib="",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            load_combination="",
            combination_key="",
            section_at=0,
            index=1,
            n=100.0,
            vy=20.0,
            vz=30.0,
            mx=10.0,
            my=50.0,
            mz=60.0,
        )

        assert result1 == result2

    def test_result_internal_force_1d_inequality(self) -> None:
        """Test that two ResultInternalForce1D instances with different values are not equal."""
        result1 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            member_rib="",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            load_combination="",
            combination_key="",
            section_at=0,
            index=1,
            n=100.0,
            vy=20.0,
            vz=30.0,
            mx=10.0,
            my=50.0,
            mz=60.0,
        )
        result2 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            member_rib="",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            load_combination="",
            combination_key="",
            section_at=0,
            index=1,
            n=200.0,
            vy=20.0,
            vz=30.0,
            mx=10.0,
            my=50.0,
            mz=60.0,
        )

        assert result1 != result2

    def test_result_internal_force_1d_hashable(self) -> None:
        """Test that ResultInternalForce1D instances are hashable (can be used in sets/dicts)."""
        result1 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            member_rib="",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            load_combination="",
            combination_key="",
            section_at=0,
            index=1,
            n=100.0,
            vy=20.0,
            vz=30.0,
            mx=10.0,
            my=50.0,
            mz=60.0,
        )
        result2 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="M1",
            member_rib="",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            load_combination="",
            combination_key="",
            section_at=0,
            index=1,
            n=100.0,
            vy=20.0,
            vz=30.0,
            mx=10.0,
            my=50.0,
            mz=60.0,
        )

        result_set = {result1, result2}
        assert len(result_set) == 1

    def test_missing_member_raises_value_error(self) -> None:
        """Test that missing member raises ValueError when result_on is ON_BEAM."""
        with pytest.raises(ValueError, match="member must be specified when"):
            ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="", result_for=ResultFor.LOAD_CASE, load_case="LC1")

    def test_missing_member_rib_raises_value_error(self) -> None:
        """Test that missing member_rib raises ValueError when result_on is ON_RIB."""
        with pytest.raises(ValueError, match="member_rib must be specified when"):
            ResultInternalForce1D(result_on=ResultOn.ON_RIB, member_rib="", result_for=ResultFor.LOAD_COMBINATION, load_combination="COM1")

    def test_missing_load_case_raises_value_error(self) -> None:
        """Test that missing load_case raises ValueError when result_for is LOAD_CASE."""
        with pytest.raises(ValueError, match="load_case must be specified when"):
            ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="")

    def test_missing_load_combination_raises_value_error(self) -> None:
        """Test that missing load_combination raises ValueError when result_for is LOAD_COMBINATION."""
        with pytest.raises(ValueError, match="load_combination must be specified when"):
            ResultInternalForce1D(result_on=ResultOn.ON_RIB, member_rib="M2", result_for=ResultFor.LOAD_COMBINATION, load_combination="")

    def test_index_less_than_one_raises_value_error(self) -> None:
        """Test that index < 1 raises ValueError."""
        with pytest.raises(ValueError, match="index must be >= 1"):
            ResultInternalForce1D(result_on=ResultOn.ON_BEAM, member="M1", result_for=ResultFor.LOAD_CASE, load_case="LC1", index=0)
