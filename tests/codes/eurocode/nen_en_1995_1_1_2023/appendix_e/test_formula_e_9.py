"""Testing Formula E.9 from EN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2023.appendix_e.formula_e_9 import FormEDot9BendingStressInILayer
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestFormEDot9BendingStressInILayer:
    """Validation for formula E.9 from EN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("n_i", "e_i", "h_i", "m_yd", "ei_ef", "expected_result"),
        [
            (2, 1, 1, 1, 1, 0.5),
            (1, 12000, 70, 10e06, 6015486104925.15, 0.6981979),
            (2, 4000, 20, 10e6, 6.2e12, 0.064516129),
            (3, 12000, 60, -8e6, 5.5e12, -0.523636),
            (2, 2000, 30, 0, 1e12, 0),
        ],
        ids=["test-1", "test-2", "test-3", "test-4", "test-5"],
    )
    def test_evaluation(self, n_i: int, e_i: float, h_i: float, m_yd: float, ei_ef: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_e_9 = FormEDot9BendingStressInILayer(i=n_i, e_i=e_i, h_i=h_i, m_yd=m_yd, ei_ef=ei_ef)
        assert form_e_9 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("n_i", "e_i", "h_i", "m_yd", "ei_ef", "expectation"),
        [
            (2, 1, 1, 1, 1, does_not_raise()),
            (3, 12000, 60, -8e6, 5.5e12, does_not_raise()),
            (3, 1, 0, 1, 1, does_not_raise()),
            (3, -12000, 60, 8e6, 5.5e12, pytest.raises(LessOrEqualToZeroError)),
            (1, 12000, -60, 8e6, 5.5e12, pytest.raises(LessOrEqualToZeroError)),
            (3, 12000, -60, 8e6, 200, pytest.raises(NegativeValueError)),
            (4, 12000, 60, 8e6, 20, pytest.raises(ValueError, match="The number of the layer must be either 1, 2 or 3")),
            (0, 12000, 60, 8e6, 20, pytest.raises(ValueError, match="The number of the layer must be either 1, 2 or 3")),
            (3, 12000, 60, 8e6, -20, pytest.raises(LessOrEqualToZeroError)),
        ],
        ids=["passes1", "passes2", "passes-h3=0", "negative_e_i", "negative_h_1", "negative_h_3", "layer>3", "layer0", "negative_ei_ef"],
    )
    def test_raise_error_incorrect_args(
        self, n_i: int, e_i: float, h_i: float, m_yd: float, ei_ef: float, expectation: AbstractContextManager
    ) -> None:
        """Test the evaluation of incorrect arguments."""
        with expectation:
            assert FormEDot9BendingStressInILayer(i=n_i, e_i=e_i, h_i=h_i, m_yd=m_yd, ei_ef=ei_ef) is not None

    @pytest.mark.parametrize(
        ("n_i", "e_i", "h_i", "m_yd", "ei_ef", "rep_short", "rep_long"),
        [
            (
                2,
                1,
                1,
                1,
                1,
                r"\sigma_{2} = 0.50",
                r"\sigma_{2} = \frac{0.5 E_2 h_2 M_{yd}}{EI_{ef}}"
                r" = \frac{0.5 \cdot 1.00 \cdot 1.00 \cdot 1.00}{1.00} = 0.50",
            ),
            (
                1,
                12000,
                70,
                10e06,
                6015486104925.15,
                r"\sigma_{1} = 0.70",
                r"\sigma_{1} = \frac{0.5 E_1 h_1 M_{yd}}{EI_{ef}}"
                r" = \frac{0.5 \cdot 12000.00 \cdot 70.00 \cdot 10000000.00}{6015486104925.15} = 0.70",
            ),
        ],
        ids=["latex_layer1", "latex_layer2"],
    )
    def test_latex(self, n_i: int, e_i: float, h_i: float, m_yd: float, ei_ef: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_e_9_latex = FormEDot9BendingStressInILayer(i=n_i, e_i=e_i, h_i=h_i, m_yd=m_yd, ei_ef=ei_ef).latex()
        assert form_e_9_latex.complete == rep_long
        assert form_e_9_latex.short == rep_short
