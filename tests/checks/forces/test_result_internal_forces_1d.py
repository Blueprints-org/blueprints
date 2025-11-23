"""Tests for ResultInternalForce1D dataclass."""

from blueprints.checks.forces.result_internal_forces_1d import ResultInternalForce1D


class TestResultInternalForce1D:
    """Tests for ResultInternalForce1D dataclass."""

    def test_result_internal_force_1d_initialization(self) -> None:
        """Test that ResultInternalForce1D can be initialized with all parameters."""
        result = ResultInternalForce1D(
            result_on="On beam",
            member="B1",
            member_rib="B2",
            result_for="Load case",
            load_case="LC1",
            load_combination="COM1",
            combination_key="1.35*LC1+1.5*LC2",
            section_at=0.1,
            index=1,
            N=100.0,
            Vy=20.0,
            Vz=30.0,
            Mx=10.0,
            My=50.0,
            Mz=60.0,
        )

        assert result.result_on == "On beam"
        assert result.member == "B1"
        assert result.member_rib == "B2"
        assert result.result_for == "Load case"
        assert result.load_case == "LC1"
        assert result.load_combination == "COM1"
        assert result.combination_key == "1.35*LC1+1.5*LC2"
        assert result.section_at == 0.1
        assert result.index == 1
        assert result.N == 100.0
        assert result.Vy == 20.0
        assert result.Vz == 30.0
        assert result.Mx == 10.0
        assert result.My == 50.0
        assert result.Mz == 60.0

    def test_result_internal_force_1d_with_negative_values(self) -> None:
        """Test that ResultInternalForce1D accepts negative values (compression, etc.)."""
        result = ResultInternalForce1D(
            result_on="",
            member="",
            member_rib="",
            result_for="",
            load_case="",
            load_combination="",
            combination_key="",
            section_at=0,
            index=0,
            N=-150.0,
            Vy=-25.0,
            Vz=-35.0,
            Mx=-15.0,
            My=-55.0,
            Mz=-65.0,
        )

        assert result.N == -150.0
        assert result.Vy == -25.0
        assert result.Vz == -35.0
        assert result.Mx == -15.0
        assert result.My == -55.0
        assert result.Mz == -65.0

    def test_result_internal_force_1d_with_zero_values(self) -> None:
        """Test that ResultInternalForce1D accepts zero values."""
        result = ResultInternalForce1D()

        assert result.result_on == ""
        assert result.member == ""
        assert result.member_rib == ""
        assert result.result_for == ""
        assert result.load_case == ""
        assert result.load_combination == ""
        assert result.combination_key == ""
        assert result.section_at == 0
        assert result.index == 0
        assert result.N == 0
        assert result.Vy == 0
        assert result.Vz == 0
        assert result.Mx == 0
        assert result.My == 0
        assert result.Mz == 0

    def test_result_internal_force_1d_equality(self) -> None:
        """Test that two ResultInternalForce1D instances with same values are equal."""
        result1 = ResultInternalForce1D(
            result_on="",
            member="",
            member_rib="",
            result_for="",
            load_case="",
            load_combination="",
            combination_key="",
            section_at=0,
            index=0,
            N=100.0,
            Vy=20.0,
            Vz=30.0,
            Mx=10.0,
            My=50.0,
            Mz=60.0,
        )
        result2 = ResultInternalForce1D(
            result_on="",
            member="",
            member_rib="",
            result_for="",
            load_case="",
            load_combination="",
            combination_key="",
            section_at=0,
            index=0,
            N=100.0,
            Vy=20.0,
            Vz=30.0,
            Mx=10.0,
            My=50.0,
            Mz=60.0,
        )

        assert result1 == result2

    def test_result_internal_force_1d_inequality(self) -> None:
        """Test that two ResultInternalForce1D instances with different values are not equal."""
        result1 = ResultInternalForce1D(
            result_on="",
            member="",
            member_rib="",
            result_for="",
            load_case="",
            load_combination="",
            combination_key="",
            section_at=0,
            index=0,
            N=100.0,
            Vy=20.0,
            Vz=30.0,
            Mx=10.0,
            My=50.0,
            Mz=60.0,
        )
        result2 = ResultInternalForce1D(
            result_on="",
            member="",
            member_rib="",
            result_for="",
            load_case="",
            load_combination="",
            combination_key="",
            section_at=0,
            index=0,
            N=200.0,
            Vy=20.0,
            Vz=30.0,
            Mx=10.0,
            My=50.0,
            Mz=60.0,
        )

        assert result1 != result2

    def test_result_internal_force_1d_hashable(self) -> None:
        """Test that ResultInternalForce1D instances are hashable (can be used in sets/dicts)."""
        result1 = ResultInternalForce1D(
            result_on="",
            member="",
            member_rib="",
            result_for="",
            load_case="",
            load_combination="",
            combination_key="",
            section_at=0,
            index=0,
            N=100.0,
            Vy=20.0,
            Vz=30.0,
            Mx=10.0,
            My=50.0,
            Mz=60.0,
        )
        result2 = ResultInternalForce1D(
            result_on="",
            member="",
            member_rib="",
            result_for="",
            load_case="",
            load_combination="",
            combination_key="",
            section_at=0,
            index=0,
            N=100.0,
            Vy=20.0,
            Vz=30.0,
            Mx=10.0,
            My=50.0,
            Mz=60.0,
        )

        result_set = {result1, result2}
        assert len(result_set) == 1
