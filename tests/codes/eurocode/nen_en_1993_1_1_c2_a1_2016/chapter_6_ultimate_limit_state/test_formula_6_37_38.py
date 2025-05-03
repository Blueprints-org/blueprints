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
        a = 0.4
        n = 0.3

        # Object to test
        formula = Form6Dot37Dot38MomentReduction(mpl_z_rd=mpl_z_rd, a=a, n=n)

        # Expected result, manually calculated
        manually_calculated_result = 60000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_38(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        mpl_z_rd = 60000.0
        a = 0.5
        n = 0.9666666667

        # Object to test
        formula = Form6Dot37Dot38MomentReduction(mpl_z_rd=mpl_z_rd, a=a, n=n)

        # Expected result, manually calculated
        manually_calculated_result = 7733.333333

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("mpl_z_rd", "n"),
        [
            (-60000.0, 0.5),  # mpl_z_rd is negative
            (60000.0, -0.5),  # n is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, mpl_z_rd: float, n: float) -> None:
        """Test invalid negative values."""
        with pytest.raises(NegativeValueError):
            Form6Dot37Dot38MomentReduction(mpl_z_rd=mpl_z_rd, a=0.4, n=n)

    @pytest.mark.parametrize(
        "a",
        [
            0.0,  # a is zero
            -0.1,  # a is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float) -> None:
        """Test invalid zero or negative values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot37Dot38MomentReduction(mpl_z_rd=60000.0, a=a, n=0.5)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{N,z,Rd} = \begin{cases} M_{pl,z,Rd} & \text{if } n \leq a \\ "
                r"M_{pl,z,Rd} \cdot \left[1 - \left(\frac{ n - a}{1 - a}\right)^2\right] & \text{if } n > a \end{cases} = "
                r"\begin{cases} 60000.000 & \text{if } 0.300 \leq 0.400 \\ "
                r"60000.000 \cdot \left[1 - \left(\frac{ 0.300 - 0.400}{1 - 0.400}\right)^2\right] & "
                r"\text{if } 0.300 > 0.400 \end{cases} = 60000.000 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{N,z,Rd} = \begin{cases} M_{pl,z,Rd} & \text{if } n \leq a \\ "
                r"M_{pl,z,Rd} \cdot \left[1 - \left(\frac{ n - a}{1 - a}\right)^2\right] & \text{if } n > a \end{cases} = "
                r"\begin{cases} 60000.000 \ Nmm & \text{if } 0.300 \leq 0.400 \\ "
                r"60000.000 \ Nmm \cdot \left[1 - \left(\frac{ 0.300 - 0.400}{1 - 0.400}\right)^2\right] & "
                r"\text{if } 0.300 > 0.400 \end{cases} = 60000.000 \ Nmm",
            ),
            ("short", r"M_{N,z,Rd} = 60000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        mpl_z_rd = 60000.0
        a = 0.4
        n = 0.3

        # Object to test
        latex = Form6Dot37Dot38MomentReduction(mpl_z_rd=mpl_z_rd, a=a, n=n).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
