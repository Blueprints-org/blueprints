"""Testing formula 8.8N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_8n import (
    Form8Dot8nAnchorageCapacityWeldedTransverseBar,
    SubForm8Dot8nConcreteStress,
    SubForm8Dot8nDesignLengthOfTransverseBar,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot8nAnchorageCapacityWeldedTransverseBar:
    """Validation for formula 8.8N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        l_td = 100  # mm
        diameter_t = 16  # mm
        sigma_td = 60  # MPa
        f_wd = 400  # kN
        form_8_8n = Form8Dot8nAnchorageCapacityWeldedTransverseBar(
            l_td=l_td,
            diameter_t=diameter_t,
            sigma_td=sigma_td,
            f_wd=f_wd,
        )

        # Expected result, manually calculated
        manually_calculated_result = 96

        assert form_8_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_maximum(self) -> None:
        """Test the evaluation of the result if the maximum is reached."""
        # Example values
        l_td = 100  # mm
        diameter_t = 16  # mm
        sigma_td = 60  # MPa
        f_wd = 50  # kN
        form_8_8n = Form8Dot8nAnchorageCapacityWeldedTransverseBar(
            l_td=l_td,
            diameter_t=diameter_t,
            sigma_td=sigma_td,
            f_wd=f_wd,
        )

        # Expected result, manually calculated
        manually_calculated_result = 50

        assert form_8_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_l_td_is_given(self) -> None:
        """Test if NegativeValueError is raised when l_td is negative."""
        # Example values
        l_td = -100  # mm
        diameter_t = 16  # mm
        sigma_td = 60  # MPa
        f_wd = 50  # kN

        with pytest.raises(NegativeValueError):
            Form8Dot8nAnchorageCapacityWeldedTransverseBar(
                l_td=l_td,
                diameter_t=diameter_t,
                sigma_td=sigma_td,
                f_wd=f_wd,
            )

    def test_raise_error_when_negative_diameter_t_is_given(self) -> None:
        """Test if NegativeValueError is raised when diameter_t is negative."""
        # Example values
        l_td = 100  # mm
        diameter_t = -16  # mm
        sigma_td = 60  # MPa
        f_wd = 50  # kN

        with pytest.raises(NegativeValueError):
            Form8Dot8nAnchorageCapacityWeldedTransverseBar(
                l_td=l_td,
                diameter_t=diameter_t,
                sigma_td=sigma_td,
                f_wd=f_wd,
            )

    def test_raise_error_when_negative_sigma_td_is_given(self) -> None:
        """Test if NegativeValueError is raised when sigma_td is negative."""
        # Example values
        l_td = 100  # mm
        diameter_t = 16  # mm
        sigma_td = -60  # MPa
        f_wd = 50  # kN

        with pytest.raises(NegativeValueError):
            Form8Dot8nAnchorageCapacityWeldedTransverseBar(
                l_td=l_td,
                diameter_t=diameter_t,
                sigma_td=sigma_td,
                f_wd=f_wd,
            )

    def test_raise_error_when_negative_f_wd_is_given(self) -> None:
        """Test if NegativeValueError is raised when f_wd is negative."""
        # Example values
        l_td = 100  # mm
        diameter_t = 16  # mm
        sigma_td = 60  # MPa
        f_wd = -50  # kN

        with pytest.raises(NegativeValueError):
            Form8Dot8nAnchorageCapacityWeldedTransverseBar(
                l_td=l_td,
                diameter_t=diameter_t,
                sigma_td=sigma_td,
                f_wd=f_wd,
            )

    def test_integration_with_sub_formula_8_8_design_length_of_transverse_bar(
        self,
    ) -> None:
        """Test the integration with sub-formula 8.8 for calculating design length of transverse bar ltd."""
        # Example values
        diameter_t = 16  # mm
        sigma_td = 60  # MPa
        f_wd = 150  # kN
        f_yd = 500  # MPa
        l_t = 100  # mm
        l_td = SubForm8Dot8nDesignLengthOfTransverseBar(
            diameter_t=diameter_t,
            f_yd=f_yd,
            sigma_td=sigma_td,
            l_t=l_t,
        )

        # Object to test
        form_8_8n = Form8Dot8nAnchorageCapacityWeldedTransverseBar(
            l_td=l_td,
            diameter_t=diameter_t,
            sigma_td=sigma_td,
            f_wd=f_wd,
        )

        # Expected result, manually calculated
        manually_calculated_result = 51.434980

        assert form_8_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_integration_with_sub_formula_8_8_concrete_stress(self) -> None:
        """Test the integration with sub-formula 8.8 for calculating concrete stress σtd."""
        # Example values
        diameter_t = 16  # mm
        f_wd = 150  # kN
        l_td = 80  # mm
        f_ctd = 3  # MPa
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
        form_8_8n = Form8Dot8nAnchorageCapacityWeldedTransverseBar(
            l_td=l_td,
            diameter_t=diameter_t,
            sigma_td=sigma_td,
            f_wd=f_wd,
        )

        # Expected result, manually calculated
        manually_calculated_result = 46.080000

        assert form_8_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{btd} = \min\left( l_{td} \cdot Ø_t \cdot \sigma_{td}, F_{wd} \right)"
                r" = \min\left( 80.00 \cdot 16.00 \cdot 36.00 / 1000, 150.00 \right) = 46.08",
            ),
            ("short", r"F_{btd} = 46.08"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        diameter_t = 16  # mm
        f_wd = 150  # kN
        l_td = 80  # mm
        f_ctd = 3  # MPa
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
        form_8_8n_latex = Form8Dot8nAnchorageCapacityWeldedTransverseBar(
            l_td=l_td,
            diameter_t=diameter_t,
            sigma_td=sigma_td,
            f_wd=f_wd,
        ).latex()

        actual = {"complete": form_8_8n_latex.complete, "short": form_8_8n_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
