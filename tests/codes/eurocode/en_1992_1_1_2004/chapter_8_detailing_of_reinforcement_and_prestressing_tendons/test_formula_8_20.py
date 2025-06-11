"""Testing formula 8.20 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_20 import (
    Form8Dot20BondStrengthAnchorageULS,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot20BondStrengthAnchorageULS:
    """Validation for formula 8.20 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        eta_p2 = 1.4
        eta_1 = 1.0
        f_ctd = 2.5  # MPa
        form_8_20 = Form8Dot20BondStrengthAnchorageULS(eta_p2=eta_p2, eta_1=eta_1, f_ctd=f_ctd)
        # manually calculated result
        manually_calculated_result = 3.5  # MPa

        assert form_8_20 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_negative_values(self) -> None:
        """Test that a NegativeValueError is raised when negative values are passed."""
        eta_p2 = -1.4
        eta_1 = 1.0
        f_ctd = 2.5  # MPa
        with pytest.raises(NegativeValueError):
            Form8Dot20BondStrengthAnchorageULS(eta_p2=eta_p2, eta_1=eta_1, f_ctd=f_ctd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"f_{bpd} = \eta_{p2} \cdot \eta_{1} \cdot f_{ctd} = 1.400 \cdot 1.000 \cdot 2.500 = 3.500"),
            ("short", r"f_{bpd} = 3.500"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        eta_p2 = 1.4
        eta_1 = 1.0
        f_ctd = 2.5  # MPa
        form_8_20 = Form8Dot20BondStrengthAnchorageULS(eta_p2=eta_p2, eta_1=eta_1, f_ctd=f_ctd)

        # Object to test
        form_8_20_latex = form_8_20.latex()

        actual = {"complete": form_8_20_latex.complete, "short": form_8_20_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
