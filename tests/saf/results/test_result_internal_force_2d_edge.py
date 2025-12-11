"""Tests for ResultInternalForce2DEdge dataclass."""

import pytest

from blueprints.saf.results.result_internal_force_2d_edge import (
    ResultFor,
    ResultInternalForce2DEdge,
    ResultOn2DEdge,
)


class TestResultInternalForce2DEdge:
    """Tests for ResultInternalForce2DEdge dataclass."""

    def test_result_internal_force_2d_edge_with_load_case(self) -> None:
        """Test valid initialization for 2D edge result with load case."""
        result = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            section_at=0.5,
            index=1,
            mx=10.0,
            my=20.0,
            mxy=5.0,
            vx=15.0,
            vy=25.0,
            nx=30.0,
            ny=35.0,
            nxy=40.0,
        )

        assert result.result_on == ResultOn2DEdge.ON_EDGE
        assert result.member_2d == "SLAB1"
        assert result.edge == 1
        assert result.result_for == ResultFor.LOAD_CASE
        assert result.load_case == "LC1"
        assert result.load_combination == ""
        assert result.section_at == 0.5
        assert result.index == 1
        assert result.mx == 10.0
        assert result.my == 20.0
        assert result.mxy == 5.0
        assert result.vx == 15.0
        assert result.vy == 25.0
        assert result.nx == 30.0
        assert result.ny == 35.0
        assert result.nxy == 40.0

    def test_result_internal_force_2d_edge_with_load_combination(self) -> None:
        """Test valid initialization for 2D edge result with load combination."""
        result = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_COMBINATION,
            member_2d="WALL1",
            edge=3,
            load_combination="COM1",
            combination_key="1.35*LC1+1.5*LC2",
            section_at=1.0,
            index=2,
            mx=12.0,
            my=22.0,
            mxy=6.0,
            vx=16.0,
            vy=26.0,
            nx=32.0,
            ny=37.0,
            nxy=42.0,
        )

        assert result.result_on == ResultOn2DEdge.ON_EDGE
        assert result.member_2d == "WALL1"
        assert result.edge == 3
        assert result.result_for == ResultFor.LOAD_COMBINATION
        assert result.load_case == ""
        assert result.load_combination == "COM1"
        assert result.combination_key == "1.35*LC1+1.5*LC2"
        assert result.section_at == 1.0
        assert result.index == 2

    def test_accepts_negative_force_values(self) -> None:
        """Test that negative force values are accepted."""
        result = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            mx=-10.0,
            my=-20.0,
            mxy=-5.0,
            vx=-15.0,
            vy=-25.0,
            nx=-30.0,
            ny=-35.0,
            nxy=-40.0,
        )

        assert result.mx == -10.0
        assert result.my == -20.0
        assert result.mxy == -5.0
        assert result.vx == -15.0
        assert result.vy == -25.0
        assert result.nx == -30.0
        assert result.ny == -35.0
        assert result.nxy == -40.0

    def test_accepts_zero_force_values(self) -> None:
        """Test that zero force values are accepted."""
        result = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            mx=0.0,
            my=0.0,
            mxy=0.0,
            vx=0.0,
            vy=0.0,
            nx=0.0,
            ny=0.0,
            nxy=0.0,
        )

        assert result.mx == 0.0
        assert result.my == 0.0
        assert result.mxy == 0.0
        assert result.vx == 0.0
        assert result.vy == 0.0
        assert result.nx == 0.0
        assert result.ny == 0.0
        assert result.nxy == 0.0

    def test_member_2d_is_required(self) -> None:
        """Test that member_2d is required."""
        with pytest.raises(ValueError, match=r"member_2d must be specified"):
            ResultInternalForce2DEdge(
                result_on=ResultOn2DEdge.ON_EDGE,
                result_for=ResultFor.LOAD_CASE,
                member_2d="",  # Empty member_2d is invalid
                edge=1,
                load_case="LC1",
            )

    def test_edge_must_be_at_least_one(self) -> None:
        """Test that edge must be >= 1 according to SAF specification."""
        with pytest.raises(ValueError, match=r"edge must be >= 1"):
            ResultInternalForce2DEdge(
                result_on=ResultOn2DEdge.ON_EDGE,
                result_for=ResultFor.LOAD_CASE,
                member_2d="SLAB1",
                edge=0,  # Invalid: must be >= 1
                load_case="LC1",
            )

    def test_load_case_requires_load_case_name(self) -> None:
        """Test that result_for=LOAD_CASE requires load_case to be specified."""
        with pytest.raises(
            ValueError,
            match=r"load_case must be specified when result_for = ResultFor\.LOAD_CASE",
        ):
            ResultInternalForce2DEdge(
                result_on=ResultOn2DEdge.ON_EDGE,
                result_for=ResultFor.LOAD_CASE,
                member_2d="SLAB1",
                edge=1,
                load_case="",  # Empty load_case is invalid
            )

    def test_load_combination_requires_load_combination_name(self) -> None:
        """Test that result_for=LOAD_COMBINATION requires load_combination to be specified."""
        with pytest.raises(
            ValueError,
            match=r"load_combination must be specified when result_for = ResultFor\.LOAD_COMBINATION",
        ):
            ResultInternalForce2DEdge(
                result_on=ResultOn2DEdge.ON_EDGE,
                result_for=ResultFor.LOAD_COMBINATION,
                member_2d="SLAB1",
                edge=1,
                load_combination="",  # Empty load_combination is invalid
            )

    def test_index_must_be_at_least_one(self) -> None:
        """Test that index must be >= 1 according to SAF specification."""
        with pytest.raises(ValueError, match=r"index must be >= 1"):
            ResultInternalForce2DEdge(
                result_on=ResultOn2DEdge.ON_EDGE,
                result_for=ResultFor.LOAD_CASE,
                member_2d="SLAB1",
                edge=1,
                load_case="LC1",
                index=0,  # Invalid: must be >= 1
            )

    def test_index_default_is_one(self) -> None:
        """Test that default index value is 1 (SAF compliance)."""
        result = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
        )
        assert result.index == 1

    def test_result_internal_force_2d_edge_equality(self) -> None:
        """Test that two instances with same values are equal."""
        result1 = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            mx=10.0,
            my=20.0,
            mxy=5.0,
        )
        result2 = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            mx=10.0,
            my=20.0,
            mxy=5.0,
        )

        assert result1 == result2

    def test_result_internal_force_2d_edge_inequality(self) -> None:
        """Test that two instances with different values are not equal."""
        result1 = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            mx=10.0,
        )
        result2 = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            mx=20.0,
        )

        assert result1 != result2

    def test_result_internal_force_2d_edge_hashable(self) -> None:
        """Test that instances are hashable (can be used in sets/dicts)."""
        result1 = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            mx=10.0,
            my=20.0,
        )
        result2 = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            mx=10.0,
            my=20.0,
        )

        result_set = {result1, result2}
        assert len(result_set) == 1

    def test_combination_key_is_optional(self) -> None:
        """Test that combination_key is optional and can be omitted."""
        result = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
        )
        assert result.combination_key == ""

    def test_section_at_can_be_zero(self) -> None:
        """Test that section_at can have any non-negative value including zero."""
        result = ResultInternalForce2DEdge(
            result_on=ResultOn2DEdge.ON_EDGE,
            result_for=ResultFor.LOAD_CASE,
            member_2d="SLAB1",
            edge=1,
            load_case="LC1",
            section_at=0.0,
        )
        assert result.section_at == 0.0

    def test_multiple_edges_on_same_member(self) -> None:
        """Test that multiple edges (1, 2, 3, 4) can be specified on same member."""
        for edge_num in [1, 2, 3, 4]:
            result = ResultInternalForce2DEdge(
                result_on=ResultOn2DEdge.ON_EDGE,
                result_for=ResultFor.LOAD_CASE,
                member_2d="SLAB1",
                edge=edge_num,
                load_case="LC1",
            )
            assert result.edge == edge_num
