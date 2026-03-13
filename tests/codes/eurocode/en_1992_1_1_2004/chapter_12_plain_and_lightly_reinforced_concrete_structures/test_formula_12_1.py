"""Testing formula 12.1 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_12_plain_and_lightly_reinforced_concrete_structures.formula_12_1 import (
    Form12Dot1PlainConcreteTensileStrength,
)
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm12Dot1PlainConcreteTensileStrength:
    """Validation for formula 12.1 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        alpha_ct = 0.8  # -
        f_ctk_0_05 = 2.5  # MPa
        gamma_c = 1.5  # -

        # Object to test
        form_12_1 = Form12Dot1PlainConcreteTensileStrength(alpha_ct=alpha_ct, f_ctk_0_05=f_ctk_0_05, gamma_c=gamma_c)

        # Expected result, manually calculated
        manually_calculated_result = 1.333  # MPa

        assert round(form_12_1, 3) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("alpha_ct", "f_ctk_0_05", "gamma_c"),
        [
            (-0.8, 2.5, 1.5),
            (0.8, -2.5, 1.5),
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self,
        alpha_ct: DIMENSIONLESS,
        f_ctk_0_05: DIMENSIONLESS,
        gamma_c: DIMENSIONLESS,
    ) -> None:
        """Test negative values for alpha_ct_pl and f_ctk_0_05."""
        with pytest.raises(NegativeValueError):
            Form12Dot1PlainConcreteTensileStrength(alpha_ct=alpha_ct, f_ctk_0_05=f_ctk_0_05, gamma_c=gamma_c)

    @pytest.mark.parametrize(
        "gamma_c",
        [
            0,
            -1.5,
        ],
    )
    def test_raise_error_when_gamma_c_is_less_or_equal_to_zero(
        self,
        gamma_c: DIMENSIONLESS,
    ) -> None:
        """Test gamma_c less or equal to zero."""
        with pytest.raises(LessOrEqualToZeroError):
            Form12Dot1PlainConcreteTensileStrength(alpha_ct=0.8, f_ctk_0_05=2.5, gamma_c=gamma_c)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{ctd,pl} = \alpha_{ct,pl} \cdot \frac{f_{ctk,0.05}}{\gamma_{C}} = 0.800 \cdot \frac{2.500}{1.500} " r"= 1.333",
            ),
            ("short", r"f_{ctd,pl} = 1.333"),
            (
                "string",
                r"f_{ctd,pl} = \alpha_{ct,pl} \cdot \frac{f_{ctk,0.05}}{\gamma_{C}} = 0.800 \cdot \frac{2.500}{1.500} " r"= 1.333",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        alpha_ct = 0.8  # -
        f_ctk_0_05 = 2.5  # MPa
        gamma_c = 1.5  # -

        # Object to test
        form_12_1_latex = Form12Dot1PlainConcreteTensileStrength(
            alpha_ct=alpha_ct,
            f_ctk_0_05=f_ctk_0_05,
            gamma_c=gamma_c,
        ).latex()

        actual = {
            "complete": form_12_1_latex.complete,
            "short": form_12_1_latex.short,
            "string": str(form_12_1_latex),
        }

        assert actual[representation] == expected, f"{representation} representation failed."
