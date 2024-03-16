"""Testing formula 5.6 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_6 import Form5Dot6TransverseForceEffectRoofDiaphragm
from blueprints.validations import NegativeValueError


class TestForm5Dot6TransverseForceEffectRoofDiaphragm:
    """Validation for formula 5.6 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN

        # Object to test
        form_5_6 = Form5Dot6TransverseForceEffectRoofDiaphragm(theta_i=theta_i, n_a=n_a)

        # Expected result, manually calculated
        manually_calculated_result = 0.015  # kN

        assert form_5_6 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_theta_i_is_given(self) -> None:
        """Test a negative value for theta_i."""
        # Example values
        theta_i = -0.003
        n_a = 5

        with pytest.raises(NegativeValueError):
            Form5Dot6TransverseForceEffectRoofDiaphragm(theta_i=theta_i, n_a=n_a)

    def test_raise_error_when_negative_n_a_is_given(self) -> None:
        """Test a negative value for n_a."""
        # Example values
        theta_i = 0.003
        n_a = -5

        with pytest.raises(NegativeValueError):
            Form5Dot6TransverseForceEffectRoofDiaphragm(theta_i=theta_i, n_a=n_a)

    def test_latex(self) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN

        # Object to test
        form_5_6_latex = Form5Dot6TransverseForceEffectRoofDiaphragm(
            theta_i=theta_i,
            n_a=n_a,
        ).latex()

        # Expected result
        latex_complete = r"H_{i} = Θ_{i} \cdot N_{a} = 0.003 \cdot 5.000 = 0.015"
        latex_short = r"H_{i} = 0.015"

        latex_test_sample = {
            "complete": {
                "expected": latex_complete,
                "actual": form_5_6_latex.complete,
            },
            "short": {"expected": latex_short, "actual": form_5_6_latex.short},
            "string": {"expected": latex_complete, "actual": str(form_5_6_latex)},
        }

        assertion_errors = []

        # A try-except block inside a loop is considered bad practice by Ruff
        # However, the documentation states that ignoring this will only have a negligible impact on performance
        # https://docs.astral.sh/ruff/rules/try-except-in-loop/
        # In this case, the desired behavior is to collect all the errors and raise them at once
        for representation, values in latex_test_sample.items():
            try:
                assert values["expected"] == values["actual"]
            except AssertionError as error_message:  # noqa: PERF203
                assertion_errors.append(rf"Error in {representation} representation. {error_message}")

        if assertion_errors:
            raise AssertionError("{} errors occurred:\n{}".format(len(assertion_errors), "\n".join(assertion_errors)))
