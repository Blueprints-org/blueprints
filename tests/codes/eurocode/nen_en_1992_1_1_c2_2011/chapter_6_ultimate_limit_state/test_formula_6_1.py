"""Testing formula 3.1 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_6_ultimate_limit_state.formula_6_1 import Form6Dot1DesignShearStrength


class TestForm6Dot1DesignShearStrength:
    """Validation for formula 6.1 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        v_rd_s = 10  # kN
        v_ccd = 10  # kN
        v_td = 10  # kN
        form = Form6Dot1DesignShearStrength(v_rd_s=v_rd_s, v_ccd=v_ccd, v_td=v_td)

        # Expected result, manually calculated
        expected = 30

        assert form == expected

    def test_raise_error_when_negative_v_rd_s_is_given(self) -> None:
        """Test a negative value for v_rd_s."""
        # Example values
        v_rd_s = -10
        v_ccd = 10
        v_td = 10

        with pytest.raises(ValueError):
            Form6Dot1DesignShearStrength(v_rd_s=v_rd_s, v_ccd=v_ccd, v_td=v_td)

    def test_raise_error_when_negative_v_ccd_is_given(self) -> None:
        """Test a negative value for v_ccd."""
        # Example values
        v_rd_s = 10
        v_ccd = -10
        v_td = 10

        with pytest.raises(ValueError):
            Form6Dot1DesignShearStrength(v_rd_s=v_rd_s, v_ccd=v_ccd, v_td=v_td)

    def test_raise_error_when_negative_v_td_is_given(self) -> None:
        """Test a negative value for v_td."""
        # Example values
        v_rd_s = 10
        v_ccd = 10
        v_td = -10

        with pytest.raises(ValueError):
            Form6Dot1DesignShearStrength(v_rd_s=v_rd_s, v_ccd=v_ccd, v_td=v_td)
