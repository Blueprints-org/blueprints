"""Testing Formula E.2 from EN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2023.appendix_e.formula_e_2 import FormEDot2MechanicalConnectEfficiencyFactor
from blueprints.validations import LessOrEqualToZeroError


class TestFormEDot2MechanicalConnectEfficiencyFactor:
    """Validation for formula E.2 from EN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("i", "e_i", "a_i", "s_i", "k_i", "length", "expected_result"),
        [
            (1, 1, 1, 1, 1, 1000, 0.9999),
            (3, 8000, 20000, 200, 8000, 5000, 0.3877),
            (2, 8000, 20000, 200, 8000, 5000, 1.00),
        ],
        ids=["test-1st-layer", "test-3rd-layer", "test-2nd-layer"],
    )
    def test_evaluation(self, i: int, e_i: float, a_i: float, s_i: float, k_i: float, length: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_e_2 = FormEDot2MechanicalConnectEfficiencyFactor(i=i, e_i=e_i, a_i=a_i, s_i=s_i, k_i=k_i, length=length)
        assert form_e_2 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("i", "e_i", "a_i", "s_i", "k_i", "length", "expectation"),
        [
            (1, 1, 1, 1, 1, 1000, does_not_raise()),
            (1, 200, 3, 4, 5, 0, pytest.raises(LessOrEqualToZeroError)),
            (3, 1000, 20, 0, 3, 1000, pytest.raises(LessOrEqualToZeroError)),
            (3, -10000, 20, 3, 4, 100, pytest.raises(LessOrEqualToZeroError)),
            (2, 10, 0, 2, 3, 4, pytest.raises(LessOrEqualToZeroError)),
            (5, 10, 1, 2, 3, 4, pytest.raises(ValueError, match="The number of the layer must be either 1, 2 or 3")),
            (0, 10, 1, 2, 3, 4, pytest.raises(ValueError, match="The number of the layer must be either 1, 2 or 3")),
        ],
        ids=["passes", "zero_l", "zero_s2", "negative_e1", "zero_a1", "layer>3", "layer0"],
    )
    def test_raise_error_incorrect_args(
        self, i: int, e_i: float, a_i: float, s_i: float, k_i: float, length: float, expectation: AbstractContextManager
    ) -> None:
        """Test the evaluation of incorrect input arguments."""
        with expectation:
            assert FormEDot2MechanicalConnectEfficiencyFactor(i=i, e_i=e_i, a_i=a_i, s_i=s_i, k_i=k_i, length=length) is not None

    @pytest.mark.parametrize(
        ("i", "e_i", "a_i", "s_i", "k_i", "length", "rep_short", "rep_long"),
        [
            (
                1,
                1,
                1,
                1,
                1,
                1000,
                r"\gamma_1 = 1.00",
                r"\gamma_1 = \frac{1}{1+\frac{\pi^2 E_1 A_1 s_1}{K_1 l^2}}"
                r" = \frac{1}{1+\frac{\pi^2 1.00 \cdot 1.00 \cdot 1.00}{1.00 \cdot 1000.00^2}}"
                r" = 1.00",
            ),
            (
                3,
                8000,
                20000,
                200,
                8000,
                5000,
                r"\gamma_3 = 0.39",
                r"\gamma_3 = \frac{1}{1+\frac{\pi^2 E_3 A_3 s_3}{K_3 l^2}}"
                r" = \frac{1}{1+\frac{\pi^2 8000.00 \cdot 20000.00 \cdot 200.00}{8000.00 \cdot 5000.00^2}}"
                r" = 0.39",
            ),
            (
                2,
                1,
                1,
                1,
                1,
                1000,
                r"\gamma_2 = 1.00",
                r"\gamma_2 = 1.00 = 1.00 = 1.00",
            ),
        ],
        ids=["lat-layer1", "lat-layer3", "lat-layer2"],
    )
    def test_latex(self, i: int, e_i: float, a_i: float, s_i: float, k_i: float, length: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_e_2_latex = FormEDot2MechanicalConnectEfficiencyFactor(i=i, e_i=e_i, a_i=a_i, s_i=s_i, k_i=k_i, length=length).latex()
        assert form_e_2_latex.complete == rep_long
        assert form_e_2_latex.short == rep_short
