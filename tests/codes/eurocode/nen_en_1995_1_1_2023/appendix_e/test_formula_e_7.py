"""Testing Formula E.7 from EN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2023.appendix_e.formula_e_7 import FormEDot7SecondMomentInertia
from blueprints.validations import LessOrEqualToZeroError


class TestFormEDot7SecondMomentInertia:
    """Validation for formula E.7 from EN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("i", "b_i", "h_i", "expected_result"),
        [
            (1, 10, 20, 6666.667),
            (3, 25, 100, 2083333.3333),
            (2, 12, 1, 1.00),
        ],
        ids=["test-1st-layer", "test-3rd-layer", "test-2nd-layer"],
    )
    def test_evaluation(self, i: int, b_i: float, h_i: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_e_7 = FormEDot7SecondMomentInertia(i=i, b_i=b_i, h_i=h_i)
        assert form_e_7 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("i", "b_i", "h_i", "expectation"),
        [
            (1, 1, 1, does_not_raise()),
            (1, -1, 1, pytest.raises(LessOrEqualToZeroError)),
            (2, 1, -1, pytest.raises(LessOrEqualToZeroError)),
            (1, 0, 1, pytest.raises(LessOrEqualToZeroError)),
            (0, 1, 1, pytest.raises(ValueError, match="The number of the layer must be either 1, 2 or 3")),
            (4, 1, 1, pytest.raises(ValueError, match="The number of the layer must be either 1, 2 or 3")),
        ],
        ids=["passes", "negative_bi", "negative_hi", "zero_bi", "layer0", "layer>3"],
    )
    def test_raise_error_incorrect_args(self, i: int, b_i: float, h_i: float, expectation: AbstractContextManager) -> None:
        """Test the evaluation of incorrect input arguments."""
        with expectation:
            assert FormEDot7SecondMomentInertia(i=i, h_i=h_i, b_i=b_i) is not None

    @pytest.mark.parametrize(
        ("i", "b_i", "h_i", "rep_short", "rep_long"),
        [
            (
                1,
                12,
                1,
                r"I_1 = 1.00",
                r"I_1 = \frac{b_1 h_1^3}{12}"
                r" = \frac{12.00 \cdot 1.00^3}{12}"
                r" = 1.00",
            ),
            (
                2,
                1000,
                20,
                r"I_2 = 666666.67",
                r"I_2 = \frac{b_2 h_2^3}{12}"
                r" = \frac{1000.00 \cdot 20.00^3}{12}"
                r" = 666666.67",
            ),
            (
                3,
                20,
                20,
                r"I_3 = 13333.33",
                r"I_3 = \frac{b_3 h_3^3}{12}"
                r" = \frac{20.00 \cdot 20.00^3}{12}"
                r" = 13333.33",
            ),
        ],
        ids=["lat-layer1", "lat-layer2", "lat-layer3"],
    )
    def test_latex(self, i: int, b_i: float, h_i: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_e_7_latex = FormEDot7SecondMomentInertia(i=i, b_i=b_i, h_i=h_i).latex()
        assert form_e_7_latex.complete == rep_long
        assert form_e_7_latex.short == rep_short
