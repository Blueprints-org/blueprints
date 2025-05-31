"""Testing formula 3.29 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_29 import Form3Dot29RatioLossOfPreStressClass2


class TestForm3Dot29RatioLossOfPreStressClass2:
    """Validation for formula 3.29 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        rho_1000 = 35.2  # %
        mu = 0.28  # -
        t = 7.4  # hours

        form_3_29 = Form3Dot29RatioLossOfPreStressClass2(rho_1000=rho_1000, mu=mu, t=t)

        # Expected result, manually calculated
        manually_calculated_result = 2.099201 * 10**-4

        assert form_3_29 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_rho_1000_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        rho_1000 = -35.2  # %
        mu = 0.28  # -
        t = 7.4  # hours

        with pytest.raises(ValueError):
            Form3Dot29RatioLossOfPreStressClass2(rho_1000=rho_1000, mu=mu, t=t)

    def test_raise_error_when_negative_t_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        rho_1000 = 35.2  # %
        mu = 0.28  # -
        t = -7.4  # hours

        with pytest.raises(ValueError):
            Form3Dot29RatioLossOfPreStressClass2(rho_1000=rho_1000, mu=mu, t=t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\frac{\Delta \sigma_{pr}}{\sigma_{pl}} = "
                r"0.66 \cdot \rho_{1000} \cdot e^{9.1 \cdot \mu} \left( \frac{t}{1000} \right)^{0.75 \cdot (1 - \mu)} \cdot 10^{-5} = "
                r"0.66 \cdot 35.200 \cdot e^{9.1 \cdot 0.280} \left( \frac{7.400}{1000} \right)^{0.75 \cdot (1 - 0.280)} \cdot 10^{-5} = 0.000210",
            ),
            ("short", r"\frac{\Delta \sigma_{pr}}{\sigma_{pl}} = 0.000210"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        rho_1000 = 35.2  # %
        mu = 0.28  # -
        t = 7.4  # hours

        # Object to test
        form_3_29_latex = Form3Dot29RatioLossOfPreStressClass2(rho_1000=rho_1000, mu=mu, t=t).latex()

        actual = {"complete": form_3_29_latex.complete, "short": form_3_29_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
