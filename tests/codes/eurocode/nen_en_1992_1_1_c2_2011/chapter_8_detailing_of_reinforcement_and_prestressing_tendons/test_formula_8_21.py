"""Testing formula 8.21 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_21 import (
    Form8Dot21AnchorageLength,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot21DispersionLength:
    """Validation for formula 8.21 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        l_pt2 = 100.0  # mm
        alpha_2 = 0.8
        diameter = 12.0  # mm
        sigma_pd = 1000.0  # MPa
        sigma_pminf = 900.0  # MPa
        f_bpd = 2.5  # MPa
        form_8_21 = Form8Dot21AnchorageLength(
            l_pt2=l_pt2, alpha_2=alpha_2, diameter=diameter, sigma_pd=sigma_pd, sigma_pminf=sigma_pminf, f_bpd=f_bpd
        )
        # manually calculated result
        manually_calculated_result = 484.0  # mm

        assert form_8_21 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_l_pt2_is_negative(self) -> None:
        """Test that a NegativeValueError is raised when l_pt2 is negative."""
        l_pt2 = -100.0  # mm
        alpha_2 = 0.8
        diameter = 12.0  # mm
        sigma_pd = 1000.0  # MPa
        sigma_pminf = 900.0  # MPa
        f_bpd = 2.5  # MPa
        with pytest.raises(NegativeValueError):
            Form8Dot21AnchorageLength(l_pt2=l_pt2, alpha_2=alpha_2, diameter=diameter, sigma_pd=sigma_pd, sigma_pminf=sigma_pminf, f_bpd=f_bpd)

    def test_raise_error_if_alpha_2_is_negative(self) -> None:
        """Test that a NegativeValueError is raised when alpha_2 is negative."""
        l_pt2 = 100.0  # mm
        alpha_2 = -0.8
        diameter = 12.0  # mm
        sigma_pd = 1000.0  # MPa
        sigma_pminf = 900.0  # MPa
        f_bpd = 2.5  # MPa
        with pytest.raises(NegativeValueError):
            Form8Dot21AnchorageLength(l_pt2=l_pt2, alpha_2=alpha_2, diameter=diameter, sigma_pd=sigma_pd, sigma_pminf=sigma_pminf, f_bpd=f_bpd)

    def test_raise_error_if_diameter_is_negative(self) -> None:
        """Test that a NegativeValueError is raised when diameter is negative."""
        l_pt2 = 100.0  # mm
        alpha_2 = 0.8
        diameter = -12.0  # mm
        sigma_pd = 1000.0  # MPa
        sigma_pminf = 900.0  # MPa
        f_bpd = 2.5  # MPa
        with pytest.raises(NegativeValueError):
            Form8Dot21AnchorageLength(l_pt2=l_pt2, alpha_2=alpha_2, diameter=diameter, sigma_pd=sigma_pd, sigma_pminf=sigma_pminf, f_bpd=f_bpd)

    def test_raise_error_if_sigma_pd_is_negative(self) -> None:
        """Test that a NegativeValueError is raised when sigma_pd is negative."""
        l_pt2 = 100.0  # mm
        alpha_2 = 0.8
        diameter = 12.0  # mm
        sigma_pd = -1000.0  # MPa
        sigma_pminf = 900.0  # MPa
        f_bpd = 2.5  # MPa
        with pytest.raises(NegativeValueError):
            Form8Dot21AnchorageLength(l_pt2=l_pt2, alpha_2=alpha_2, diameter=diameter, sigma_pd=sigma_pd, sigma_pminf=sigma_pminf, f_bpd=f_bpd)

    def test_raise_error_if_sigma_pminf_is_negative(self) -> None:
        """Test that a NegativeValueError is raised when sigma_pminf is negative."""
        l_pt2 = 100.0  # mm
        alpha_2 = 0.8
        diameter = 12.0  # mm
        sigma_pd = 1000.0  # MPa
        sigma_pminf = -900.0  # MPa
        f_bpd = 2.5  # MPa
        with pytest.raises(NegativeValueError):
            Form8Dot21AnchorageLength(l_pt2=l_pt2, alpha_2=alpha_2, diameter=diameter, sigma_pd=sigma_pd, sigma_pminf=sigma_pminf, f_bpd=f_bpd)

    def test_raise_error_if_f_bpd_is_zero_or_negative(self) -> None:
        """Test that a LessOrEqualToZeroError is raised when f_bpd is zero or negative."""
        l_pt2 = 100.0  # mm
        alpha_2 = 0.8
        diameter = 12.0  # mm
        sigma_pd = 1000.0  # MPa
        sigma_pminf = 900.0  # MPa
        f_bpd = 0.0  # MPa
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot21AnchorageLength(l_pt2=l_pt2, alpha_2=alpha_2, diameter=diameter, sigma_pd=sigma_pd, sigma_pminf=sigma_pminf, f_bpd=f_bpd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"l_{bpd} = l_{pt2} + \alpha_{2} \cdot Ø \cdot \frac{\sigma_{pd} - \sigma_{pm\infty}}{f_{bpd}} = "
                r"100.000 + 0.800 \cdot 12.000 \cdot \frac{1000.000 - 900.000}{2.500} = 484.000",
            ),
            ("short", r"l_{bpd} = 484.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        l_pt2 = 100.0  # mm
        alpha_2 = 0.8
        diameter = 12.0  # mm
        sigma_pd = 1000.0  # MPa
        sigma_pminf = 900.0  # MPa
        f_bpd = 2.5  # MPa
        form_8_21 = Form8Dot21AnchorageLength(
            l_pt2=l_pt2, alpha_2=alpha_2, diameter=diameter, sigma_pd=sigma_pd, sigma_pminf=sigma_pminf, f_bpd=f_bpd
        )

        # Object to test
        form_8_21_latex = form_8_21.latex()

        actual = {"complete": form_8_21_latex.complete, "short": form_8_21_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
