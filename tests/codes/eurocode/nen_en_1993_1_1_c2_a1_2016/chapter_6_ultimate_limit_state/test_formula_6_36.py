"""Testing formula 6.36 from NEN-EN 1993-1-1+C2+A1:2016."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_6_ultimate_limit_state.formula_6_36 import Form6Dot36MomentReduction
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot36MomentReduction:
    """Validation for formula 6.36 from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        mpl_y_rd = 50000.0
        capital_a = 3000.0
        b = 100.0
        tf = 10.0
        n_ed = 10000.0
        n_pl_rd = 20000.0

        # Object to test
        formula = Form6Dot36MomentReduction(mpl_y_rd=mpl_y_rd, capital_a=capital_a, b=b, tf=tf, n_ed=n_ed, n_pl_rd=n_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 30000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation2(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        mpl_y_rd = 50000.0
        capital_a = 3000.0
        b = 100.0
        tf = 10.0
        n_ed = 1.0
        n_pl_rd = 20000.0

        # Object to test
        formula = Form6Dot36MomentReduction(mpl_y_rd=mpl_y_rd, capital_a=capital_a, b=b, tf=tf, n_ed=n_ed, n_pl_rd=n_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 50000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("mpl_y_rd", "n_ed"),
        [
            (-50000.0, 10000.0),  # mpl_y_rd is negative
            (50000.0, -10000.0),  # n_ed is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, mpl_y_rd: float, n_ed: float) -> None:
        """Test invalid negative values."""
        with pytest.raises(NegativeValueError):
            Form6Dot36MomentReduction(mpl_y_rd=mpl_y_rd, capital_a=3000.0, b=10.0, tf=10.0, n_ed=n_ed, n_pl_rd=30000.0)

    @pytest.mark.parametrize(
        ("capital_a", "b", "tf", "n_pl_rd"),
        [
            (0.0, 100.0, 10.0, 20000.0),  # capital_a is zero
            (3000.0, 0.0, 10.0, 20000.0),  # b is zero
            (3000.0, 100.0, 0.0, 20000.0),  # tf is zero
            (3000.0, 100.0, 10.0, 0.0),  # n_pl_rd is zero
            (-3000.0, 100.0, 10.0, 20000.0),  # capital_a is negative
            (3000.0, 100.0, 10.0, -20000.0),  # n_pl_rd is negative
            (3000.0, -100.0, 10.0, 20000.0),  # b is negative
            (3000.0, 100.0, -10.0, 20000.0),  # tf is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, capital_a: float, b: float, tf: float, n_pl_rd: float) -> None:
        """Test invalid zero or negative values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot36MomentReduction(mpl_y_rd=10000.0, capital_a=capital_a, b=b, tf=tf, n_ed=1000.0, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{N,y,Rd} = \min\left(M_{pl,y,Rd}, M_{pl,y,Rd} \cdot \left( 1 - \frac{N_{Ed}}{N_{pl,Rd}} \cdot "
                r"\frac{1}{1 - 0.5 \cdot \frac{A - 2 \cdot b \cdot t_f}{A}} \right)\right) = "
                r"\min\left(50000.000, 50000.000 \cdot \left( 1 - \frac{10000.000}{20000.000} \cdot \frac{1}"
                r"{1 - 0.5 \cdot \frac{3000.000 - 2 \cdot 100.000 \cdot 10.000}{3000.000}} \right)\right) = 30000.000 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{N,y,Rd} = \min\left(M_{pl,y,Rd}, M_{pl,y,Rd} \cdot \left( 1 - \frac{N_{Ed}}{N_{pl,Rd}} \cdot "
                r"\frac{1}{1 - 0.5 \cdot \frac{A - 2 \cdot b \cdot t_f}{A}} \right)\right) = "
                r"\min\left(50000.000 \ Nmm, 50000.000 \ Nmm \cdot \left( 1 - \frac{10000.000 \ N}{20000.000 \ N} "
                r"\cdot \frac{1}{1 - 0.5 \cdot \frac{3000.000 \ mm^2 - 2 \cdot 100.000 \ mm \cdot 10.000 \ mm}"
                r"{3000.000 \ mm^2}} \right)\right) = 30000.000 \ Nmm",
            ),
            ("short", r"M_{N,y,Rd} = 30000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        mpl_y_rd = 50000.0
        capital_a = 3000.0
        b = 100.0
        tf = 10.0
        n_ed = 10000.0
        n_pl_rd = 20000.0

        # Object to test
        latex = Form6Dot36MomentReduction(mpl_y_rd=mpl_y_rd, capital_a=capital_a, b=b, tf=tf, n_ed=n_ed, n_pl_rd=n_pl_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
