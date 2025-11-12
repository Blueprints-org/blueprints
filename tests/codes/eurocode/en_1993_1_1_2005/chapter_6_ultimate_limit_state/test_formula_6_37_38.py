"""Testing formulas 6.37 and 6.38 from EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_37_38 import (
    Form6Dot37And38MomentReduction,
    Form6Dot38A,
    Form6Dot38N,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot37And38MomentReduction:
    """Validation for formulas 6.37 and 6.38 from EN 1993-1-1:2005."""

    def test_evaluation_37(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        mpl_z_rd = 60000.0
        a = 0.4
        n = 0.3

        # Object to test
        formula = Form6Dot37And38MomentReduction(mpl_z_rd=mpl_z_rd, a=a, n=n)

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
        formula = Form6Dot37And38MomentReduction(mpl_z_rd=mpl_z_rd, a=a, n=n)

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
            Form6Dot37And38MomentReduction(mpl_z_rd=mpl_z_rd, a=0.4, n=n)

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
            Form6Dot37And38MomentReduction(mpl_z_rd=60000.0, a=a, n=0.5)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{N,z,Rd} = \begin{cases} M_{pl,z,Rd} & \text{if } n \leq a \\ "
                r"M_{pl,z,Rd} \cdot \left[1 - \left(\frac{ n - a}{1 - a}\right)^2\right] & \text{if } "
                r"n > a \end{cases} = "
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
        latex = Form6Dot37And38MomentReduction(mpl_z_rd=mpl_z_rd, a=a, n=n).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot38N:
    """Validation for formula 6.38n from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 50000.0
        n_pl_rd = 100000.0

        # Object to test
        formula = Form6Dot38N(n_ed=n_ed, n_pl_rd=n_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 0.5

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed", "n_pl_rd"),
        [
            (-50000.0, 100000.0),  # n_ed is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, n_ed: float, n_pl_rd: float) -> None:
        """Test invalid negative values."""
        with pytest.raises(NegativeValueError):
            Form6Dot38N(n_ed=n_ed, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        "n_pl_rd",
        [
            0.0,  # n_pl_rd is zero
            -0.1,  # n_pl_rd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_pl_rd: float) -> None:
        """Test invalid zero or negative values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot38N(n_ed=50000.0, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"n = \frac{N_{Ed}}{N_{pl,Rd}} = \frac{50000.000}{100000.000} = 0.500 \ -",
            ),
            (
                "complete_with_units",
                r"n = \frac{N_{Ed}}{N_{pl,Rd}} = \frac{50000.000 \ N}{100000.000 \ N} = 0.500 \ -",
            ),
            ("short", r"n = 0.500 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 50000.0
        n_pl_rd = 100000.0

        # Object to test
        latex = Form6Dot38N(n_ed=n_ed, n_pl_rd=n_pl_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot38A:
    """Validation for formula 6.38a from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        capital_a = 2000.0
        b = 100.0
        tf = 10.0

        # Object to test
        formula = Form6Dot38A(capital_a=capital_a, b=b, tf=tf)

        # Expected result, manually calculated
        manually_calculated_result = 0.00

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation2(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        capital_a = 20000.0
        b = 100.0
        tf = 10.0

        # Object to test
        formula = Form6Dot38A(capital_a=capital_a, b=b, tf=tf)

        # Expected result, manually calculated
        manually_calculated_result = 0.50

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("capital_a", "b", "tf"),
        [
            (0.0, 100.0, 10.0),  # capital_a is zero
            (-2000.0, 100.0, 10.0),  # capital_a is negative
            (2000.0, -100.0, 10.0),  # b is negative
            (2000.0, 100.0, -10.0),  # tf is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, capital_a: float, b: float, tf: float) -> None:
        """Test invalid zero or negative values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot38A(capital_a=capital_a, b=b, tf=tf)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a = \min\left(\frac{A - 2 \cdot b \cdot t_f}{A}, 0.5\right) = \min\left(\frac{2000.000 - "
                r"2 \cdot 100.000 \cdot 10.000}{2000.000}, 0.5\right) = 0.000 \ -",
            ),
            (
                "complete_with_units",
                r"a = \min\left(\frac{A - 2 \cdot b \cdot t_f}{A}, 0.5\right) = \min\left(\frac{2000.000 \ mm^2 - "
                r"2 \cdot 100.000 \ mm \cdot 10.000 \ mm}{2000.000 \ mm^2}, 0.5\right) = 0.000 \ -",
            ),
            ("short", r"a = 0.000 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        capital_a = 2000.0
        b = 100.0
        tf = 10.0

        # Object to test
        latex = Form6Dot38A(capital_a=capital_a, b=b, tf=tf).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
