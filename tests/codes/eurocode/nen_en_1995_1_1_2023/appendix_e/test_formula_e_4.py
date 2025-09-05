"""Testing Formula E.4 from EN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2023.appendix_e.formula_e_4 import FormEDot4DistanceToCentroidA2
from blueprints.validations import LessOrEqualToZeroError


class TestFormEDot4DistanceToCentroidA2:
    """Validation for formula E.4 from EN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("e_i", "a_i", "gamma_i", "h_i", "expected_result"),
        [
            ([1, 1, 2], [1, 1, 2], [1, 1, 2], [1, 1, 2], -1.10),
            ([1, 1, 200], [1, 1, 400], [1, 1, 0.2], [1, 1, 0.25], -0.625),
            ([1, 1], [1, 1], [1, 1], [1, 1], 0.50),
            ([1000, 2000], [2000, 2000], [0.5, 0.8], [30, 30], 7.143),
        ],
        ids=["test-3arg", "test-3argb", "test-2arg", "test-2argb"],
    )
    def test_evaluation(self, e_i: list[float], a_i: list[float], gamma_i: list[float], h_i: list[float], expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_e_4 = FormEDot4DistanceToCentroidA2(e_i=e_i, a_i=a_i, gamma_i=gamma_i, h_i=h_i)
        assert form_e_4 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("e_i", "a_i", "gamma_i", "h_i", "expectation"),
        [
            ([1, 1, 2], [1, 1, 2], [1, 1, 2], [1, 1, 2], does_not_raise()),
            ([1, 1], [1, 1], [1, 1], [1, 1], does_not_raise()),
            ([1, 1], [1, 1], [1, -1], [1, 1], pytest.raises(LessOrEqualToZeroError)),
            ([1, 1], [1, 1], [1, 1], [1, 0], pytest.raises(LessOrEqualToZeroError)),
            ([-1, 1], [1, 1], [1, 1], [1, 1], pytest.raises(LessOrEqualToZeroError)),
            ([1, 1], [0, 1], [1, 1], [1, 1], pytest.raises(LessOrEqualToZeroError)),
            ([1, 1, 0], [1, 1], [1, 1], [1, 1], pytest.raises(ValueError, match="All input lists must have the same length")),
            (
                [1, 1, 0, 2],
                [1, 1, 2, 3],
                [1, 1, 2, 1],
                [1, 1, 1, 1],
                pytest.raises(ValueError, match="The length of the lists/layers must be either 2 or 3"),
            ),
        ],
        ids=["integer number", "decimal number", "negative_gamma_i", "zero_h_i", "negative_E_i", "zero_A_i", "unequal_lists", "long lists"],
    )
    def test_raise_error_incorrect_args(
        self, e_i: list[float], a_i: list[float], gamma_i: list[float], h_i: list[float], expectation: AbstractContextManager
    ) -> None:
        """Test the evaluation of incorrect arguments."""
        with expectation:
            assert FormEDot4DistanceToCentroidA2(e_i=e_i, a_i=a_i, gamma_i=gamma_i, h_i=h_i) is not None

    @pytest.mark.parametrize(
        ("e_i", "a_i", "gamma_i", "h_i", "rep_short", "rep_long"),
        [
            (
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                r"\alpha_{2} = 0.50",
                r"\alpha_{2} = \frac{\gamma_1 E_1 A_1 (h_1 + h_2)}{2 \left(\gamma_1 E_1 A_1 + \gamma_2 E_2 A_2\right)}"
                r" = \frac{1.00 \cdot 1.00 \cdot 1.00 (1.00 + 1.00)}{2 \left(1.00 \cdot 1.00 \cdot 1.00 + 1.00 \cdot 1.00 \cdot 1.00\right)}"
                " = 0.50",
            ),
            (
                [1, 1, 200],
                [1, 1, 400],
                [1, 1, 0.2],
                [1, 1, 0.25],
                r"\alpha_{2} = -0.62",
                r"\alpha_{2} = \frac{\gamma_1 E_1 A_1 (h_1 + h_2) - \gamma_3 E_3 A_3 (h_2 + h_3)}"
                r"{2 \left(\gamma_1 E_1 A_1 + \gamma_2 E_2 A_2 + \gamma_3 E_3 A_3\right)}"
                r" = \frac{1.00 \cdot 1.00 \cdot 1.00 (1.00 + 1.00) - 0.20 \cdot 200.00 \cdot 400.00 (1.00 + 0.25)}"
                r"{2 \left(1.00 \cdot 1.00 \cdot 1.00 + 1.00 \cdot 1.00 \cdot 1.00 + 0.20 \cdot 200.00 \cdot 400.00\right)}"
                " = -0.62",
            ),
        ],
        ids=["length_2", "length_3"],
    )
    def test_latex(self, e_i: list[float], a_i: list[float], gamma_i: list[float], h_i: list[float], rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_e_4_latex = FormEDot4DistanceToCentroidA2(e_i=e_i, a_i=a_i, gamma_i=gamma_i, h_i=h_i).latex()
        assert form_e_4_latex.complete == rep_long
        assert form_e_4_latex.short == rep_short
