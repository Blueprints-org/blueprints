"""Testing formula 3.1 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_1 import Form6Dot1DesignShearStrength


class TestForm6Dot1DesignShearStrength:
    """Validation for formula 6.1 from EN 1992-1-1:2004."""

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

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"V_{Rd} = V_{Rd,s} + V_{ccd} + V_{td} = 2.000 + 3.000 + 4.000 = 9.000"),
            ("short", r"V_{Rd} = 9.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_rd_s = 2.0
        v_ccd = 3.0
        v_td = 4.0

        # Object to test
        form_6_1_latex = Form6Dot1DesignShearStrength(v_rd_s=v_rd_s, v_ccd=v_ccd, v_td=v_td).latex()

        actual = {"complete": form_6_1_latex.complete, "short": form_6_1_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
