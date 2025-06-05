"""Testing sub-formula 1 for 8.8N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_8n import (
    SubForm8Dot8nConcreteStress,
    SubForm8Dot8nDesignLengthOfTransverseBar,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestSubForm8Dot8nDesignLengthOfTransverseBar:
    """Validation for sub-formula 8.8N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        diameter_t = 16  # mm
        f_yd = 500  # MPa
        sigma_td = 60  # MPa
        l_t = 100  # mm
        sub_form_8_8n_1 = SubForm8Dot8nDesignLengthOfTransverseBar(
            diameter_t=diameter_t,
            f_yd=f_yd,
            sigma_td=sigma_td,
            l_t=l_t,
        )
        # Expected result, manually calculated
        manually_result = 53.578104
        assert sub_form_8_8n_1 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_evaluation_upper_limit(self) -> None:
        """Test the evaluation of the result if the upper limit is reached."""
        diameter_t = 32  # mm
        f_yd = 500  # MPa
        sigma_td = 60  # MPa
        l_t = 50  # mm
        sub_form_8_8n_1 = SubForm8Dot8nDesignLengthOfTransverseBar(
            diameter_t=diameter_t,
            f_yd=f_yd,
            sigma_td=sigma_td,
            l_t=l_t,
        )
        # Expected result, manually calculated
        manually_result = 50
        assert sub_form_8_8n_1 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_diameter_t_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when diameter_t is negative."""
        # Example values
        diameter_t = -16  # mm
        f_yd = 500  # MPa
        sigma_td = 60  # MPa
        l_t = 100  # mm

        with pytest.raises(NegativeValueError):
            SubForm8Dot8nDesignLengthOfTransverseBar(
                diameter_t=diameter_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_raise_error_when_f_yd_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when f_yd is negative."""
        # Example values
        diameter_t = 16  # mm
        f_yd = -500  # MPa
        sigma_td = 60  # MPa
        l_t = 100  # mm

        with pytest.raises(NegativeValueError):
            SubForm8Dot8nDesignLengthOfTransverseBar(
                diameter_t=diameter_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_raise_error_when_sigma_td_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when sigma_td is negative."""
        # Example values
        diameter_t = 16  # mm
        f_yd = 500  # MPa
        sigma_td = -60  # MPa
        l_t = 100  # mm

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8nDesignLengthOfTransverseBar(
                diameter_t=diameter_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_raise_error_when_sigma_td_is_zero(self) -> None:
        """Test if a NegativeValueError is raised when sigma_td is zero."""
        # Example values
        diameter_t = 16  # mm
        f_yd = 500  # MPa
        sigma_td = 0  # MPa
        l_t = 100  # mm

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8nDesignLengthOfTransverseBar(
                diameter_t=diameter_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_raise_error_when_l_t_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when l_t is negative."""
        # Example values
        diameter_t = 16  # mm
        f_yd = 500  # MPa
        sigma_td = 60  # MPa
        l_t = -100  # mm

        with pytest.raises(NegativeValueError):
            SubForm8Dot8nDesignLengthOfTransverseBar(
                diameter_t=diameter_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_integration_with_sub_form_8_8n_concrete_stress(self) -> None:
        """Test the integration with sub-formula 8.8 for calculating concrete stress."""
        # Example values
        diameter_t = 16  # mm
        f_yd = 500  # MPa
        l_t = 100  # mm
        f_ctd = 2.6  # MPa
        sigma_cm = 15  # MPa
        y_function = 0.5  # -
        f_cd = 25  # MPa
        sigma_td = SubForm8Dot8nConcreteStress(
            f_ctd=f_ctd,
            sigma_cm=sigma_cm,
            y_function=y_function,
            f_cd=f_cd,
        )

        # Object to test
        form_8_8n = SubForm8Dot8nDesignLengthOfTransverseBar(
            diameter_t=diameter_t,
            f_yd=f_yd,
            sigma_td=sigma_td,
            l_t=l_t,
        )

        manually_calculated_result = 69.950631942

        assert form_8_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"l_{td} = \min\left(l_t, 1.16 \cdot Ø_t \cdot ({\frac{f_{yd}}{\sigma_{td}}})^{0.5} \right) = "
                    r"\min\left(100.00, 1.16 \cdot 16.00 \cdot ({\frac{500.00}{35.20}})^{0.5} \right) = 69.95"
                ),
            ),
            ("short", r"l_{td} = 69.95"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        diameter_t = 16  # mm
        f_yd = 500  # MPa
        l_t = 100  # mm
        f_ctd = 2.6  # MPa
        sigma_cm = 15  # MPa
        y_function = 0.5  # -
        f_cd = 25  # MPa
        sigma_td = SubForm8Dot8nConcreteStress(
            f_ctd=f_ctd,
            sigma_cm=sigma_cm,
            y_function=y_function,
            f_cd=f_cd,
        )

        # Object to test
        sub_form_8_8n_1_latex = SubForm8Dot8nDesignLengthOfTransverseBar(
            diameter_t=diameter_t,
            f_yd=f_yd,
            sigma_td=sigma_td,
            l_t=l_t,
        ).latex()

        actual = {"complete": sub_form_8_8n_1_latex.complete, "short": sub_form_8_8n_1_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
