"""Testing formula 8.86 of FprEN 1992-1-1:2023."""

from collections.abc import Sequence

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_86 import Form8Dot86CheckInteractionInternalForces
from blueprints.validations import LessOrEqualToZeroError, ListsNotSameLengthError, NegativeValueError

# Torsional moment, bending moment and shear stress of one cross-section, in Nmm, Nmm and MPa respectively.
# The ratios are 0.25, 0.30 and 0.30, so the sum of the linear criterion is 0.85.
S_ED = (25.0e6, 150.0e6, 0.6)
S_RD = (100.0e6, 500.0e6, 2.0)


class TestForm8Dot86CheckInteractionInternalForces:
    """Validation for formula 8.86 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("s_ed", "s_rd", "expected"),
        [
            (S_ED, S_RD, True),  # 0.25 + 0.30 + 0.30 = 0.85, the cross-section resists the combination
            ((50.0e6, 250.0e6), (100.0e6, 500.0e6), True),  # 0.50 + 0.50 = 1.00, exactly on the limit, which the standard includes
            ((80.0e6, 300.0e6, 1.5), (100.0e6, 500.0e6, 2.0), False),  # 0.80 + 0.60 + 0.75 = 2.15, the combination is not resisted
            ((0.0,), (2.0,), True),  # a single internal force that is not acting at all
        ],
    )
    def test_evaluation(self, s_ed: Sequence[float], s_rd: Sequence[float], expected: bool) -> None:
        """Tests the evaluation of the result."""
        assert bool(Form8Dot86CheckInteractionInternalForces(s_ed=s_ed, s_rd=s_rd)) is expected

    def test_unity_check(self) -> None:
        """Tests that the unity check is the sum of the ratios, since the limit of the criterion is 1,0."""
        formula = Form8Dot86CheckInteractionInternalForces(s_ed=S_ED, s_rd=S_RD)

        # Expected result, manually calculated
        manually_calculated_result = 0.85  # -

        assert formula.unity_check == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("s_ed", "s_rd"),
        [
            ((25.0e6, 150.0e6), (100.0e6, 500.0e6, 2.0)),  # more resistances than actions
            ((25.0e6, 150.0e6, 0.6), (100.0e6, 500.0e6)),  # more actions than resistances
        ],
    )
    def test_raise_error_when_lists_differ_in_length(self, s_ed: Sequence[float], s_rd: Sequence[float]) -> None:
        """Test that an action without its resistance, or the other way round, is rejected."""
        with pytest.raises(ListsNotSameLengthError):
            Form8Dot86CheckInteractionInternalForces(s_ed=s_ed, s_rd=s_rd)

    def test_raise_error_when_no_internal_force_is_given(self) -> None:
        """Test that an empty combination is rejected, since summing nothing would pass the criterion silently."""
        with pytest.raises(ValueError, match="At least one internal force"):
            Form8Dot86CheckInteractionInternalForces(s_ed=(), s_rd=())

    @pytest.mark.parametrize(
        ("s_ed", "s_rd"),
        [
            ((-25.0e6, 150.0e6), (100.0e6, 500.0e6)),  # an action is negative
            ((25.0e6, 150.0e6), (-100.0e6, 500.0e6)),  # a resistance is negative
            ((25.0e6, 150.0e6), (0.0, 500.0e6)),  # a resistance is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, s_ed: Sequence[float], s_rd: Sequence[float]) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot86CheckInteractionInternalForces(s_ed=s_ed, s_rd=s_rd)

    @pytest.mark.parametrize(
        ("s_ed", "representation", "expected"),
        [
            (
                (40.0, 90.0),
                "complete",
                (
                    r"CHECK \to \sum \left( \frac{S_{Ed}}{S_{Rd}} \right)_{i} \leq 1.0 \to "
                    r"\frac{40.000}{100.000} + \frac{90.000}{300.000} \leq 1.0 \to OK"
                ),
            ),
            (
                (40.0, 90.0),
                "complete_with_units",
                (
                    r"CHECK \to \sum \left( \frac{S_{Ed}}{S_{Rd}} \right)_{i} \leq 1.0 \to "
                    r"\frac{40.000}{100.000} + \frac{90.000}{300.000} \leq 1.0 \to OK"
                ),
            ),
            ((40.0, 90.0), "short", r"CHECK \to OK"),
            ((120.0, 90.0), "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, s_ed: Sequence[float], representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot86CheckInteractionInternalForces(s_ed=s_ed, s_rd=(100.0, 300.0)).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
