"""Testing formula 8.85 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_85 import (
    Form8Dot85CheckCotangentCompressionFieldTorsion,
    SubForm8Dot85LowerBound,
    SubForm8Dot85UpperBound,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError

# Angles chosen so that their cotangents are round numbers, which keeps the hand calculations readable
THETA_COT_0_25 = 75.963756532074  # cot(theta) = 0.25
THETA_COT_0_4 = 68.198590513648  # cot(theta) = 0.4
THETA_COT_1 = 45.0  # cot(theta) = 1
THETA_COT_2 = 26.565051177078  # cot(theta) = 2
THETA_COT_2_5 = 21.801409486352  # cot(theta) = 2.5
THETA_COT_3 = 18.434948822922  # cot(theta) = 3


class TestForm8Dot85CheckCotangentCompressionFieldTorsion:
    """Validation for formula 8.85 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("theta", "expected"),
        [
            # With cot(theta_min) = 2.5 the printed range on cot(theta) runs from 1/2.5 = 0.4 up to 2.5
            (THETA_COT_1, True),  # in the middle of the range, where both bounds are equally far away
            (THETA_COT_2, True),  # inside the range
            (THETA_COT_2_5, True),  # exactly on the upper bound, which is inclusive
            (THETA_COT_3, False),  # steeper than the upper bound allows
            (THETA_COT_0_4, True),  # exactly on the lower bound, which is inclusive
            (THETA_COT_0_25, False),  # flatter than the lower bound allows
        ],
    )
    def test_evaluation(self, theta: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        # Create object to test
        formula = Form8Dot85CheckCotangentCompressionFieldTorsion(theta=theta, theta_min=THETA_COT_2_5)

        # Perform test by assert
        assert bool(formula) is expected

    def test_range_is_wider_than_the_one_of_formula_8_41(self) -> None:
        """The lower bound is 1/cot(theta_min) and not the constant 1 of Formula (8.41), so an inclination
        flatter than 45 degrees passes here while (8.41) would reject it.
        """
        # cot(theta) = 0.5, which is below the lower bound of 1 that Formula (8.41) prints
        formula = Form8Dot85CheckCotangentCompressionFieldTorsion(theta=63.434948822922, theta_min=THETA_COT_2_5)

        assert bool(formula) is True

    @pytest.mark.parametrize("theta", [THETA_COT_1, THETA_COT_2, 60.0])
    def test_an_inverted_range_is_not_silently_reordered(self, theta: float) -> None:
        """For cot(theta_min) < 1 the printed lower bound 1/cot(theta_min) exceeds the printed upper bound
        cot(theta_min), so nothing can satisfy the relation. The standard prints the two sides fixed, so the
        class reports that rather than swapping them into a range that would pass.

        8.2.3(4) puts cot(theta_min) at 2,5 or higher, so this does not arise in practice. It is here so that a
        later change cannot introduce the reordering unnoticed.
        """
        # theta_min = 60 degrees gives cot(theta_min) = 0.577, hence a lower bound of 1.732 above an upper
        # bound of 0.577
        formula = Form8Dot85CheckCotangentCompressionFieldTorsion(theta=theta, theta_min=60.0)

        assert bool(formula) is False

    @pytest.mark.parametrize(
        ("theta", "expected_unity_check"),
        [
            (THETA_COT_1, 0.4),  # both bounds give 0.4, since the range is symmetric in cot(theta) about 1
            (THETA_COT_2, 0.8),  # the upper bound governs: 2.0 / 2.5
            (THETA_COT_3, 1.2),  # the upper bound governs and is violated: 3.0 / 2.5
            (THETA_COT_0_25, 1.6),  # the lower bound governs and is violated: 0.4 / 0.25
        ],
    )
    def test_unity_check_is_the_governing_bound(self, theta: float, expected_unity_check: float) -> None:
        """Aggregating with all takes the largest unity check, so the governing bound is the one reported."""
        # Create object to test
        formula = Form8Dot85CheckCotangentCompressionFieldTorsion(theta=theta, theta_min=THETA_COT_2_5)

        # Perform test by assert
        assert formula.unity_check == pytest.approx(expected=expected_unity_check, rel=1e-4)

    def test_both_bounds_are_exposed_separately(self) -> None:
        """Each half of the printed range keeps its own left-hand side, right-hand side and unity check."""
        # Example values
        formula = Form8Dot85CheckCotangentCompressionFieldTorsion(theta=THETA_COT_2, theta_min=THETA_COT_2_5)
        lower, upper = formula.comparison_formulas

        # Perform test by assert
        assert lower.lhs == pytest.approx(expected=0.4, rel=1e-4)
        assert lower.rhs == pytest.approx(expected=2.0, rel=1e-4)
        assert lower.unity_check == pytest.approx(expected=0.2, rel=1e-4)
        assert upper.lhs == pytest.approx(expected=2.0, rel=1e-4)
        assert upper.rhs == pytest.approx(expected=2.5, rel=1e-4)
        assert upper.unity_check == pytest.approx(expected=0.8, rel=1e-4)

    @pytest.mark.parametrize(
        ("theta", "theta_min"),
        [
            (0.0, THETA_COT_2_5),  # theta is zero, for which the cotangent diverges
            (-THETA_COT_2, THETA_COT_2_5),  # theta is negative
            (THETA_COT_2, 0.0),  # theta_min is zero, for which the cotangent diverges
            (THETA_COT_2, -THETA_COT_2_5),  # theta_min is negative
        ],
    )
    def test_raise_error_when_the_angles_are_less_or_equal_to_zero(self, theta: float, theta_min: float) -> None:
        """Both inputs are inclinations, so neither can be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot85CheckCotangentCompressionFieldTorsion(theta=theta, theta_min=theta_min)

    @pytest.mark.parametrize(
        ("theta", "theta_min"),
        [
            (120.0, THETA_COT_2_5),  # theta exceeds 90 degrees
            (THETA_COT_2, 120.0),  # theta_min exceeds 90 degrees
        ],
    )
    def test_raise_error_when_the_angles_exceed_90_degrees(self, theta: float, theta_min: float) -> None:
        """Beyond 90 degrees the cotangent turns negative, which is not an inclination the standard offers."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot85CheckCotangentCompressionFieldTorsion(theta=theta, theta_min=theta_min)

    @pytest.mark.parametrize(
        ("theta", "representation", "expected"),
        [
            (
                THETA_COT_2,
                "complete",
                (
                    r"CHECK \to \frac{1}{\cot(\theta_{min})} \leq \cot(\theta) \leq \cot(\theta_{min}) \to "
                    r"\frac{1}{\cot(21.801)} \leq \cot(26.565) \leq \cot(21.801) \to OK"
                ),
            ),
            (
                THETA_COT_2,
                "complete_with_units",
                (
                    r"CHECK \to \frac{1}{\cot(\theta_{min})} \leq \cot(\theta) \leq \cot(\theta_{min}) \to "
                    r"\frac{1}{\cot(21.801 ^\circ)} \leq \cot(26.565 ^\circ) \leq \cot(21.801 ^\circ) \to OK"
                ),
            ),
            (THETA_COT_2, "short", r"CHECK \to OK"),
            (
                THETA_COT_3,
                "complete",
                (
                    r"CHECK \to \frac{1}{\cot(\theta_{min})} \leq \cot(\theta) \leq \cot(\theta_{min}) \to "
                    r"\frac{1}{\cot(21.801)} \leq \cot(18.435) \leq \cot(21.801) \to \text{Not OK}"
                ),
            ),
            (THETA_COT_3, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, theta: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot85CheckCotangentCompressionFieldTorsion(theta=theta, theta_min=THETA_COT_2_5).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestSubForm8Dot85Bounds:
    """Validation for the two halves of formula 8.85 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("theta", "expected", "expected_latex"),
        [
            (
                THETA_COT_2,
                True,
                r"CHECK \to \frac{1}{\cot(\theta_{min})} \leq \cot(\theta) \to \frac{1}{\cot(21.801)} \leq \cot(26.565) \to OK",
            ),
            (
                THETA_COT_0_25,
                False,
                (
                    r"CHECK \to \frac{1}{\cot(\theta_{min})} \leq \cot(\theta) \to "
                    r"\frac{1}{\cot(21.801)} \leq \cot(75.964) \to \text{Not OK}"
                ),
            ),
        ],
    )
    def test_lower_bound(self, theta: float, expected: bool, expected_latex: str) -> None:
        """Tests the lower bound on its own."""
        # Create object to test
        formula = SubForm8Dot85LowerBound(theta=theta, theta_min=THETA_COT_2_5)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex

    @pytest.mark.parametrize(
        ("theta", "expected", "expected_latex"),
        [
            (THETA_COT_2, True, r"CHECK \to \cot(\theta) \leq \cot(\theta_{min}) \to \cot(26.565) \leq \cot(21.801) \to OK"),
            (
                THETA_COT_3,
                False,
                r"CHECK \to \cot(\theta) \leq \cot(\theta_{min}) \to \cot(18.435) \leq \cot(21.801) \to \text{Not OK}",
            ),
        ],
    )
    def test_upper_bound(self, theta: float, expected: bool, expected_latex: str) -> None:
        """Tests the upper bound on its own."""
        # Create object to test
        formula = SubForm8Dot85UpperBound(theta=theta, theta_min=THETA_COT_2_5)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex
