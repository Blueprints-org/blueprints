import pytest

from blueprints.structural.result.result_internal_forces_2d import ResultInternalForces2D


class TestResultInternalForces2D:
    """Test class for the ResultInternalForce2D class."""

    @pytest.mark.parametrize(
        "n_x, n_y, n_xy, v_xz, v_yz, m_xx, m_yy, m_xy, m_yx", 
        [
            (10, 20, 30, 40, 50, 60, 70, 80, 90),
            (-10, -20, -30, -40, -50, -60, -70, -80, -90),
            (0, 0, 0, 0, 0, 0, 0, 0, 0),
            (1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5),
        ]
    )
    def test_constructor(self, n_x, n_y, n_xy, v_xz, v_yz, m_xx, m_yy, m_xy, m_yx):
        """ test constructor returns expected"""
        result = ResultInternalForces2D(n_x, n_y, n_xy, v_xz, v_yz, m_xx, m_yy, m_xy, m_yx)
        assert result.n_x == n_x
        assert result.n_y == n_y
        assert result.n_xy == n_xy
        assert result.v_xz == v_xz
        assert result.v_yz == v_yz
        assert result.m_xx == m_xx
        assert result.m_yy == m_yy
        assert result.m_xy == m_xy
        assert result.m_yx == m_yx

