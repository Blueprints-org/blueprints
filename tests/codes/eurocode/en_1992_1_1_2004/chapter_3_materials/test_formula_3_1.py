"""Testing formula 3.1 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_1 import Form3Dot1EstimationConcreteCompressiveStrength
from blueprints.validations import NegativeValueError


class TestForm3Dot1EstimationConcreteCompressiveStrength:
    """Validation for formula 3.1 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = 1  # -
        f_cm = 10  # MPa
        form_3_1 = Form3Dot1EstimationConcreteCompressiveStrength(beta_cc_t=beta_cc_t, f_cm=f_cm)

        # Expected result, manually calculated
        manually_calculated_result = 10

        assert form_3_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_beta_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = -1  # -
        f_cm = 10  # MPa

        with pytest.raises(NegativeValueError):
            Form3Dot1EstimationConcreteCompressiveStrength(beta_cc_t=beta_cc_t, f_cm=f_cm)

    def test_raise_error_when_negative_f_cm_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = 1  # -
        f_cm = -10  # MPa

        with pytest.raises(NegativeValueError):
            Form3Dot1EstimationConcreteCompressiveStrength(beta_cc_t=beta_cc_t, f_cm=f_cm)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{cm}(t) = \beta_{cc}(t) \cdot f_{cm} = 1.000 \cdot 10.000 = 10.000",
            ),
            ("short", r"f_{cm}(t) = 10.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta_cc_t = 1  # -
        f_cm = 10  # MPa

        # Object to test
        form_3_1_latex = Form3Dot1EstimationConcreteCompressiveStrength(beta_cc_t=beta_cc_t, f_cm=f_cm).latex()

        actual = {"complete": form_3_1_latex.complete, "short": form_3_1_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
