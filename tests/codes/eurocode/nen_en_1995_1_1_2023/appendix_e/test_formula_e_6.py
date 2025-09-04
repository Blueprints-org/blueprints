"""Testing Formula E.6 from EN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2023.appendix_e.formula_e_6 import FormEDot6AreaOfLayerI
from blueprints.validations import LessOrEqualToZeroError


class TestFormEDot6AreaOfLayerI:
    """Validation for formula E.6 from EN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("i", "b_i", "h_i", "expected_result"),
        [
            (1, 10, 20, 200.00),
            (3, 25, 100, 2500.00),
            (2, 1000, 12, 12000.00),
        ],
        ids=["test-1st-layer", "test-3rd-layer", "test-2nd-layer"],
    )
    def test_evaluation(self, i: int, b_i: float, h_i: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_e_6 = FormEDot6AreaOfLayerI(i=i, b_i=b_i, h_i=h_i)
        assert form_e_6 == pytest.approx(expected=expected_result, abs=1e-3)

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
            assert FormEDot6AreaOfLayerI(i=i, h_i=h_i, b_i=b_i) is not None

    @pytest.mark.parametrize(
        ("i", "b_i", "h_i", "rep_short", "rep_long"),
        [
            (
                1,
                12,
                10,
                r"A_1 = 120.00",
                r"A_1 = b_1 h_1"
                r" = 12.00 \cdot 10.00"
                r" = 120.00",
            ),
            (
                2,
                1000,
                20,
                r"A_2 = 20000.00",
                r"A_2 = b_2 h_2"
                r" = 1000.00 \cdot 20.00"
                r" = 20000.00",
            ),
            (
                3,
                20,
                20,
                r"A_3 = 400.00",
                r"A_3 = b_3 h_3"
                r" = 20.00 \cdot 20.00"
                r" = 400.00",
            ),
        ],
        ids=["lat-layer1", "lat-layer2", "lat-layer3"],
    )
    def test_latex(self, i: int, b_i: float, h_i: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_e_7_latex = FormEDot6AreaOfLayerI(i=i, b_i=b_i, h_i=h_i).latex()
        assert form_e_7_latex.complete == rep_long
        assert form_e_7_latex.short == rep_short
