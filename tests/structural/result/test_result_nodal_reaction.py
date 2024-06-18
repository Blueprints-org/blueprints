import pytest

from blueprints.structural.result.result_internal_forces_1d import ResultInternalForces1D


class TestResultInternalForces2D:
    """Test class for the ResultInternalForce1D class."""

    @pytest.mark.parametrize(
        "n, v_y, v_z, m_x, m_y, m_z", 
        [
            (10, 20, 30, 40, 50, 60),
            (-10, -20, -30, -40, -50, -60),
            (0, 0, 0, 0, 0, 0),
            (1.5, 2.5, 3.5, 4.5, 5.5, 6.5),
        ]
    )
    def test_constructor(self, n, v_y, v_z, m_x, m_y, m_z):
        """ test constructor returns expected"""
        result = ResultInternalForces1D(
            n=n,
            v_y=v_y,
            v_z=v_z,
            m_x=m_x,
            m_y=m_y,
            m_z=m_z
        )
        assert result.n == n
        assert result.v_y == v_y
        assert result.v_z == v_z
        assert result.m_x == m_x
        assert result.m_y == m_y
        assert result.m_z == m_z
