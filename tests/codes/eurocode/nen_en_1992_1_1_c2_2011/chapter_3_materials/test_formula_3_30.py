"""Testing formula 3.30 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_30 import Form3Dot30RatioLossOfPreStressClass3


class TestForm3Dot30RatioLossOfPreStressClass3:
    """Validation for formula 3.30 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        rho_1000 = 35.2  # %
        mu = 0.28  # -
        t = 7.4  # hours

        form_3_30 = Form3Dot30RatioLossOfPreStressClass3(rho_1000=rho_1000, mu=mu, t=t)

        # Expected result, manually calculated
        manually_calculated_result = 4.628205 * 10**-4

        assert form_3_30 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_rho_1000_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        rho_1000 = -35.2  # %
        mu = 0.28  # -
        t = 7.4  # hours

        with pytest.raises(ValueError):
            Form3Dot30RatioLossOfPreStressClass3(rho_1000=rho_1000, mu=mu, t=t)

    def test_raise_error_when_negative_t_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        rho_1000 = 35.2  # %
        mu = 0.28  # -
        t = -7.4  # hours

        with pytest.raises(ValueError):
            Form3Dot30RatioLossOfPreStressClass3(rho_1000=rho_1000, mu=mu, t=t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\frac{\Delta \sigma_{pr}}{\sigma_{pl}} = "
                r"1.98 \cdot \rho_{1000} \cdot e^{8 \cdot \mu} \left( \frac{t}{1000} \right)^{0.75 \cdot (1 - \mu)} \cdot 10^{-5} = "
                r"1.98 \cdot 35.200 \cdot e^{8 \cdot 0.280} \left( \frac{7.400}{1000} \right)^{0.75 \cdot (1 - 0.280)} \cdot 10^{-5} = 0.000463",
            ),
            ("short", r"\frac{\Delta \sigma_{pr}}{\sigma_{pl}} = 0.000463"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        rho_1000 = 35.2  # %
        mu = 0.28  # -
        t = 7.4  # hours

        # Object to test
        form_3_30_latex = Form3Dot30RatioLossOfPreStressClass3(rho_1000=rho_1000, mu=mu, t=t).latex()

        actual = {"complete": form_3_30_latex.complete, "short": form_3_30_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
