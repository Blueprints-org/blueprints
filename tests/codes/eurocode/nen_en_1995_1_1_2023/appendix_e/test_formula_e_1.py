"""Testing Formula E.1 from EN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2023.appendix_e.formula_e_1 import FormEDot1EffBendingStiffness
from blueprints.validations import LessOrEqualToZeroError


class TestFormEDot1EffBendingStiffnessLi:
    """Validation for formula E.1 from EN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("e_i", "i_i", "gamma_i", "a_i", "alpha_i", "expected_result"),
        [
            ([1, 1, 2], [1, 1, 2], [1, 1, 2], [1, 1, 2], [1, 1, 2], 40),
            ([1, 1, 200], [1, 1, 400], [1, 1, 0.2], [1, 1, 0.5], [1, 1, 0.25], 80005.250),
            ([1, 1], [1, 1], [1, 1], [1, 1], [1, 1], 4),
            ([1, 1], [1, 1], [1, 1], [1, 1], [1, 0], 3),
        ],
        ids=["test-3arg", "test-3argb", "test-2arg", "test-2argb"],
    )
    def test_evaluation(
        self, e_i: list[float], i_i: list[float], gamma_i: list[float], a_i: list[float], alpha_i: list[float], expected_result: float
    ) -> None:
        """Test the evaluation of the result."""
        form_e_1 = FormEDot1EffBendingStiffness(e_i=e_i, i_i=i_i, gamma_i=gamma_i, a_i=a_i, alpha_i=alpha_i)
        assert form_e_1 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("e_i", "i_i", "gamma_i", "a_i", "alpha_i", "expectation"),
        [
            ([1, 1, 2], [1, 1, 2], [1, 1, 2], [1, 1, 2], [1, 1, 2], does_not_raise()),
            ([1, 1], [1, 1], [1, 1], [1, 1], [1, 0], does_not_raise()),
            ([1, 1], [1, 1], [1, -1], [1, 1], [1, 0], pytest.raises(LessOrEqualToZeroError)),
            ([1, 1], [1, 1], [1, 1], [-1, 1], [1, 0], pytest.raises(LessOrEqualToZeroError)),
            ([-1, 1], [1, 1], [1, 1], [1, 1], [1, 0], pytest.raises(LessOrEqualToZeroError)),
            ([1, 1], [0, 1], [1, 1], [1, 1], [1, 0], pytest.raises(LessOrEqualToZeroError)),
            ([1, 1, 0], [1, 1], [1, 1], [1, 1], [1, 0], pytest.raises(ValueError, match="All input lists must have the same length")),
            (
                [1, 1, 0, 2],
                [1, 1, 2, 3],
                [1, 1, 2, 1],
                [1, 1, 1, 1],
                [1, 0, 1, 1],
                pytest.raises(ValueError, match="The length of the lists/layers must be either 2 or 3"),
            ),
        ],
        ids=["integer number", "decimal number", "negative_gamma_i", "negative_A_i", "negative_E_i", "zero_I_i", "unequal_lists", "long lists"],
    )
    def test_raise_error_incorrect_args(
        self, e_i: list[float], i_i: list[float], gamma_i: list[float], a_i: list[float], alpha_i: list[float], expectation: AbstractContextManager
    ) -> None:
        """Test the evaluation of incorrect arguments."""
        with expectation:
            assert FormEDot1EffBendingStiffness(e_i=e_i, i_i=i_i, gamma_i=gamma_i, a_i=a_i, alpha_i=alpha_i) is not None

    @pytest.mark.parametrize(
        ("e_i", "i_i", "gamma_i", "a_i", "alpha_i", "rep_short", "rep_long"),
        [
            (
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                r"(EI)_{ef} = 4.00",
                r"(EI)_{ef} = (E_1 I_1 + \gamma_1 E_1 A_1 \alpha_1^2) + (E_2 I_2 + \gamma_2 E_2 A_2 \alpha_2^2) = "
                r"(1.00 \cdot 1.00 + 1.00 \cdot 1.00 \cdot 1.00 \cdot 1.00^2) + "
                r"(1.00 \cdot 1.00 + 1.00 \cdot 1.00 \cdot 1.00 \cdot 1.00^2) = 4.00",
            ),
            (
                [1, 1, 200],
                [1, 1, 400],
                [1, 1, 0.2],
                [1, 1, 0.5],
                [1, 1, 0.25],
                r"(EI)_{ef} = 80005.25",
                r"(EI)_{ef} = (E_1 I_1 + \gamma_1 E_1 A_1 \alpha_1^2) + (E_2 I_2 + \gamma_2 E_2 A_2 \alpha_2^2) + "
                r"(E_3 I_3 + \gamma_3 E_3 A_3 \alpha_3^2) = "
                r"(1.00 \cdot 1.00 + 1.00 \cdot 1.00 \cdot 1.00 \cdot 1.00^2) + "
                r"(1.00 \cdot 1.00 + 1.00 \cdot 1.00 \cdot 1.00 \cdot 1.00^2) + "
                r"(200.00 \cdot 400.00 + 0.20 \cdot 200.00 \cdot 0.50 \cdot 0.25^2) = 80005.25",
            ),
        ],
        ids=["length_2", "length_3"],
    )
    def test_latex(
        self, e_i: list[float], i_i: list[float], gamma_i: list[float], a_i: list[float], alpha_i: list[float], rep_short: str, rep_long: str
    ) -> None:
        """Test the latex representation of the formula."""
        form_e_1_a_latex = FormEDot1EffBendingStiffness(e_i=e_i, i_i=i_i, gamma_i=gamma_i, a_i=a_i, alpha_i=alpha_i).latex()
        assert form_e_1_a_latex.complete == rep_long
        assert form_e_1_a_latex.short == rep_short
