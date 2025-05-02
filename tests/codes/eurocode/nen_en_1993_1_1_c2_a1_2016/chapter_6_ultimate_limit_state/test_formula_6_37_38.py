"""Testing formulas 6.37 and 6.38 from NEN-EN 1993-1-1+C2+A1:2016."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_6_ultimate_limit_state.formula_6_37_38 import Form6Dot37Dot38MomentReduction
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot37Dot38MomentReduction:
    """Validation for formulas 6.37 and 6.38 from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation_37(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        mpl_z_rd = 60000.0
        capital_a = 25000.0
        b = 120.0
        tf = 15.0
        n_ed = 15000.0
        n_pl_rd = 30000.0

        # Object to test
        formula = Form6Dot37Dot38MomentReduction(mpl_z_rd=mpl_z_rd, capital_a=capital_a, b=b, tf=tf, n_ed=n_ed, n_pl_rd=n_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 60000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_38(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        mpl_z_rd = 60000.0
        capital_a = 25000.0
        b = 120.0
        tf = 15.0
        n_ed = 29000.0
        n_pl_rd = 30000.0

        # Object to test
        formula = Form6Dot37Dot38MomentReduction(mpl_z_rd=mpl_z_rd, capital_a=capital_a, b=b, tf=tf, n_ed=n_ed, n_pl_rd=n_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 7733.333333

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("mpl_z_rd", "n_ed"),
        [
            (-60000.0, 15000.0),  # mpl_z_rd is negative
            (60000.0, -15000.0),  # n_ed is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, mpl_z_rd: float, n_ed: float) -> None:
        """Test invalid negative values."""
        with pytest.raises(NegativeValueError):
            Form6Dot37Dot38MomentReduction(mpl_z_rd=mpl_z_rd, capital_a=25000.0, b=120.0, tf=15.0, n_ed=n_ed, n_pl_rd=30000.0)

    @pytest.mark.parametrize(
        ("capital_a", "b", "tf", "n_pl_rd"),
        [
            (0.0, 120.0, 15.0, 30000.0),  # capital_a is zero
            (25000.0, 0.0, 15.0, 30000.0),  # b is zero
            (25000.0, 120.0, 0.0, 30000.0),  # tf is zero
            (25000.0, 120.0, 15.0, 0.0),  # n_pl_rd is zero
            (-25000.0, 120.0, 15.0, 30000.0),  # capital_a is negative
            (25000.0, -120.0, 15.0, 30000.0),  # b is negative
            (25000.0, 120.0, -15.0, 30000.0),  # tf is negative
            (25000.0, 120.0, 15.0, -30000.0),  # n_pl_rd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, capital_a: float, b: float, tf: float, n_pl_rd: float) -> None:
        """Test invalid zero or negative values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot37Dot38MomentReduction(mpl_z_rd=60000.0, capital_a=capital_a, b=b, tf=tf, n_ed=15000.0, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{N,z,Rd} = \begin{cases} M_{pl,z,Rd} & \text{if } \frac{N_{Ed}}{N_{pl,Rd}} "
                r"\leq \frac{A - 2 \cdot b \cdot t_f}{A} \\ "
                r"M_{pl,z,Rd} \cdot \left[1 - \left(\frac{\frac{N_{Ed}}{N_{pl,Rd}} - \frac{A - 2 \cdot b \cdot t_f}{A}}"
                r"{1 - \frac{A - 2 \cdot b \cdot t_f}{A}}\right)^2\right] & \text{if } \frac{N_{Ed}}{N_{pl,Rd}} "
                r"> \frac{A - 2 \cdot b \cdot t_f}{A} \end{cases} = "
                r"\begin{cases} 60000.000 & \text{if } \frac{15000.000}{30000.000} \leq "
                r"\frac{25000.000 - 2 \cdot 120.000 \cdot 15.000}{25000.000} \\ "
                r"60000.000 \cdot \left[1 - \left(\frac{\frac{15000.000}{30000.000} - \frac{25000.000 - "
                r"2 \cdot 120.000 \cdot 15.000}{25000.000}}{1 - \frac{25000.000 - 2 \cdot 120.000 \cdot 15.000}{25000.000}}\right)^2"
                r"\right] & \text{if } \frac{15000.000}{30000.000} > \frac{25000.000 - 2 \cdot 120.000 \cdot 15.000}{25000.000} "
                r"\end{cases} = 60000.000 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{N,z,Rd} = \begin{cases} M_{pl,z,Rd} & \text{if } \frac{N_{Ed}}{N_{pl,Rd}} \leq \frac{A - 2 \cdot b \cdot t_f}{A} \\ "
                r"M_{pl,z,Rd} \cdot \left[1 - \left(\frac{\frac{N_{Ed}}{N_{pl,Rd}} - \frac{A - 2 \cdot b \cdot t_f}{A}}"
                r"{1 - \frac{A - 2 \cdot b \cdot t_f}{A}}\right)^2\right] & \text{if } \frac{N_{Ed}}{N_{pl,Rd}} "
                r"> \frac{A - 2 \cdot b \cdot t_f}{A} \end{cases} = "
                r"\begin{cases} 60000.000 \ Nmm & \text{if } \frac{15000.000 \ N}{30000.000 \ N} \leq \frac{25000.000 \ mm^2 - "
                r"2 \cdot 120.000 \ mm \cdot 15.000 \ mm}{25000.000 \ mm^2} \\ "
                r"60000.000 \ Nmm \cdot \left[1 - \left(\frac{\frac{15000.000 \ N}{30000.000 \ N} - \frac{25000.000 \ mm^2 - "
                r"2 \cdot 120.000 \ mm \cdot 15.000 \ mm}{25000.000 \ mm^2}}{1 - \frac{25000.000 \ mm^2 - 2 \cdot 120.000 \ mm \cdot "
                r"15.000 \ mm}{25000.000 \ mm^2}}\right)^2\right] & \text{if } \frac{15000.000 \ N}{30000.000 \ N} > \frac{25000.000 "
                r"\ mm^2 - 2 \cdot 120.000 \ mm \cdot 15.000 \ mm}{25000.000 \ mm^2} \end{cases} = 60000.000 \ Nmm",
            ),
            ("short", r"M_{N,z,Rd} = 60000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        mpl_z_rd = 60000.0
        capital_a = 25000.0
        b = 120.0
        tf = 15.0
        n_ed = 15000.0
        n_pl_rd = 30000.0

        # Object to test
        latex = Form6Dot37Dot38MomentReduction(mpl_z_rd=mpl_z_rd, capital_a=capital_a, b=b, tf=tf, n_ed=n_ed, n_pl_rd=n_pl_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
