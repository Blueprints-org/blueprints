"""Testing formulas 8.67 and 8.68 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_67_68 import (
    Form8Dot67To68CheckCotangentFlangeCompressionField,
    SubForm8Dot67To68LowerBound,
    SubForm8Dot67To68UpperBound,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot67To68CheckCotangentFlangeCompressionField:
    """Validation for formulas 8.67 and 8.68 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("cot_theta_f", "flange_type", "expected"),
        [
            # Formula (8.67), compression flanges, bounded at 3.0
            ("2.0", "compression", True),
            ("3.0", "compression", True),  # at the upper bound, which is inclusive
            ("3.5", "compression", False),  # above the upper bound
            # Formula (8.68), tension flanges, bounded at 1.25
            ("1.25", "tension", True),  # at the upper bound, which is inclusive
            ("1.5", "tension", False),  # above the upper bound
            # the same cotangent passes in a compression flange and fails in a tension flange
            ("2.0", "tension", False),
            # the lower bound is the same for both and is inclusive
            ("1.0", "compression", True),
            ("1.0", "tension", True),
            ("0.9", "compression", False),
            ("0.9", "tension", False),
        ],
    )
    def test_evaluation(self, cot_theta_f: str, flange_type: str, expected: bool) -> None:
        """Tests the evaluation of the result for both flange types."""
        # Create object to test
        formula = Form8Dot67To68CheckCotangentFlangeCompressionField(cot_theta_f=float(cot_theta_f), flange_type=flange_type)

        # Perform test by assert
        assert bool(formula) is expected

    @pytest.mark.parametrize(
        ("cot_theta_f", "flange_type", "expected_unity_check"),
        [
            (2.0, "compression", 0.6666666666666666),  # the upper bound governs: 2.0 / 3.0
            (2.0, "tension", 1.6),  # the upper bound governs and is violated: 2.0 / 1.25
            (0.8, "compression", 1.25),  # the lower bound governs: 1 / 0.8
        ],
    )
    def test_unity_check_is_the_governing_bound(self, cot_theta_f: float, flange_type: str, expected_unity_check: float) -> None:
        """Aggregating with all takes the largest unity check, so the governing bound is the one reported."""
        # Create object to test
        formula = Form8Dot67To68CheckCotangentFlangeCompressionField(cot_theta_f=cot_theta_f, flange_type=flange_type)

        # Perform test by assert
        assert formula.unity_check == pytest.approx(expected=expected_unity_check, rel=1e-4)

    def test_both_bounds_are_exposed_separately(self) -> None:
        """Each half of the printed range keeps its own left-hand side and right-hand side."""
        # Example values
        formula = Form8Dot67To68CheckCotangentFlangeCompressionField(cot_theta_f=2.0, flange_type="compression")
        lower, upper = formula.comparison_formulas

        # Perform test by assert
        assert lower.lhs == pytest.approx(expected=1.0, rel=1e-4)
        assert lower.rhs == pytest.approx(expected=2.0, rel=1e-4)
        assert upper.lhs == pytest.approx(expected=2.0, rel=1e-4)
        assert upper.rhs == pytest.approx(expected=3.0, rel=1e-4)

    def test_raise_error_for_an_unknown_flange_type(self) -> None:
        """The standard prints two formulas and no third case, so anything else is rejected."""
        with pytest.raises(ValueError, match="Invalid flange type"):
            Form8Dot67To68CheckCotangentFlangeCompressionField(cot_theta_f=2.0, flange_type="shear")

    @pytest.mark.parametrize("cot_theta_f", [0.0, -1.0])
    def test_raise_error_when_the_cotangent_is_not_positive(self, cot_theta_f: float) -> None:
        """A cotangent of zero or less is not the inclination of a compression field and must be refused.

        Reporting it as a failed check is not enough, because the check would not fail. The verdict is reached
        through the unity check, which for the lower bound is 1 divided by the cotangent: a negative cotangent
        turns that ratio negative and the bound reports OK, and a zero cotangent divides by zero.
        """
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot67To68CheckCotangentFlangeCompressionField(cot_theta_f=cot_theta_f, flange_type="compression")

    @pytest.mark.parametrize(
        ("cot_theta_f", "flange_type", "representation", "expected"),
        [
            (2.0, "compression", "complete", r"CHECK \to 1 \leq \cot(\theta_f) \leq limit \to 1 \leq 2.000 \leq 3.000 \to OK"),
            (2.0, "compression", "complete_with_units", r"CHECK \to 1 \leq \cot(\theta_f) \leq limit \to 1 \leq 2.000 \leq 3.000 \to OK"),
            (2.0, "compression", "short", r"CHECK \to OK"),
            (2.0, "tension", "complete", r"CHECK \to 1 \leq \cot(\theta_f) \leq limit \to 1 \leq 2.000 \leq 1.250 \to \text{Not OK}"),
            (2.0, "tension", "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, cot_theta_f: float, flange_type: str, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot67To68CheckCotangentFlangeCompressionField(cot_theta_f=cot_theta_f, flange_type=flange_type).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestSubForm8Dot67To68Bounds:
    """Validation for the two halves of formulas 8.67 and 8.68 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("cot_theta_f", "expected", "expected_latex"),
        [
            (2.0, True, r"CHECK \to 1 \leq \cot(\theta_f) \to 1 \leq 2.000 \to OK"),
            (0.8, False, r"CHECK \to 1 \leq \cot(\theta_f) \to 1 \leq 0.800 \to \text{Not OK}"),
        ],
    )
    def test_lower_bound(self, cot_theta_f: float, expected: bool, expected_latex: str) -> None:
        """Tests the lower bound on its own."""
        # Create object to test
        formula = SubForm8Dot67To68LowerBound(cot_theta_f=cot_theta_f)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex

    @pytest.mark.parametrize(
        ("cot_theta_f", "flange_type", "expected", "expected_latex"),
        [
            (2.0, "compression", True, r"CHECK \to \cot(\theta_f) \leq limit \to 2.000 \leq 3.000 \to OK"),
            (2.0, "tension", False, r"CHECK \to \cot(\theta_f) \leq limit \to 2.000 \leq 1.250 \to \text{Not OK}"),
        ],
    )
    def test_upper_bound(self, cot_theta_f: float, flange_type: str, expected: bool, expected_latex: str) -> None:
        """Tests the upper bound on its own, for both flange types."""
        # Create object to test
        formula = SubForm8Dot67To68UpperBound(cot_theta_f=cot_theta_f, flange_type=flange_type)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex

    def test_raise_error_for_an_unknown_flange_type(self) -> None:
        """The upper bound rejects anything that is neither of the two printed cases."""
        with pytest.raises(ValueError, match="Invalid flange type"):
            SubForm8Dot67To68UpperBound(cot_theta_f=2.0, flange_type="shear")

    @pytest.mark.parametrize("cot_theta_f", [0.0, -1.0])
    def test_both_bounds_refuse_a_non_positive_cotangent(self, cot_theta_f: float) -> None:
        """Each half refuses a cotangent of zero or less on its own, not only through the aggregate."""
        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot67To68LowerBound(cot_theta_f=cot_theta_f)
        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot67To68UpperBound(cot_theta_f=cot_theta_f, flange_type="compression")
