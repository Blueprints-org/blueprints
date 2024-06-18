import pytest

from blueprints.structural.result.result_nodal_reaction import ResultNodalReaction


class TestResultInternalForces2D:
    """Test class for the ResultInternalForce1D class."""

    @pytest.mark.parametrize(
        "r_x, r_y, r_z, m_x, m_y, m_z", 
        [
            (10, 20, 30, 40, 50, 60),
            (-10, -20, -30, -40, -50, -60),
            (0, 0, 0, 0, 0, 0),
            (1.5, 2.5, 3.5, 4.5, 5.5, 6.5),
        ]
    )
    def test_constructor(self, r_x, r_y, r_z, m_x, m_y, m_z):
        """ test constructor returns expected"""
        result = ResultNodalReaction(
            r_x=r_x,
            r_y=r_y,
            r_z=r_z,
            m_x=m_x,
            m_y=m_y,
            m_z=m_z
        )
        assert result.r_x == r_x
        assert result.r_y == r_y
        assert result.r_z == r_z
        assert result.m_x == m_x
        assert result.m_y == m_y
        assert result.m_z == m_z
