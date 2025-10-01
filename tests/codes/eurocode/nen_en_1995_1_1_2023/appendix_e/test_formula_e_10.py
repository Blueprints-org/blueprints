"""Testing Formula E.10 from EN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from dataclasses import asdict, dataclass

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2023.appendix_e.formula_e_10 import FormEDot10ShearStressInLayer2
from blueprints.validations import LessOrEqualToZeroError


@dataclass(frozen=True)
class FormE10Params:
    """Container for the input parameters of Formula E.10 from EN 1995-1-1:2023, Annex E."""

    gamma_3: float
    e_2: float
    e_3: float
    a_3: float
    alpha_2: float
    alpha_3: float
    h_2: float
    b_2: float
    v_d: float
    ei_ef: float


class TestFormEDot10MaxShearStressInLayer2:
    """Validation for formula E.10 from EN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("params", "expected_result"),
        [
            (FormE10Params(1, 1, 1, 1, 1, 1, 1, 1, 1, 1), 1.5),
            (FormE10Params(0.767, 4000, 12000, 60000, 0, 70, 80, 1000, 10e03, 6015486104925.15), 0.0695920),
            (FormE10Params(0.86822, 12000, 12000, 30000, 12.035, 32.96469, 60, 1000, 20e03, 2173632196491.10), 0.1664219),
            (FormE10Params(0.92946, 12000, 12000, 15000, -10.002, 55.0018, 60, 20, 20000, 814959895024.47), 11.38334),
        ],
        ids=["test-1", "test-2", "test-3", "test-4"],
    )
    def test_evaluation(self, params: FormE10Params, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_e_10 = FormEDot10ShearStressInLayer2(**asdict(params))
        assert form_e_10 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("params", "expectation"),
        [
            (FormE10Params(1, 1, 1, 1, 1, 1, 1, 1, 1, 1), does_not_raise()),
            (FormE10Params(0.767, 4000, 12000, 60000, 0, 70, 80, 1000, 10e03, 6015486104925.15), does_not_raise()),
            (FormE10Params(0.767, 4000, 12000, 60000, 0, 70, 80, 1000, -10e03, 6015486104925.15), does_not_raise()),
            (FormE10Params(0.767, -4000, 12000, 60000, 0, 70, 80, 1000, 10e03, 6015486104925.15), pytest.raises(LessOrEqualToZeroError)),
            (FormE10Params(0.767, 4000, -12000, 60000, 0, 70, 80, 1000, 10e03, 6015486104925.15), pytest.raises(LessOrEqualToZeroError)),
            (FormE10Params(0.767, 4000, 12000, -60000, 0, 70, 80, 1000, 10e03, 6015486104925.15), pytest.raises(LessOrEqualToZeroError)),
            (FormE10Params(0.767, 4000, 12000, 60000, 0, -70, 80, 1000, 10e03, 6015486104925.15), pytest.raises(LessOrEqualToZeroError)),
            (FormE10Params(0.767, 4000, 12000, 60000, 0, 70, 0, 1000, 10e03, 6015486104925.15), pytest.raises(LessOrEqualToZeroError)),
            (FormE10Params(0.767, 4000, 12000, 60000, 0, 70, 80, -1000, 10e03, 6015486104925.15), pytest.raises(LessOrEqualToZeroError)),
            (FormE10Params(0.767, 4000, 12000, 60000, 0, 70, 80, 1000, 10e03, -6015486104925.15), pytest.raises(LessOrEqualToZeroError)),
        ],
        ids=[
            "passes1",
            "passes2",
            "passes-vd<0",
            "negative_e_2",
            "negative_e_3",
            "negative_a_3",
            "negative_alpha_3",
            "h2=0",
            "negative_b2",
            "negative_ei_ef",
        ],
    )
    def test_raise_error_incorrect_args(self, params: FormE10Params, expectation: AbstractContextManager) -> None:
        """Test the evaluation of incorrect arguments."""
        with expectation:
            assert FormEDot10ShearStressInLayer2(**asdict(params)) is not None

    @pytest.mark.parametrize(
        ("params", "rep_short", "rep_long"),
        [
            (
                FormE10Params(1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                r"\tau_{2,max} = 1.50",
                r"\tau_{2,max} = \left[\gamma_3 E_3 A_3 \alpha_3"
                r" + 0.5 E_2 b_2 \left(\frac{\alpha_2 + h_2}{2}\right)^2\right] \frac{V_d}{b_{2} EI_{ef}}"
                r" = \left[1.00 \cdot 1.00 \cdot 1.00 \cdot 1.00"
                r" + 0.5 \cdot 1.00 \cdot 1.00 \left(\frac{1.00 + 1.00}{2}\right)^2\right] \frac{1.00}{1.00 \cdot 1.00}"
                r" = 1.50",
            ),
            (
                FormE10Params(0.767, 4000, 12000, 60000, 0, 70, 80, 1000, 10e03, 6015486104925.15),
                r"\tau_{2,max} = 0.07",
                r"\tau_{2,max} = \left[\gamma_3 E_3 A_3 \alpha_3"
                r" + 0.5 E_2 b_2 \left(\frac{\alpha_2 + h_2}{2}\right)^2\right] \frac{V_d}{b_{2} EI_{ef}}"
                r" = \left[0.77 \cdot 12000.00 \cdot 60000.00 \cdot 70.00"
                r" + 0.5 \cdot 4000.00 \cdot 1000.00 \left(\frac{0.00 + 80.00}{2}\right)^2\right] \frac{10000.00}{1000.00 \cdot 6015486104925.15}"
                r" = 0.07",
            ),
        ],
        ids=["latex-test-1", "latex-test-2"],
    )
    def test_latex(self, params: FormE10Params, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_e_10_latex = FormEDot10ShearStressInLayer2(**asdict(params)).latex()
        assert form_e_10_latex.complete == rep_long
        assert form_e_10_latex.short == rep_short
