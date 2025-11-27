"""Tests for ResultInternalForce1D dataclass."""

import pytest

from blueprints.saf.results.result_internal_force_1d import (
    ResultFor,
    ResultInternalForce1D,
    ResultOn,
)


class TestResultInternalForce1D:
    """Tests for ResultInternalForce1D dataclass."""

    def test_result_internal_force_1d_on_beam_with_load_case(self) -> None:
        """Test valid initialization for result on beam with load case."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
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
        assert result.member == "B1"
        assert result.member_rib == ""
        assert result.result_for == ResultFor.LOAD_CASE
        assert result.load_case == "LC1"
        assert result.load_combination == ""
        assert result.combination_key == "1.35*LC1+1.5*LC2"
        assert result.section_at == 0.1
        assert result.index == 1
        assert result.n == 100.0
        assert result.vy == 20.0
        assert result.vz == 30.0
        assert result.mx == 10.0
        assert result.my == 50.0
        assert result.mz == 60.0

    def test_result_internal_force_1d_on_rib_with_load_combination(self) -> None:
        """Test valid initialization for result on rib with load combination."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_RIB,
            member_rib="R1",
            result_for=ResultFor.LOAD_COMBINATION,
            load_combination="COM1",
            section_at=0.5,
            index=2,
            n=150.0,
            vy=25.0,
            vz=35.0,
            mx=15.0,
            my=55.0,
            mz=65.0,
        )

        assert result.result_on == ResultOn.ON_RIB
        assert result.member == ""
        assert result.member_rib == "R1"
        assert result.result_for == ResultFor.LOAD_COMBINATION
        assert result.load_case == ""
        assert result.load_combination == "COM1"
        assert result.section_at == 0.5
        assert result.index == 2

    def test_result_internal_force_1d_accepts_negative_force_values(self) -> None:
        """Test that ResultInternalForce1D accepts negative force values (compression)."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
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

    def test_result_internal_force_1d_accepts_zero_force_values(self) -> None:
        """Test that ResultInternalForce1D accepts zero force values."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=0.0,
            vy=0.0,
            vz=0.0,
            mx=0.0,
            my=0.0,
            mz=0.0,
        )

        assert result.n == 0.0
        assert result.vy == 0.0
        assert result.vz == 0.0
        assert result.mx == 0.0
        assert result.my == 0.0
        assert result.mz == 0.0

    def test_on_beam_requires_member(self) -> None:
        """Test that result_on=ON_BEAM requires member to be specified."""
        with pytest.raises(
            ValueError,
            match=r"member must be specified when result_on = ResultOn\.ON_BEAM",
        ):
            ResultInternalForce1D(
                result_on=ResultOn.ON_BEAM,
                member="",  # Empty member is invalid
                result_for=ResultFor.LOAD_CASE,
                load_case="LC1",
            )

    def test_on_rib_requires_member_rib(self) -> None:
        """Test that result_on=ON_RIB requires member_rib to be specified."""
        with pytest.raises(
            ValueError,
            match=r"member_rib must be specified when result_on = ResultOn\.ON_RIB",
        ):
            ResultInternalForce1D(
                result_on=ResultOn.ON_RIB,
                member_rib="",  # Empty member_rib is invalid
                result_for=ResultFor.LOAD_CASE,
                load_case="LC1",
            )

    def test_load_case_requires_load_case_name(self) -> None:
        """Test that result_for=LOAD_CASE requires load_case to be specified."""
        with pytest.raises(
            ValueError,
            match=r"load_case must be specified when result_for = ResultFor\.LOAD_CASE",
        ):
            ResultInternalForce1D(
                result_on=ResultOn.ON_BEAM,
                member="B1",
                result_for=ResultFor.LOAD_CASE,
                load_case="",  # Empty load_case is invalid
            )

    def test_load_combination_requires_load_combination_name(self) -> None:
        """Test that result_for=LOAD_COMBINATION requires load_combination to be specified."""
        with pytest.raises(
            ValueError,
            match=r"load_combination must be specified when result_for = ResultFor\.LOAD_COMBINATION",
        ):
            ResultInternalForce1D(
                result_on=ResultOn.ON_BEAM,
                member="B1",
                result_for=ResultFor.LOAD_COMBINATION,
                load_combination="",  # Empty load_combination is invalid
            )

    def test_index_must_be_at_least_one(self) -> None:
        """Test that index must be >= 1 according to SAF specification."""
        with pytest.raises(
            ValueError,
            match=r"index must be >= 1",
        ):
            ResultInternalForce1D(
                result_on=ResultOn.ON_BEAM,
                member="B1",
                result_for=ResultFor.LOAD_CASE,
                load_case="LC1",
                index=0,  # Invalid: must be >= 1
            )

    def test_index_default_is_one(self) -> None:
        """Test that default index value is 1 (SAF compliance)."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
        )
        assert result.index == 1

    def test_result_internal_force_1d_equality(self) -> None:
        """Test that two instances with same values are equal."""
        result1 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=100.0,
            vy=20.0,
            vz=30.0,
            mx=10.0,
            my=50.0,
            mz=60.0,
        )
        result2 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=100.0,
            vy=20.0,
            vz=30.0,
            mx=10.0,
            my=50.0,
            mz=60.0,
        )

        assert result1 == result2

    def test_result_internal_force_1d_inequality(self) -> None:
        """Test that two instances with different values are not equal."""
        result1 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=100.0,
        )
        result2 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=200.0,
        )

        assert result1 != result2

    def test_result_internal_force_1d_hashable(self) -> None:
        """Test that instances are hashable (can be used in sets/dicts)."""
        result1 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=100.0,
            vy=20.0,
        )
        result2 = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
            n=100.0,
            vy=20.0,
        )

        result_set = {result1, result2}
        assert len(result_set) == 1

    def test_combination_key_is_optional(self) -> None:
        """Test that combination_key is optional and can be omitted."""
        result = ResultInternalForce1D(
            result_on=ResultOn.ON_BEAM,
            member="B1",
            result_for=ResultFor.LOAD_CASE,
            load_case="LC1",
        )
        assert result.combination_key == ""
