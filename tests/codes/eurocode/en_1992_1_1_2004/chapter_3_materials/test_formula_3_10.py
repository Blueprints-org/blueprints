"""Testing formula 3.10 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_10 import Form3Dot10CoefficientAgeConcreteDryingShrinkage


class TestForm3Dot10CoefficientAgeConcreteDryingShrinkage:
    """Validation for formula 3.10 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        t = 10  # -
        t_s = 2  # -
        h_0 = 200  # -
        form_3_10 = Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)

        # Expected result, manually calculated
        manually_calculated_result = 0.06604088

        assert form_3_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_t_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        t = -10  # -
        t_s = 2  # -
        h_0 = 200  # -

        with pytest.raises(ValueError):
            Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)

    def test_raise_error_when_negative_t_s_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        t = 10  # -
        t_s = -2  # -
        h_0 = 200  # -

        with pytest.raises(ValueError):
            Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)

    def test_raise_error_when_negative_h_0_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        t = 10  # -
        t_s = 2  # -
        h_0 = -200  # -

        with pytest.raises(ValueError):
            Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)

    def test_raise_error_when_t_is_smaller_than_t_s(self) -> None:
        """Test a comparison."""
        # Example values
        t = 10  # -
        t_s = 12  # -
        h_0 = 200  # -

        with pytest.raises(ValueError):
            Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\beta_{ds}(t,t_s) = \frac{(t - t_s)}{(t - t_s) + 0.04 \sqrt{h_0^3}} = "
                r"\frac{(10.00 - 2.00)}{(10.00 - 2.00) + 0.04 \sqrt{200.00^3}} = 0.07",
            ),
            ("short", r"\beta_{ds}(t,t_s) = 0.07"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t = 10  # -
        t_s = 2  # -
        h_0 = 200  # -

        # Object to test
        form_3_10_latex = Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0).latex()

        actual = {"complete": form_3_10_latex.complete, "short": form_3_10_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
