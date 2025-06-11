"""Testing formula 12.5 and 12.6 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_12_plain_and_lightly_reinforced_concrete_structures.formula_12_5_6 import (
    Form12Dot3PlainConcreteShearStress,
    Form12Dot5And6PlainConcreteBendingResistance,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm12Dot5PlainConcreteBendingResistance:
    """Validation for formula 12.5 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ctd_pl = 2.5  # MPa
        sigma_cp = 1.0  # MPa
        sigma_c_lim = 1.5  # MPa

        # Object to test
        form_12_5 = Form12Dot5And6PlainConcreteBendingResistance(f_ctd_pl=f_ctd_pl, sigma_cp=sigma_cp, sigma_c_lim=sigma_c_lim)

        # Expected result, manually calculated
        manually_calculated_result = 2.958

        assert round(form_12_5, 3) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_comparison_not_satisfied(self) -> None:
        """Test the evaluation of the result when the comparison is not satisfied."""
        # Example values
        f_ctd_pl = 2.5  # MPa
        sigma_cp = 2.0  # MPa
        sigma_c_lim = 1.5  # MPa

        # Object to test
        form_12_5 = Form12Dot5And6PlainConcreteBendingResistance(f_ctd_pl=f_ctd_pl, sigma_cp=sigma_cp, sigma_c_lim=sigma_c_lim)

        # Expected result, manually calculated
        manually_calculated_result = 3.112

        assert round(form_12_5, 3) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_ctd_pl", "sigma_cp"),
        [
            (-2.5, 1.0),
            (2.5, -1.0),
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self,
        f_ctd_pl: float,
        sigma_cp: float,
    ) -> None:
        """Test negative values for f_ctd_pl and sigma_cp."""
        with pytest.raises(LessOrEqualToZeroError):
            Form12Dot5And6PlainConcreteBendingResistance(f_ctd_pl=f_ctd_pl, sigma_cp=sigma_cp, sigma_c_lim=1.5)

    @pytest.mark.parametrize(
        ("f_ctd_pl", "sigma_cp"),
        [
            (0.0, 1.0),
            (2.5, 0.0),
        ],
    )
    def test_raise_error_when_values_are_less_or_equal_to_zero(
        self,
        f_ctd_pl: float,
        sigma_cp: float,
    ) -> None:
        """Test values less or equal to zero for f_ctd_pl and sigma_cp."""
        with pytest.raises(LessOrEqualToZeroError):
            Form12Dot5And6PlainConcreteBendingResistance(f_ctd_pl=f_ctd_pl, sigma_cp=sigma_cp, sigma_c_lim=1.5)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{cvd} = \sqrt{f_{ctd, pl} ^ 2 + \sigma_{cp} \cdot f_{ctd, pl}} = \sqrt{2.500 ^ 2 + 1.000 \cdot 2.500} = 2.958",
            ),
            ("short", r"f_{cvd} = 2.958"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ctd_pl = 2.5  # MPa
        sigma_cp = 1.0  # MPa
        sigma_c_lim = 1.5  # MPa

        # Object to test
        form_12_5_latex = Form12Dot5And6PlainConcreteBendingResistance(
            f_ctd_pl=f_ctd_pl,
            sigma_cp=sigma_cp,
            sigma_c_lim=sigma_c_lim,
        ).latex()

        actual = {
            "complete": form_12_5_latex.complete,
            "short": form_12_5_latex.short,
            "string": str(form_12_5_latex),
        }

        assert actual[representation] == expected, f"{representation} representation failed."

    def test_latex_comparison_not_satisfied(self) -> None:
        """Test the latex representation of the formula when the comparison is not satisfied."""
        # Example values
        f_ctd_pl = 2.5  # MPa
        sigma_cp = 2.0  # MPa
        sigma_c_lim = 1.5  # MPa

        # Object to test
        form_12_5_latex = Form12Dot5And6PlainConcreteBendingResistance(
            f_ctd_pl=f_ctd_pl,
            sigma_cp=sigma_cp,
            sigma_c_lim=sigma_c_lim,
        ).latex()

        expected = (
            r"f_{cvd} = \sqrt{f_{ctd, pl} ^ 2 + \sigma_{cp} \cdot f_{ctd, pl} - "
            r"\left(\frac{\sigma_{cp} - \sigma_{c, lim}}{2}\right) ^ 2} = "
            r"\sqrt{2.500 ^ 2 + 2.000 \cdot 2.500 - \left(\frac{2.000 - "
            r"1.500}2\right) ^ 2} = 3.112"
        )

        assert form_12_5_latex.complete == expected, "Latex representation failed when comparison is not satisfied."

    def test_evaluation_with_sigma_cp_object(self) -> None:
        """Test the evaluation of the result with sigma_cp as an object."""
        # Example values
        f_ctd_pl = 2.5  # MPa
        sigma_cp_object = Form12Dot3PlainConcreteShearStress(n_ed=100000.0, a_cc=50000.0)  # MPa
        sigma_c_lim = 1.5  # MPa

        # Object to test
        form_12_5 = Form12Dot5And6PlainConcreteBendingResistance(f_ctd_pl=f_ctd_pl, sigma_cp=sigma_cp_object, sigma_c_lim=sigma_c_lim)

        manually_calculated_result = 3.112
        assert round(form_12_5, 3) == pytest.approx(expected=round(manually_calculated_result, 3), rel=1e-4)
