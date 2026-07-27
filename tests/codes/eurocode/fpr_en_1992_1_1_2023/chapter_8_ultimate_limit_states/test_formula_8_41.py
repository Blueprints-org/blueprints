"""Testing formula 8.41 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_41 import (
    Form8Dot41CheckCotangentCompressionFieldAngle,
    SubForm8Dot41LowerBound,
    SubForm8Dot41UpperBound,
)


class TestForm8Dot41CheckCotangentCompressionFieldAngle:
    """Validation for formula 8.41 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("cot_theta", "cot_theta_min", "expected"),
        [
            (2.0, 2.5, True),  # inside the range
            (1.0, 2.5, True),  # at the lower bound, which is inclusive
            (2.5, 2.5, True),  # at the upper bound, which is inclusive
            (0.8, 2.5, False),  # below the lower bound
            (3.0, 2.5, False),  # above the upper bound
            (2.8, 3.0, True),  # a member with significant axial compressive force
            (1.5, 1.4, False),  # a member in axial tension, where the upper bound approaches the lower one
            (1.0, 0.9, False),  # an upper bound below 1 leaves an empty range, so no selected inclination can pass
        ],
    )
    def test_evaluation(self, cot_theta: float, cot_theta_min: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        # Create object to test
        formula = Form8Dot41CheckCotangentCompressionFieldAngle(cot_theta=cot_theta, cot_theta_min=cot_theta_min)

        # Perform test by assert
        assert bool(formula) is expected

    @pytest.mark.parametrize(
        ("cot_theta", "expected_unity_check"),
        [
            (2.0, 0.8),  # the upper bound governs: 2.0 / 2.5
            (0.8, 1.25),  # the lower bound governs: 1 / 0.8
            (3.0, 1.2),  # the upper bound governs and is violated: 3.0 / 2.5
        ],
    )
    def test_unity_check_is_the_governing_bound(self, cot_theta: float, expected_unity_check: float) -> None:
        """Aggregating with all takes the largest unity check, so the governing bound is the one reported."""
        # Create object to test
        formula = Form8Dot41CheckCotangentCompressionFieldAngle(cot_theta=cot_theta, cot_theta_min=2.5)

        # Perform test by assert
        assert formula.unity_check == pytest.approx(expected=expected_unity_check, rel=1e-4)

    def test_both_bounds_are_exposed_separately(self) -> None:
        """Each half of the printed range keeps its own left-hand side, right-hand side and unity check."""
        # Example values
        formula = Form8Dot41CheckCotangentCompressionFieldAngle(cot_theta=2.0, cot_theta_min=2.5)
        lower, upper = formula.comparison_formulas

        # Perform test by assert
        assert lower.lhs == pytest.approx(expected=1.0, rel=1e-4)
        assert lower.rhs == pytest.approx(expected=2.0, rel=1e-4)
        assert upper.lhs == pytest.approx(expected=2.0, rel=1e-4)
        assert upper.rhs == pytest.approx(expected=2.5, rel=1e-4)

    @pytest.mark.parametrize(
        ("cot_theta", "representation", "expected"),
        [
            (2.0, "complete", r"CHECK \to 1 \leq \cot(\theta) \leq \cot(\theta_{min}) \to 1 \leq 2.000 \leq 2.500 \to OK"),
            (2.0, "complete_with_units", r"CHECK \to 1 \leq \cot(\theta) \leq \cot(\theta_{min}) \to 1 \leq 2.000 \leq 2.500 \to OK"),
            (2.0, "short", r"CHECK \to OK"),
            (3.0, "complete", r"CHECK \to 1 \leq \cot(\theta) \leq \cot(\theta_{min}) \to 1 \leq 3.000 \leq 2.500 \to \text{Not OK}"),
            (3.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, cot_theta: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot41CheckCotangentCompressionFieldAngle(cot_theta=cot_theta, cot_theta_min=2.5).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestSubForm8Dot41Bounds:
    """Validation for the two halves of formula 8.41 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("cot_theta", "expected", "expected_latex"),
        [
            (2.0, True, r"CHECK \to 1 \leq \cot(\theta) \to 1 \leq 2.000 \to OK"),
            (0.8, False, r"CHECK \to 1 \leq \cot(\theta) \to 1 \leq 0.800 \to \text{Not OK}"),
        ],
    )
    def test_lower_bound(self, cot_theta: float, expected: bool, expected_latex: str) -> None:
        """Tests the lower bound on its own."""
        # Create object to test
        formula = SubForm8Dot41LowerBound(cot_theta=cot_theta)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex

    @pytest.mark.parametrize(
        ("cot_theta", "expected", "expected_latex"),
        [
            (2.0, True, r"CHECK \to \cot(\theta) \leq \cot(\theta_{min}) \to 2.000 \leq 2.500 \to OK"),
            (3.0, False, r"CHECK \to \cot(\theta) \leq \cot(\theta_{min}) \to 3.000 \leq 2.500 \to \text{Not OK}"),
        ],
    )
    def test_upper_bound(self, cot_theta: float, expected: bool, expected_latex: str) -> None:
        """Tests the upper bound on its own."""
        # Create object to test
        formula = SubForm8Dot41UpperBound(cot_theta=cot_theta, cot_theta_min=2.5)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex
