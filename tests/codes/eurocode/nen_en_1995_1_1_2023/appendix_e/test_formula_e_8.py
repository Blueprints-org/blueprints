"""Testing Formula E.8 from EN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2023.appendix_e.formula_e_8 import FormEDot8AxialStressInILayer
from blueprints.validations import LessOrEqualToZeroError


class TestFormEDot8AxialStressInILayer:
    """Validation for formula E.8 from EN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("n_i", "gamma_i", "e_i", "alpha_i", "m_yd", "ei_ef", "expected_result"),
        [
            (2, 1, 1, 1, 1, 1, 1),
            (1, 0.767, 12000, 70, 10e06, 6015486104925.15, 1.071035),
            (2, 1, 4000, 20, 10e6, 6.2e12, 0.129032258),
            (3, 0.8, 12000, 60, -8e6, 5.5e12, -0.837818),
            (2, 1, 2000, -10, 0, 1e12, 0),
        ],
        ids=["test-1", "test-2", "test-3", "test-4", "test-5"],
    )
    def test_evaluation(self, n_i: int, gamma_i: float, e_i: float, alpha_i: float, m_yd: float, ei_ef: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_e_8 = FormEDot8AxialStressInILayer(i=n_i, gamma_i=gamma_i, e_i=e_i, alpha_i=alpha_i, m_yd=m_yd, ei_ef=ei_ef)
        assert form_e_8 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("n_i", "gamma_i", "e_i", "alpha_i", "m_yd", "ei_ef", "expectation"),
        [
            (2, 1, 1, 1, 1, 1, does_not_raise()),
            (3, 0.8, 12000, 60, -8e6, 5.5e12, does_not_raise()),
            (2, 1, 1, 0.0000001, 1, 1, does_not_raise()),
            (3, -0.8, 12000, 60, 8e6, 5.5e12, pytest.raises(LessOrEqualToZeroError)),
            (1, 0.8, -12000, 60, 8e6, 5.5e12, pytest.raises(LessOrEqualToZeroError)),
            (3, 0.8, 12000, 60, 8e6, 0, pytest.raises(LessOrEqualToZeroError)),
            (4, 0.8, 12000, 60, 8e6, 20, pytest.raises(ValueError, match="The number of the layer must be either 1, 2 or 3")),
            (0, 0.8, 12000, 60, 8e6, 20, pytest.raises(ValueError, match="The number of the layer must be either 1, 2 or 3")),
            (3, 0.8, 12000, -60, 8e6, 20, pytest.raises(LessOrEqualToZeroError)),
            (2, 0.8, 12000, -60, 8e6, 30, does_not_raise()),
        ],
        ids=[
            "passes1",
            "passes2",
            "passes3",
            "negative_gamma_i",
            "negative_e_i",
            "zero_ei_ef",
            "layer>3",
            "layer0",
            "negative_alpha_3",
            "passes_neg_alpha_2",
        ],
    )
    def test_raise_error_incorrect_args(
        self, n_i: int, gamma_i: float, e_i: float, alpha_i: float, m_yd: float, ei_ef: float, expectation: AbstractContextManager
    ) -> None:
        """Test the evaluation of incorrect arguments."""
        with expectation:
            assert FormEDot8AxialStressInILayer(i=n_i, gamma_i=gamma_i, e_i=e_i, alpha_i=alpha_i, m_yd=m_yd, ei_ef=ei_ef) is not None

    @pytest.mark.parametrize(
        ("n_i", "gamma_i", "e_i", "alpha_i", "m_yd", "ei_ef", "rep_short", "rep_long"),
        [
            (
                2,
                1,
                1,
                1,
                1,
                1,
                r"\sigma_{2} = 1.00",
                r"\sigma_{2} = \frac{\gamma_2 E_2 \alpha_2 M_{yd}}{EI_{ef}}"
                r" = \frac{1.00 \cdot 1.00 \cdot 1.00 \cdot 1.00}{1.00} = 1.00",
            ),
            (
                1,
                0.767,
                12000,
                70,
                10e06,
                6015486104925.15,
                r"\sigma_{1} = 1.07",
                r"\sigma_{1} = \frac{\gamma_1 E_1 \alpha_1 M_{yd}}{EI_{ef}}"
                r" = \frac{0.77 \cdot 12000.00 \cdot 70.00 \cdot 10000000.00}{6015486104925.15} = 1.07",
            ),
        ],
        ids=["latex_layer1", "latex_layer2"],
    )
    def test_latex(self, n_i: int, gamma_i: float, e_i: float, alpha_i: float, m_yd: float, ei_ef: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_e_8_latex = FormEDot8AxialStressInILayer(i=n_i, gamma_i=gamma_i, e_i=e_i, alpha_i=alpha_i, m_yd=m_yd, ei_ef=ei_ef).latex()
        assert form_e_8_latex.complete == rep_long
        assert form_e_8_latex.short == rep_short
