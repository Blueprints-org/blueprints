"""Testing formula 6.5 of NEN-EN 1993-1-1+C2+A1:2016."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_6_ultimate_limit_state.formula_6_5 import Form6Dot5UnityCheckTensileStrength

# pylint: disable=arguments-differ


class TestForm6Dot5UnityCheckTensileStrength:
    """Validation for formula 6.5 from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation(self):
        """Test the evaluation of the result."""
        # Example values
        n_ed = 7  # kN
        n_t_rd = 10  # kN
        form = Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

        # Expected result, manually calculated
        expected = 0.7

        assert form == expected

    def test_raise_error_when_negative_n_ed_is_given(self):
        """Test a negative value for v_rd_s."""
        # Example values
        n_ed = -7
        n_t_rd = 10

        with pytest.raises(ValueError):
            Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

    def test_raise_error_when_negative_n__t_rd_is_given(self):
        """Test a negative value for v_ccd."""
        # Example values
        n_ed = 7
        n_t_rd = -10

        with pytest.raises(ValueError):
            Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

    def test_raise_error_when_zero_n_t_rd_is_given(self):
        """Test a negative value for v_td."""
        # Example values
        n_ed = 10
        n_t_rd = 0

        with pytest.raises(ValueError):
            Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)
